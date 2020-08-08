
from EventProcessor.ProcessorUtil import ProcessorUtil
from Parser.ParserStorage import ParserStorage

class EventProcessor:

    def __init__(self, prev_line, curr_line, info: ParserStorage, event):
        self.prev_line = prev_line
        self.curr_line = curr_line
        self.info: ParserStorage = info
        self.util: ProcessorUtil = ProcessorUtil(prev_line, curr_line)

        self.event = event
        self.name = self.util.get_pokemon_name(event)
        self.team = self.util.get_pokemon_team(event)

    def check_if_event(self, event):
        input_len = len(event)
        potential_event = self.curr_line[:input_len]

        if potential_event == event:
            return True
        else:
            return False

    def process(self):
        pass
