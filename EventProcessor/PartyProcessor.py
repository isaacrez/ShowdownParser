
from EventProcessor.EventProcessor import EventProcessor

class PartyProcessor(EventProcessor):

    def process(self):
        self.info.add_pokemon(self.name, self.team)