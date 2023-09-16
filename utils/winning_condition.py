from game_state import GameState


class WinningConditionChecker:
    def __init__(self, winning_conditions, game_state: GameState):
        self.winning_conditions = winning_conditions
        self.game_state = game_state

    def check_winning_condition(self):
        item_names_in_inventory = self.game_state.current_inventory_items_names
        required_items_met = all(
            item in item_names_in_inventory for item in self.winning_conditions["items"]
        )
        correct_command_used = (
            self.game_state.current_command == self.winning_conditions["command"]
        )
        in_correct_room = (
            self.game_state.current_room_name == self.winning_conditions["room"]
        )

        return required_items_met and correct_command_used and in_correct_room

    def update_game_state_winning_condition(self):
        self.game_state.current_win_condition = "Done"
