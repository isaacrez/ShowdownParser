
from Parser.ParserStorage import *
from Parser.ParserUtil import *

class ParserManipulator:

    def __init__(self):
        self.current_line = " "

    def start(self, filename):
        self.parser = Parser()
        self.f = open(filename)
        self._file_loop()
        self.f.close()

    def _file_loop(self):
        while self.current_line:
            self._update_line()
            self.parser.parse_loop(self.current_line)

    def _update_line(self):
        try:
            self.current_line = self.f.readline()
        except Exception as e:
            print("File reading error!")
            print(e)

    def get_data(self) -> ParserStorage:
        return self.parser.info


class Parser:

    MAJOR_STATUS_KOs = ["psn"]
    MINOR_STATUS_KOs = []
    HAZARDS_KOs = ["Stealth Rock",
                   "Spikes"]

    current_line = ""
    previous_line = ""
    last_move_by = ""
    info: ParserStorage = ParserStorage()

    def parse_loop(self, current_line):
        POTENTIAL_EVENTS = {
            "|poke": self.process_party_member,
            "|move": self.process_move,
            "|-status": self.process_status,
            "|switch": self.process_switch,
            "|drag": self.process_switch,
            "|faint": self.process_faint
        }

        self.previous_line = self.current_line
        self.current_line = current_line

        for event in POTENTIAL_EVENTS:
            if self.current_start_is(event):
                POTENTIAL_EVENTS[event]()
                break

    def process_party_member(self):
        EVENT = "|poke"
        name = self.get_pokemon_name(EVENT)
        team = self.get_pokemon_team(EVENT)
        self.info.party_lineup[team].append(name)

    def process_move(self):
        EVENT = "|move"
        name = self.get_pokemon_name(EVENT)
        team = self.get_pokemon_team(EVENT)
        team = invert_teams(team)
        self.last_move_by = name

        FAILED = -1
        for hazard in self.HAZARDS_KOs:
            if self.current_line.find(hazard, 6) != FAILED:
                self.info.hazards[team] = {hazard: name}

    def process_status(self):
        EVENT = "|-status"
        name = self.get_pokemon_name(EVENT)
        team = self.get_pokemon_team(EVENT)

        if self.last_move_by:
            self.info.pokemon[name][5] = self.last_move_by
        else:
            self.info.pokemon[name][5] = self.info.hazards[team]["Toxic Spikes"]

    def process_switch(self):
        EVENT = "|switch"
        self.process_swap(EVENT)

    def process_drag(self):
        EVENT = "|drag"
        self.process_swap(EVENT)

    def process_swap(self, EVENT):
        name = self.get_pokemon_name(EVENT)
        team = self.get_pokemon_team(EVENT)

        if self.is_first_time_in(name):
            species = self.get_species_name(EVENT, name)
            self.info.species_to_nickname[species] = name
            self.info.pokemon[name] = [team, species, 0, 0, 0, "", {}]

        # Reset information
        self.last_move_by = ""
        self.info.pokemon[name][6] = {}
        self.info.current_pokes[team] = name

    def is_first_time_in(self, name):
        return name not in self.info.pokemon.keys()

    def process_faint(self):
        EVENT = "|faint"
        name = self.get_pokemon_name(EVENT)
        team = self.get_pokemon_team(EVENT)

        passive_KO = True

        if self.is_death_from(self.HAZARDS_KOs):
            killer = self.find_hazard_setter(team)
        elif self.is_death_from(self.MAJOR_STATUS_KOs):
            killer = self.find_major_status_setter(name)
        elif self.is_death_from(self.MINOR_STATUS_KOs):
            killer = self.find_minor_status_setter(name)
        else:
            killer = self.last_move_by
            passive_KO = False

        self.info.pokemon[name][4] = 1
        if passive_KO:
            self.info.pokemon[killer][3] += 1
        else:
            self.info.pokemon[killer][2] += 1

    def is_death_from(self, causes):
        for cause in causes:
            if self.prev_end_is(cause):
                return True
        return False

    def get_death_cause(self, causes):
        for cause in causes:
            if self.prev_end_is(cause):
                return cause
        raise ValueError("Cause not found from list:", causes)

    def find_hazard_setter(self, team):
        cause = self.get_death_cause(self.HAZARDS_KOs)
        return self.info.hazards[team][cause]

    def find_major_status_setter(self, name):
        return self.info.pokemon[name][5]

    def find_minor_status_setter(self, name):
        cause = self.get_death_cause(self.MINOR_STATUS_KOs)
        return self.info.pokemon[name][6][cause]

    def get_pokemon_team(self, event_type):
        OFFSET_LENGTH = {
            "|poke": 6,
            "|move": 6,
            "|-status": 9,
            "|switch": 8,
            "|drag": 6,
            "|faint": 7
        }

        offset = OFFSET_LENGTH[event_type]
        team = self.current_line[offset:offset + 2]
        return team

    def get_pokemon_name(self, event_type):
        OFFSET_LENGTH = {
            "|poke": 9,
            "|move": 11,
            "|-status": 14,
            "|switch": 13,
            "|drag": 11,
            "|faint": 12
        }

        offset = OFFSET_LENGTH[event_type]
        end_index = self.get_index_end_for_section(offset)
        name = self.current_line[offset:end_index]
        return name

    def get_species_name(self, event_type, nickname):
        OFFSET_LENGTH = {
            "|switch": 13,
            "|drag": 11
        }

        offset = OFFSET_LENGTH[event_type] + len(nickname) + 1
        end_index = self.get_index_end_for_section(offset)
        species = self.current_line[offset:end_index]
        return species

    def get_index_end_for_section(self, offset):
        name_end_index = self.current_line.find(",", offset)
        section_end_index = self.current_line.find("|", offset)
        line_end_index = self.current_line.find("\n", offset)

        FAILED = -1
        if section_end_index == FAILED:
            end_index = line_end_index
        elif name_end_index == FAILED:
            end_index = section_end_index
        elif name_end_index < section_end_index:
            end_index = name_end_index
        else:
            end_index = section_end_index

        return end_index

    def current_start_is(self, text):
        return check_start_for(text, self.current_line)

    def current_end_is(self, text):
        return check_line_end_for(text, self.current_line)

    def prev_end_is(self, text):
        return check_line_end_for(text, self.previous_line)
