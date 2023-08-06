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


# Global dependencies
import asyncio
import threading
import traceback

from smartyparse.parsers import ParseError

from golix import ThirdParty
from golix import SecondParty
from golix import SecurityError

from golix._getlow import GIDC
from golix._getlow import GEOC
from golix._getlow import GOBS
from golix._getlow import GOBD
from golix._getlow import GDXX
from golix._getlow import GARQ

# Local dependencies
from .hypothetical import API
from .hypothetical import public_api
from .hypothetical import fixture_api
from .hypothetical import fixture_noop
from .hypothetical import fixture_return

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
from .utils import KeyedAsyncioLock


# ###############################################
# Boilerplate
# ###############################################


import logging
logger = logging.getLogger(__name__)

# Control * imports.
__all__ = [
    'PersistenceCore',
]


# ###############################################
# Lib
# ###############################################
        
        
class _BaseLite:
    __slots__ = [
        'ghid',
        '__weakref__',
    ]
    
    def __hash__(self):
        return hash(self.ghid)
        
    def __eq__(self, other):
        try:
            return self.ghid == other.ghid
        except AttributeError as exc:
            raise TypeError('Incomparable types.') from exc
            
    def __str__(self):
        ''' The string format should tell the type name and the ghid.
        '''
        return type(self).__name__ + '(' + str(self.ghid) + ')'
        
        
class _GidcLite(_BaseLite):
    ''' Lightweight description of a GIDC.
    '''
    __slots__ = [
        'identity'
    ]
    
    def __init__(self, ghid, identity):
        self.ghid = ghid
        self.identity = identity
        
    @classmethod
    def from_golix(cls, golix_obj):
        ''' Convert the golix object to a lightweight representation.
        '''
        identity = SecondParty.from_identity(golix_obj)
        return cls(
            ghid = golix_obj.ghid,
            identity = identity,
        )
        
        
class _GeocLite(_BaseLite):
    ''' Lightweight description of a GEOC.
    '''
    __slots__ = [
        'author',
    ]
    
    def __init__(self, ghid, author):
        self.ghid = ghid
        self.author = author
        
    def __eq__(self, other):
        try:
            return (
                super().__eq__(other) and
                self.author == other.author
            )
        # This will not catch a super() TyperError, so we want to be able to
        # compare anything with a ghid. In reality, any situation where the
        # authors don't match but the ghids do is almost certainly a bug; but,
        # compare it anyways just in case.
        except AttributeError as exc:
            return False
        
    @classmethod
    def from_golix(cls, golix_obj):
        ''' Convert the golix object to a lightweight representation.
        '''
        return cls(
            ghid = golix_obj.ghid,
            author = golix_obj.author,
        )
        
        
class _GobsLite(_BaseLite):
    ''' Lightweight description of a GOBS.
    '''
    __slots__ = [
        'author',
        'target',
    ]
    
    def __init__(self, ghid, author, target):
        self.ghid = ghid
        self.author = author
        self.target = target
        
    def __eq__(self, other):
        try:
            return (
                super().__eq__(other) and
                self.author == other.author and
                self.target == other.target
            )
            
        # This will not catch a super() TyperError, so we want to be able to
        # compare anything with a ghid. In reality, any situation where the
        # authors don't match but the ghids do is almost certainly a bug; but,
        # compare it anyways just in case.
        except AttributeError as exc:
            return False
        
    @classmethod
    def from_golix(cls, golix_obj):
        ''' Convert the golix object to a lightweight representation.
        '''
        return cls(
            ghid = golix_obj.ghid,
            author = golix_obj.binder,
            target = golix_obj.target,
        )
    
        
class _GobdLite(_BaseLite):
    ''' Lightweight description of a GOBD.
    '''
    __slots__ = [
        'author',
        'counter',
        'target_vector',
        'frame_ghid'
    ]
    
    def __init__(self, ghid, author, counter, target_vector, frame_ghid):
        self.ghid = ghid
        self.author = author
        self.counter = counter
        self.target_vector = target_vector
        self.frame_ghid = frame_ghid
        
    def __eq__(self, other):
        try:
            return (
                super().__eq__(other) and
                self.author == other.author and
                self.target == other.target and
                self.frame_ghid == other.frame_ghid
                # Skip history, because it could potentially vary
                # self.history == other.history
            )
            
        # This will not catch a super() TyperError, so we want to be able to
        # compare anything with a ghid. In reality, any situation where the
        # authors don't match but the ghids do is almost certainly a bug; but,
        # compare it anyways just in case.
        except AttributeError as exc:
            return False
        
    @classmethod
    def from_golix(cls, golix_obj):
        ''' Convert the golix object to a lightweight representation.
        '''
        return cls(
            ghid = golix_obj.ghid_dynamic,
            author = golix_obj.binder,
            counter = golix_obj.counter,
            target_vector = golix_obj.target_vector,
            frame_ghid = golix_obj.ghid
        )
        
    @property
    def target(self):
        ''' Access the current target.
        '''
        return self.target_vector[0]
    
        
