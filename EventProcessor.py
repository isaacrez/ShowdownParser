
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

    MINOR_STATUS = [
        "confusion",
        "perish3"
    ]

    def process(self):
        for status in self.MINOR_STATUS:
            if self.util.current_end_is(status):
                self.assign_responsibility(status)
                break

        if self.util.current_end_is("perish0"):
            self.handle_perish_song()

    def assign_responsibility(self, status):
        name = self.name

        responsible_poke = self.info.last_move_by
        self.info.pokemon[name]["minor sts src"][status] = responsible_poke

    # This would preferably be in "FaintedProcessor", but it requires AT LEAST
    # two prior lines (likely more if two Pokemon faint at once due to Perish Song)
    def handle_perish_song(self):
        name = self.name
        responsible_poke = self.info.pokemon[name]["minor sts src"]["perish3"]
        self.info.pokemon[name]["deaths"] = 1

        if responsible_poke != name:
            self.info.pokemon[responsible_poke]["direct KOs"] += 1
        else:
            other_team = self.util.invert_team(self.team)
            other_poke = self.info.current_pokes[other_team]
            self.info.pokemon[other_poke]["indirect KOs"] += 1


class SwitchProcessor(EventProcessor):

    def process(self):
        name = self.name
        team = self.team

        if self.is_first_time_in(name):
            species = self.util.get_species_name()
            self.info.initialize_pokemon(name, team, species)
            self.info.add_nickname(species, name)

        # Reset information
        self.info.last_move_by = ""
        self.info.pokemon[name][6] = {}
        self.info.current_pokes[team] = name

    def is_first_time_in(self, name):
        return name not in self.info.pokemon.keys()


class MoveProcessor(EventProcessor):

    def process(self):
        self.info.last_move_by = self.name
        self.process_if_minor_status_move()

    def is_move(self, move):
        return move == self.util.curr_components[3]

    def process_if_minor_status_move(self):
        if self.is_move("Perish Song"):
            #TODO: Add handling for Perish Song
            pass


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

    MAJOR_STATUS_KOs = ["psn"]
    MINOR_STATUS_KOs = ["confusion"]

    def process(self):
        self.update_killer_stats()
        self.update_killed_stats()

    def is_self_KO(self):
        return self.info.last_move_by == self.name

    def process_self_KO(self):
        self.info.pokemon[self.name]["deaths"] = 1

        other_team = self.util.invert_team(self.team)
        present_opponent = self.info.current_pokes[other_team]
        self.info.pokemon[present_opponent]["indirect KOs"] += 1

    def update_killer_stats(self):
        kill_type = "indirect KOs"

        print("Death occurred:", self.curr_line[:-1])

        if self.is_accounted_for():
            return

        elif self.is_death_from(self.HAZARDS):
            print("It's due to hazards!")
            killer = self.find_hazard_setter()

        elif self.is_death_from(self.MAJOR_STATUS_KOs):
            print("It's due a status condition!")
            killer = self.find_major_status_setter()

        elif self.is_death_from(self.MINOR_STATUS_KOs):
            print("It's due to a volatile status!")
            killer = self.find_minor_status_setter()

        elif self.is_self_KO():
            print("Heh, they did themselves in!")
            self.process_self_KO()
            return

        else:
            print("The other fella hit 'em!")
            killer = self.info.last_move_by
            kill_type = "direct KOs"

        self.info.pokemon[killer][kill_type] += 1

    def update_killed_stats(self):
        self.info.pokemon[self.name]["deaths"] = 1

    def is_accounted_for(self):
        return self.util.prev_end_is("|upkeep")

    def is_death_from(self, causes):
        for cause in causes:
            if self.util.prev_end_is(cause):
                return True
        return False

    def find_hazard_setter(self):
        cause = self.get_death_cause(self.HAZARDS)
        return self.info.hazards[self.team][cause]

    def get_death_cause(self, causes):
        for cause in causes:
            if self.util.prev_end_is(cause):
                return cause
        raise ValueError("Cause not found from list:", causes)

    def find_major_status_setter(self):
        return self.info.pokemon[self.name]["major sts src"]

    def find_minor_status_setter(self):
        status = self.get_death_cause(self.MINOR_STATUS_KOs)
        return self.info.pokemon[self.name]["minor sts src"][status]