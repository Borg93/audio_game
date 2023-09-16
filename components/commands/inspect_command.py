from .base_command import Command


class InspectCommand(Command):
    def execute(self):
        target_name = self.kwargs.get("target_name")

        if self._is_inspecting_room(target_name):
            return self.response(self.room.description)

        if self._is_inspecting_inventory(target_name):
            return self.response(self.player.inventory_summary())

        item_description = self.player.find_item(target_name)
        if item_description:
            return self.response(item_description.description)

        inspectable_description = self._find_inspectable_description(target_name)
        if inspectable_description:
            return self.response(inspectable_description)

        return self.response(
            f"Cannot inspect '{target_name}'. It might not exist in this room or your inventory.",
            status="failure",
        )

    def _is_inspecting_room(self, name):
        return name == self.room.name or name == "room"

    def _is_inspecting_inventory(self, name):
        return name == "inventory"

    def _find_inspectable_description(self, name):
        inspectable = (
            self.room.find_item(name)
            or self.room.find_container(name)
            or self.room.find_npc(name)
        )
        return inspectable.description if inspectable else None