class _GdxxLite(_BaseLite):
    ''' Lightweight description of a GDXX.
    '''
    __slots__ = [
        'author',
        'target',
        '_debinding',
    ]
    
    def __init__(self, ghid, author, target):
        self.ghid = ghid
        self.author = author
        self.target = target
        self._debinding = True
        
    def __eq__(self, other):
        try:
            return (
                super().__eq__(other) and
                self.author == other.author and
                self._debinding == other._debinding
            )
            
        # This will not catch a super() TyperError, so we want to be able to
        # compare anything with a ghid. In reality, any situation where the
        # authors don't match but the ghids do is almost certainly a bug; but,
        # compare it anyways just in case.
        except AttributeError as exc:
            return False
        
    @classmethod
    def from_golix(cls, golix_obj):
        ''' Convert the golix object to a lightweight representation.
        '''
        return cls(
            ghid = golix_obj.ghid,
            author = golix_obj.debinder,
            target = golix_obj.target,
        )
        
        
class _GarqLite(_BaseLite):
    ''' Lightweight description of a GARQ.
    '''
    __slots__ = [
        'recipient',
    ]
    
    def __init__(self, ghid, recipient):
        self.ghid = ghid
        self.recipient = recipient
        
    def __eq__(self, other):
        try:
            return (
                super().__eq__(other) and
                self.recipient == other.recipient
            )
            
        # This will not catch a super() TyperError, so we want to be able to
        # compare anything with a ghid. In reality, any situation where the
        # authors don't match but the ghids do is almost certainly a bug; but,
        # compare it anyways just in case.
        except AttributeError as exc:
            return False
        
    @classmethod
    def from_golix(cls, golix_obj):
        ''' Convert the golix object to a lightweight representation.
        '''
        return cls(
            ghid = golix_obj.ghid,
            recipient = golix_obj.recipient,
        )
                
        
