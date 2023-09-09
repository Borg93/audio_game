import networkx as nx
import matplotlib.pyplot as plt
from .observer import Observer


class Visualization(Observer):
    def __init__(self, game_engine, show_updates=True):
        self.game_engine = game_engine
        self.G = nx.Graph()
        self.create_graph()
        self.pos = nx.spring_layout(
            self.G, seed=420
        )  # Set a fixed seed for consistent layout
        self.show_updates = show_updates  # Flag to control visualization updates

    def create_graph(self):
        for room in self.game_engine.rooms:
            self.G.add_node(room.name)
            for exit, next_room in room.exits.items():
                self.G.add_edge(room.name, next_room.name)

    def update(self, observable, *args, **kwargs):
        if not self.show_updates:
            return
        if "win" in args:
            print("Congratulations! You have won the game!")
        self.show_graph()

    def show_graph(self):
        plt.figure(figsize=(10, 4))

        # Create custom labels
        labels = {node: node for node in self.G.nodes()}

        node_colors = [
            "blue" if node == self.game_engine.player.location.name else "red"
            for node in self.G.nodes()
        ]
        nx.draw(
            self.G,
            self.pos,
            labels=labels,
            with_labels=True,
            node_color=node_colors,
            node_size=1000,
            font_size=12,
            font_weight="bold",
            edge_color="gray",
        )

        # Title and Subtitle
        plt.title(
            str(self.game_engine.state.current_action), fontsize=14
        )  # Explicitly convert to string

        # Display player's inventory
        inventory_names = [
            item.name for item in self.game_engine.state.player_inventory
        ]
        inventory_text = (
            "Inventory: " + ", ".join(inventory_names)
            if inventory_names
            else "Inventory: Empty"
        )
        plt.annotate(
            inventory_text,
            xy=(0.05, 0.05),
            xycoords="axes fraction",
            fontsize=12,
            color="green",
        )

        plt.show(block=False)
        plt.pause(0.1)
        plt.clf()
