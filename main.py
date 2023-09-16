from audio_game.game_data_loader import GameDataLoader
from audio_game.game_engine import GameEngine
from audio_game.utils.visualization import Visualization
from audio_game.utils.winning_condition import WinningConditionChecker

from audio_game.utils.utils import pretty_print
from audio_game.game_state import GameState

from audio_game.components.commands.inspect_command import InspectCommand
from audio_game.components.commands.pick_up_command import PickUpCommand

#     DropCommand,
#     TalkCommand,
#     MoveCommand,
#     UseCommand,
# )

from audio_game.game_objects.game_data import game_data

from audio_game.game_objects.game_object_factory import (
    GameObjectFactory,
    ItemFactory,
    MechanismFactory,
    ContainerFactory,
    NPCFactory,
)


if __name__ == "__main__":
    item_factory = ItemFactory()
    mechanism_factory = MechanismFactory()
    container_factory = ContainerFactory(item_factory)
    npc_factory = NPCFactory(item_factory)

    factory = GameObjectFactory(item_factory, mechanism_factory, container_factory, npc_factory)

    game_loader = GameDataLoader(factory)
    player = game_loader.load_player(game_data["player"])
    rooms = game_loader.load_room(game_data["rooms"])

    game_state = GameState(rooms, player)
    winning_condition_checker = WinningConditionChecker(game_data["winning_conditions"], game_state)

    game = GameEngine(game_state, winning_condition_checker)

    vizualizer = Visualization(game_state)
    game.add_observer(vizualizer)

    # Player starts in "The Closet"
    vizualizer.show_graph()
    pretty_print(game_state.state)

    # Player inspect the shelf to discover the uniform

    game.take_action(
        InspectCommand(
            player=game_state.player,
            room=game_state.current_room_location,
            target_name="shelf",
        )
    )
    pretty_print(game_state.state)

    # # Player picks up the uniform from the shelf
    # game.take_action(
    #     PickUpCommand(
    #         game_state.player,
    #         game_state.current_room_location,
    #         item_name="uniform",
    #         target=["shelf"],
    #     )
    # )

    # pretty_print(game_state.get_state())

    # # Player moves to "The Control Room"
    # response = game.take_action(MoveCommand(game, direction="n"))
    # pretty_print(response)

    # # Player talks to the guard to get the ID card
    # response = game.take_action(TalkCommand(game, npc_name="guard"))
    # pretty_print(response)

    # # Player picks up the ID card handed over by the guard
    # response = game.take_action(PickUpCommand(game, item_name="id"))
    # pretty_print(response)

    # # Player picks up the lever from the control room
    # response = game.take_action(PickUpCommand(game, item_name="lever"))
    # pretty_print(response)

    # # Player moves to "The Airlock"
    # response = game.take_action(MoveCommand(game, direction="e"))
    # pretty_print(response)

    # # Player uses the lever on the airlock to activate it
    # response = game.take_action(
    #     UseCommand(game, item_name="lever", target_name="airlock")
    # )
    # pretty_print(response)
