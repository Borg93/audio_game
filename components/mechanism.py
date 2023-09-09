from interactables.base_interactable import Interactable


class Mechanism(Interactable):
    def __init__(self, name, description, activated=False, activators=None):
        self.name = name
        self.description = description
        self.activated = activated
        self.is_movable = False  # Mechanisms are not movable
        self.activators = activators if activators else []

    def interact(self, item=None):
        if item and item.name in self.activators:
            self.activated = not self.activated
            return f"You used the {item.name} on the {self.name}. It's now {'activated' if self.activated else 'deactivated'}."
        return self.description
