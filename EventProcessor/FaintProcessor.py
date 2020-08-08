
from EventProcessor.EventProcessor import EventProcessor

class FaintProcessor(EventProcessor):

    DIRECT_KO = 2
    PASSIVE_KO = 3
    DEATH = 4

    MAJOR_STATUS_KOs = ["psn"]

    HAZARDS_KOs = [
        "Stealth Rock",
        "Toxic Spikes",
        "Spikes"
    ]

    def process(self):
        EVENT = "|faint"
        self.name = self.util.get_pokemon_name(EVENT)
        self.team = self.util.get_pokemon_team(EVENT)

        if self.is_self_KO():
            self.process_self_KO()
        else:
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

        if self.is_death_from(self.HAZARDS_KOs):
            killer = self.find_hazard_setter(self.team)
        elif self.is_death_from(self.MAJOR_STATUS_KOs):
            killer = self.find_status_setter(self.name)
        elif self.is_death_from(["recoil"]):
            other_team = self.util.invert_team(self.team)
            killer = self.info.current_pokes[other_team]
        else:
            killer = self.info.last_move_by
            is_passive = False

        if is_passive:
            self.info.pokemon[killer][self.PASSIVE_KO] += 1
        else:
            self.info.pokemon[killer][self.DIRECT_KO] += 1

    def update_killed_stats(self):
        self.info.pokemon[self.name][self.DEATH] = 1

    def is_death_from(self, causes):
        for cause in causes:
            if self.util.prev_end_is(cause):
                return True
        return False
    
    def find_hazard_setter(self, team):
        cause = self.get_death_cause(self.HAZARDS_KOs)
        return self.info.hazards[team][cause]

    def get_death_cause(self, causes):
        for cause in causes:
            if self.util.prev_end_is(cause):
                return cause
        raise ValueError("Cause not found from list:", causes)

    def find_status_setter(self, name):
        return self.info.pokemon[name][5]