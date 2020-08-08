
from EventProcessor.EventProcessor import EventProcessor

class PartyProcessor(EventProcessor):

    def process(self):
        name = self.name
        team = self.team
        self.info.party_lineup[team].append(name)
