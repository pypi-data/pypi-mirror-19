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
import logging
import collections
import weakref
import queue
import threading
import traceback
import asyncio
import loopa

from loopa.utils import make_background_future

# Local dependencies
from .persistence import _GidcLite
from .persistence import _GeocLite
from .persistence import _GobsLite
from .persistence import _GobdLite
from .persistence import _GdxxLite
from .persistence import _GarqLite

from .utils import SetMap
from .utils import WeakSetMap
from .utils import WeakKeySetMap
from .utils import weak_property

from .gao import GAOCore

from .hypothetical import API
from .hypothetical import public_api
from .hypothetical import fixture_api
from .hypothetical import fixture_noop
from .hypothetical import fixture_return


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
            

_SubsUpdate = collections.namedtuple(
    typename = '_SubsUpdate',
    field_names = ('subscription', 'notification', 'skip_conn'),
)

            
class PostalCore(loopa.TaskLooper, metaclass=API):
    ''' Tracks, delivers notifications about objects using **only weak
    references** to them. Threadsafe.
    
    ♫ Please Mister Postman... ♫
    
    Question: should the distributed state management of GARQ recipients
    be managed here, or in the bookie (where it currently is)?
    '''
    _librarian = weak_property('__librarian')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # The scheduling queue is created at loop init.
        self._scheduled = None
        # The delayed lookup. <awaiting ghid>: set(<subscribed ghids>)
        self._deferred = SetMap()
        
        # Resolve primitives into their schedulers.
        self._scheduler_lookup = {
            _GidcLite: self._schedule_gidc,
            _GeocLite: self._schedule_geoc,
            _GobsLite: self._schedule_gobs,
            _GobdLite: self._schedule_gobd,
            _GdxxLite: self._schedule_gdxx,
            _GarqLite: self._schedule_garq
        }
        
    @fixture_api
    def RESET(self):
        ''' In general this would be where you'd reset self._scheduled,
        but since self.schedule() is fixtured as a NOOP, there's no
        real reason to do anything here.
        '''
        
    def assemble(self, librarian):
        # Links the librarian.
        self._librarian = librarian
        
    async def await_idle(self):
        ''' Wait until the postman has no more deliveries to perform.
        '''
        while self._scheduled is None:
            await asyncio.sleep(.01)
        
        await self._scheduled.join()
        
    async def loop_init(self):
        ''' Init all of the needed async primitives.
        '''
        self._scheduled = asyncio.Queue()
        
    async def loop_run(self):
        ''' Deliver notifications as soon as they are available.
        TODO: support parallel sending.
        '''
        subscription, notification, skip_conn = await self._scheduled.get()
        
        try:
            logger.info(str(subscription) + ' subscription out for delivery.')
            # We can't spin this out into a thread because some of our
            # delivery mechanisms want this to have an event loop.
            await self._deliver(subscription, notification, skip_conn)
            
        except asyncio.CancelledError:
            logger.debug('PostalCore cancelled.')
            raise
        
        except Exception:
            logger.error(str(subscription) + ' subscription FAILED for ' +
                         'notification ' + str(notification) +
                         ' w/ traceback:\n' +
                         ''.join(traceback.format_exc()))
            
        finally:
            self._scheduled.task_done()
        
    async def loop_stop(self):
        ''' Clear the async primitives.
        '''
        # Ehhhhh, should the queue be emptied before being destroyed?
        self._scheduled = None
        
    @fixture_return(True)
    @public_api
    async def schedule(self, obj, removed=False, skip_conn=None):
        ''' Schedules update delivery for the passed object.
        '''
        # It's possible we're being told to schedule nothing, so catch that
        # here.
        if obj is None:
            return
        
        else:
            try:
                scheduler = self._scheduler_lookup[type(obj)]
            
            except KeyError:
                raise TypeError('Postman scheduling failed for ' +
                                type(obj).__name__) from None
            
            else:
                await scheduler(obj, removed, skip_conn)
                
            return True
        
    async def _schedule_gidc(self, obj, removed, skip_conn):
        # GIDC will never trigger a subscription.
        pass
        
    async def _schedule_geoc(self, obj, removed, skip_conn):
        # GEOC will never trigger a subscription directly, though they might
        # have deferred updates.
        # Note that these have already been put into _SubsUpdate form.
        for deferred in self._deferred.pop_any(obj.ghid):
            await self._scheduled.put(deferred)
        
    async def _schedule_gobs(self, obj, removed, skip_conn):
        # GOBS will never trigger a subscription.
        pass
        
    async def _schedule_gobd(self, obj, removed, skip_conn):
        # GOBD might trigger a subscription! But, we also might to need to
        # defer it. Or, we might be removing it.
        if removed:
            debinding_ghids = await self._librarian.debind_status(obj.ghid)
            
            # Check to see that there are the proper number of debindings
            num_debindings = len(debinding_ghids)
            if num_debindings != 1:
                raise ValueError('Improper debinding number: ' +
                                 str(num_debindings) + ' for ' + str(obj))
                
            # Debinding_ghids is a frozenset; this is the fastest way of
            # getting the single element from it.
            debinding_ghid = next(iter(debinding_ghids))
            await self._scheduled.put(
                _SubsUpdate(obj.ghid, debinding_ghid, skip_conn)
            )
            
        else:
            notifier = _SubsUpdate(obj.ghid, obj.frame_ghid, skip_conn)
            if (await self._librarian.contains(obj.target)):
                logger.debug(str(obj) +
                             ' subscription notification scheduled for: ' +
                             str(obj.target))
                await self._scheduled.put(notifier)
            
            else:
                self._deferred.add(obj.target, notifier)
                logger.debug(str(obj) +
                             ' subscription notification deferred for: ' +
                             str(obj.target))
        
    async def _schedule_gdxx(self, obj, removed, skip_conn):
        # GDXX will never directly trigger a subscription. If they are removing
        # a subscribed object, the actual removal (in the undertaker GC) will
        # trigger a subscription without us.
        pass
        
    async def _schedule_garq(self, obj, removed, skip_conn):
        # GARQ might trigger a subscription! Or we might be removing it.
        if removed:
            debinding_ghids = await self._librarian.debind_status(obj.ghid)
            
            # Check to see that there are the proper number of debindings
            num_debindings = len(debinding_ghids)
            if num_debindings != 1:
                raise ValueError('Improper debinding number: ' +
                                 str(num_debindings) + ' for ' + str(obj))
                
            # Debinding_ghids is a frozenset; this is the fastest way of
            # getting the single element from it.
            debinding_ghid = next(iter(debinding_ghids))
            await self._scheduled.put(
                _SubsUpdate(obj.recipient, debinding_ghid, skip_conn)
            )
        else:
            await self._scheduled.put(
                _SubsUpdate(obj.recipient, obj.ghid, skip_conn)
            )
            
    async def _deliver(self, subscription, notification, skip_conn):
        ''' Do the actual subscription update.
        '''
        # We need to freeze the listeners before we operate on them, but we
        # don't need to lock them while we go through all of the callbacks.
        # Instead, just sacrifice any subs being added concurrently to the
        # current delivery run.
        pass


