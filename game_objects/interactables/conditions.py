from .mechanism import Mechanism


# Condition
class Condition:
    def __init__(self, required_items=None, required_mechanisms=None, password=None):
        self.required_items = required_items or []
        self.required_mechanisms = required_mechanisms or {}
        self.expected_password = password

    def __str__(self):
        return f"Condition(required_items={self.required_items}, required_mechanisms={self.required_mechanisms}, expected_password={self.expected_password})"

    def __repr__(self):
        return self.__str__()

    def is_met(self, player_inventory, rooms, provided_password=None):
        return (
            self._check_items(player_inventory)
            and self._check_mechanisms(rooms)
            and self._check_password(provided_password)
        )

    def _check_items(self, player_inventory):
        return all(item in player_inventory for item in self.required_items)

    def _check_mechanisms(self, rooms):
        for mech_name, expected_state in self.required_mechanisms.items():
            mechanism = next(
                (
                    item
                    for room in rooms
                    for item in room.items
                    if isinstance(item, Mechanism) and item.name == mech_name
                ),
                None,
            )
            if not mechanism or mechanism.activated != expected_state:
                return False
        return True

    def _check_password(self, provided_password):
        if self.expected_password:
            return provided_password == self.expected_password
        return True
