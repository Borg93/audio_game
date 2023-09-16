class ItemRemover:
    def __init__(self, room):
        self.room = room

    def remove_item_from_source(self, item, source_type):
        if source_type == "room":
            self.room.items.remove(item)
        elif source_type == "container":
            self.remove_item_from_list(self.room.containers, item)
        elif source_type == "npc":
            self.remove_item_from_list(self.room.npcs, item)

    def remove_item_from_list(self, obj_list, item):
        for obj in obj_list:
            if item in obj.contained_items:
                obj.contained_items.remove(item)
                return
            if item in obj.inventory:
                obj.inventory.remove(item)
                return
