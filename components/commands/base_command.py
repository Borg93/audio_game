from abc import ABC, abstractmethod


class Command(ABC):
    def __init__(self, player, room, **kwargs):
        self.player = player
        self.room = room
        self.kwargs = kwargs

    @abstractmethod
    def execute(self):
        pass

    def find_item_in_room(self, item_name):
        return next(
            (item for item in self.room.items if item.name == item_name),
            None,
        )

    def find_npc_in_room(self, npc_name):
        return next(
            (npc for npc in self.room.npcs if npc.name == npc_name),
            None,
        )

    def find_container_in_room(self, container_name):
        return next(
            (
                container
                for container in self.room.containers
                if container.name == container_name
            ),
            None,
        )

    def find_item_in_inventory(self, item_name):
        return next(
            (item for item in self.player.inventory if item.name == item_name),
            None,
        )

    def response(self, message, status="success"):
        return {"message": message, "status_response": status}
