from base_command import Command


class DropCommand(Command):
    def execute(self):
        item_name = self.kwargs.get("item_name")
        item_to_drop = self.find_item_in_inventory(item_name)

        if not item_to_drop:
            return self.response("You don't have that item.", status="failure")

        self.game_engine.player.location.items.append(item_to_drop)
        self.game_engine.state.remove_from_inventory(item_to_drop)

        return self.response(f"Dropped {item_to_drop.name}.")