class PersistenceCore(metaclass=API):
    ''' Provides the core functions for storing Golix objects. Required
    for the hypergolix service to start.
    
    Can coordinate with both "upstream" and "downstream" persisters.
    Other persisters should pass through the "ingestive tract". Local
    objects can be published directly through calling the ingest_<type>
    methods.
    
    TODO: add librarian validation, so that attempting to update an
    object we already have an identical copy to silently exits.
    '''
    _doorman = weak_property('__doorman')
    _enforcer = weak_property('__enforcer')
    _lawyer = weak_property('__lawyer')
    _bookie = weak_property('__bookie')
    _postman = weak_property('__postman')
    _undertaker = weak_property('__undertaker')
    _librarian = weak_property('__librarian')
    _salmonator = weak_property('__salmonator')
    
    # This is a messy way of getting the suffix for validation and stuff but
    # it's getting the job done.
    _ATTR_LOOKUP = {
        _GidcLite: 'gidc',
        _GeocLite: 'geoc',
        _GobsLite: 'gobs',
        _GobdLite: 'gobd',
        _GdxxLite: 'gdxx',
        _GarqLite: 'garq'
    }
    
    @public_api
    def __init__(self, loop=None, *args, **kwargs):
        ''' Create a KeyedAsyncioLock for ingestion.
        '''
        self._ingestion_mutex = KeyedAsyncioLock(loop)
        
    @__init__.fixture
    def __init__(self, librarian=None, *args, **kwargs):
        ''' Right now, well, this is basically a noop. Anticipating
        substantial changes!
        '''
        super(PersistenceCore.__fixture__, self).__init__(
            *args,
            **kwargs
        )
        
        if librarian is not None:
            self._librarian = librarian
        
    def assemble(self, doorman, enforcer, lawyer, bookie, librarian, postman,
                 undertaker, salmonator):
        self._doorman = doorman
        self._enforcer = enforcer
        self._lawyer = lawyer
        self._bookie = bookie
        self._postman = postman
        self._undertaker = undertaker
        self._librarian = librarian
        self._salmonator = salmonator
    
    @public_api
    async def direct_ingest(self, obj, packed, remotable, skip_conn=None):
        ''' Standard ingestion flow for stuff. To be called from ingest
        above, or directly (for objects created "in-house").
        '''
        # Check for a redundant object, which will immediately short-circuit.
        if isinstance(obj, _GobdLite):
            check_ghid = obj.frame_ghid
            log_frame = True
            counter = obj.counter
            target = obj.target
        else:
            check_ghid = obj.ghid
            log_frame = False
            counter = 0
            target = None
        
        async with self._ingestion_mutex(check_ghid):
            if (await self._librarian.contains(check_ghid)):
                logger.debug(
                    str(check_ghid) + ' not ingested: already exists.'
                )
                return False
            
            else:
                logger.info(
                    'Ingesting ' + str(obj) +
                    (
                        ' frame ' + str(counter) + ': ' + str(check_ghid) +
                        ', target: ' + str(target)
                    ) * log_frame + '...'
                )
                # Calculate "gidc", etc
                suffix = self._ATTR_LOOKUP[type(obj)]
                validation_method = 'validate_' + suffix
                
                # Validate the object... (will raise for invalid)
                # ########################
                # Enforce target selection
                await getattr(self._enforcer, validation_method)(obj)
                # Now make sure authorship requirements are satisfied
                await getattr(self._lawyer, validation_method)(obj)
                # Finally make sure persistence rules are followed
                await getattr(self._bookie, validation_method)(obj)
                
                # Ingest the object
                # ########################
                # Alert the undertaker for any necessary GC of targets, etc. Do
                # that before storing at the librarian, so that the undertaker
                # has access to the old state.
                await getattr(self._undertaker, 'alert_' + suffix)(obj,
                                                                   skip_conn)
                # Finally, add it to the librarian.
                await self._librarian.store(obj, packed)
                
                if remotable:
                    await self._salmonator.push(obj.ghid)
            
                return True
    
    @direct_ingest.fixture
    async def direct_ingest(self, obj, packed, remotable, skip_conn=None):
        ''' Fixture direct ingest to just store at librarian directly
        with no verification (if librarian exists), otherwise simply
        return None.
        '''
        try:
            librarian = self._librarian
        except AttributeError:
            return None
        else:
            await librarian.store(obj, packed)
    
    @public_api
    async def attempt_load(self, packed, quiet=True):
        ''' Attempt to load a packed golix object. If quiet=False, it
        will raise if there is no loader.
        
        TODO: move into doorman.
        '''
        # This is kinda silly, but instead of spewing off a million different
        # threads that will immediately die, let's pre-select the loader
        magic = bytes(packed[:4])
        loaders = {
            b'GIDC': self._doorman.load_gidc,
            b'GEOC': self._doorman.load_geoc,
            b'GOBS': self._doorman.load_gobs,
            b'GOBD': self._doorman.load_gobd,
            b'GDXX': self._doorman.load_gdxx,
            b'GARQ': self._doorman.load_garq
        }
        
        try:
            loader = loaders[magic]
            
        # If no successful loader was found, return None, and allow the parent
        # to raise.
        except KeyError as exc:
            if quiet:
                return None
            else:
                raise MalformedGolixPrimitive('No loader found for magic: ' +
                                              str(magic)) from exc
        
        obj = await loader(packed)
            
        return obj
        
    @attempt_load.fixture
    async def attempt_load(self, packed):
        ''' Create an ad-hoc doorman fixture.
        '''
        # Note that, because of the weak ref, we need to actually hold this
        # here to prevent the doorman from being gc'd. So, just create a
        # disposable one.
        doorman = Doorman.__fixture__()
        self._doorman = doorman
        result = \
            await super(PersistenceCore.__fixture__, self).attempt_load(packed)
        del doorman
        return result
    
    @fixture_noop
    @public_api
    async def ingest(self, packed, remotable=True, skip_conn=None):
        ''' Called on an untrusted and unknown object. May be bypassed
        by locally-created, trusted objects (by calling the individual
        ingest methods directly). Parses, validates, and stores the
        object, and returns True; or, raises an error.
        '''
        # This may return None, but that will be caught by the KeyError below.
        obj = await self.attempt_load(packed)
        if obj is None:
            raise MalformedGolixPrimitive(
                'Packed bytes do not appear to be a Golix primitive.'
            )
        
        ingested = await self.direct_ingest(obj, packed, remotable)
        
        # Note that individual ingest methods are only called directly for
        # locally-built objects, which do not need a mail run.
        # If the object is identical to what we already have, the ingester
        # will return None.
        if ingested:
            await self._postman.schedule(obj, skip_conn=skip_conn)
            
        else:
            logger.debug(str(obj.ghid) + ' postal scheduling aborted on ' +
                         'unchanged object.')
        
        # Note: this is not the place for salmonator pushing! Locally
        # created/updated objects call the individual ingest methods
        # directly, so they have to be the ones that actually deal with it.
        
        return ingested
        
        
