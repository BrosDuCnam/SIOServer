import eventlet
import socketio
from server import Server
from Dataclasses.callback import Callback

sio = socketio.Server()
app = socketio.WSGIApp(sio)
server = Server(sio)


@sio.event
def connect(sid, environ):
    sio.save_session(sid, {'type': environ["HTTP_TYPE"].lower()})
    print("connect", sid)


@sio.event
def disconnect(sid):
    server.leave_game(sid)
    print("disconnect", sid)


# game based events
@sio.event
def create(sid, data):
    callback = server.create_game(sid)
    callback.data = server.games[-1].id
    print("create", sid, callback.toJSON())
    return callback.toJSON()


@sio.event
def join(sid, data):
    callback = server.join_game(data, sid)
    print("join", sid, callback.toJSON())
    return callback.toJSON()


@sio.event
def leave(sid, data):
    callback = server.leave_game(sid)
    print("leave", sid, callback.toJSON())
    return callback.toJSON()


# API events
@sio.event
def get_games(sid, data):
    ids: list[str] = []

    for i in range(1):
        ids.append(server.get_random_id())

    for p in server.games:
        ids.append(p.id)

    print("get games", Callback(True, data=ids).toJSON())
    return Callback(True, data=ids).toJSON()


# Game events
@sio.event
def chat(sid, data):
    print("chat", sid, data)

    game = server.get_player_game(sid)
    if game is not None:
        game.broadcast(data)
        return Callback(True).toJSON()
    return Callback(False, "You are not in any game").toJSON()


if __name__ == '__main__':
    print("SERVER START")
    eventlet.wsgi.server(eventlet.listen(('', 5000)), app)
    print("SERVER END")
