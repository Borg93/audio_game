class GameState:
    def __init__(self, player):
        self.player = player
        self.current_action = ""
        self.status_response = ""
        self.command_taken = ""
        self.win_condition = "Pending"
        self.update_room_state()

    def update_room_state(self):
        location = self.player.location
        self.room_description = location.description
        self.room_items = [item.name for item in location.items]
        self.npc_items = {
            npc.name: [item.name for item in npc.contained_items]
            for npc in location.npcs
        }
        self.container_items = {
            container.name: [item.name for item in container.contained_items]
            for container in location.containers
        }
        self.player_inventory = self.player.inventory  # This line is updated

    def update_state(self, response_dict, command_name=""):
        self.current_action = response_dict["message"]
        self.status_response = response_dict["status_response"]
        self.command_taken = command_name
        self.update_room_state()

    def get_state(self):
        return {
            "current_room": self.player.location.name,
            "room_description": self.room_description,
            "room_items": self.room_items,
            "npc_items": self.npc_items,
            "container_items": self.container_items,
            "player_inventory": self.player_inventory,
            "command_taken": self.command_taken,
            "current_action": self.current_action,
            "status_response": self.status_response,
            "win_condition": self.win_condition,
        }

    def add_to_inventory(self, item):
        self.player.inventory.append(item)
        self.update_room_state()

    def remove_from_inventory(self, item):
        self.player.inventory.remove(item)
        self.update_room_state()
