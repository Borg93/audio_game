from game_object_factory import GameObjectFactory


# Updated GameDataLoader
class GameDataLoader:
    @staticmethod
    def load_data(data):
        factory = GameObjectFactory()
        rooms = [factory.create_room(room_data) for room_data in data["rooms"]]
        player = factory.create_player(data["player"], rooms)
        return rooms, player
