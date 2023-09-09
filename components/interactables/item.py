from base_interactable import Interactable
from npc import NPC
from player import Player
from container import Container
from room import Room


class Item(Interactable):
    def __init__(self, name, description, is_movable=True):
        self.name = name
        self.description = description
        self.is_movable = is_movable

    def interact(self, target=None):
        return f"You tried to use {self.name}, but nothing happened."


class Consumable(Item):
    def __init__(self, name, description, effect, is_consumed_on_use=True):
        super().__init__(name, description)
        self.effect = effect
        self.is_consumed_on_use = is_consumed_on_use

    def interact(self, target=None):
        if isinstance(target, (NPC, Player)):
            if self.is_consumed_on_use:
                # Logic to remove from inventory will be handled in UseCommand
                return f"You used {self.name} on {target.name}. {self.effect}"
            return f"You used {self.name} on {target.name}."
        return super().use(target)


class Tool(Item):
    def interact(self, target=None):
        if isinstance(target, (NPC, Item, Container, Room)):
            return f"You used {self.name} on {target.name}."
        return super().use(target)
