from langchain.chat_models import ChatOpenAI
from langchain.schema import AIMessage, HumanMessage
from langchain.agents import initialize_agent, AgentType
from langchain.memory import ConversationBufferWindowMemory
from langchain.tools import BaseTool

import openai
import gradio as gr
from dotenv import load_dotenv


from audio_game.game_data_loader import GameDataLoader
from audio_game.game_engine import GameEngine
from audio_game.utils.visualization import Visualization
from audio_game.utils.winning_condition import WinningConditionChecker
from audio_game.utils.utils import pretty_print
from audio_game.game_state import GameState
from audio_game.components.commands.move_command import MoveCommand
from audio_game.game_objects.game_data import game_data
from audio_game.game_objects.game_object_factory import (
    GameObjectFactory,
    ItemFactory,
    MechanismFactory,
    ContainerFactory,
    NPCFactory,
)

load_dotenv()


def chat_response(input_text, history):
    game_context = """This is an game an you are the narrator of the game.
      First reply will be the initial context to start the conversation.
      Only use tools if you need to. 
      """
    response = agent_chain.run(input=f"game_context: {game_context} input: {input_text} context: {game_state.state}")
    return response


def intialize_game():
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

    viz = Visualization(game_state, show_updates=False)
    game.add_observer(viz)

    return game, game_state, viz


desc = (
    "Use this tool when you need to Move between rooms. "
    "Dont use this tool when you only need to know where currently are. Than just check your context instead"
    "To use the tool, you must parse the direction from the message, following parameters is: "
    "['direction']."
    "Possible values for direction is n, s, e, w."
    "Example of input to tool: n"
    "return current room and current exits from the response."
)


class MoveTool(BaseTool):
    name = "Audio_game Interact"
    description = desc

    def _run(self, direction):
        game.take_action(
            MoveCommand(player=game_state.player, room=game_state.current_room_location, direction=direction)
        )
        return str(game_state.state)

    def _arun(self, direction):
        raise NotImplementedError("This tool does not support async")


if __name__ == "__main__":
    game, game_state, viz = intialize_game()

    tools = [MoveTool()]

    # memory = ConversationBufferWindowMemory(memory_key="chat_history", return_messages=True, k=2)

    llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613")
    agent_chain = initialize_agent(
        tools,
        llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,  # "chat-conversational-react-description",
        verbose=True,
        # memory=memory,
        max_iterations=3,
        early_stopping_method="generate",
    )

    gr.ChatInterface(
        chat_response,
        undo_btn=None,
    ).launch()
