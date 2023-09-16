class SourceFinder:
    def __init__(self, room, item_name, target=None):
        self.room = room
        self.item_name = item_name
        self.target = target

    def find_item_source(self):
        if self.target:
            source = self.find_target()
            if source:
                return self.target, self.find_item_in_source(source)
        else:
            for source_type, source in self.get_search_sources():
                item = self.find_item_in_source(source)
                if item:
                    return source_type, item
        return None, None

    def find_target(self):
        return next((container for container in self.room.containers if container.name == self.target), None)

    def get_search_sources(self):
        return [
            ("room", self.room),
            ("container", self.room.containers),
            ("npc", self.room.npcs),
        ]

    def find_item_in_source(self, source):
        if hasattr(source, "items"):
            return source.items.get(self.item_name)
        if hasattr(source, "inventory"):
            return source.inventory.get(self.item_name)
        if isinstance(source, list):
            return self.find_item_in_list(source)
        return None

    def find_item_in_list(self, source_list):
        for obj in source_list:
            if hasattr(obj, "contained_items"):
                return obj.contained_items.get(self.item_name)
            if hasattr(obj, "inventory"):
                return obj.inventory.get(self.item_name)
        return None
