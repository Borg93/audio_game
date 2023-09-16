def pretty_print(response):
    print("---" * 25)
    print("Game Status")

    # Current Room
    if "current_room" in response:
        print("\nRoom Information:")
        print("  Name:", response["current_room"].name)
        print("  Description:", response["current_room"].description)
        print(
            "  Items:",
            ", ".join([item.name for item in response["current_room"].items]),
        )
        print("  NPCs:", ", ".join([npc.name for npc in response["current_room"].npcs]))
        print(
            "  Containers:",
            ", ".join(
                [container.name for container in response["current_room"].containers]
            ),
        )
        print(
            "  Exits:",
            ", ".join(
                [
                    f"{direction} to {room_name}"
                    for direction, room_name in response["current_room"].exits.items()
                ]
            ),
        )

    # Player Information
    if "player_inventory" in response:
        print("\nPlayer Information:")
        print("  Inventory:", ", ".join(response["player_inventory"]))

    # Command and Action
    if "command_taken" in response or "current_action" in response:
        print("\nCommand:")
        print("  Command Taken:", response["command_taken"])
        print("  Action:", response["current_action"])
        print("  Status:", response["status_response"])

    if "win_condition" in response:
        print("\nWin Condition:", response["win_condition"])
