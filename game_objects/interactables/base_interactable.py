from abc import ABC, abstractmethod


class Interactable(ABC):
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

    @abstractmethod
    def interact(self):
        pass

    def __str__(self):
        return self.name
