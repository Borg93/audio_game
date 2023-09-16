from typing import List, Union


class Player:
    def __init__(
        self, name: str, location: str, inventory: List[Union["Item", "Mechanism"]]
    ):
        self.name = name
        self.location = location
        self.inventory = inventory

    def __str__(self):
        inventory_str = ", ".join([item.name for item in self.inventory])
        return (
            f"Player(name={self.name}, location={self.location}, "
            f"inventory=[{inventory_str}])"
        )

    def __repr__(self):
        return self.__str__()

    def find_item(self, item_name):
        return next((item for item in self.inventory if item.name == item_name), None)

    def inventory_summary(self):
        items_str = ", ".join([item.name for item in self.inventory])
        return f"Your inventory contains: {items_str}."

    def current_location(self, rooms):
        return next((room for room in rooms if room.name == self.location), None)
