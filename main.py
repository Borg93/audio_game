from game_data_loader import GameDataLoader
from game_engine import GameEngine
from utils.visualization import Visualization
from utils.utils import pretty_print
from components.commands import (
    InspectCommand,
    PickUpCommand,
    DropCommand,
    TalkCommand,
    MoveCommand,
    UseCommand,
)

if __name__ == "__main__":
    game_data = {
        "rooms": [
            {
                "name": "The Closet",
                "description": "You are in a small nondescript closet.",
                "containers": [
                    {
                        "name": "shelf",
                        "description": "A wooden shelf that looks old.",
                        "contained_items": [
                            {
                                "name": "uniform",
                                "description": "The uniform is blue and drab. It might be useful.",
                                "is_movable": True,
                            }
                        ],
                    }
                ],
                "items": [],
                "npcs": [],
                "exits": {"n": "The Control Room"},
            },
            {
                "name": "The Control Room",
                "description": "You are in a control room with an airlock to the east. There's a guard here, and he seems to be guarding something.",
                "items": [
                    {
                        "name": "lock",
                        "description": "An electronic lock. It seems to require an ID card.",
                        "is_movable": False,
                    },
                    {
                        "name": "lever",
                        "description": "A rusty lever attached to the wall. It seems to control something.",
                        "is_movable": True,
                    },
                ],
                "npcs": [
                    {
                        "name": "guard",
                        "description": "The guard looks mean.",
                        "interaction_response": "The guard grumbles and reluctantly hands you an ID card.",
                        "condition": {
                            "required_items": ["uniform"],
                            "password": "secret",
                        },
                        "contained_items": [
                            {
                                "name": "id",
                                "description": "A silver ID card. It looks important.",
                                "is_movable": True,
                            }
                        ],
                    }
                ],
                "exits": {"s": "The Closet", "e": "The Airlock"},
            },
            {
                "name": "The Airlock",
                "description": "You are in an airlock. It's the only way out, but you need a special item to operate it.",
                "items": [
                    {
                        "name": "airlock",
                        "description": "A heavy-duty airlock. It seems to require a lever to operate.",
                        "type": "mechanism",
                        "activators": ["lever"],
                    }
                ],
                "npcs": [],
                "exits": {"w": "The Control Room"},
            },
        ],
        "player": {
            "name": "The Player",
            "starting_location": "The Closet",
            "inventory": [],  # Example initial items
        },
        "winning_conditions": {
            "room": "The Airlock",
            "items": ["id", "lever"],
            "command": "UseCommand",
        },
    }

    rooms, player = GameDataLoader.load_data(game_data)
    game = GameEngine(
        rooms, player, Visualization, game_data, show_updates=True
    )  # This will show updates
    game.add_observer(game.viz)

    # Player starts in "The Closet"
    game.viz.show_graph()
    pretty_print(game.state.get_state())

    # Player inspect the shelf to discover the uniform
    response = game.take_action(InspectCommand(game, name="shelf"))
    pretty_print(response)

    # Player picks up the uniform from the shelf
    response = game.take_action(PickUpCommand(game, item_name="uniform"))
    pretty_print(response)

    # Player moves to "The Control Room"
    response = game.take_action(MoveCommand(game, direction="n"))
    pretty_print(response)

    # Player talks to the guard to get the ID card
    response = game.take_action(TalkCommand(game, npc_name="guard"))
    pretty_print(response)

    # Player picks up the ID card handed over by the guard
    response = game.take_action(PickUpCommand(game, item_name="id"))
    pretty_print(response)

    # Player picks up the lever from the control room
    response = game.take_action(PickUpCommand(game, item_name="lever"))
    pretty_print(response)

    # Player moves to "The Airlock"
    response = game.take_action(MoveCommand(game, direction="e"))
    pretty_print(response)

    # Player uses the lever on the airlock to activate it
    response = game.take_action(
        UseCommand(game, item_name="lever", target_name="airlock")
    )
    pretty_print(response)
