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

# External deps
import logging
import os
import asyncio

# This is only used for padding **within** encrypted containers
import random

from loopa.utils import make_background_future

# from golix import SecondParty
from hashlib import sha512
from golix import Ghid
from golix import Secret
from golix import FirstParty

# These deps are for publishing our identity elsewhere (super awkwardly)
from golix._getlow import GIDC
from .persistence import _GidcLite

# Internal deps
from .hypothetical import API
from .hypothetical import public_api
from .hypothetical import fixture_noop
from .hypothetical import fixture_api

from .utils import immortal_property
from .utils import weak_property
from .utils import SetMap

from .gao import GAO
from .gao import GAOSet
from .gao import GAODict
from .gao import GAOSetMap

# Local dependencies
# from .persistence import _GarqLite
# from .persistence import _GdxxLite


# ###############################################
# Boilerplate
# ###############################################


logger = logging.getLogger(__name__)

# Control * imports.
__all__ = [
    # 'Inquisitor',
]


# ###############################################
# Library
# ###############################################


class Account(metaclass=API):
    ''' Accounts settle all sorts of stuff.
    
    TODO: move GolixCore into account. That way, everything to do with
    the private keys stays within the account, and is never directly
    accessed outside of it.
    '''
    _identity = immortal_property('__identity')
    _user_id = immortal_property('__user_id')
    
    _golcore = weak_property('__golcore')
    _ghidproxy = weak_property('__ghidproxy')
    _privateer = weak_property('__privateer')
    _oracle = weak_property('__oracle')
    _rolodex = weak_property('__rolodex')
    _dispatch = weak_property('__dispatch')
    _percore = weak_property('__percore')
    _librarian = weak_property('__librarian')
    _salmonator = weak_property('__salmonator')
    
    @public_api
    def __init__(self, user_id, root_secret, *args, hgxcore, **kwargs):
        ''' Gets everything ready for account bootstrapping.
        
        +   user_id explicitly passed with None means create a new
            Account.
        +   identity explicitly passed with None means load an existing
            account.
        +   user_id XOR identity must be passed.
        '''
        super().__init__(*args, **kwargs)
        
        if isinstance(user_id, Ghid):
            logger.info('Logging in with existing user ID: ' + str(user_id))
            self._identity = None
            self._user_id = user_id
        
        # This is used exclusively for testing.
        elif isinstance(user_id, FirstParty):
            logger.info('Creating a new account.')
            self._identity = user_id
            self._user_id = None
        
        else:
            raise TypeError('user_id must be an instance of Ghid or None.')
            
        self._golcore = hgxcore.golcore
        self._ghidproxy = hgxcore.ghidproxy
        self._privateer = hgxcore.privateer
        self._oracle = hgxcore.oracle
        self._rolodex = hgxcore.rolodex
        self._dispatch = hgxcore.dispatch
        self._percore = hgxcore.percore
        self._librarian = hgxcore.librarian
        self._salmonator = hgxcore.salmonator
        
        self._root_secret = root_secret
        
    @__init__.fixture
    def __init__(self, identity, *args, **kwargs):
        ''' Lulz just ignore errytang and skip calling super!
        '''
        self._identity = identity
        
        self.privateer_persistent = {}
        self.privateer_quarantine = {}
        
        self.rolodex_pending = {}
        self.rolodex_outstanding = SetMap()
        
        self.dispatch_tokens = set()
        self.dispatch_startup = {}
        self.dispatch_private = {}
        self.dispatch_incoming = set()
        self.dispatch_orphan_acks = SetMap()
        self.dispatch_orphan_naks = SetMap()
        
    @property
    def _fingerprint(self):
        ''' Get our fingerprint.
        '''
        return self._identity.ghid
        
    async def _inject_gao(self, gao):
        ''' Bypass the normal oracle get_object, new_object process and
        create the object directly.
        '''
        await self._salmonator.register(gao.ghid)
        await self._salmonator.attempt_pull(gao.ghid, quiet=True)
        gao._ctx = asyncio.Event()
        gao._ctx.set()
        self._oracle._lookup[gao.ghid] = gao
            
    async def bootstrap(self):
        ''' Used for account creation, to initialize the root node with
        its resource directory.
        '''
        # We need to pre-allocate the privateer stuff so we can bootstrap it
        # before pulling the root node when reloading.
        self.privateer_persistent = GAODict(
            ghid = None,
            dynamic = True,
            author = None,
            legroom = 7,
            golcore = self._golcore,
            ghidproxy = self._ghidproxy,
            privateer = self._privateer,
            percore = self._percore,
            librarian = self._librarian
        )
        self.privateer_quarantine = GAODict(
            ghid = None,
            dynamic = True,
            author = None,
            legroom = 7,
            golcore = self._golcore,
            ghidproxy = self._ghidproxy,
            privateer = self._privateer,
            percore = self._percore,
            librarian = self._librarian
        )
        
        # Privateer can be bootstrapped with or without pulling. Even though it
        # won't work *right* before pulling, it won't work AT ALL until it's
        # bootstrapped, so bootstrap first and pull later.
        logger.info('Bootstrapping privateer.')
        self._privateer.bootstrap(self)
        
        if self._user_id is not None:
            logger.info('Loading the root node.')
            root_node = GAO(
                ghid = self._user_id,
                dynamic = True,
                author = None,
                legroom = 7,
                state = b'you pass butter',
                golcore = self._golcore,
                ghidproxy = self._ghidproxy,
                privateer = self._privateer,
                percore = self._percore,
                librarian = self._librarian,
                master_secret = self._root_secret
            )
            # And now, remove the root secret from the parent namespace. This
            # will make the root_node GAO the only live reference to the root
            # secret from within the Account.
            del self._root_secret
            await root_node._pull()
                
            # TODO: convert all of this into a smartyparser (after rewriting
            # smartyparse, that is)
            
            # The last 64 bytes of the state is a SHA512 checksum for the whole
            # rest of the state
            password_validator = root_node.state[-64:]
            password_comparator = root_node.state[:-64]
            
            # This comparison is timing-insensitive: if attempting to brute
            # force a password, incorrect password attempts cannot extract any
            # information from the timing of the comparison.
            if sha512(password_comparator).digest() != password_validator:
                logger.critical('Incorrect password.')
                raise ValueError('Incorrect password.')
            
            # Identity
            identity_ghid = Ghid.from_bytes(
                root_node.state[0: 65])     # 65 bytes
            identity_master = Secret.from_bytes(
                root_node.state[65: 118])   # 53 bytes
            
            # Privateer
            privateer_persistent_ghid = Ghid.from_bytes(
                root_node.state[118: 183])
            privateer_persistent_master = Secret.from_bytes(
                root_node.state[183: 236])
            
            privateer_quarantine_ghid = Ghid.from_bytes(
                root_node.state[236: 301])
            privateer_quarantine_master = Secret.from_bytes(
                root_node.state[301: 354])
            
            # Rolodex stuff
            rolodex_pending_ghid = Ghid.from_bytes(
                root_node.state[354: 419])
            rolodex_pending_master = Secret.from_bytes(
                root_node.state[419: 472])
            
            rolodex_outstanding_ghid = Ghid.from_bytes(
                root_node.state[472: 537])
            rolodex_outstanding_master = Secret.from_bytes(
                root_node.state[537: 590])
            
            # Dispatch stuff
            dispatch_tokens_ghid = Ghid.from_bytes(
                root_node.state[590: 655])
            dispatch_tokens_master = Secret.from_bytes(
                root_node.state[655: 708])
            
            dispatch_startup_ghid = Ghid.from_bytes(
                root_node.state[708: 773])
            dispatch_startup_master = Secret.from_bytes(
                root_node.state[773: 826])
            
            dispatch_private_ghid = Ghid.from_bytes(
                root_node.state[826: 891])
            dispatch_private_master = Secret.from_bytes(
                root_node.state[891: 944])
            
            dispatch_incoming_ghid = Ghid.from_bytes(
                root_node.state[944: 1009])
            dispatch_incoming_master = Secret.from_bytes(
                root_node.state[1009: 1062])
            
            dispatch_orphan_acks_ghid = Ghid.from_bytes(
                root_node.state[1062: 1127])
            dispatch_orphan_acks_master = Secret.from_bytes(
                root_node.state[1127: 1180])
            
            dispatch_orphan_naks_ghid = Ghid.from_bytes(
                root_node.state[1180: 1245])
            dispatch_orphan_naks_master = Secret.from_bytes(
                root_node.state[1245: 1298])
        
        else:
            # We need an identity at to golcore before we can do anything
            logger.info('Bootstrapping golcore.')
            self._golcore.bootstrap(self)
            
            # Note that we first need to push our identity secondparty.
            packed = self._identity.second_party.packed
            gidc = _GidcLite.from_golix(GIDC.unpack(packed))
            logger.info('Publishing public keys.')
            # We haven't bootstrapped salmonator yet, so don't remote the keys
            await self._percore.direct_ingest(gidc, packed, remotable=False)
            
            # Now we need to declare the root note. It needs some kind of
            # useless, garbage data as well, lest it error out because it can't
            # encrypt nothingness.
            root_node = GAO(
                ghid = None,
                dynamic = True,
                author = None,
                legroom = 7,
                state = b'you pass butter',
                golcore = self._golcore,
                ghidproxy = self._ghidproxy,
                privateer = self._privateer,
                percore = self._percore,
                librarian = self._librarian,
                master_secret = self._root_secret
            )
            # And now, remove the root secret from the parent namespace. This
            # will make the root_node GAO the only live reference to the root
            # secret from within the Account.
            del self._root_secret
            
            identity_ghid = None
            identity_master = self._identity.new_secret()
            
            privateer_persistent_ghid = None
            privateer_persistent_master = self._identity.new_secret()
            
            privateer_quarantine_ghid = None
            privateer_quarantine_master = self._identity.new_secret()
            
            # Rolodex stuff
            rolodex_pending_ghid = None
            rolodex_pending_master = self._identity.new_secret()
            
            rolodex_outstanding_ghid = None
            rolodex_outstanding_master = self._identity.new_secret()
            
            # Dispatch stuff
            dispatch_tokens_ghid = None
            dispatch_tokens_master = self._identity.new_secret()
            
            dispatch_startup_ghid = None
            dispatch_startup_master = self._identity.new_secret()
            
            dispatch_private_ghid = None
            dispatch_private_master = self._identity.new_secret()
            
            dispatch_incoming_ghid = None
            dispatch_incoming_master = self._identity.new_secret()
            
            dispatch_orphan_acks_ghid = None
            dispatch_orphan_acks_master = self._identity.new_secret()
            
            dispatch_orphan_naks_ghid = None
            dispatch_orphan_naks_master = self._identity.new_secret()
        
        # Allocate the identity container
        #######################################################################
        # This stores the private keys
        identity_container = GAODict(
            ghid = identity_ghid,
            dynamic = True,
            author = None,
            legroom = 7,
            golcore = self._golcore,
            ghidproxy = self._ghidproxy,
            privateer = self._privateer,
            percore = self._percore,
            librarian = self._librarian,
            master_secret = identity_master
        )
        
        # Jiggery-pokery for the privateer restoration
        #######################################################################
        # This stores persistent secrets
        self.privateer_persistent.ghid = privateer_persistent_ghid
        self.privateer_persistent._inject_msec(privateer_persistent_master)
        
        self.privateer_quarantine.ghid = privateer_quarantine_ghid
        self.privateer_quarantine._inject_msec(privateer_quarantine_master)
        
        # Save/load the identity container and bootstrap golcore, privateer
        #######################################################################
        
        # Load existing account
        if self._user_id is not None:
            logger.info('Loading identity.')
            await identity_container._pull()
            self._identity = FirstParty._from_serialized(
                identity_container.state
            )
            logger.info('Bootstrapping golcore.')
            self._golcore.bootstrap(self)
            logger.info('Bootstrapping salmonator.')
            await self._salmonator.bootstrap(self)
            
            logger.info('Loading persistent keystore.')
            await self.privateer_persistent._pull()

            logger.info('Loading quarantined keystore.')
            await self.privateer_quarantine._pull()
            
        # Save new account
        else:
            # First, bootstrap salmonator, so that we don't get errors as an
            # unknown author
            await self._salmonator.bootstrap(self)
            # Initializing is needed to prevent losing the first frame while
            # the secret ratchet initializes
            logger.info('Allocating the root node.')
            await root_node._push()
            # Don't forget to do this before creating the actual identity
            # frame, or we'll lose the first frame (and therefore, everything
            # we care about)
            logger.info('Allocating identity container.')
            await identity_container._push(force=True)
            logger.info('Saving identity.')
            identity_container.update(self._identity._serialize())
            await identity_container._push(force=True)
            
            # Because these use a master secret, they need to be initialized,
            # or the first frame will be unrecoverable.
            logger.info('Allocating persistent keystore.')
            await self.privateer_persistent._push(force=True)
            await self.privateer_persistent._push(force=True)
            
            logger.info('Allocating quarantined keystore.')
            await self.privateer_quarantine._push(force=True)
            await self.privateer_quarantine._push(force=True)
            
        # Establish the rest of the above at the various tracking agencies
        logger.info('Reticulating keystores.')
        await self._inject_gao(self.privateer_persistent)
        await self._inject_gao(self.privateer_quarantine)
        # We don't need to do this with the secondary manifest (unless we're
        # planning on adding things to it while already running, which would
        # imply an ad-hoc, on-the-fly upgrade process)
        
        # Rolodex gaos:
        self.rolodex_pending = GAODict(
            ghid = rolodex_pending_ghid,
            dynamic = True,
            author = None,
            legroom = 7,
            golcore = self._golcore,
            ghidproxy = self._ghidproxy,
            privateer = self._privateer,
            percore = self._percore,
            librarian = self._librarian,
            master_secret = rolodex_pending_master
        )
        self.rolodex_outstanding = GAOSetMap(
            ghid = rolodex_outstanding_ghid,
            dynamic = True,
            author = None,
            legroom = 7,
            golcore = self._golcore,
            ghidproxy = self._ghidproxy,
            privateer = self._privateer,
            percore = self._percore,
            librarian = self._librarian,
            master_secret = rolodex_outstanding_master
        )
        
        # Dispatch gaos:
        self.dispatch_tokens = GAOSet(
            ghid = dispatch_tokens_ghid,
            dynamic = True,
            author = None,
            legroom = 7,
            golcore = self._golcore,
            ghidproxy = self._ghidproxy,
            privateer = self._privateer,
            percore = self._percore,
            librarian = self._librarian,
            master_secret = dispatch_tokens_master
        )
        self.dispatch_startup = GAODict(
            ghid = dispatch_startup_ghid,
            dynamic = True,
            author = None,
            legroom = 7,
            golcore = self._golcore,
            ghidproxy = self._ghidproxy,
            privateer = self._privateer,
            percore = self._percore,
            librarian = self._librarian,
            master_secret = dispatch_startup_master
        )
        self.dispatch_private = GAODict(
            ghid = dispatch_private_ghid,
            dynamic = True,
            author = None,
            legroom = 7,
            golcore = self._golcore,
            ghidproxy = self._ghidproxy,
            privateer = self._privateer,
            percore = self._percore,
            librarian = self._librarian,
            master_secret = dispatch_private_master
        )
        self.dispatch_incoming = GAOSet(
            ghid = dispatch_incoming_ghid,
            dynamic = True,
            author = None,
            legroom = 7,
            golcore = self._golcore,
            ghidproxy = self._ghidproxy,
            privateer = self._privateer,
            percore = self._percore,
            librarian = self._librarian,
            master_secret = dispatch_incoming_master
        )
        self.dispatch_orphan_acks = GAOSetMap(
            ghid = dispatch_orphan_acks_ghid,
            dynamic = True,
            author = None,
            legroom = 7,
            golcore = self._golcore,
            ghidproxy = self._ghidproxy,
            privateer = self._privateer,
            percore = self._percore,
            librarian = self._librarian,
            master_secret = dispatch_orphan_acks_master
        )
        self.dispatch_orphan_naks = GAOSetMap(
            ghid = dispatch_orphan_naks_ghid,
            dynamic = True,
            author = None,
            legroom = 7,
            golcore = self._golcore,
            ghidproxy = self._ghidproxy,
            privateer = self._privateer,
            percore = self._percore,
            librarian = self._librarian,
            master_secret = dispatch_orphan_naks_master
        )
        
        # These need not have the actual objects pulled yet
        self._rolodex.bootstrap(self)
        self._dispatch.bootstrap(self)
        
        if self._user_id is not None:
            logger.info('Restoring sharing subsystem.')
            await self.rolodex_pending._pull()
            await self.rolodex_outstanding._pull()
            
            logger.info('Restoring object dispatch.')
            await self.dispatch_tokens._pull()
            await self.dispatch_startup._pull()
            await self.dispatch_private._pull()
            await self.dispatch_incoming._pull()
            await self.dispatch_orphan_acks._pull()
            await self.dispatch_orphan_naks._pull()
        
        else:
            logger.info('Building sharing subsystem.')
            await self.rolodex_pending._push(force=True)
            await self.rolodex_pending._push(force=True)
            await self.rolodex_outstanding._push(force=True)
            await self.rolodex_outstanding._push(force=True)
            
            logger.info('Building object dispatch.')
            await self.dispatch_tokens._push(force=True)
            await self.dispatch_tokens._push(force=True)
            await self.dispatch_startup._push(force=True)
            await self.dispatch_startup._push(force=True)
            await self.dispatch_private._push(force=True)
            await self.dispatch_private._push(force=True)
            await self.dispatch_incoming._push(force=True)
            await self.dispatch_incoming._push(force=True)
            await self.dispatch_orphan_acks._push(force=True)
            await self.dispatch_orphan_acks._push(force=True)
            await self.dispatch_orphan_naks._push(force=True)
            await self.dispatch_orphan_naks._push(force=True)
            
            self._user_id = root_node.ghid
        
            logger.info('Building root node...')
            # Generate secure-random-length, pseudorandom-content padding
            logger.info('    Generating noisy padding.')
            # Note that we don't actually need CSRNG for the padding, just the
            # padding length, since the whole thing is encrypted. We could just
            # as easily fill it with zeros, but by filling it with pseudorandom
            # noise, we can remove a recognizable pattern and therefore slighly
            # hinder brute force attacks against the password.
            # While we COULD use CSRNG despite all that, entropy is a limited
            # resource, and I'd rather conserve it as much as possible.
            padding_seed = int.from_bytes(os.urandom(2), byteorder='big')
            padding_min_size = 1024
            padding_clip_mask = 0b0001111111111111
            # Clip the seed to an upper range of 13 bits, of 8191, for a
            # maximum padding length of 8191 + 1024 = 9215 bytes
            padding_len = padding_min_size + (padding_seed & padding_clip_mask)
            padding_int = random.getrandbits(padding_len * 8)
            padding = padding_int.to_bytes(length=padding_len, byteorder='big')
            
            logger.info('    Serializing primary manifest.')
            root_node.state = (bytes(identity_container.ghid) +
                               bytes(identity_master) +
                               bytes(self.privateer_persistent.ghid) +
                               bytes(privateer_persistent_master) +
                               bytes(self.privateer_quarantine.ghid) +
                               bytes(privateer_quarantine_master) +
                               bytes(self.rolodex_pending.ghid) +
                               bytes(rolodex_pending_master) +
                               bytes(self.rolodex_outstanding.ghid) +
                               bytes(rolodex_outstanding_master) +
                               bytes(self.dispatch_tokens.ghid) +
                               bytes(dispatch_tokens_master) +
                               bytes(self.dispatch_startup.ghid) +
                               bytes(dispatch_startup_master) +
                               bytes(self.dispatch_private.ghid) +
                               bytes(dispatch_private_master) +
                               bytes(self.dispatch_incoming.ghid) +
                               bytes(dispatch_incoming_master) +
                               bytes(self.dispatch_orphan_acks.ghid) +
                               bytes(dispatch_orphan_acks_master) +
                               bytes(self.dispatch_orphan_naks.ghid) +
                               bytes(dispatch_orphan_naks_master) +
                               padding)
            
            # We'll use this upon future logins to verify password correctness
            logger.info('    Generating validator and comparator.')
            # Just append a SHA512 checksum to the whole thing
            password_validator = sha512(root_node.state).digest()
            root_node.state += password_validator
            
            logger.info('Saving root node.')
            await root_node._push()
        
        #######################################################################
        #######################################################################
        # ROOT NODE CREATION (PRIMARY BOOTSTRAP) COMPLETE!
        #######################################################################
        #######################################################################
        
        logger.info('Reticulating sharing subsystem.')
        await self._inject_gao(self.rolodex_pending)
        await self._inject_gao(self.rolodex_outstanding)
        
        logger.info('Reticulating object dispatch.')
        await self._inject_gao(self.dispatch_tokens)
        await self._inject_gao(self.dispatch_startup)
        await self._inject_gao(self.dispatch_private)
        await self._inject_gao(self.dispatch_incoming)
        await self._inject_gao(self.dispatch_orphan_acks)
        await self._inject_gao(self.dispatch_orphan_naks)
        
        logger.info('Account login successful.')
    
    @fixture_noop
    @public_api
    async def flush(self):
        ''' Push changes to any modified account components.
        '''
        tasks = {
            make_background_future(self.privateer_persistent.push()),
            make_background_future(self.privateer_quarantine.push()),
            make_background_future(self.rolodex_pending.push()),
            make_background_future(self.rolodex_outstanding.push()),
            make_background_future(self.dispatch_tokens.push()),
            make_background_future(self.dispatch_startup.push()),
            make_background_future(self.dispatch_private.push()),
            make_background_future(self.dispatch_incoming.push()),
            make_background_future(self.dispatch_orphan_acks.push()),
            make_background_future(self.dispatch_orphan_naks.push())
        }
        await asyncio.wait(fs=tasks, return_when=asyncio.ALL_COMPLETED)


class Accountant:
    ''' The accountant handles account meta-operations. For example,
    tracks device IDs associated with the account, for the purposes of
    making a distributed GAO locks, etc etc etc. Other uses are, for
    example, tracking which devices have handled a given incoming share,
    etc etc etc.
    '''
    pass
