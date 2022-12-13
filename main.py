import eventlet
import socketio
from gamemanager import GameManager
from Dataclasses.callback import Callback

sio = socketio.Server()
app = socketio.WSGIApp(sio)
games = GameManager(sio)


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
def join(sid, data):
    callback = games.join_game(data, sid)
    return callback.toJSON()


@sio.event
def leave(sid, data):
    callback = games.leave_game(sid)
    return callback.toJSON()


# API events
@sio.event
def get_games(sid, data):
    ids: list[str] = []

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


if __name__ == '__main__':
    eventlet.wsgi.games(eventlet.listen(('', 5000)), app)
