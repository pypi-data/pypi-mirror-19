# coding: utf-8

import inspect

import tornado
import tornado.escape
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.websocket


class WebSocketHandler(tornado.websocket.WebSocketHandler):
    """
        Represents a WebSocket connection, wrapper of
        `tornado.websocket.WebSocketHandler <http://www.tornadoweb.org/en/stable/websocket.html#event-handlers>`_
        class.

        This class should not be instantiated directly; use the :class:`~tornado_websockets.websocket.WebSocket` class
        instead.
    """

    def initialize(self, websocket):
        """
            Called when class initialization, makes a link between a :class:`~tornado_websockets.websocket.WebSocket`
            instance and this object.

            :param websocket: instance of WebSocket.
            :type websocket: WebSocket
        """

        # Make a link between a WebSocket instance and this object
        self.websocket = websocket
        websocket.handlers.append(self)

    def open(self):
        """
            Called when the WebSocket is opened
        """

        for event in self.websocket.events:
            if event.endswith('open'):
                self.on_message('{"event": "%s", "data": {}}' % event)

    def check_origin(self, origin):
        return True

    def on_message(self, message):
        """
            Handle incoming messages on the WebSocket.

            :param message: JSON string
            :type message: str
        """

        try:
            message = tornado.escape.json_decode(message)
            event = message.get('event')
            data = message.get('data')
        except ValueError:
            self.emit_warning('Invalid JSON was sent.')
            return

        if not event:
            self.emit_warning('There is no event in this JSON.')
            return

        if not self.websocket.events.get(event):
            return

        if not data:
            data = {}
        elif not isinstance(data, dict):
            self.emit_warning('The data should be a dictionary.')
            return

        callback = self.websocket.events.get(event)
        spec = inspect.getargspec(callback)
        kwargs = {}

        if 'self' in spec.args:
            kwargs['self'] = self.websocket.context
        if 'socket' in spec.args:
            kwargs['socket'] = self
        if 'data' in spec.args:
            kwargs['data'] = data

        return callback(**kwargs)

    def emit(self, event, data):
        """
            Sends a given event/data combinaison to the client of this WebSocket.

            Wrapper for `tornado.websocket.WebSocketHandler.write_message <http://www.tornadoweb.org/en/stable/
            websocket.html#tornado.websocket.WebSocketHandler.write_message>`_ method.

            :param event: event name to emit
            :param data: associated data
            :type event: str
            :type data: dict
        """

        self.write_message({
            'event': event,
            'data': data
        })

    def emit_warning(self, message):
        """
            Shortuct to emit a warning.

            :param message: error message
            :type message: str
        """

        return self.emit('warning', {'message': message})

    def on_close(self):
        """
            Called when the WebSocket is closed, delete the link between this object and its WebSocket.
        """

        self.websocket.handlers.remove(self)
