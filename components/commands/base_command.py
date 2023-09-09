from abc import ABC, abstractmethod


class Command(ABC):
    def __init__(self, game_engine, **kwargs):
        self.game_engine = game_engine
        self.kwargs = kwargs

    @abstractmethod
    def execute(self):
        pass

    def find_room_in_rooms(self, room_name):
        return next(
            (room for room in self.game_engine.rooms if room.name == room_name), None
        )

    def find_item_in_room(self, item_name):
        return next(
            (
                item
                for item in self.game_engine.player.location.items
                if item.name == item_name
            ),
            None,
        )

    def find_npc_in_room(self, npc_name):
        return next(
            (
                npc
                for npc in self.game_engine.player.location.npcs
                if npc.name == npc_name
            ),
            None,
        )

    def find_container_in_room(self, container_name):
        return next(
            (
                container
                for container in self.game_engine.player.location.containers
                if container.name == container_name
            ),
            None,
        )

    def find_item_in_inventory(self, item_name):
        return next(
            (
                item
                for item in self.game_engine.state.player_inventory
                if item.name == item_name
            ),
            None,
        )

    def find_item_in_room(self, item_name):
        # First, try to find the item directly in the room
        item = next(
            (
                item
                for item in self.game_engine.player.location.items
                if item.name == item_name
            ),
            None,
        )

        # If the item is not found directly in the room, check inside containers
        if not item:
            for container in self.game_engine.player.location.containers:
                item = next(
                    (
                        item
                        for item in container.contained_items
                        if item.name == item_name
                    ),
                    None,
                )
                if item:
                    break
        return item

    def response(self, message, status="success"):
        return {"message": message, "status_response": status}
