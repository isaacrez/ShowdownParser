
from Parser.Parser import *

DIRECT_KOs_ID = 2
PASSIVE_KOs_ID = 3
DEATHS_ID = 4

class ParserSimulator:

    def __init__(self, pokemon_data):
        self.parser = Parser()
        self.cmd_maker = ParserCommandMaker()
        self.pokemon_data = pokemon_data

    def load_all(self):
        for nickname in self.pokemon_data:
            team = self.pokemon_data[nickname][0]
            species = self.pokemon_data[nickname][1]

            self.cmd_maker.set_new_command("poke")
            self.cmd_maker.add_team_to_command(team)
            self.cmd_maker.add_species_to_command(species)
            self.cmd_maker.add_command_end()
            self.apply_command()

    def switch_in_all(self):
        for nickname in self.pokemon_data:
            self.switch_in_species(nickname)

    def switch_in_species(self, nickname):
        team = self.pokemon_data[nickname][0]

        self.cmd_maker.set_new_command("switch")
        self.cmd_maker.add_team_to_command(team)
        self.cmd_maker.add_nickname_to_command(nickname)
        self.cmd_maker.add_command_end()

        self.apply_command()

    def move(self, attacker, move, defender):
        team = self.pokemon_data[attacker][0]
        opposing_team = self._invert_team(team)

        self.cmd_maker.set_new_command("move")
        self.cmd_maker.add_team_to_command(team)
        self.cmd_maker.add_nickname_to_command(attacker)
        self.cmd_maker.add_move_to_command(move)
        self.cmd_maker.add_team_to_command(opposing_team)
        self.cmd_maker.add_nickname_to_command(defender)

        self.apply_command()

    def damage(self, nickname, src=None):
        team = self.pokemon_data[nickname][0]

        self.cmd_maker.set_new_command("-damage")
        self.cmd_maker.add_team_to_command(team)
        self.cmd_maker.add_nickname_to_command(nickname)

        if src is None:
            self.cmd_maker.add_command_end()
        else:
            self.cmd_maker.add_unique_damaged_end(src)

    def faint(self, nickname):
        team = self.pokemon_data[nickname][0]

        self.cmd_maker.set_new_command("faint")
        self.cmd_maker.add_team_to_command(team)
        self.cmd_maker.add_nickname_to_command(nickname)

        self.apply_command()

    def apply_command(self):
        cmd = self.cmd_maker.parse_command
        self.parser.parse_loop(cmd)
        self.cmd_maker.reset()

    @staticmethod
    def _invert_team(team):
        if team == "p1":
            return "p2"
        else:
            return "p1"

class ParserCommandMaker:

    command_type: str = ""
    parse_command: str = ""

    def set_new_command(self, command):
        self.command_type = command
        self.parse_command = "|" + command

    def reset(self):
        self.command_type = ""
        self.parse_command = ""

    def add_team_to_command(self, team):
        if self.command_type == "poke":
            self.parse_command += "|" + team
        else:
            self.parse_command += "|" + team + "a: "

    def add_species_to_command(self, species):
        self.parse_command += "|" + species

    def add_nickname_to_command(self, nickname):
        self.parse_command += nickname

    def add_move_to_command(self, move):
        self.parse_command += "|" + move

    def add_command_end(self):
        COMMAND_END = {
            "switch": "|999\/999\n",
            "poke": "|item\n",
            "-damage": "|1\/999\n"
        }
        DEFAULT = "\n"

        if self.command_type in COMMAND_END:
            ending = COMMAND_END[self.command_type]
            self.parse_command += ending
        else:
            self.parse_command += DEFAULT

    def add_unique_damaged_end(self, damage_src):
        self.parse_command += "|0 fnt|[from] "
        self.parse_command += damage_src + "\n"


class ParserReader:

    def __init__(self, parser: Parser):
        self.data = parser.info.pokemon

    def get_direct_KOs_of(self, nickname):
        return self.data[nickname][DIRECT_KOs_ID]

    def get_indirect_KOs_of(self, nickname):
        return self.data[nickname][PASSIVE_KOs_ID]

    def is_fainted(self, nickname):
        if self.data[nickname][DEATHS_ID] == 0:
            return False
        else:
            return True
