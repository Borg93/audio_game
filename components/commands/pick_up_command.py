from .base_command import Command
from .utils.source_finder import SourceFinder
from .utils.item_remover import ItemRemover


class PickUpCommand(Command):
    def execute(self):
        item_name = self.kwargs.get("item_name")
        target = self.kwargs.get("target")

        source_finder = SourceFinder(self.room, item_name, target)
        source_type, item = source_finder.find_item_source()

        if source_type is None or item is None:
            return self.response(f"Invalid item: {item_name}", status="failure")

        self.add_item_to_inventory(item)

        item_remover = ItemRemover(self.room)
        item_remover.remove_item_from_source(item, source_type)

        return self.response(f"Picked up {item.name}.")

    def add_item_to_inventory(self, item):
        self.player.add_to_inventory(item)
