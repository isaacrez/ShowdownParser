class ProcessorUtil:

    def __init__(self, prev_line, curr_line):
        self.prev_line = prev_line.rstrip('\n')
        self.curr_line = curr_line.rstrip('\n')
        self.curr_components = self.curr_line.split('|')

    def get_pokemon_team(self):
        return self.curr_components[2][0:2]

    def get_pokemon_name(self):
        nickname = self.curr_components[2]
        return nickname.lstrip('p12a: ')

    def get_species_name(self):
        if self.curr_components[3].endswith("shiny"):
            self.curr_components[3] = self.curr_components[3][:-6]
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
