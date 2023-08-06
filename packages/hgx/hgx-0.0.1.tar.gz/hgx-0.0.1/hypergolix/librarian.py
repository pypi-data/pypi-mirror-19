'''
LICENSING
-------------------------------------------------

hypergolix: A python Golix client.
    Copyright (C) 2016 Muterra, Inc.
    
    Contributors
    ------------
    Nick Badger
        badg@muterra.io | badg@nickbadger.com | nickbadger.com

    This library is free software; you can redistribute it and/or
    modify it under the terms of the GNU Lesser General Public
    License as published by the Free Software Foundation; either
    version 2.1 of the License, or (at your option) any later version.

    This library is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
    Lesser General Public License for more details.

    You should have received a copy of the GNU Lesser General Public
    License along with this library; if not, write to the
    Free Software Foundation, Inc.,
    51 Franklin Street,
    Fifth Floor,
    Boston, MA  02110-1301 USA

------------------------------------------------------
'''

# External dependencies
import logging
import collections
import weakref
import queue
import threading
import traceback
import asyncio
import loopa
import pathlib

from golix import ThirdParty
from golix import SecondParty
from golix import Ghid
from golix import Secret
from golix import ParseError
from golix import SecurityError

from golix.crypto_utils import generate_ghidlist_parser

from golix._getlow import GIDC
from golix._getlow import GEOC
from golix._getlow import GOBS
from golix._getlow import GOBD
from golix._getlow import GDXX
from golix._getlow import GARQ

# Internal dependencies
from .persistence import _GidcLite
from .persistence import _GeocLite
from .persistence import _GobsLite
from .persistence import _GobdLite
from .persistence import _GdxxLite
from .persistence import _GarqLite

from .persistence import Enforcer
from .lawyer import LawyerCore

from .gao import GAO

from .hypothetical import API
from .hypothetical import public_api
from .hypothetical import fixture_api
from .hypothetical import fixture_noop

from .exceptions import HypergolixException
from .exceptions import RemoteNak
from .exceptions import MalformedGolixPrimitive
from .exceptions import VerificationFailure
from .exceptions import UnboundContainer
from .exceptions import InvalidIdentity
from .exceptions import DoesNotExist
from .exceptions import AlreadyDebound
from .exceptions import InvalidTarget
from .exceptions import StillBoundWarning
from .exceptions import RequestError
from .exceptions import InconsistentAuthor
from .exceptions import IllegalDynamicFrame
from .exceptions import IntegrityError
from .exceptions import UnavailableUpstream

from .utils import weak_property
from .utils import readonly_property
from .utils import TruthyLock
from .utils import SetMap
from .utils import WeakSetMap
from .utils import _generate_threadnames
from .utils import FiniteDict
from .utils import KeyedAsyncioLock


# ###############################################
# Boilerplate
# ###############################################


logger = logging.getLogger(__name__)


# Control * imports.
__all__ = [
    # 'PersistenceCore',
]


# ###############################################
# Lib
# ###############################################
            

