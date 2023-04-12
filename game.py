import random
from enum import Enum
from Dataclasses.callback import Callback
from Dataclasses.throwdata import ThrowData
from Dataclasses.order import Order

from Utils.logger import log
from apscheduler.schedulers.background import BackgroundScheduler


class PlayerType(Enum):
    Cook = 0
    Driver = 1


class Game:

    def __init__(self, sio, id):
        self.sio = sio
        self.cook = None
        self.driver = None

        self.id = id

        self.scheduler = BackgroundScheduler()
        self.scheduler.add_job(self.get_new_order, 'interval', seconds=random.randint(30, 60))
        self.scheduler.start()

    def add_player(self, sid: str) -> Callback:
        """
        Function to add a player to the game
        :param sid: SocketID of the player
        :return: the callback to show success or error and message
        """
        player_type = self.get_player_type(sid)
        success = False

        if player_type is None:
            return Callback(False, "Player type undefined")

        if player_type == PlayerType.Cook and self.cook is None:
            self.cook = sid
            success = True

        if player_type == PlayerType.Driver and self.driver is None:
            self.driver = sid
            success = True

        if success:
            self.sio.enter_room(sid, self.id)
            self.sio.emit('join_game', {'message': self.id}, room=sid)
            return Callback(True)

        return Callback(False, "The game is full")

    def remove_player(self, sid: str) -> Callback:
        """
        Function to remove player to the game
        :param sid: SocketID of the player
        :return: the callback to show success or error and message
        """
        player_type = self.get_player_type(sid)
        success = False

        if player_type is None:
            return Callback(False, "Player type undefined")

        if player_type == PlayerType.Cook and self.cook == sid:
            self.cook = None
            success = True

        if player_type == PlayerType.Driver and self.driver == sid:
            self.driver = None
            success = True

        if success:
            if self.driver is None and self.cook is None:
                self.scheduler.shutdown()

            self.sio.leave_room(sid, self.id)
            self.sio.emit('leave_game', {'message': self.id}, room=sid)
            return Callback(True)

        return Callback(False, "Player not found in the game")

    def get_player_type(self, sid) -> PlayerType:
        """
        Function to get the player type
        :param sid: SocketID of the player
        :return: the type of the player
        """
        session = self.sio.get_session(sid)

        if session['type'] == "cook":
            return PlayerType.Cook

        if session['type'] == "driver":
            return PlayerType.Driver

        return None

    def get_new_order(self):
        order: Order = Order()

        log("New order for " + self.id + " : " + str(order.to_dict()))
        self.sio.emit('new_order', {'message': order.to_dict()}, room=self.id)

    def broadcast(self, value):
        log("Currently broadcast with : " + str(value))
        self.sio.emit('broadcast', {'message': value}, room=self.id)

    def throw_object(self, throw_data: ThrowData):
        if self.driver is None:
            return

        self.sio.emit('throw_object', throw_data.toJSON())
