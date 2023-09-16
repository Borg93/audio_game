from .base_command import Command


class MoveCommand(Command):
    def execute(self):
        direction = self.kwargs.get("direction")
        exit_data = self._get_exit_data(direction)

        if not exit_data:
            return self.response("Invalid direction.", status="failure")

        room_name = exit_data  # At this point, exit_data is simply the name of the room
        self._move_to_room(room_name)

        return self.response(f"Moved to {self.player.location}")

    def _get_exit_data(self, direction):
        return self.room.exits.get(direction)

    def _move_to_room(self, room_name):
        self.player.location = room_name


# class MoveCommand(Command):
#     def execute(self):
#         direction = self.kwargs.get("direction")
#         password = self.kwargs.get("password")
#         exit_data = self._get_exit_data(direction)

#         if not exit_data:
#             return self.response("Invalid direction.", status="failure")

#         previous_location = self.player.location.name

#         if not self._can_move_to_direction(exit_data, password):
#             return self.response(
#                 f"Trying to move to {self.player.location.name}. However, you can't move in that direction due to certain conditions."
#             )

#         room_name = exit_data.get("room") if isinstance(exit_data, dict) else exit_data
#         self._move_to_room(room_name)

#         return self.response(f"Moved from {previous_location} to {self.player.location.name}")

#     def _get_exit_data(self, direction):
#         return self.room.exits.get(direction)

#     def _can_move_to_direction(self, exit_data, password):
#         if not exit_data or ("condition" in exit_data and not self._meet_condition(exit_data["condition"], password)):
#             return False
#         return True

#     def _meet_condition(self, condition_data, password):
#         condition = Condition(
#             required_items=condition_data.get("required_items"),
#             required_mechanisms=condition_data.get("required_mechanisms"),
#             password=condition_data.get("password"),
#         )
#         return condition.is_met(self.player.inventory, self.room, password)

#     def _move_to_room(self, room_name):
#         target_room = self.find_room_in_rooms(room_name)  # Assume this method exists in the base class or is imported
#         if target_room:
#             self.player.location = target_room
#         else:
#             raise ValueError(f"No room found with the name '{room_name}'")
