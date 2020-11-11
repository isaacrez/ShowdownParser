class ProcessorUtil:

    def __init__(self, prev_line, curr_line):
        self.prev_line = prev_line
        self.curr_line = curr_line
        self.curr_components = curr_line.split('|')

    def get_pokemon_team(self):
        return self.curr_components[2][0:2]

    def get_pokemon_name(self):
        nickname = self.curr_components[2]
        return nickname.lstrip('p12a: ').rstrip('\n')

    def get_species_name(self):
        return self.curr_components[3].rstrip(", MF")

    def current_start_is(self, text):
        return self.curr_line.startswith(text)

    def current_end_is(self, text):
        return self.curr_line.endswith(text)

    def prev_end_is(self, text):
        return self.prev_line.endswith(text)

    @staticmethod
    def invert_team(team):
        if team == "p1":
            return "p2"
        else:
            return "p1"