class MrPostman(PostalCore, metaclass=API):
    ''' Postman to use for LOCAL persistence systems -- ie ones that
    have logins and do not support subsription.
    
    Note that MrPostman doesn't need to worry about silencing updates,
    because the persistence ingestion tract will only result in a mail
    run if there's a new object there. So, by definition, any re-sent
    objects will be DOA.
    '''
    _rolodex = weak_property('__rolodex')
    _golcore = weak_property('__golcore')
    _oracle = weak_property('__oracle')
    _salmonator = weak_property('__salmonator')
        
    def assemble(self, golcore, oracle, librarian, rolodex, salmonator):
        super().assemble(librarian)
        self._golcore = golcore
        self._rolodex = rolodex
        self._oracle = oracle
        self._salmonator = salmonator
            
    async def _deliver(self, subscription, notification, skip_conn):
        ''' Do the actual subscription update.
        
        NOTE THAT SKIP_CONN is a weakref.ref (or None).
        '''
        # We just got a garq for our identity. Rolodex handles these.
        if subscription == self._golcore.whoami:
            logger.debug(str(subscription) +
                         'subscription notification handed off to rolodex...')
            await self._rolodex.notification_handler(
                subscription,
                notification
            )
        
        # Anything else is an object subscription. Handle those by directly,
        # but only if we have them in memory.
        # elif subscription in self._oracle:
        # Note: that was causing issues so I'm holding off on it as premature
        # optimization / feature creep
        else:
            # The ingestion pipeline will already have applied any new updates
            # to the ghidproxy.
            try:
                obj = await self._oracle.get_object(GAOCore, subscription)
            
            except KeyError:
                logger.debug(str(subscription) + ' subscription delivery ' +
                             'ignored: unavailable at oracle: ' +
                             str(notification))
                await self._salmonator.deregister(subscription)
                
            else:
                logger.debug(str(subscription) + ' subscription delivery ' +
                             'starting for ' + str(notification))
                await obj.pull(notification)
        
        
