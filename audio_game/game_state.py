from .game_objects.room import Room
from .game_objects.player import Player

from typing import List


class GameState:
    def __init__(self, rooms: List[Room], player: Player):
        self.rooms = rooms
        self.player = player
        self.initialize_state()

    def initialize_state(self):
        self.state = {
            "current_room": self.current_room_location,
            "current_exits": self.available_exits,
            "player_inventory": self.player.inventory,
            "command_taken": "",
            "current_action": "",
            "status_response": "",
            "win_condition": "Pending",
        }
        self.update_state()

    def update_state(self, response_dict=None, command_name=""):
        if response_dict:
            self.state["current_action"] = response_dict["message"]
            self.state["status_response"] = response_dict["status_response"]
            self.state["command_taken"] = command_name

        self.state["current_room"] = self.current_room_location
        self.state["current_exits"] = self.available_exits
        self.state["player_inventory"] = self.player.inventory

        if self.state["current_room"] is None:
            raise ValueError(f"Invalid room: {self.player.location}")

    @property
    def current_room_location(self):
        return next((room for room in self.rooms if room.name == self.player.location), None)

    @property
    def current_room_location_name(self):
        return self.current_room_location.name if self.current_room_location else None

    @property
    def available_exits(self):
        current_room = self.current_room_location
        if current_room is not None:
            return current_room.exits
        else:
            return "No available exits."

    def add_to_inventory(self, item):
        self.player.inventory.append(item)
        self.update_state()

    def remove_from_inventory(self, item):
        self.player.inventory.remove(item)
        self.update_state()

    @property
    def current_inventory_items_names(self):
        return [item.name for item in self.state["player_inventory"]]

    @property
    def current_command(self):
        return self.state["command_taken"]

    @property
    def current_action(self):
        return self.state["current_action"]

    @property
    def current_room_name(self):
        return self.state["current_room"].name if self.state["current_room"] else None

    @property
    def current_win_condition(self):
        return self.state["win_condition"]

    @current_win_condition.setter
    def current_win_condition(self, condition: str):
        self.state["win_condition"] = condition
