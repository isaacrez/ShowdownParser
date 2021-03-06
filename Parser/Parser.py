
from EventProcessor import *
from Parser.ParserStorage import *

class Parser:

    curr_line = " "
    prev_line = " "
    info: ParserStorage = ParserStorage()

    POTENTIAL_EVENTS = {
        "|poke": PartyProcessor,
        "|-weather": WeatherProcessor,
        "|-start": StartProcessor,
        "|-fieldactivate": PerishSongProcessor,
        "|switch": SwitchProcessor,
        "|drag": SwitchProcessor,
        "|replace": SwitchProcessor,
        "|move": MoveProcessor,
        "|-damage": DamageProcessor,
        "|-sidestart": HazardProcessor,
        "|-status": StatusProcessor,
        "|faint": FaintProcessor
    }

    def start(self, filename):
        self.info.reset()
        self.curr_line = " "
        self.prev_line = " "

        try:
            self.f = open(filename)
            self._read_loop()
            self.f.close()
        except FileNotFoundError:
            print("ERROR: The following wasn't found...", filename)

    def _read_loop(self):
        while self.curr_line:
            self._update_line()
            self._parse_loop()
    
    def _parse_loop(self):
        for event in self.POTENTIAL_EVENTS:
            if self._is_event(event):
                self._use_processor(event)

    def _is_event(self, event):
        return self.curr_line.startswith(event)

    def _use_processor(self, event):
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
