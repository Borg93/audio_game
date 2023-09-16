from abc import ABC, abstractmethod


class Command(ABC):
    def __init__(self, player, room, **kwargs):
        self.player = player
        self.room = room
        self.kwargs = kwargs

    @abstractmethod
    def execute(self):
        pass

    def response(self, message, status="success"):
        return {"message": message, "status_response": status}