class LibrarianCore(metaclass=API):
    ''' Base class for caching systems common to non-volatile librarians
    such as DiskLibrarian, S3Librarian, etc.
    
    TODO: make ghid vs frame ghid usage more consistent across things.
    
    NOTE: ideally, everything stateful should be in the librarian. In
    other words, you shouldn't use a bookie to track binding status and
    stuff; that should all be handled within librarian. That would make
    the librarian the single source of truth. Unfortunately, there's not
    really a good way of doing that right now ops-wise; you'd need some
    kind of relational filesystem.
    
    TODO: instead, should create a dedicated "cache" system. It can be
    responsible for restoration of stuff, atomic state updates, etc.
    '''
    _enforcer = weak_property('__enforcer')
    _lawyer = weak_property('__lawyer')
    _percore = weak_property('__percore')
    
    @public_api
    def __init__(self, *args, memory_cache=10000, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Lookup for ghid -> hypergolix description
        # This may be GC'd by the python process.
        self._catalog = FiniteDict(maxlen=memory_cache)
        
    @__init__.fixture
    def __init__(self, *args, **kwargs):
        ''' Construct an in-memory-only version of librarian.
        '''
        super(LibrarianCore.__fixture__, self).__init__(*args, **kwargs)
        
        # Lookup <ghid>: <raw data>
        self._shelf = {}
        
        # Lookup for dynamic ghid -> frame ghid
        self._dyn_resolver = {}
        
        # Lookup <bound ghid>: set(<binding obj>)
        self._bound_by_ghid = SetMap()
        
        # Lookup <debound ghid>: set(<debinding ghid>)
        self._debound_by_ghid = SetMap()
        
        # Lookup <recipient>: set(<request ghid>)
        self._requests_for_recipient = SetMap()
        
    @fixture_api
    def RESET(self):
        ''' Reset all of the librarian.
        '''
        self._catalog.clear()
        self._shelf.clear()
        self._dyn_resolver.clear()
        self._bound_by_ghid.clear_all()
        self._debound_by_ghid.clear_all()
        self._requests_for_recipient.clear_all()
        
    def assemble(self, enforcer, lawyer, percore):
        ''' Assign stuff hereto avoid circuitous problems.
        '''
        # We need to be able to check the legality of debindings whose targets
        # are uploaded after the debinding itself is.
        self._enforcer = enforcer
        self._lawyer = lawyer
        # And we need to be able to load things back up from the cache
        self._percore = percore
    
    @public_api
    async def is_bound(self, obj):
        ''' Check to see if the object has been bound.
        '''
        bindings = await self.bind_status(obj.ghid)
        return bool(bindings)
    
    @public_api
    async def is_debound(self, obj):
        # We need to validate any unvalidated bindings. For now, just always
        # validate debindings when an object is being checked.
        debindings = await self.debind_status(obj.ghid)
        invalidated = 0
        for debinding_ghid in debindings:
            # Get the existing debinding object
            debinding = await self.summarize(debinding_ghid)
            
            # Validate existing binding against newly-known target
            try:
                await self._enforcer.validate_gdxx(debinding, target_obj=obj)
                await self._lawyer.validate_gdxx(debinding, target_obj=obj)
                
            # Validation failed. Remove illegal debinding.
            except (InvalidTarget, InconsistentAuthor):
                logger.error(''.join((
                    'Removed invalid existing debinding.\n',
                    '    Debinding author:     ', str(debinding.author), '\n',
                    '    Valid object author:  ', str(obj.author), '\n',
                    '    Debinding target:     ', str(debinding.target), '\n',
                    '    Target type:          ', str(type(obj))
                )))
                # There's no need to do anything with the undertaker, because
                # debindings don't get subscribed to, and we (the librarian)
                # are the sole source of truth.
                await self.abandon(debinding)
                
                # Record that this was invalidated
                invalidated += 1
                
            # If we were differentiating between validated debindings and
            # provisional (unvalidated) debindings, this would be the place to
            # commit the provisional to the validated.
        
        # Instead of making another call to debind_status, we can calculate it
        # directly. NOTE! There is a race condition between the initial
        # validity check on upload, and the commit call.
        
        return bool(len(debindings) - invalidated)
        
    @is_debound.fixture
    async def is_debound(self, obj):
        ''' Create ad-hoc enforcers and lawyers when fixturing self.
        '''
        enforcer = Enforcer.__fixture__(librarian=self)
        lawyer = LawyerCore.__fixture__(librarian=self)
        self._enforcer = enforcer
        self._lawyer = lawyer
        result = await super(LibrarianCore.__fixture__, self).is_debound(obj)
        del enforcer
        del lawyer
        return result
    
    @public_api
    async def store(self, obj, data):
        ''' Starts tracking an object.
        obj is a hypergolix representation object.
        raw is bytes-like.
        '''
        if isinstance(obj, _GobdLite):
            reference_ghid = obj.frame_ghid
            # If we have an existing frame, get ITS frame ghid, so we can clear
            # it if the storage succeeds.
            try:
                old_ghid = await self.resolve_frame(obj.ghid)
            except KeyError:
                old_ghid = None
            
        else:
            reference_ghid = obj.ghid
            old_ghid = None
            
        await self.add_to_cache(obj, data)
        self._catalog[reference_ghid] = obj
        
        # If successful (which is any time we get to here), we also need to get
        # rid of any old dynamic frames and pop them from the catalog.
        if old_ghid is not None:
            await self.remove_from_cache(old_ghid)
            # We need the None regardless of bugs, in case the old frame is
            # "stale" enough to have been released from memory
            self._catalog.pop(old_ghid, None)
    
    @public_api
    async def retrieve(self, ghid):
        ''' Returns the raw data associated with the ghid, checking only
        locally.
        '''
        try:
            ghid = await self.resolve_frame(ghid)
        except KeyError:
            pass
            
        return (await self.get_from_cache(ghid))
    
    @public_api
    async def summarize(self, ghid):
        ''' Returns a lightweight Hypergolix description of the object.
        Checks only locally.
        '''
        try:
            ghid = await self.resolve_frame(ghid)
        except KeyError:
            pass
        
        try:
            obj = self._catalog[ghid]
        
        except KeyError:
            logger.debug('Attempting lazy-load for ' + str(ghid))
            # This will raise DoesNotExist if missing.
            data = await self.get_from_cache(ghid)
            # This does NOT ingest the data into the persistence system!
            obj = await self._percore.attempt_load(data, quiet=False)
            self._catalog[ghid] = obj
            
        return obj
        
    @public_api
    async def abandon(self, obj):
        ''' Forces erasure of an object without notifying anyone else.
        Idempotent. Should never raise KeyError.
        '''
        if isinstance(obj, _GobdLite):
            ghid = obj.frame_ghid
        else:
            ghid = obj.ghid
        
        await self.remove_from_cache(ghid)
        
        # Delete it from the catalog (if it exists there)
        self._catalog.pop(ghid, None)
    
    # Subclasses MAY define this, but are not required to do so.
    @fixture_api
    async def restore(self):
        ''' For LibrarianCore, do nothing. This is just here as an
        endpoint for restore calls. If subclasses want/need to support
        restoration, they should override this.
        '''
    
    # Subclasses MUST define this to work!
    # @abc.abstractmethod
    @fixture_api
    async def contains(self, ghid):
        ''' Checks the ghidcache for the ghid.
        '''
        try:
            ghid = await self.resolve_frame(ghid)
        except KeyError:
            pass
        
        # Catalog may only be accurate locally. Shelf is accurate globally.
        return ghid in self._shelf
    
    # Subclasses MUST define this to work!
    # @abc.abstractmethod
    @fixture_api
    async def resolve_frame(self, ghid):
        ''' Get the current frame ghid from the dynamic ghid.
        '''
        if not isinstance(ghid, Ghid):
            raise TypeError('Ghid must be a Ghid.')
            
        if ghid in self._dyn_resolver:
            return self._dyn_resolver[ghid]
        else:
            raise KeyError(str(ghid) + ' not known as dynamic ghid.')
    
    # Subclasses MUST define this to work!
    # @abc.abstractmethod
    @fixture_api
    async def recipient_status(self, ghid):
        ''' Return a frozenset of ghids assigned to the passed ghid as
        a recipient.
        '''
        return self._requests_for_recipient.get_any(ghid)
    
    # Subclasses MUST define this to work!
    # @abc.abstractmethod
    @fixture_api
    async def bind_status(self, ghid):
        ''' Return a frozenset of ghids binding the passed ghid.
        '''
        return self._bound_by_ghid.get_any(ghid)
    
    # Subclasses MUST define this to work!
    # @abc.abstractmethod
    @fixture_api
    async def debind_status(self, ghid):
        ''' Return either a ghid, or None.
        '''
        # Note that any particular object can have exactly zero or one VALID
        # debinds, but that a malicious actor could find a race condition and
        # debind something FOR SOMEONE ELSE before the bookie knows about the
        # original object authorship.
        return self._debound_by_ghid.get_any(ghid)
            
    # Subclasses MUST define this to work!
    # @abc.abstractmethod
    @fixture_api
    async def add_to_cache(self, obj, data):
        ''' Adds the passed raw data to the cache.
        '''
        if isinstance(obj, _GobsLite):
            reference_ghid = obj.ghid
            self._bound_by_ghid.add(obj.target, obj.ghid)
            
        elif isinstance(obj, _GobdLite):
            reference_ghid = obj.frame_ghid
            try:
                existing = await self.summarize(obj.ghid)
            except KeyError:
                pass
            else:
                self._bound_by_ghid.remove(existing.target, obj.ghid)
                
            # Now we have a clean slate and need to update things accordingly.
            self._bound_by_ghid.add(obj.target, obj.ghid)
            self._dyn_resolver[obj.ghid] = obj.frame_ghid
                
        elif isinstance(obj, _GdxxLite):
            reference_ghid = obj.ghid
            self._debound_by_ghid.add(obj.target, obj.ghid)
            
        elif isinstance(obj, _GarqLite):
            reference_ghid = obj.ghid
            # NOTE: this is only necessary for a persistence server
            self._requests_for_recipient.add(obj.recipient, obj.ghid)
            
        else:
            reference_ghid = obj.ghid
            
        self._shelf[reference_ghid] = data
        
    # Subclasses MUST define this to work!
    # @abc.abstractmethod
    @fixture_api
    async def remove_from_cache(self, ghid):
        ''' Removes the data associated with the passed ghid from the
        cache.
        '''
        obj = await self.summarize(ghid)
        
        if isinstance(obj, _GobsLite):
            reference_ghid = obj.ghid
            self._bound_by_ghid.discard(obj.target, obj.ghid)
            
        elif isinstance(obj, _GobdLite):
            reference_ghid = obj.frame_ghid
            self._bound_by_ghid.discard(obj.target, obj.ghid)
            
            if self._dyn_resolver.get(obj.ghid, None) == obj.frame_ghid:
                self._dyn_resolver.pop(obj.ghid, None)
            
        elif isinstance(obj, _GdxxLite):
            reference_ghid = obj.ghid
            self._debound_by_ghid.discard(obj.target, obj.ghid)
            
        elif isinstance(obj, _GarqLite):
            reference_ghid = obj.ghid
            self._requests_for_recipient.discard(obj.recipient, obj.ghid)
            
        else:
            reference_ghid = obj.ghid
        
        try:
            self._shelf.pop(reference_ghid)
        except KeyError as exc:
            # Protect the full GHID from accidental exposure
            raise DoesNotExist(str(ghid)) from None
        
    # Subclasses MUST define this to work!
    # @abc.abstractmethod
    @fixture_api
    async def get_from_cache(self, ghid):
        ''' Returns the raw data associated with the ghid.
        '''
        try:
            return self._shelf[ghid]
        except KeyError as exc:
            # Protect the full GHID from accidental exposure
            raise DoesNotExist(str(ghid)) from None
    
    
class DiskLibrarian(LibrarianCore):
    ''' Librarian that caches data to disk, but keeps all status state
    in memory.
    '''
    
    def __init__(self, cache_dir, executor, loop, *args, **kwargs):
        ''' cache_dir should be relative to current.
        '''
        super().__init__(*args, **kwargs)
        
        cache_dir = pathlib.Path(cache_dir)
        if not cache_dir.exists():
            raise ValueError('Path does not exist: ' + cache_dir.as_posix())
        elif not cache_dir.is_dir():
            raise ValueError('Path is not an available directory: ' +
                             cache_dir.as_posix())
        
        self._loop = loop
        self._executor = executor
        self._cachedir = cache_dir
        
        # This allows us to be lazy when restoring things, without rewriting
        # disk data
        self._restoration_flag = False
        
        # Lookup for dynamic ghid -> frame ghid
        self._dyn_resolver = {}
        
        # Lookup <bound ghid>: set(<binding obj>)
        self._bound_by_ghid = SetMap()
        
        # Lookup <debound ghid>: set(<debinding ghid>)
        self._debound_by_ghid = SetMap()
        
        # Lookup <recipient>: set(<request ghid>)
        self._requests_for_recipient = SetMap()
        
        # Make sure we don't do concurrent write/reads into the cache, which
        # could potentially create contention issues for stuff.
        # TODO: make this keyed, so that we can do simultaneous read/write of
        # different things at the same time (just not the same thing at the
        # same time)
        self._cache_lock = KeyedAsyncioLock(loop=self._loop)
        
    def __read_from_disk(self, ghid):
        ''' Gets a file path from the disk cache, wrapping misses in
        DoesNotExist.
        '''
        fpath = self._make_path(ghid)
        
        try:
            return fpath.read_bytes()
        
        except FileNotFoundError as exc:
            # Remove the filename from the exception context so as not to
            # disclose the full GHID
            raise DoesNotExist(str(ghid)) from None
            
    def __remove_from_disk(self, ghid):
        ''' Removes a ghid from the disk cache, wrapping misses in
        DoesNotExist.
        '''
        try:
            fpath = self._make_path(ghid)
            fpath.unlink()
            
        except FileNotFoundError:
            # Suppress the full name of the file to prevent knowing its whole
            # GHID
            raise DoesNotExist(str(ghid)) from None
        
    async def get_from_cache(self, ghid):
        ''' Returns the raw data associated with the ghid.
        '''
        try:
            ghid = await self.resolve_frame(ghid)
        except KeyError:
            pass
        
        async with self._cache_lock(ghid):
            return (await self._loop.run_in_executor(self._executor,
                                                     self.__read_from_disk,
                                                     ghid))
            
    async def add_to_cache(self, obj, data):
        ''' Adds the passed raw data to the cache.
        '''
        if isinstance(obj, _GobsLite):
            reference_ghid = obj.ghid
            self._bound_by_ghid.add(obj.target, obj.ghid)
            
        elif isinstance(obj, _GobdLite):
            reference_ghid = obj.frame_ghid
            try:
                existing = await self.summarize(obj.ghid)
            except KeyError:
                pass
            else:
                self._bound_by_ghid.remove(existing.target, obj.ghid)
                
            # Now we have a clean slate and need to update things accordingly.
            self._bound_by_ghid.add(obj.target, obj.ghid)
            self._dyn_resolver[obj.ghid] = obj.frame_ghid
                
        elif isinstance(obj, _GdxxLite):
            reference_ghid = obj.ghid
            self._debound_by_ghid.add(obj.target, obj.ghid)
            
        elif isinstance(obj, _GarqLite):
            reference_ghid = obj.ghid
            # NOTE: this is only necessary for a persistence server
            self._requests_for_recipient.add(obj.recipient, obj.ghid)
            
        else:
            reference_ghid = obj.ghid
            
        if not self._restoration_flag:
            fpath = self._make_path(reference_ghid)
            
            async with self._cache_lock(reference_ghid):
                await self._loop.run_in_executor(self._executor,
                                                 fpath.write_bytes, data)
    
    async def remove_from_cache(self, ghid):
        ''' Removes the data associated with the passed ghid from the
        cache.
        '''
        obj = await self.summarize(ghid)
        
        if isinstance(obj, _GobsLite):
            reference_ghid = obj.ghid
            self._bound_by_ghid.discard(obj.target, obj.ghid)
            
        elif isinstance(obj, _GobdLite):
            reference_ghid = obj.frame_ghid
            self._bound_by_ghid.discard(obj.target, obj.ghid)
            
            if self._dyn_resolver.get(obj.ghid, None) == obj.frame_ghid:
                self._dyn_resolver.pop(obj.ghid, None)
            
        elif isinstance(obj, _GdxxLite):
            reference_ghid = obj.ghid
            self._debound_by_ghid.discard(obj.target, obj.ghid)
            
        elif isinstance(obj, _GarqLite):
            reference_ghid = obj.ghid
            self._requests_for_recipient.discard(obj.recipient, obj.ghid)
            
        else:
            reference_ghid = obj.ghid
        
        async with self._cache_lock(reference_ghid):
            await self._loop.run_in_executor(self._executor,
                                             self.__remove_from_disk,
                                             reference_ghid)
        
    async def contains(self, ghid):
        ''' Checks the ghidcache for the ghid.
        '''
        try:
            ghid = await self.resolve_frame(ghid)
        except KeyError:
            pass
        
        fpath = self._make_path(ghid)
        return (await self._loop.run_in_executor(self._executor, fpath.exists))
    
    async def resolve_frame(self, ghid):
        ''' Get the current frame ghid from the dynamic ghid.
        '''
        if not isinstance(ghid, Ghid):
            raise TypeError('Ghid must be a Ghid.')
            
        if ghid in self._dyn_resolver:
            return self._dyn_resolver[ghid]
        else:
            raise KeyError(str(ghid) + ' not known as dynamic ghid.')
    
    async def recipient_status(self, ghid):
        ''' Return a frozenset of ghids assigned to the passed ghid as
        a recipient.
        '''
        return self._requests_for_recipient.get_any(ghid)
    
    async def bind_status(self, ghid):
        ''' Return a frozenset of ghids binding the passed ghid.
        '''
        return self._bound_by_ghid.get_any(ghid)
    
    async def debind_status(self, ghid):
        ''' Return either a ghid, or None.
        '''
        # Note that any particular object can have exactly zero or one VALID
        # debinds, but that a malicious actor could find a race condition and
        # debind something FOR SOMEONE ELSE before the bookie knows about the
        # original object authorship.
        return self._debound_by_ghid.get_any(ghid)
    
    # If subclasses want/need to do anything to restore themselves, they should
    # override this.
    async def restore(self):
        ''' Loads any existing files from the cache.  All existing
        files there will be attempted to be loaded, so it's best not to
        have extraneous stuff in the directory. Will be passed through
        to the core for processing.
        '''
        self._restoration_flag = True
        try:
            # Get all available files (this is a massive contention problem
            # and race condition waiting to happen. DON'T use concurrent copies
            # of the librarian.)
            # Iterate over each file within the cache. We're doing this one
            # time only, so don't bother doing the iterdir in an executor
            for child in self._cachedir.iterdir():
                if child.is_file():
                    data = await self._loop.run_in_executor(self._executor,
                                                            child.read_bytes)
                    obj = await self._percore.attempt_load(data)
                    # Lazily just use store to re-load our previous bookkeeping
                    # state
                    await self.store(obj, data)
                
        # Reset the restoration flag
        finally:
            self._restoration_flag = False
        
    def _make_path(self, ghid):
        ''' Converts the ghid to a file path.
        '''
        fname = ghid.as_str() + '.ghid'
        fpath = self._cachedir / fname
        return fpath
