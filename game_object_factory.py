from components.interactables.room import Room
from components.interactables.container import Container
from components.interactables.player import Player
from components.interactables.npc import NPC
from components.interactables.item import Item
from components.mechanism import Mechanism


class GameObjectFactory:
    def create_room(self, room_data):
        room = Room(room_data["name"], room_data["description"])

        for item_data in room_data.get("items", []):
            if "type" in item_data and item_data["type"] == "mechanism":
                item = self.create_mechanism(item_data)
            else:
                item = self.create_item(item_data)
            room.items.append(item)

        for container_data in room_data.get("containers", []):
            container = self.create_container(container_data)
            room.containers.append(container)

        for npc_data in room_data.get("npcs", []):
            npc = self.create_npc(npc_data)
            room.npcs.append(npc)

        return room

    def create_player(self, player_data, rooms):
        starting_room_name = player_data["starting_location"]
        starting_room = next(room for room in rooms if room.name == starting_room_name)
        starting_inventory = [
            self.create_item(item_data)
            for item_data in player_data.get("inventory", [])
        ]
        return Player(player_data["name"], starting_room, starting_inventory)

    def create_item(self, item_data):
        return Item(
            item_data["name"], item_data["description"], item_data["is_movable"]
        )

    def create_container(self, container_data):
        contained_items = [
            self.create_item(item_data)
            for item_data in container_data.get("contained_items", [])
        ]
        return Container(
            container_data["name"], container_data["description"], contained_items
        )

    def create_npc(self, npc_data):
        npc = NPC(
            npc_data["name"], npc_data["description"], npc_data["interaction_response"]
        )
        npc.contained_items = [
            self.create_item(item_data)
            for item_data in npc_data.get("contained_items", [])
        ]
        return npc

    def create_mechanism(self, mechanism_data):
        return Mechanism(
            mechanism_data["name"],
            mechanism_data["description"],
            activators=mechanism_data.get("activators", []),
        )
