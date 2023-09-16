from game_objects.game_object_factory import GameObjectFactory


# Updated GameDataLoader
class GameDataLoader:
    def __init__(self, factory: GameObjectFactory):
        self.factory = factory

    def load_room(self, rooms_data):
        rooms = [self.factory.create_room(room_data) for room_data in rooms_data]
        return rooms

    def load_player(self, player_data):
        return self.factory.create_player(player_data)


if __name__ == "__main__":
    from game_objects.game_data import game_data
    from game_objects.game_object_factory import (
        ItemFactory,
        MechanismFactory,
        ContainerFactory,
        NPCFactory,
    )

    item_factory = ItemFactory()
    mechanism_factory = MechanismFactory()
    container_factory = ContainerFactory(item_factory)
    npc_factory = NPCFactory(item_factory)

    factory = GameObjectFactory(
        item_factory, mechanism_factory, container_factory, npc_factory
    )
    game_loader = GameDataLoader(factory)
    player = game_loader.load_player(game_data["player"])
    rooms = game_loader.load_room(game_data["rooms"])

    for room in rooms:
        print(room)

    # print(player)
