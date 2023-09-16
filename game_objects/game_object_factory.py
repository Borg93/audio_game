from .interactables import Room, Container, Player, NPC, Item, Mechanism, Condition


class ItemFactory:
    def create(self, item_data):
        name, description, is_movable = self.extract_data(item_data)
        return Item(name, description, is_movable)

    def extract_data(self, item_data):
        name = item_data.get("name", "Unnamed")
        description = item_data.get("description", "No Description")
        is_movable = item_data.get("is_movable", False)
        return name, description, is_movable


class MechanismFactory(ItemFactory):
    def create(self, mechanism_data):
        name, description, activated, activators = self.extract_data(mechanism_data)
        return Mechanism(name, description, activated=activated, activators=activators)

    def extract_data(self, mechanism_data):
        name = mechanism_data.get("name", "Unnamed")
        description = mechanism_data.get("description", "No Description")
        activated = mechanism_data.get("activated", False)
        activators = mechanism_data.get("activators", [])
        return name, description, activated, activators


class ContainerFactory:
    def __init__(self, item_factory: ItemFactory):
        self.item_factory = item_factory

    def create(self, container_data):
        name, description, contained_items = self.extract_data(container_data)
        return Container(name, description, contained_items)

    def extract_data(self, container_data):
        name = container_data.get("name", "Unnamed")
        description = container_data.get("description", "No Description")
        contained_items = [
            self.item_factory.create(item_data)
            for item_data in container_data.get("contained_items", [])
        ]
        return name, description, contained_items


class NPCFactory:
    def __init__(self, item_factory: ItemFactory):
        self.item_factory = item_factory

    def create(self, npc_data):
        (
            name,
            description,
            interaction_response,
            contained_items,
            condition,
        ) = self.extract_data(npc_data)
        return NPC(name, description, interaction_response, contained_items, condition)

    def extract_data(self, npc_data):
        name = npc_data.get("name", "Unnamed")
        description = npc_data.get("description", "No Description")
        interaction_response = npc_data.get("interaction_response", "No Response")

        contained_items = [
            self.item_factory.create(item_data)
            for item_data in npc_data.get("contained_items", [])
        ]

        condition_data = npc_data.get("condition", None)
        condition = None
        if condition_data:
            condition = Condition(
                required_items=condition_data.get("required_items", []),
                password=condition_data.get("password", None),
            )

        return name, description, interaction_response, contained_items, condition


class GameObjectFactory:
    def __init__(
        self,
        item_factory: ItemFactory,
        mechanism_factory: MechanismFactory,
        container_factory: ContainerFactory,
        npc_factory: NPCFactory,
    ):
        self.item_factory = item_factory
        self.mechanism_factory = mechanism_factory
        self.container_factory = container_factory
        self.npc_factory = npc_factory

    def create_room(self, room_data):
        room = self._create_basic_room(room_data)
        self._populate_room(room, room_data)
        return room

    def _create_basic_room(self, room_data):
        return Room(room_data["name"], room_data["description"])

    def _populate_room(self, room, room_data):
        room.items = self._create_items_or_mechanisms(room_data.get("items", []))
        room.containers = self._create_containers(room_data.get("containers", []))
        room.npcs = self._create_npcs(room_data.get("npcs", []))
        room.exits = room_data.get("exits", {})

    def _create_items_or_mechanisms(self, items_data):
        return [self._create_item_or_mechanism(item) for item in items_data]

    def _create_item_or_mechanism(self, item_data):
        if "type" in item_data and item_data["type"] == "mechanism":
            return self.mechanism_factory.create(item_data)
        else:
            return self.item_factory.create(item_data)

    def _create_containers(self, containers_data):
        return [
            self.container_factory.create(container) for container in containers_data
        ]

    def _create_npcs(self, npcs_data):
        return [self.npc_factory.create(npc) for npc in npcs_data]

    def create_player(self, player_data):
        starting_inventory = self._create_items(player_data.get("inventory", []))
        return Player(
            player_data["name"], player_data["starting_location"], starting_inventory
        )

    def _create_items(self, items_data):
        return [self.item_factory.create(item) for item in items_data]
