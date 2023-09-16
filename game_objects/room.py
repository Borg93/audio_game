from typing import List, Dict
from .interactables.item import Item
from .interactables.container import Container
from .interactables.npc import NPC


class Room:
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.exits: Dict[str, str] = {}
        self.items: List[Item] = []
        self.containers: List[Container] = []
        self.npcs: List[NPC] = []

    def __str__(self):
        items_str = ", ".join([item.name for item in self.items])
        npcs_str = ", ".join([npc.name for npc in self.npcs])
        containers_str = ", ".join([container.name for container in self.containers])
        exits_str = ", ".join([f"{direction} to {room_name}" for direction, room_name in self.exits.items()])

        return (
            f"Room(name={self.name}, description={self.description}, "
            f"items=[{items_str}], npcs=[{npcs_str}], containers=[{containers_str}], exits=[{exits_str}])"
        )

    def __repr__(self):
        return self.__str__()

    def find_item(self, item_name):
        return next((item for item in self.items if item.name == item_name), None)

    def find_container(self, container_name):
        return next(
            (container for container in self.containers if container.name == container_name),
            None,
        )

    def find_npc(self, npc_name):
        return next((npc for npc in self.npcs if npc.name == npc_name), None)

    def description_summary(self):
        items_str = ", ".join([item.name for item in self.items])
        npcs_str = ", ".join([npc.name for npc in self.npcs])
        containers_str = ", ".join([container.name for container in self.containers])
        return f"Items: [{items_str}], NPCs: [{npcs_str}], Containers: [{containers_str}]"

    def available_exits(self):
        exits_str = ", ".join([f"{direction} to {room_name}" for direction, room_name in self.exits.items()])
        return f"Available exits: [{exits_str}]"
