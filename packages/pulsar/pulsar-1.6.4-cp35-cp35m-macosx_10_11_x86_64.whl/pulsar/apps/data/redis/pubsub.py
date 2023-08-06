from functools import partial
from asyncio import gather

from pulsar import Protocol
from pulsar.apps.data import PubSub, Channels, PubSubClient


class PubsubProtocol(Protocol):

    def __init__(self, handler, **kw):
        super().__init__(handler._loop, **kw)
        self.parser = self._producer._parser_class()
        self.handler = handler

    async def execute(self, *args):
        # must be an asynchronous object like the base class method
        chunk = self.parser.multi_bulk(args)
        self._transport.write(chunk)

    def data_received(self, data):
        parser = self.parser
        parser.feed(data)
        response = parser.get()
        while response is not False:
            if not isinstance(response, Exception):
                if isinstance(response, list):
                    command = response[0]
                    if command == b'message':
                        response = response[1:3]
                        self.handler.broadcast(response)
                    elif command == b'pmessage':
                        response = response[2:4]
                        self.handler.broadcast(response)
            else:
                raise response
            response = parser.get()


class RedisPubSub(PubSub):
    '''Asynchronous Publish/Subscriber handler for pulsar and redis stores.
    '''
    def publish(self, channel, message):
        if self._protocol:
            message = self._protocol.encode(message)
        return self.store.execute('PUBLISH', channel, message)

    def count(self, *channels):
        kw = {'subcommand': 'numsub'}
        return self.store.execute('PUBSUB', 'NUMSUB', *channels, **kw)

    def count_patterns(self):
        kw = {'subcommand': 'numpat'}
        return self.store.execute('PUBSUB', 'NUMPAT', **kw)

    def channels(self, pattern=None):
        '''Lists the currently active channels matching ``pattern``
        '''
        if pattern:
            return self.store.execute('PUBSUB', 'CHANNELS', pattern)
        else:
            return self.store.execute('PUBSUB', 'CHANNELS')

    def psubscribe(self, pattern, *patterns):
        return self._subscribe('PSUBSCRIBE', pattern, *patterns)

    def punsubscribe(self, *patterns):
        if self._connection:
            return self._connection.execute('PUNSUBSCRIBE', *patterns)

    def subscribe(self, channel, *channels):
        return self._subscribe('SUBSCRIBE', channel, *channels)

    def unsubscribe(self, *channels):
        '''Un-subscribe from a list of ``channels``.
        '''
        if self._connection:
            return self._connection.execute('UNSUBSCRIBE', *channels)

    async def close(self):
        '''Stop listening for messages.
        '''
        if self._connection:
            await gather(
                self._connection.execute('PUNSUBSCRIBE'),
                self._connection.execute('UNSUBSCRIBE'),
                loop=self._loop
            )
            await self._connection.close()

    #    INTERNALS
    async def _subscribe(self, *args):
        if not self._connection:
            protocol_factory = partial(PubsubProtocol, self,
                                       producer=self.store)
            self._connection = await self.store.connect(protocol_factory)
            self._connection.bind_event('connection_lost', self._conn_lost)
        result = await self._connection.execute(*args)
        return result

    def _conn_lost(self, con, exc=None):
        self._connection = None
        self.fire_event('connection_lost')


class RedisChannels(Channels, PubSubClient):
    """Manage redis channels-events
    """
    def __init__(self, pubsub, **kw):
        assert pubsub.protocol, "protocol required for channels"
        super().__init__(pubsub.store, **kw)
        self.pubsub = pubsub
        self.pubsub.bind_event('connection_lost', self._connection_lost)
        self.pubsub.add_client(self)

    def lock(self, name, **kwargs):
        """Global distributed lock
        """
        return self.pubsub.store.client().lock(self.prefixed(name), **kwargs)

    async def publish(self, channel, event, data=None):
        """Publish a new ``event`` on a ``channel``

        :param channel: channel name
        :param event: event name
        :param data: optional payload to include in the event
        :return: a coroutine and therefore it must be awaited
        """
        msg = {'event': event, 'channel': channel}
        if data:
            msg['data'] = data
        try:
            await self.pubsub.publish(self.prefixed(channel), msg)
        except ConnectionRefusedError:
            self.connection_error = True
            self.logger.critical(
                '%s cannot publish on "%s" channel - connection error',
                self,
                channel
            )
        else:
            self.connection_ok()

    async def _subscribe(self, channel, event=None):
        channel_name = self.prefixed(channel.name)
        await self.pubsub.subscribe(channel_name)

    async def _unsubscribe(self, channel, event=None):
        channel_name = self.prefixed(channel.name)
        await self.pubsub.unsubscribe(channel_name)

    async def close(self):
        """Close channels and underlying pubsub handler

        :return: a coroutine and therefore it must be awaited
        """
        self.pubsub.remove_callback('connection_lost', self._connection_lost)
        self.status = self.statusType.closed
        await self.pubsub.close()
