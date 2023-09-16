from .base_interactable import Interactable

from typing import List, Union


class Container(Interactable):
    def __init__(
        self,
        name: str,
        description: str,
        contained_items: List[Union["Item", "Mechanism"]] = None,
    ):
        super().__init__(name, description)
        self.contained_items = contained_items if contained_items else []

    def __str__(self):
        return f"Container(name={self.name}, description={self.description}, contained_items={self.contained_items})"

    def __repr__(self):
        return self.__str__()

    def interact(self, game_engine):
        print(
            f"Items in {self.name} before interaction: {[item.name for item in self.contained_items]}"
        )  # Debug line
        if self.contained_items:
            response = f"You inspect the {self.name} and find: {', '.join([item.name for item in self.contained_items])}."
            room = next(room for room in game_engine.rooms if self in room.containers)
            room.items.extend(self.contained_items)
            self.contained_items = []
            print(
                f"Items in {self.name} after interaction: {self.contained_items}"
            )  # Debug line
            return response
        return f"You interacted with {self.name}, but it's empty."
