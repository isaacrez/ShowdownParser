
from EventProcessor.EventProcessor import EventProcessor

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