import string
import random
import game
from Dataclasses.callback import Callback


class GameManager:
    games = []

    def __init__(self, sio):
        self.sio = sio

    def create_game(self, creator_sid: str) -> Callback:
        """
        Function to create a game and store it
        :param creator_sid: the SocketID of the creator to add it directly into the game
        :return: the callback to show success or error and message
        """
        temp_game = self.get_player_game(creator_sid)
        if temp_game is not None:
            return Callback(False, "The player is already in a game")

        temp_game = game.Game(self.sio, self.get_random_id())  # Create the game
        self.games.append(temp_game)  # Add the game list

        return temp_game.add_player(creator_sid)  # Try to add the creator player to the new game

    def join_game(self, game_id: str, sid: str) -> Callback:
        """
        Function to add player to a game
        :param game_id: ID of the game to join
        :param sid: SocketID of the player to add to the game
        :return: the callback to show success or error and message
        """
        temp_game = self.get_player_game(sid)
        if temp_game is not None:
            return Callback(False, "The player is already in a game")

        temp_game = self.get_game(game_id)
        if temp_game is None:
            return Callback(False, "game id not found")

        return temp_game.add_player(sid)

    def leave_game(self, sid: str) -> Callback:
        """
        Function to remove player from a game, will automatically remove the game if needed
        :param sid: SocketID of the player to remove of the game
        :return: the callback to show success or error and message
        """
        temp_game = self.get_player_game(sid)
        if temp_game is None:
            return Callback(False, "Player is not in any game")

        temp_game.remove_player(sid)
        if temp_game.cook is None and temp_game.driver is None:
            self.games.remove(temp_game)

        return Callback(True)

    def get_random_id(self) -> str:
        """
        Function to generate a random a unique id
        :return: the id
        """
        characters = string.digits + string.ascii_uppercase
        id = ""

        while id == "" or self.get_game(id) is not None:
            id = ""
            for x in range(5):
                id += random.choice(characters)

        return id

    def get_game(self, id: str) -> game.Game:
        """
        Function to get game from an ID
        :param id: ID of the game
        :return: the game
        """
        for p in self.games:
            if p.id == id:
                return p

        return None

    def get_player_game(self, sid: str) -> game.Game:
        """
        Function to get game from a player
        :param sid: SocketID of the player
        :return: the game of the player, none if player is not in a game
        """
        for p in self.games:
            if p.cook == sid or p.driver == sid:
                return p

        return None
