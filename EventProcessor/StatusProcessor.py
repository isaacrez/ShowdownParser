
from EventProcessor.EventProcessor import EventProcessor

class StatusProcessor(EventProcessor):

    STATUS_INDEX = 5

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
        self.info.pokemon[name][self.STATUS_INDEX] = responsible_pokemon
