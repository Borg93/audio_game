from langchain.tools import BaseTool


class MoveTool(BaseTool):
    name = "Audio_game Interact"
    description = "use this tool when you need to Move between rooms. Only direction needs to be passed"

    def _run(self, direction):
        game.take_action(
            MoveCommand(player=game_state.player, room=game_state.current_room_location, direction=direction)
        )

    def _arun(self, game, MoveCommand, game_state, room, directiom):
        raise NotImplementedError("This tool does not support async")
