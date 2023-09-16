class ConditionChecker:
    def __init__(self, exit_data, player_inventory, rooms, password):
        self.exit_data = exit_data
        self.player_inventory = player_inventory
        self.rooms = rooms
        self.password = password

    def can_move(self):
        if isinstance(self.exit_data, dict) and "condition" in self.exit_data:
            condition_data = self.exit_data["condition"]
            return self._check_condition(condition_data)
        return True

    def _check_condition(self, condition_data):
        # your condition checking logic here
        return True  # or False
