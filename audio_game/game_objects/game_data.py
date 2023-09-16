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
                    "is_movable": False,  # or True, depending on your game logic
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
