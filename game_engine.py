from game_state import GameState
from utils.observer import Observable


class GameEngine(Observable):
    def __init__(self, rooms, player, visualizer_class, game_data, show_updates=True):
        super().__init__()  # Initialize the Observable part of GameEngine
        self.initial_rooms = rooms
        self.initial_player_location = player.location
        self.rooms = rooms.copy()
        self.player = player
        self.game_data = game_data
        self.winning_conditions = game_data["winning_conditions"]
        self.link_rooms()
        self.viz = visualizer_class(
            self, show_updates
        )  # Initialize the Visualization with the show_updates argument
        self.state = GameState(self.player)

    def link_rooms(self):
        room_dict = {room.name: room for room in self.rooms}
        for room_data, room in zip(self.game_data["rooms"], self.rooms):
            for direction, exit_name in room_data["exits"].items():
                room.exits[direction] = room_dict[exit_name]

    def take_action(self, command):
        response_dict = command.execute()
        last_command_name = command.__class__.__name__

        # Update the state with the message from the response_dict
        self.state.update_state(response_dict, command_name=last_command_name)

        if self.check_winning_condition():
            self.state.win_condition = "Done"  # Update the win_condition attribute

        self.notify_observers()
        return self.state.get_state()

    def check_winning_condition(self):
        item_names_in_inventory = [item.name for item in self.state.player_inventory]
        required_items_met = all(
            item in item_names_in_inventory for item in self.winning_conditions["items"]
        )
        correct_command_used = (
            self.state.command_taken == self.winning_conditions["command"]
        )
        in_correct_room = (
            self.state.get_state()["current_room"] == self.winning_conditions["room"]
        )

        return required_items_met and correct_command_used and in_correct_room
