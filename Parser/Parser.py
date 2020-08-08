
from EventProcessor.PartyProcessor import *
from EventProcessor.MoveProcessor import *
from EventProcessor.StatusProcessor import *
from EventProcessor.SwitchProcessor import *
from EventProcessor.FaintProcessor import *
from Parser.ParserStorage import *

class Parser:

    curr_line = " "
    prev_line = " "
    info: ParserStorage = ParserStorage()

    POTENTIAL_EVENTS = {
        "|poke": PartyProcessor,
        "|move": MoveProcessor,
        "|-status": StatusProcessor,
        "|switch": SwitchProcessor,
        "|drag": SwitchProcessor,
        "|faint": FaintProcessor
    }

    def start(self, filename):
        self.f = open(filename)
        self._read_loop()
        self.f.close()

    def _read_loop(self):
        while self.curr_line:
            self._update_line()
            self._parse_loop()
    
    def _parse_loop(self):
        for event in self.POTENTIAL_EVENTS:
            if self.is_event(event):
                self.use_processor(event)

    def is_event(self, event):
        end_index = len(event)
        possible_event = self.curr_line[:end_index]
        if event == possible_event:
            return True
        else:
            return False

    def use_processor(self, event):
        generator = self.POTENTIAL_EVENTS[event]
        processor = generator(self.prev_line, self.curr_line, self.info, event)
        processor.process()

    def _update_line(self):
        try:
            self.prev_line = self.curr_line
            self.curr_line = self.f.readline()
        except Exception as e:
            print("File reading error - this should be harmless.")
            print(e, "\n")

    def get_data(self) -> ParserStorage:
        return self.info
