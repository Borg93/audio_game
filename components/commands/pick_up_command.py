from .base_command import Command


class PickUpCommand(Command):
    def execute(self):
        item_name = self.kwargs.get("item_name")
        source, item = self.find_item_source(item_name)

        print(source, item)

        if source is None or item is None:
            return self.response(f"Invalid item: {item_name}", status="failure")

        self.add_item_to_inventory(item)
        self.remove_item_from_source(item, source)

        return self.response(f"Picked up {item.name}.")

    def find_item_source(self, item_name):
        for source_name, source in [
            ("room", self.room),
            ("container", self.room.containers),
            ("npc", self.room.npcs),
        ]:
            item = self.find_item_in_source(source, item_name)
            if item:
                return source_name, item
        return None, None

    def find_item_in_source(self, source, item_name):
        if hasattr(source, "items") and item_name in source.items:
            return source.items.get(item_name)
        if hasattr(source, "inventory") and item_name in source.inventory:
            return source.inventory.get(item_name)
        if isinstance(source, list):
            for obj in source:
                if hasattr(obj, "contained_items") and item_name in obj.contained_items:
                    return obj.contained_items.get(item_name)
                if hasattr(obj, "inventory") and item_name in obj.inventory:
                    return obj.inventory.get(item_name)
        return None

    def add_item_to_inventory(self, item):
        self.player.add_to_inventory(item)

    def remove_item_from_source(self, item, source):
        if source == "room":
            self.room.items.remove(item)
        elif source == "container":
            for container in self.room.containers:
                if item in container.contained_items:
                    container.contained_items.remove(item)
                    break
        elif source == "npc":
            for npc in self.room.npcs:
                if item in npc.inventory:
                    npc.inventory.remove(item)
                    break
