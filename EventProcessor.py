
from ProcessorUtil import *
from Parser.ParserStorage import ParserStorage

class EventProcessor:

    HAZARDS = ["Stealth Rock",
               "Toxic Spikes",
               "Spikes"]

    def __init__(self, prev_line, curr_line, info: ParserStorage, event):
        self.prev_line = prev_line
        self.curr_line = curr_line
        self.info: ParserStorage = info
        self.util: ProcessorUtil = ProcessorUtil(prev_line, curr_line)

        self.event = event
        self.name = self.util.get_pokemon_name()
        self.team = self.util.get_pokemon_team()

    def check_if_event(self, event):
        return self.curr_line.startswith(event)

    def process(self):
        pass


class PartyProcessor(EventProcessor):

    def __init__(self, prev_line, curr_line, info: ParserStorage, event):
        self.info = info
        util = ProcessorUtil(prev_line, curr_line)

        self.species = util.get_species_name()
        self.team = util.get_pokemon_team()

    def process(self):
        self.info.update_lineup(self.species, self.team)


class StartProcessor(EventProcessor):

    MINOR_STATUS = ["confusion"]

    def process(self):
        for status in self.MINOR_STATUS:
            if self.util.current_end_is(status):
                self.assign_responsibility(status)
                break

    def assign_responsibility(self, status):
        name = self.name
        responsible_poke = self.info.last_move_by
        self.info.pokemon[name]["minor sts src"][status] = responsible_poke


class PerishSongProcessor(EventProcessor):

    def process(self):
        for team in self.info.current_pokes:
            name = self.info.current_pokes[team]
            self.info.pokemon[name]["minor sts src"]["Perish Song"] = self.info.last_move_by

class SwitchProcessor(EventProcessor):

    def process(self):
        if self.is_first_time_in():
            species = self.util.get_species_name()
            self.info.initialize_pokemon(self.name, self.team, species)
            self.info.add_nickname(species, self.name)

        self.info.update_field(self.name)

    def is_first_time_in(self):
        return self.name not in self.info.pokemon.keys()


class MoveProcessor(EventProcessor):

    def process(self):
        self.info.last_move_by = self.name

    def is_move(self, move):
        return move == self.util.curr_components[3]


class DamageProcessor(EventProcessor):

    def process(self):
        src = "direct"
        if len(self.util.curr_components) > 4:
            src = self.util.curr_components[4][7:]

        self.info.update_damage(self.name, src)

class HazardProcessor(EventProcessor):

    def process(self):
        if self.util.curr_components[3].startswith("move: "):
            team = self.util.curr_components[2][0:2]
            setting_team = self.util.invert_team(team)
            setter = self.info.current_pokes[setting_team]
            hazard_set = self.util.curr_components[3][6:-1]
            self.info.hazards[team][hazard_set] = setter


class StatusProcessor(EventProcessor):

    def process(self):
        if self.status_from_hazard():
            responsible_pokemon = self.info.hazards[self.team]["Toxic Spikes"]
        else:
            responsible_pokemon = self.info.last_move_by
        self.label_responsible_pokemon(responsible_pokemon)

    def status_from_hazard(self):
        return self.info.last_move_by == ""

    def label_responsible_pokemon(self, responsible_pokemon):
        name = self.name
        self.info.pokemon[name]["major sts src"] = responsible_pokemon


class FaintProcessor(EventProcessor):

    def process(self):
        if self.not_accounted_for():
            self.update_killer_stats()
            self.update_killed_stats()
        print(self.info.pokemon)

    def not_accounted_for(self):
        return not self.info.pokemon[self.name]["deaths"] == 1

    def update_killer_stats(self):
        if self.name in self.info.damaged_by:
            killer = self.info.damaged_by[self.name][0]
            kill_type = self.info.damaged_by[self.name][1]

        else:
            # Perish Song kill
            killer = self.info.pokemon[self.name]["minor sts src"]["Perish Song"]
            if killer == self.name:
                killer = self.info.other_field_pokemon(self.name)
            kill_type = "indirect"

        self.info.pokemon[killer][kill_type + " KOs"] += 1

    def update_killed_stats(self):
        self.info.pokemon[self.name]["deaths"] = 1
