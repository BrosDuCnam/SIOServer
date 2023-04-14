import sys
#import eventlet
from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler
import socketio
import Dataclasses.order as order
from typing import List

from gamemanager import GameManager
from Dataclasses.callback import Callback
from Dataclasses.throwdata import ThrowData
from Utils.logger import log

sio = socketio.Server(async_mode='gevent')
app = socketio.WSGIApp(sio)
games = GameManager(sio)

@sio.event
def connect(sid, environ):
    sio.save_session(sid, {'type': environ["HTTP_TYPE"].lower()})
    log("connect", sid)


@sio.event
def disconnect(sid):
    games.leave_game(sid)
    log("disconnect", sid)


# game based events
@sio.event
def create(sid, data):
    callback = games.create_game(sid)
    callback.data = games.games[-1].id
    log("create", sid, callback.toJSON())

    return callback.toJSON()


@sio.event
def join_game(sid, data):
    log("Try to join : ", data)
    callback = games.join_game(data, sid)
    return callback.toJSON()


@sio.event
def leave(sid, data):
    callback = games.leave_game(sid)
    return callback.toJSON()


# API events
@sio.event
def get_games(sid, data):
    ids: List[str] = []

    for p in games.games:
        ids.append(p.id)

    log(Callback(True, data=ids).toJSON())
    return Callback(True, data=ids).toJSON()


# Game events
@sio.event
def chat(sid, data):
    log("chat", sid, data)

    game = games.get_player_game(sid)
    if game is not None:
        game.broadcast(data)
        return Callback(True).toJSON()
    return Callback(False, "You are not in any game").toJSON()


# Event on event throw from the cook
@sio.event
def on_object_thrown(sid, data):
    game = games.get_player_game(sid)

    if game is None:
        return Callback(False).toJSON()

    # print the data
    log("on_object_thrown", sid, data)

    game.throw_object(ThrowData(data))
    return Callback(True).toJSON()


@sio.event
def get_order(sid, data):
    log("get order", sid, data)

    game = games.get_player_game(sid)
    if game is None:
        return Callback(False).toJSON()

    game.get_new_order()
    return Callback(True).toJSON()


# Get random throw (for debug)
@sio.event
def get_random_throw_data(sid, data):
    game = games.get_player_game(sid)
    if game is None:
        return Callback(False).toJSON()
    game.throw_object(ThrowData.get_random())
    return Callback(True).toJSON()


@sio.event
def ping(sid, data):
    return Callback(True, "", "pong !").toJSON()


if __name__ == '__main__':
    log("started")
    # log(order.Order().to_dict())

    pywsgi.WSGIServer(('', 5000), app, handler_class=WebSocketHandler).serve_forever()
    #eventlet.wsgi.server(eventlet.listen(('', 5000)), app)
