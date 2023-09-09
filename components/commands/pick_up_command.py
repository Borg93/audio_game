from base_command import Command


class PickUpCommand(Command):
    def execute(self):
        item_name = self.kwargs.get("item_name")
        item = self.find_item_in_room(item_name)

        if not item:
            return self.response(f"Invalid item : {item_name} ", status="failure")

        self.game_engine.state.add_to_inventory(item)

        # Check if the item is directly in the room or inside a container
        if item in self.game_engine.player.location.items:
            self.game_engine.player.location.items.remove(item)
        else:
            for container in self.game_engine.player.location.containers:
                if item in container.contained_items:
                    container.contained_items.remove(item)
                    break

        return self.response(f"Picked up {item.name}.")
