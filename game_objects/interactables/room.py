from typing import List, Dict


class Room:
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.exits: Dict[str, str] = {}
        self.items: List["Item"] = []
        self.containers: List["Container"] = []
        self.npcs: List["NPC"] = []

    def __str__(self):
        items_str = ", ".join([item.name for item in self.items])
        npcs_str = ", ".join([npc.name for npc in self.npcs])
        containers_str = ", ".join([container.name for container in self.containers])
        exits_str = ", ".join(
            [
                f"{direction} to {room_name}"
                for direction, room_name in self.exits.items()
            ]
        )

        return (
            f"Room(name={self.name}, description={self.description}, "
            f"items=[{items_str}], npcs=[{npcs_str}], containers=[{containers_str}], exits=[{exits_str}])"
        )

    def __repr__(self):
        return self.__str__()

    def set_items(self, items):
        self.items = items

    def set_containers(self, containers):
        self.containers = containers

    def set_npcs(self, npcs):
        self.npcs = npcs
