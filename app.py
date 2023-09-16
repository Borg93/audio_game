from langchain.chat_models import ChatOpenAI
from langchain.schema import AIMessage, HumanMessage
from langchain.agents import initialize_agent
from langchain.memory import ConversationBufferWindowMemory
from langchain.agents import Tool

from custom_tooling import MoveTool

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


def chat_response(input_text):
    response = agent_chain.run(input=input_text)
    return response


def predict(message, history):
    history_langchain_format = []
    for human, ai in history:
        history_langchain_format.append(HumanMessage(content=human))
        history_langchain_format.append(AIMessage(content=ai))
    history_langchain_format.append(HumanMessage(content=message))
    gpt_response = llm(history_langchain_format)
    return gpt_response.content


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


if __name__ == "__main__":
    game, game_state, viz = intialize_game()

    tools = [MoveTool(game, game_state)]

    memory = ConversationBufferWindowMemory(memory_key="chat_history", return_messages=True, k=2)

    llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613")
    agent_chain = initialize_agent(
        tools,
        llm,
        agent="chat-conversational-react-description",
        verbose=True,
        memory=memory,
        max_iterations=3,
        early_stopping_method="generate",
    )

    # Player starts in "The Closet"
    # viz.show_graph()
    # pretty_print(game_state.state)

    # game.take_action(MoveCommand(player=game_state.player, room=game_state.current_room_location, direction="n"))

    # pretty_print(game_state.state)

    gr.ChatInterface(
        chat_response,
        undo_btn=None,
    ).launch()
