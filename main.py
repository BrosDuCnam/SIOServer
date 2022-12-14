import sys
import eventlet
import socketio
from typing import List

from gamemanager import GameManager
from Dataclasses.callback import Callback
from Dataclasses.throwdata import ThrowData


sio = socketio.Server()
app = socketio.WSGIApp(sio)
games = GameManager(sio)

port: int

@sio.event
def connect(sid, environ):
    sio.save_session(sid, {'type': environ["HTTP_TYPE"].lower()})
    print("connect", sid)


@sio.event
def disconnect(sid):
    games.leave_game(sid)
    print("disconnect", sid)


# game based events
@sio.event
def create(sid, data):
    callback = games.create_game(sid)
    print("create", sid, callback.toJSON())
    return callback.toJSON()


@sio.event
def join_game(sid, data):
    print("Try to join : ", data)
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

    for i in range(5):
        ids.append(games.get_random_id())

    for p in games.games:
        ids.append(p.id)

    print(Callback(True, data=ids).toJSON())
    return Callback(True, data=ids).toJSON()


# Game events
@sio.event
def chat(sid, data):
    print("chat", sid, data)

    game = games.get_player_game(sid)
    if game is not None:
        game.broadcast(data)
        return Callback(True).toJSON()
    return Callback(False, "You are not in any game").toJSON()


# Event on event throw from the cook
@sio.event
def on_object_thrown(sid, data):
    game = games.get_player_game(sid)

    game.throw_object(ThrowData(data))
    return Callback(True).toJSON()


# Get random throw (for debug)
@sio.event
def get_random_throw_data(sid, data):
    game = games.get_player_game(sid)
    game.throw_object(ThrowData.get_random_throw())
    return Callback(True).toJSON()


if __name__ == '__main__':
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    else:
        port = 5000

    print("Starting server on port", port)
    eventlet.wsgi.server(eventlet.listen(('vwm-sioserver.herokuapp.com', port)), app)
