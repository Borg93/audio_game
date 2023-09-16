from base_command import Command
from ..mechanism import Mechanism


class UseCommand(Command):
    def execute(self):
        item_name = self.kwargs.get("item_name")
        target_name = self.kwargs.get("target_name")

        item = self.find_item_in_inventory(item_name)
        target = self.find_item_in_room(target_name)

        if item and target:
            if isinstance(target, Mechanism):
                return self.response(target.interact(item))
            else:
                return self.response(
                    f"You can't use {item.name} on {target.name}.", status="failure"
                )
        else:
            return self.response("Invalid item or target.", status="failure")
