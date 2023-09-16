import networkx as nx
import matplotlib.pyplot as plt


class GraphManager:
    def __init__(self, game_state):
        self.G = nx.Graph()
        self.create_graph(game_state.rooms)  # Access rooms from game_state
        self.pos = nx.spring_layout(self.G, seed=420)

    def create_graph(self, rooms):
        for room in rooms:
            self.G.add_node(room.name)
            for _, next_room in room.exits.items():
                self.G.add_edge(room.name, next_room)

    def draw_graph(self, node_colors, labels):
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

    @property
    def nodes(self):
        return list(self.G.nodes())


class Visualization:
    def __init__(self, game_state, show_updates=True):
        self.graph_manager = GraphManager(game_state)  # Pass game_state
        self.show_updates = show_updates
        self.game_state = game_state

    def update(self, observable, *args, **kwargs):
        if not self.show_updates:
            return
        if "win" in args:
            print("Congratulations! You have won the game!")

        self.show_graph()

    def show_graph(self):
        plt.figure(figsize=(10, 4))

        labels = {node: node for node in self.graph_manager.nodes}

        node_colors = [
            "blue" if node == self.game_state.current_room_location_name else "red"
            for node in self.graph_manager.nodes
        ]

        self.graph_manager.draw_graph(node_colors, labels)

        # Display player's inventory using game_state
        inventory_text = self._build_inventory_text(
            self.game_state.current_inventory_items_names
        )

        plt.title(self.game_state.current_action, fontsize=14)

        # Using text instead of annotate
        plt.text(
            0.05,
            0.05,
            inventory_text,
            transform=plt.gca().transAxes,
            fontsize=12,
            color="green",
        )

        plt.show()

    def _build_inventory_text(self, inventory_names):
        return (
            f"Inventory: {', '.join(inventory_names)}"
            if inventory_names
            else "Inventory: Empty"
        )
