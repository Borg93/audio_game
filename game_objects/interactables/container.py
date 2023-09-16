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
        print(f"Items in {self.name} before interaction: {[item.name for item in self.contained_items]}")  # Debug line

        if self.contained_items:
            return f"You inspect the {self.name} and find: {', '.join([item.name for item in self.contained_items])}."
        return f"You interacted with {self.name}, but it's empty."

    def find_item(self, item_name: str):
        return next((item for item in self.contained_items if item.name == item_name), None)