class Doorman(metaclass=API):
    ''' Parses files and enforces crypto. Can be bypassed for trusted
    (aka locally-created) objects. Only called from within the typeless
    PersisterCore.ingest() method.
    '''
    _librarian = weak_property('__librarian')
    
    # Async stuff
    _executor = readonly_property('__executor')
    _loop = readonly_property('__loop')
    
    @public_api
    def __init__(self, executor, loop, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._golix = ThirdParty()
        
        # These coordinate the threads in the executor to bolt-on thread safety
        # to the un-thread-safe smartyparse stuff.
        self._parselock_gidc = threading.Lock()
        self._parselock_geoc = threading.Lock()
        self._parselock_gobs = threading.Lock()
        self._parselock_gobd = threading.Lock()
        self._parselock_gdxx = threading.Lock()
        self._parselock_garq = threading.Lock()
        
        # Async-specific stuff
        setattr(self, '__executor', executor)
        setattr(self, '__loop', loop)
        
    @__init__.fixture
    def __init__(self, *args, **kwargs):
        super(Doorman.__fixture__, self).__init__(
            executor = None,
            loop = None
        )
        
    def assemble(self, librarian):
        # Called to link to the librarian.
        self._librarian = librarian
            
    def _verify_golix(self, obj, author):
        ''' Performs golix verification of the object. Meant to be
        called from within the executor.
        '''
        try:
            self._golix.verify_object(
                second_party = author.identity,
                obj = obj,
            )
        except SecurityError as exc:
            raise VerificationFailure(str(obj)) from exc
        
    @public_api
    async def load_gidc(self, packed):
        # Run the actual loader in the executor
        obj = await self._loop.run_in_executor(
            self._executor,
            self._load_gidc,
            packed
        )
            
        # No further verification required.
        return _GidcLite.from_golix(obj)
        
    @load_gidc.fixture
    async def load_gidc(self, packed):
        ''' Bypass the executor.
        '''
        return _GidcLite.from_golix(self._load_gidc(packed))
        
    def _load_gidc(self, packed):
        ''' Performs the actual loading.
        '''
        try:
            with self._parselock_gidc:
                return GIDC.unpack(packed)
        
        except Exception as exc:
            raise MalformedGolixPrimitive('Invalid formatting for GIDC ' +
                                          'object.') from exc
    
    @public_api
    async def load_geoc(self, packed):
        # Run the actual loader in the executor
        obj = await self._loop.run_in_executor(
            self._executor,
            self._load_geoc,
            packed
        )
            
        # Okay, now we need to verify the object
        try:
            author = await self._librarian.summarize(obj.author)
        
        except KeyError as exc:
            raise InvalidIdentity('Unknown author: ' +
                                  str(obj.author)) from exc
        
        # Finally, verify the Golix signature
        await self._loop.run_in_executor(
            self._executor,
            self._verify_golix,
            obj,
            author
        )
            
        return _GeocLite.from_golix(obj)
        
    @load_geoc.fixture
    async def load_geoc(self, packed):
        ''' Bypass the executor.
        '''
        return _GeocLite.from_golix(self._load_geoc(packed))
        
    def _load_geoc(self, packed):
        ''' Performs the actual loading.
        '''
        try:
            with self._parselock_geoc:
                return GEOC.unpack(packed)
        
        except Exception as exc:
            raise MalformedGolixPrimitive('Invalid formatting for GEOC ' +
                                          'object.') from exc
    
    @public_api
    async def load_gobs(self, packed):
        # Run the actual loader in the executor
        obj = await self._loop.run_in_executor(
            self._executor,
            self._load_gobs,
            packed
        )
            
        # Okay, now we need to verify the object
        try:
            author = await self._librarian.summarize(obj.binder)
        except KeyError as exc:
            raise InvalidIdentity('Unknown author: ' +
                                  str(obj.binder)) from exc
        
        # Finally, verify the Golix signature
        await self._loop.run_in_executor(
            self._executor,
            self._verify_golix,
            obj,
            author
        )
            
        return _GobsLite.from_golix(obj)
        
    @load_gobs.fixture
    async def load_gobs(self, packed):
        ''' Bypass the executor.
        '''
        return _GobsLite.from_golix(self._load_gobs(packed))
        
    def _load_gobs(self, packed):
        ''' Performs the actual loading.
        '''
        try:
            with self._parselock_gobs:
                return GOBS.unpack(packed)
        
        except Exception as exc:
            raise MalformedGolixPrimitive('Invalid formatting for GOBS ' +
                                          'object.') from exc
    
    @public_api
    async def load_gobd(self, packed):
        # Run the actual loader in the executor
        obj = await self._loop.run_in_executor(
            self._executor,
            self._load_gobd,
            packed
        )
            
        # Okay, now we need to verify the object
        try:
            author = await self._librarian.summarize(obj.binder)
        except KeyError as exc:
            raise InvalidIdentity('Unknown author: ' +
                                  str(obj.binder)) from exc
        
        # Finally, verify the Golix signature
        await self._loop.run_in_executor(
            self._executor,
            self._verify_golix,
            obj,
            author
        )
            
        return _GobdLite.from_golix(obj)
        
    @load_gobd.fixture
    async def load_gobd(self, packed):
        ''' Bypass the executor.
        '''
        return _GobdLite.from_golix(self._load_gobd(packed))
        
    def _load_gobd(self, packed):
        ''' Performs the actual loading.
        '''
        try:
            with self._parselock_gobd:
                return GOBD.unpack(packed)
        
        except Exception as exc:
            raise MalformedGolixPrimitive('Invalid formatting for GOBD '
                                          'object.') from exc
    
    @public_api
    async def load_gdxx(self, packed):
        # Run the actual loader in the executor
        obj = await self._loop.run_in_executor(
            self._executor,
            self._load_gdxx,
            packed
        )
            
        # Okay, now we need to verify the object
        try:
            author = await self._librarian.summarize(obj.debinder)
        except KeyError as exc:
            raise InvalidIdentity('Unknown author: ' +
                                  str(obj.debinder)) from exc
        
        # Finally, verify the Golix signature
        await self._loop.run_in_executor(
            self._executor,
            self._verify_golix,
            obj,
            author
        )
            
        return _GdxxLite.from_golix(obj)
        
    @load_gdxx.fixture
    async def load_gdxx(self, packed):
        ''' Bypass the executor.
        '''
        return _GdxxLite.from_golix(self._load_gdxx(packed))
        
    def _load_gdxx(self, packed):
        ''' Performs the actual loading.
        '''
        try:
            with self._parselock_gdxx:
                return GDXX.unpack(packed)
        
        except Exception as exc:
            raise MalformedGolixPrimitive('Invalid formatting for GDXX ' +
                                          'object.') from exc
    
    @public_api
    async def load_garq(self, packed):
        # Run the actual loader in the executor
        obj = await self._loop.run_in_executor(
            self._executor,
            self._load_garq,
            packed
        )
            
        # Persisters cannot further verify the object.
        return _GarqLite.from_golix(obj)
        
    @load_garq.fixture
    async def load_garq(self, packed):
        ''' Bypass the executor.
        '''
        return _GarqLite.from_golix(self._load_garq(packed))
        
    def _load_garq(self, packed):
        ''' Performs the actual loading.
        '''
        try:
            with self._parselock_garq:
                return GARQ.unpack(packed)
        
        except Exception as exc:
            raise MalformedGolixPrimitive('Invalid formatting for GARQ ' +
                                          'object.') from exc


class Enforcer(metaclass=API):
    ''' Enforces valid target selections.
    '''
    _librarian = weak_property('__librarian')
    
    @fixture_api
    def __init__(self, librarian, *args, **kwargs):
        super(Enforcer.__fixture__, self).__init__(*args, **kwargs)
        self._librarian = librarian
        
    def assemble(self, librarian):
        # Call before using.
        self._librarian = librarian
        
    async def validate_gidc(self, obj):
        ''' GIDC need no target verification.
        '''
        return True
        
    async def validate_geoc(self, obj):
        ''' GEOC need no target validation.
        '''
        return True
        
    async def validate_gobs(self, obj):
        ''' Check if target is known, and if it is, validate it.
        '''
        try:
            target = await self._librarian.summarize(obj.target)
        # TODO: think more about this, and whether everything has been updated
        # appropriately to raise a DoesNotExist instead of a KeyError.
        # This could be more specific and say DoesNotExist
        except KeyError:
            logger.debug(str(obj) + ' target missing from librarian: ' +
                         str(obj.target))
        else:
            for forbidden in (_GidcLite, _GobsLite, _GdxxLite, _GarqLite):
                if isinstance(target, forbidden):
                    raise InvalidTarget(str(obj) + ' target invalid: ' +
                                        str(target))
        return True
        
    async def validate_gobd(self, obj):
        ''' Check if target is known, and if it is, validate it.
        
        Also do a state check on the dynamic binding.
        '''
        try:
            target = await self._librarian.summarize(obj.target)
        except KeyError:
            logger.debug(str(obj) + ' target missing from librarian: ' +
                         str(obj.target))
        else:
            for forbidden in (_GidcLite, _GobsLite, _GdxxLite, _GarqLite):
                if isinstance(target, forbidden):
                    raise InvalidTarget(str(obj) + ' target invalid: ' +
                                        str(target))
                    
        await self._validate_dynamic_history(obj)
                    
        return True
        
    async def validate_gdxx(self, obj, target_obj=None):
        ''' Check if target is known, and if it is, validate it.
        '''
        try:
            if target_obj is None:
                target = await self._librarian.summarize(obj.target)
            else:
                target = target_obj
        except KeyError:
            logger.warning(str(obj) + ' validated by Enforcer, but its ' +
                           'target was unknown: ' + str(obj.target))
            logger.debug(str(obj) + ' missing target traceback:\n' +
                         ''.join(traceback.format_exc()))
            
        else:
            # NOTE: if this changes, will need to modify place_gdxx in _Bookie
            for forbidden in (_GidcLite, _GeocLite):
                if isinstance(target, forbidden):
                    raise InvalidTarget(str(obj) + ' target invalid: ' +
                                        str(target))
        return True
        
    async def validate_garq(self, obj):
        ''' No additional validation needed.
        '''
        return True
        
    async def _validate_dynamic_history(self, obj):
        ''' Enforces state flow / progression for dynamic objects. In
        other words, ensures monotonic counter.
        '''
        # Try getting an existing binding.
        try:
            existing = await self._librarian.summarize(obj.ghid)
        
        # TOFU (trust on first upload lulz)
        except KeyError:
            pass
                
        else:
            if existing.counter >= obj.counter:
                logger.debug('New obj frame:     ' +
                             str(obj.frame_ghid))
                logger.debug('New obj tarvec:    ' +
                             str(obj.target_vector))
                logger.debug('Existing frame:    ' +
                             str(existing.frame_ghid))
                logger.debug('Existing tarvec:   ' +
                             str(existing.target_vector))
                raise IllegalDynamicFrame(str(obj.ghid) + ' counter ' +
                                          'decreased from ' +
                                          str(existing.counter) + ' to ' +
                                          str(obj.counter))


class Bookie(metaclass=API):
    ''' Tracks state relationships between objects using **only weak
    references** to them. ONLY CONCERNED WITH LIFETIMES! Does not check
    (for example) consistent authorship.
    '''
    _librarian = weak_property('__librarian')
        
    def assemble(self, librarian):
        # Call before using.
        self._librarian = librarian
        
    async def validate_gidc(self, obj):
        ''' GIDC need no state verification.
        '''
        return True
        
    async def validate_geoc(self, obj):
        ''' GEOC must verify that they are bound.
        '''
        if not (await self._librarian.is_bound(obj)):
            raise UnboundContainer(str(obj))
        
        return True
        
    async def validate_gobs(self, obj):
        if (await self._librarian.is_debound(obj)):
            raise AlreadyDebound(str(obj), ghid=obj.ghid)
            
        return True
        
    async def validate_gobd(self, obj):
        # A deliberate binding can override a debinding for GOBD.
        if (await self._librarian.is_debound(obj)):
            if not (await self._librarian.is_bound(obj)):
                raise AlreadyDebound(str(obj), ghid=obj.ghid)
                
        return True
        
    async def validate_gdxx(self, obj):
        if (await self._librarian.is_debound(obj)):
            raise AlreadyDebound(str(obj), ghid=obj.ghid)
            
        return True
        
    async def validate_garq(self, obj):
        if (await self._librarian.is_debound(obj)):
            raise AlreadyDebound(str(obj), ghid=obj.ghid)
            
        return True
