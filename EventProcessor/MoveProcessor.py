
from EventProcessor.EventProcessor import EventProcessor

class MoveProcessor(EventProcessor):

    HAZARDS = [
        "Stealth Rock",
        "Toxic Spikes",
        "Spikes"
    ]

    def process(self):
        self.info.last_move_by = self.name
        self.process_if_setting_hazards()
        self.process_if_minor_status_move()

    def process_if_setting_hazards(self):
        for hazard in self.HAZARDS:
            if self.is_move(hazard):
                self.process_hazard_move(hazard)
                break

    def is_move(self, move):
        base_index = 12
        start_index = base_index + len(self.name)
        end_index = start_index + len(move)

        potential_move = self.curr_line[start_index:end_index]
        if potential_move == move:
            return True
        else:
            return False

    def process_hazard_move(self, hazard):
        other_team = self.util.invert_team(self.team)
        self.info.hazards[other_team][hazard] = self.name

    def process_if_minor_status_move(self):
        if self.is_move("Perish Song"):
            #TODO: Add handling for Perish Song
            pass
