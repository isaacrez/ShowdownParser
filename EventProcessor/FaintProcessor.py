
from EventProcessor.EventProcessor import EventProcessor

class FaintProcessor(EventProcessor):

    DIRECT_KO = 2
    PASSIVE_KO = 3
    DEATH = 4
    MAJOR_STATUS = 5
    MINOR_STATUS = 6

    MAJOR_STATUS_KOs = [
        "psn"
    ]

    MINOR_STATUS_KOs = [
        "confusion"
    ]

    HAZARDS_KOs = [
        "Stealth Rock",
        "Toxic Spikes",
        "Spikes"
    ]

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

        elif self.is_death_from(self.HAZARDS_KOs):
            killer = self.find_hazard_setter()

        elif self.is_death_from(self.MAJOR_STATUS_KOs):
            killer = self.find_major_status_setter()

        elif self.is_death_from(self.MINOR_STATUS_KOs):
            killer = self.find_minor_status_setter()

        elif self.is_self_KO():
            self.process_self_KO()
            return

        else:
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