class PostOffice(PostalCore, metaclass=API):
    ''' Postman to use for remote persistence servers.
    '''
    _remote_protocol = weak_property('__remote_protocol')
    
    def __init__(self, *args, subs_timeout=30, **kwargs):
        super().__init__(*args, **kwargs)
        # By using WeakSetMap we can automatically handle dropped connections
        # Lookup <subscribed ghid>: set(<subscribed callbacks>)
        self._connections = WeakSetMap()
        self._subscriptions = WeakKeySetMap()
        
        self._subs_timeout = subs_timeout
        
    def assemble(self, librarian, remote_protocol):
        super().assemble(librarian)
        self._remote_protocol = remote_protocol
    
    @fixture_noop
    @public_api
    async def subscribe(self, connection, ghid):
        ''' Tells the postman that the connection would like to be
        updated about ghid.
        '''
        logger.debug('CONN ' + str(connection) + ' subscribed to ' + str(ghid))
        
        # First add the subscription listeners
        self._connections.add(ghid, connection)
        self._subscriptions.add(connection, ghid)
        
        # Now manually reinstate any desired notifications for garq requests
        # that have yet to be handled
        for existing_mail in (await self._librarian.recipient_status(ghid)):
            obj = await self._librarian.summarize(existing_mail)
            await self.schedule(obj)
    
    @fixture_noop
    @public_api
    async def unsubscribe(self, connection, ghid):
        ''' Remove the callback for ghid. Indempotent; will never raise
        a keyerror.
        '''
        try:
            # Discard the subscription (no keyerror)
            self._subscriptions.discard(connection, ghid)
            # Remove the connection (allowing it to raise if missing)
            self._connections.remove(ghid, connection)
            
        except KeyError:
            logger.debug('CONN ' + str(connection) + ' never subscribed to ' +
                         str(ghid))
            return False
            
        else:
            logger.debug('CONN ' + str(connection) + ' unsubscribed to ' +
                         str(ghid))
            return True
            
    async def _deliver(self, subscription, notification, skip_conn):
        ''' Do the actual subscription update.
        
        NOTE THAT SKIP_CONN is a weakref.ref.
        '''
        pkg_label = (str(subscription) + ' subscription, notification ' +
                     str(notification))
        # We need to freeze the listeners before we operate on them, but we
        # don't need to lock them while we go through all of the callbacks.
        # Instead, just sacrifice any subs being added concurrently to the
        # current delivery run.
        connections = self._connections.get_any(subscription)
        logger.debug(
            pkg_label + ' has ' + str(len(connections)) + ' listeners.'
        )
        
        # Resolve the weak reference to the connection
        if skip_conn is not None:
            # This could still be None, but that won't affect our comparison
            skip_conn = skip_conn()
            
        for connection in connections:
            if connection is not skip_conn:
                # Make this a background task, or one blocking connection can
                # hold up the entire subscription queue
                make_background_future(
                    self._remote_protocol.subscription_update(
                        connection,
                        subscription,
                        notification,
                        timeout = self._subs_timeout
                    )
                )
            else:
                logger.debug(pkg_label + ' skipped one connection.')
    
    @fixture_return(frozenset())
    @public_api
    async def list_subs(self, connection):
        ''' List all subscriptions for the connection.
        '''
        return self._subscriptions.get_any(connection)
    
    @fixture_noop
    @public_api
    async def clear_subs(self, connection):
        ''' Clear all subscriptions for the connection.
        '''
        subscriptions = self._subscriptions.pop_any(connection)
        for ghid in subscriptions:
            self._connections.discard(ghid, connection)
