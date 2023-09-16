from .base_command import Command


class InspectCommand(Command):
    def execute(self):
        # player
        # room
        target_name = self.kwargs.get("target_name")

        if self._is_inspecting_room(target_name):
            return self.response(self.room.description)

        if self._is_inspecting_inventory(target_name):
            return self.response(self._get_inventory_description())

        item_description = self._get_item_description_from_inventory(target_name)
        if item_description:
            return self.response(item_description)

        inspectable_description = self._get_inspectable_description(target_name)
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

    def _get_inventory_description(self):
        if not self.player.inventory:
            return "Your inventory is empty."
        items = [item.name for item in self.player.inventory]
        return f"Your inventory contains: {', '.join(items)}."

    def _get_item_description_from_inventory(self, name):
        item = self.find_item_in_inventory(name)
        if item:
            return item.description
        return None

    def _get_inspectable_description(self, name):
        inspectable = self._find_inspectable(name)
        if inspectable:
            return inspectable.description
        return None

    def _find_inspectable(self, name):
        """Find an inspectable item, container, or NPC in the room."""
        return (
            self.find_item_in_room(name)
            or self.find_container_in_room(name)
            or self.find_npc_in_room(name)
        )
