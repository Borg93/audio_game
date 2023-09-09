from base_command import Command


class MoveCommand(Command):
    def execute(self):
        direction = self.kwargs.get("direction")
        password = self.kwargs.get("password")
        exit_data = self._get_exit_data(direction)

        if not exit_data:
            return self.response("Invalid direction.", status="failure")

        if not self._can_move_to_direction(exit_data, password):
            return self.response(
                f"Trying to move to {self.game_engine.player.location.name}. However, you can't move in that direction due to certain conditions."
            )

        if isinstance(exit_data, dict):
            room_name = exit_data.get("room")
        else:
            room_name = exit_data

        self._move_to_room(room_name)
        return self.response(f"Moved to {self.game_engine.player.location.name}")

    def _get_exit_data(self, direction):
        exit_data = self.game_engine.player.location.exits.get(direction)
        if isinstance(exit_data, Room):
            return exit_data.name
        return exit_data

    def _can_move_to_direction(self, exit_data, password):
        if (
            isinstance(exit_data, dict) and "condition" in exit_data
        ):  # Check if exit_data is a dictionary with a "condition" key
            condition_data = exit_data["condition"]
            condition = Condition(
                required_items=condition_data.get("required_items"),
                required_mechanisms=condition_data.get("required_mechanisms"),
                password=condition_data.get("password"),
            )
            return condition.is_met(
                self.game_engine.state.player_inventory,
                self.game_engine.rooms,
                password,
            )
        return True

    def _move_to_room(self, room_name):
        target_room = self.find_room_in_rooms(room_name)
        if target_room:
            self.game_engine.player.location = target_room
        else:
            raise ValueError(f"No room found with the name '{room_name}'")
