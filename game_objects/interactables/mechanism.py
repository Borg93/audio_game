from .base_interactable import Interactable


class Mechanism(Interactable):
    def __init__(self, name, description, activated=False, activators=None):
        self.name = name
        self.description = description
        self.activated = activated
        self.is_movable = False  # Mechanisms are not movable
        self.activators = activators if activators else []

    def __str__(self):
        return f"Mechanism(name={self.name}, description={self.description}, activated={self.activated}, activators={self.activators})"

    def __repr__(self):
        return self.__str__()

    def interact(self, item=None):
        if item and item.name in self.activators:
            self.activated = not self.activated
            return f"You used the {item.name} on the {self.name}. It's now {'activated' if self.activated else 'deactivated'}."
        return self.description
