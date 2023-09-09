from base_interactable import Interactable


class Container(Interactable):
    def __init__(self, name, description, contained_items=None):
        self.name = name
        self.description = description
        self.contained_items = contained_items if contained_items else []

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
