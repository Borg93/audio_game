from .base_interactable import Interactable

from typing import Optional, List, Union


class NPC(Interactable):
    def __init__(
        self,
        name: str,
        description: str,
        interaction_response: str,
        contained_items: List[Union["Item", "Mechanism"]],
        condition: Optional["Condition"] = None,
    ):
        super().__init__(name, description)
        self.interaction_response = interaction_response
        self.contained_items = contained_items
        self.condition = condition

    def interact(self, game_engine, provided_password=None):
        if self.condition and not self.condition.is_met(
            game_engine.state.player_inventory, game_engine.rooms, provided_password
        ):
            return "The NPC doesn't want to talk to you right now."

        # Debug line to print items in the NPC before interaction
        print(f"Items in {self.name} before interaction: {[item.name for item in self.contained_items]}")

        if hasattr(self, "contained_items") and self.contained_items:
            # Find the room where the NPC is located
            room = next(room for room in game_engine.rooms if self in room.npcs)

            # Debug line to print items in the room before adding
            print(f"Items in {room.name} before adding: {[item.name for item in room.items]}")

            # Move items from the NPC to the room
            room.items.extend(self.contained_items)

            # Debug line to print items in the room after adding
            print(f"Items in {room.name} after adding: {[item.name for item in room.items]}")

            self.contained_items = []

            # Debug line to print items in the NPC after interaction
            print(f"Items in {self.name} after interaction: {[item.name for item in self.contained_items]}")

        return self.interaction_response
