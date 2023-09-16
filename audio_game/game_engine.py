from .utils.observer import Observable
from .utils.winning_condition import WinningConditionChecker
from .game_state import GameState
from .components.commands.base_command import Command


class GameEngine(Observable):
    def __init__(self, game_state: GameState, winning_condition_checker: WinningConditionChecker):
        super().__init__()  # Initialize the Observable part of GameEngine
        self.game_state = game_state
        self.winning_condition_checker = winning_condition_checker

    def take_action(self, command: Command):
        response_dict = command.execute()
        last_command_name = command.__class__.__name__

        # Update the state with the message from the response_dict
        self.game_state.update_state(response_dict, command_name=last_command_name)

        if self.winning_condition_checker.check_winning_condition():
            self.winning_condition_checker.update_game_state_winning_condition()

        self.notify_observers(game_state=self.game_state)
