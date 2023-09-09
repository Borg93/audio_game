from abc import ABC, abstractmethod


class Interactable(ABC):
    @abstractmethod
    def interact(self):
        pass

    def __str__(self):
        return self.name


# Obersever pattern for event for as interaction for instance between items and player
