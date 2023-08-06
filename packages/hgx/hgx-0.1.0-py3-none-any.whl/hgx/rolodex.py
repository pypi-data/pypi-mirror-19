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
import traceback
import collections
import asyncio

from golix import Ghid

from golix.crypto_utils import AsymHandshake
from golix.crypto_utils import AsymAck
from golix.crypto_utils import AsymNak

from loopa.utils import make_background_future

# Local dependencies
from .hypothetical import API
from .hypothetical import public_api
from .hypothetical import fixture_api
from .hypothetical import fixture_noop

from .exceptions import UnknownParty

from .persistence import _GeocLite
from .persistence import _GobdLite
from .persistence import _GarqLite
from .persistence import _GdxxLite

from .utils import weak_property
from .utils import readonly_property


# ###############################################
# Boilerplate
# ###############################################


import logging
logger = logging.getLogger(__name__)

# Control * imports.
__all__ = [
    'Rolodex',
]


# ###############################################
# Library
# ###############################################
            
            
_SharePair = collections.namedtuple(
    typename = '_SharePair',
    field_names = ('ghid', 'recipient'),
)


class Rolodex(metaclass=API):
    ''' Handles sharing, requests, etc.
    
    In the future, will maintain a contacts list to approve/reject
    incoming requests. In the further future, will maintain sharing
    pipelines, negotiated through handshakes, to perform sharing
    symmetrically between contacts.
    '''
    _account = weak_property('__account')
    _golcore = weak_property('__golcore')
    _ghidproxy = weak_property('__ghidproxy')
    _privateer = weak_property('__privateer')
    _percore = weak_property('__percore')
    _librarian = weak_property('__librarian')
    _salmonator = weak_property('__salmonator')
    _dispatch = weak_property('__dispatch')
    
    @public_api
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Persistent dict-like lookup for
        # request_ghid -> (request_target, request recipient)
        self._pending_requests = None
        # Lookup for <target_obj_ghid, recipient> -> set(<app_tokens>)
        self._outstanding_shares = None
        
    @__init__.fixture
    def __init__(self, *args, **kwargs):
        ''' Init the fixture.
        '''
        super(Rolodex.__fixture__, self).__init__(*args, **kwargs)
        
        self.shared = {}
        self._pending_requests = {}
        self._outstanding_shares = {}
        
    @fixture_api
    def RESET(self):
        ''' Super simple reset alias to __init__.
        '''
        self.shared.clear()
        self._pending_requests.clear()
        self._outstanding_shares.clear()
        
    @fixture_noop
    @public_api
    def bootstrap(self, account):
        ''' Initialize distributed state.
        '''
        self._account = account
        
        # Persistent dict-like lookup for
        # request_ghid -> (request_target, request recipient)
        self._pending_requests = account.rolodex_pending
        
        # These need to be distributed but aren't yet. TODO!
        # Lookup for <target_obj_ghid, recipient> -> set(<app_tokens>)
        self._outstanding_shares = account.rolodex_outstanding
        
    def assemble(self, golcore, ghidproxy, privateer, percore, librarian,
                 salmonator, dispatch):
        # Chicken, meet egg.
        self._golcore = golcore
        self._ghidproxy = ghidproxy
        self._privateer = privateer
        self._percore = percore
        self._librarian = librarian
        self._salmonator = salmonator
        self._dispatch = dispatch
        
    @public_api
    async def share_object(self, target, recipient, requesting_token):
        ''' Share a target ghid with the recipient.
        '''
        if not isinstance(target, Ghid):
            raise TypeError(
                'target must be Ghid or similar.'
            )
        if not isinstance(recipient, Ghid):
            raise TypeError(
                'recipient must be Ghid or similar.'
            )

        sharepair = _SharePair(target, recipient)
            
        # For now, this is just doing a handshake with some typechecking.
        await self._hand_object(*sharepair)
        
        if requesting_token is not None:
            self._outstanding_shares.add(sharepair, requesting_token)
            await self._account.flush()
            
    @share_object.fixture
    async def share_object(self, target, recipient, requesting_token):
        ''' Pretty basic.
        '''
        # Ignore requesting token, because we won't generally set it when
        # testing this.
        self.shared[target] = recipient
        
    async def _hand_object(self, target, recipient):
        ''' Initiates a handshake request with the recipient.
        '''
        if not (await self._librarian.contains(recipient)):
            await self._salmonator.attempt_pull(recipient, quiet=True)
        
        recipient_identity = \
            (await self._librarian.summarize(recipient)).identity
        
        # This is guaranteed to resolve the container fully.
        container_ghid = await self._ghidproxy.resolve(target)
        
        # TODO: fix Golix library so this isn't such a shitshow re:
        # breaking abstraction barriers.
        handshake = self._golcore._identity.make_handshake(
            target = target,
            secret = self._privateer.get(container_ghid)
        )
        
        request = self._golcore._identity.make_request(
            recipient = recipient_identity,
            request = handshake
        )
        
        # Note that this must be called before publishing to the persister, or
        # there's a race condition between them.
        self._pending_requests[request.ghid] = target, recipient
        
        # Note the potential race condition here. Should catch errors with the
        # persister in case we need to resolve pending requests that didn't
        # successfully post.
        await self._percore.direct_ingest(
            obj = _GarqLite.from_golix(request),
            packed = request.packed,
            remotable = True
        )
    
    @fixture_noop
    @public_api
    async def notification_handler(self, subscription, notification):
        ''' Callback to handle any requests.
        '''
        if not (await self._librarian.contains(notification)):
            await self._salmonator.attempt_pull(notification, quiet=True)
        
        # Note that the notification could also be a GDXX.
        request_or_debind = await self._librarian.summarize(notification)
        
        if isinstance(request_or_debind, _GarqLite):
            await self._handle_request(notification)
            
        elif isinstance(request_or_debind, _GdxxLite):
            # This case should only be relevant if we have multiple agents
            # logged in at separate locations at the same time, processing the
            # same GARQs.
            await self._handle_debinding(request_or_debind)
            
        else:
            raise RuntimeError(
                'Unexpected Golix primitive while listening for requests.'
            )
            
    async def _handle_request(self, notification):
        ''' The notification is an asymmetric request. Deal with it.
        '''
        try:
            packed = await self._librarian.retrieve(notification)
            unpacked = await self._golcore.unpack_request(packed)
        
            # TODO: have this filter based on contacts.
            if not (await self._librarian.contains(unpacked.author)):
                await self._salmonator.attempt_pull(
                    unpacked.author,
                    quiet = True
                )
        
            payload = await self._golcore.open_request(unpacked)
            await self._dispatch_payload(payload, notification)

        # Don't forget to (always) debind.
        finally:
            debinding = await self._golcore.make_debinding(notification)
            await self._percore.direct_ingest(
                obj = _GdxxLite.from_golix(debinding),
                packed = debinding.packed,
                remotable = True
            )
        
    async def _handle_debinding(self, debinding):
        ''' The notification is a debinding. Deal with it.
        '''
        # For now we just need to remove any pending requests for the
        # debinding's target.
        try:
            del self._pending_requests[debinding.target]
            await self._account.flush()
        except KeyError:
            logger.debug(
                'Request at ' + str(debinding.ghid) + ' target missing ' +
                'from pending requests: ' + str(debinding.target)
            )
        
    async def _dispatch_payload(self, payload, source_ghid):
        ''' Appropriately handles a request payload.
        '''
        if isinstance(payload, AsymHandshake):
            logger.debug(
                'Share handshake received from ' + str(payload.author) +
                ' at ' + str(source_ghid) + ' for ' + str(payload.target)
            )
            await self._handle_handshake(payload, source_ghid)
            
        elif isinstance(payload, AsymAck):
            logger.debug(
                'Handshake ACK received from ' + str(payload.author) +
                ' at ' + str(source_ghid) + ' for ' + str(payload.target)
            )
            await self._handle_ack(payload)
            
        elif isinstance(payload, AsymNak):
            logger.debug(
                'Handshake NAK received from ' + str(payload.author) +
                ' at ' + str(source_ghid) + ' for ' + str(payload.target)
            )
            await self._handle_nak(payload)
            
        else:
            raise RuntimeError('Encountered an unknown request type.')
            
    async def _handle_handshake(self, request, source_ghid):
        ''' Handles a handshake request after reception.
        '''
        try:
            # First, we need to figure out what the actual container object's
            # address is, and then stage the secret for it.
            # ALWAYS attempt to pull it first, or we may have a stale frame
            # locally, and attempt to stage a new secret for a long-expired
            # frame
            await self._salmonator.attempt_pull(
                request.target,
                quiet = True
            )
            
            binding_or_obj = await self._librarian.summarize(request.target)
            if isinstance(binding_or_obj, _GobdLite):
                container_ghid = binding_or_obj.target
                self._privateer.quarantine(
                    ghid = container_ghid,
                    secret = request.secret
                )
                if not (await self._librarian.contains(container_ghid)):
                    await self._salmonator.attempt_pull(
                        container_ghid,
                        quiet = True
                    )
            elif isinstance(binding_or_obj, _GeocLite):
                self._privateer.quarantine(
                    ghid = binding_or_obj.ghid,
                    secret = request.secret
                )
            else:
                raise TypeError(
                    'Invalid handshake target: ' + str(type(binding_or_obj))
                )
            
            # Note that unless we raise a HandshakeError RIGHT NOW, we'll be
            # sending an ack to the handshake, just to indicate successful
            # receipt of the share. If the originating app wants to check for
            # availability, well, that's currently on them. In the future, add
            # handle for that in SHARE instead of HANDSHAKE?
            
        except asyncio.CancelledError:
            logger.debug('Handshake handler cancelled.')
            raise
            
        except Exception as exc:
            logger.error(
                'Exception encountered while handling a handshake. Returned a '
                'NAK.\n' + ''.join(traceback.format_exc())
            )
            # Erfolglos. Send a nak to whomever sent the handshake
            response_obj = self._golcore._identity.make_nak(
                target = source_ghid
            )
            
        else:
            # Success. Send an ack to whomever sent the handshake
            response_obj = self._golcore._identity.make_ack(
                target = source_ghid
            )
        
        response = await self._golcore.make_request(
            request.author,
            response_obj
        )
        await self._percore.direct_ingest(
            obj = _GarqLite.from_golix(response),
            packed = response.packed,
            remotable = True
        )
            
        await self.share_handler(request.target, request.author)
            
    async def _handle_ack(self, request):
        ''' Handles a handshake ack after reception.
        '''
        try:
            target, recipient = self._pending_requests.pop(request.target)
        except KeyError:
            logger.error(
                'Received an ACK for an unknown origin: ' +
                str(request.target)
            )
        else:
            await self.receipt_ack_handler(target, recipient)
            
    async def _handle_nak(self, request):
        ''' Handles a handshake nak after reception.
        '''
        try:
            target, recipient = self._pending_requests.pop(request.target)
        except KeyError:
            logger.error(
                'Received a NAK for an unknown origin: ' +
                str(request.target)
            )
        else:
            await self.receipt_nak_handler(target, recipient)
    
    @fixture_noop
    @public_api
    async def share_handler(self, target, sender):
        ''' Incoming share targets (well, their ghids anyways) are
        forwarded to the _ipccore.
        
        Only separate from _handle_handshake right now because in the
        future, object sharing will be at least partly handled within
        its own dedicated rolodex pipeline.
        '''
        # Make sure we actually have the target
        if not (await self._librarian.contains(target)):
            await self._salmonator.attempt_pull(target, quiet=True)
        
        # Distribute the share in the background
        make_background_future(
            self._dispatch.distribute_share(target, sender)
        )
    
    @fixture_noop
    @public_api
    async def receipt_ack_handler(self, target, recipient):
        ''' Receives a share ack from the rolodex and passes it on to
        the application that requested the share.
        '''
        sharepair = _SharePair(target, recipient)
        tokens = self._outstanding_shares.pop_any(sharepair)
        await self._account.flush()
        
        # Distribute the share success in the background
        make_background_future(
            self._dispatch.distribute_share_success(
                target,
                recipient,
                tokens
            )
        )
    
    @fixture_noop
    @public_api
    async def receipt_nak_handler(self, target, recipient):
        ''' Receives a share nak from the rolodex and passes it on to
        the application that requested the share.
        '''
        sharepair = _SharePair(target, recipient)
        tokens = self._outstanding_shares.pop_any(sharepair)
        await self._account.flush()
        
        # Distribute the share failure in the background
        make_background_future(
            self._dispatch.distribute_share_failure(
                target,
                recipient,
                tokens
            )
        )
