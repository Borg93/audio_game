from base_command import Command


class TalkCommand(Command):
    def execute(self):
        npc_name = self.kwargs.get("npc_name")
        password = self.kwargs.get("password")
        npc = self.find_npc_in_room(npc_name)

        if npc:
            return self.response(
                npc.interact(self.game_engine, provided_password=password)
            )
        else:
            return self.response("No one by that name here.", status="failure")
