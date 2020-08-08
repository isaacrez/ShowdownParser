
from EventProcessor.EventProcessor import EventProcessor

class StartProcessor(EventProcessor):

    DIRECT_KO = 2
    PASSIVE_KO = 3
    DEATH = 4
    MINOR_STATUS_ID = 6
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
        self.info.pokemon[name][self.MINOR_STATUS_ID][status] = responsible_poke

    # This would preferably be in "FaintedProcessor", but it requires AT LEAST
    # two prior lines (likely more if two Pokemon faint at once due to Perish Song)
    def handle_perish_song(self):
        name = self.name
        responsible_poke = self.info.pokemon[name][self.MINOR_STATUS_ID]["perish3"]
        self.info.pokemon[name][self.DEATH] += 1

        if responsible_poke != name:
            self.info.pokemon[responsible_poke][self.DIRECT_KO] += 1
        else:
            other_team = self.util.invert_team(self.team)
            other_poke = self.info.current_pokes[other_team]
            self.info.pokemon[other_poke][self.PASSIVE_KO] += 1
