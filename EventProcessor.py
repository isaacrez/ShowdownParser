
from ProcessorUtil import *
from Parser.ParserStorage import ParserStorage

class EventProcessor:

    DIRECT_KO = 2
    PASSIVE_KO = 3
    DEATH = 4
    MAJOR_STATUS = 5
    MINOR_STATUS = 6

    HAZARDS = ["Stealth Rock",
               "Toxic Spikes",
               "Spikes"]

    def __init__(self, prev_line, curr_line, info: ParserStorage, event):
        self.prev_line = prev_line
        self.curr_line = curr_line
        self.info: ParserStorage = info
        self.util: ProcessorUtil = ProcessorUtil(prev_line, curr_line)

        self.event = event
        self.name = self.util.get_pokemon_name(event)
        self.team = self.util.get_pokemon_team(event)

    def check_if_event(self, event):
        input_len = len(event)
        potential_event = self.curr_line[:input_len]

        if potential_event == event:
            return True
        else:
            return False

    def process(self):
        pass


class PartyProcessor(EventProcessor):
    def process(self):
        self.info.add_pokemon(self.name, self.team)


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
        self.info.pokemon[name][self.MINOR_STATUS][status] = responsible_poke

    # This would preferably be in "FaintedProcessor", but it requires AT LEAST
    # two prior lines (likely more if two Pokemon faint at once due to Perish Song)
    def handle_perish_song(self):
        name = self.name
        responsible_poke = self.info.pokemon[name][self.MINOR_STATUS]["perish3"]
        self.info.pokemon[name][self.DEATH] += 1

        if responsible_poke != name:
            self.info.pokemon[responsible_poke][self.DIRECT_KO] += 1
        else:
            other_team = self.util.invert_team(self.team)
            other_poke = self.info.current_pokes[other_team]
            self.info.pokemon[other_poke][self.PASSIVE_KO] += 1


class SwitchProcessor(EventProcessor):

    event_variants = [
        "|switch",
        "|drag"
    ]

    def process(self):
        name = self.name
        team = self.team

        if self.is_first_time_in(name):
            species = self.util.get_species_name(self.event, name)
            self.info.species_to_nickname[species] = name
            self.info.pokemon[name] = [team, species, 0, 0, 0, "", {}]

        # Reset information
        self.info.last_move_by = ""
        self.info.pokemon[name][6] = {}
        self.info.current_pokes[team] = name

    def is_first_time_in(self, name):
        return name not in self.info.pokemon.keys()

class MoveProcessor(EventProcessor):
    def process(self):
        self.info.last_move_by = self.name
        self.process_if_setting_hazards()
        self.process_if_minor_status_move()

    def process_if_setting_hazards(self):
        for hazard in self.HAZARDS:
            if self.is_move(hazard):
                self.process_hazard_move(hazard)
                break

    def is_move(self, move):
        base_index = 12
        start_index = base_index + len(self.name)
        end_index = start_index + len(move)

        potential_move = self.curr_line[start_index:end_index]
        if potential_move == move:
            return True
        else:
            return False

    def process_hazard_move(self, hazard):
        other_team = self.util.invert_team(self.team)
        self.info.hazards[other_team][hazard] = self.name

    def process_if_minor_status_move(self):
        if self.is_move("Perish Song"):
            #TODO: Add handling for Perish Song
            pass


class StatusProcessor(EventProcessor):

    def process(self):
        if self.status_from_hazard():
            responsible_pokemon = self.info.hazards[self.team]["Toxic Spikes"]
        else:
            responsible_pokemon = self.info.last_move_by
        self.label_responsible_pokemon(responsible_pokemon)

    def status_from_hazard(self):
        if self.info.last_move_by == "":
            return True
        else:
            return False

    def label_responsible_pokemon(self, responsible_pokemon):
        name = self.name
        self.info.pokemon[name][self.MAJOR_STATUS] = responsible_pokemon


class FaintProcessor(EventProcessor):

    MAJOR_STATUS_KOs = ["psn"]
    MINOR_STATUS_KOs = ["confusion"]

    def process(self):
        EVENT = "|faint"
        self.name = self.util.get_pokemon_name(EVENT)
        self.team = self.util.get_pokemon_team(EVENT)

        self.update_killer_stats()
        self.update_killed_stats()

    def is_self_KO(self):
        if self.info.last_move_by == self.name:
            return True
        else:
            return False

    def process_self_KO(self):
        self.info.pokemon[self.name][self.DEATH] += 1

        other_team = self.util.invert_team(self.team)
        present_opponent = self.info.current_pokes[other_team]
        self.info.pokemon[present_opponent][self.PASSIVE_KO] += 1

    def update_killer_stats(self):
        is_passive = True

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
            is_passive = False

        if is_passive:
            self.info.pokemon[killer][self.PASSIVE_KO] += 1
        else:
            self.info.pokemon[killer][self.DIRECT_KO] += 1

    def update_killed_stats(self):
        self.info.pokemon[self.name][self.DEATH] = 1

    def is_accounted_for(self):
        if self.util.prev_end_is("|upkeep"):
            print("Death accounted for outside of FaintProcessor")
            return True
        else:
            return False

    def is_death_from(self, causes):
        for cause in causes:
            if self.util.prev_end_is(cause):
                return True
        return False

    def find_hazard_setter(self):
        cause = self.get_death_cause(self.HAZARDS_KOs)
        return self.info.hazards[self.team][cause]

    def get_death_cause(self, causes):
        for cause in causes:
            if self.util.prev_end_is(cause):
                return cause
        raise ValueError("Cause not found from list:", causes)

    def find_major_status_setter(self):
        return self.info.pokemon[self.name][self.MAJOR_STATUS]

    def find_minor_status_setter(self):
        status = self.get_death_cause(self.MINOR_STATUS_KOs)
        return self.info.pokemon[self.name][self.MINOR_STATUS][status]