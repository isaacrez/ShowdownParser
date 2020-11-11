class ProcessorUtil:

    def __init__(self, prev_line, curr_line):
        self.prev_line = prev_line
        self.curr_line = curr_line

    def get_pokemon_team(self, event_type):
        OFFSET_LENGTH = {
            "|poke": 6,
            "|move": 6,
            "|-status": 9,
            "|-start": 8,
            "|switch": 8,
            "|drag": 6,
            "|faint": 7
        }

        offset = OFFSET_LENGTH[event_type]
        team = self.curr_line[offset:offset + 2]
        return team

    def get_pokemon_name(self, event_type):
        OFFSET_LENGTH = {
            "|poke": 9,
            "|move": 11,
            "|-status": 14,
            "|-start": 13,
            "|switch": 13,
            "|drag": 11,
            "|faint": 12
        }

        offset = OFFSET_LENGTH[event_type]
        end_index = self.get_index_end_for_section(offset)
        name = self.curr_line[offset:end_index]
        return name

    def get_species_name(self, event_type, nickname):
        OFFSET_LENGTH = {
            "|switch": 13,
            "|drag": 11
        }

        offset = OFFSET_LENGTH[event_type] + len(nickname) + 1
        end_index = self.get_index_end_for_section(offset)
        species = self.curr_line[offset:end_index]
        return species

    def get_index_end_for_section(self, offset):
        name_end_index = self.curr_line.find(",", offset)
        section_end_index = self.curr_line.find("|", offset)
        line_end_index = self.curr_line.find("\n", offset)

        FAILED = -1
        if section_end_index == FAILED:
            end_index = line_end_index
        elif name_end_index == FAILED:
            end_index = section_end_index
        elif name_end_index < section_end_index:
            end_index = name_end_index
        else:
            end_index = section_end_index

        return end_index

    def current_start_is(self, text):
        return check_start_for(text, self.curr_line)

    def current_end_is(self, text):
        return check_line_end_for(text, self.curr_line)

    def prev_end_is(self, text):
        return check_line_end_for(text, self.prev_line)

    @staticmethod
    def invert_team(team):
        if team == "p1":
            return "p2"
        else:
            return "p1"

def check_start_for(text, full_line):
    i = 0
    j = i + len(text)

    if full_line[i:j] == text:
        return True
    else:
        return False

def check_line_end_for(text, full_line):
    line_end_symbol_offset = -1
    j = line_end_symbol_offset
    i = j - len(text)

    if full_line[i:j] == text:
        return True
    else:
        return False