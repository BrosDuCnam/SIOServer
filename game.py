import random
from enum import Enum
from Dataclasses.callback import Callback
from Dataclasses.throwdata import ThrowData
from Dataclasses.order import Order

from Utils.logger import log
from Utils.vector import Vector

from apscheduler.schedulers.background import BackgroundScheduler


class PlayerType(Enum):
    Cook = 0
    Driver = 1


class Game:

    def __init__(self, sio, id):
        self.sio = sio
        self.cook = None
        self.driver = None
        self.order_id = 0
        self.score = 0

        self.id = id

        # self.scheduler = BackgroundScheduler()
        # self.scheduler.add_job(self.get_new_order, 'interval', seconds=random.randint(15, 30))
        # self.scheduler.start()

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
            self.sio.emit('join_game', {'message': self.id,
                                        'type': player_type.name},
                          room=sid)

            # if it's the first player, get new order
            if self.driver is not None and self.cook is not None:
                self.get_new_order()

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
        self.order_id += 1

        order: Order = Order(self.order_id)

        log("New order for " + self.id + " : " + str(order.to_dict()))
        self.sio.emit('new_order', {'message': order.to_dict()}, room=self.id)

        return order.to_dict()

    def set_kitchen_pos(self, pos):

        # Send kitchen position to players
        self.sio.emit('kitchen_pos', {'message': pos}, room=self.id)

    def broadcast(self, value):
        log("Currently broadcast with : " + str(value))
        self.sio.emit('broadcast', {'message': value}, room=self.id)

    def throw_object(self, throw_data: ThrowData):
        if self.driver is None:
            return

        self.sio.emit('throw_object', throw_data.toJSON())

    def add_score(self, score):
        self.score += score
        self.score_updated()

    def score_updated(self):
        self.sio.emit('score_updated', {'message': self.score}, room=self.id)

    def toggle_horn(self, state):
        self.sio.emit('toggle_horn', {'message': state}, room=self.id)
        pass

    def apply_physic(self, vector):
        self.sio.emit('apply_physic', {'message': vector}, room=self.id)
        pass

    def end_game(self):
        self.sio.emit('game_finished', {'score': self.score}, room=self.id)
        pass