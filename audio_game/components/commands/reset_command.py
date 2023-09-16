from base_command import Command


class ResetCommand(Command):
    def execute(self):
        self.game_engine.rooms = self.game_engine.initial_rooms.copy()
        self.game_engine.player.location = self.game_engine.initial_player_location
        self.game_engine.link_rooms()
        return self.response("Game reset.")
