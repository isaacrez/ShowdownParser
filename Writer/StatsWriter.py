
from Parser.Parser import ParserStorage

class StatsWriter:

    FILENAME = "stats.csv"

    def __init__(self, data: ParserStorage):
        self.data = data
        self.make_data_writable()

        self.f = open(self.FILENAME, "w")
        self.write_header()
        self.populate_data()
        self.f.close()

    def make_data_writable(self):
        self.writeable_data = []
        party_lineup = self.data.party_lineup

        for team in party_lineup:
            for species in party_lineup[team]:
                self.writeable_data.append([team, species])

        DEFAULT_EXTENSION = [0, 0, 0]
        for entry in self.writeable_data:

            species = entry[1]

            try:
                name = self.data.species_to_nickname[species]
                extension = self.data.pokemon[name][2:5]
            except KeyError:
                extension = DEFAULT_EXTENSION

            for value in extension:
                entry.append(value)

    def write_header(self):
        self.write_to_file("Team,\tSpecies,\tDirect KOs,\tPassive KOs,\tDeaths\n")

    def populate_data(self):
        line_length = len(self.writeable_data[0])

        for entry in self.writeable_data:
            new_line = ""
            for i in range(0, line_length):
                stat = entry[i]
                new_line = new_line + str(stat) + ",\t"
            new_line = new_line[:-2] + "\n"
            self.write_to_file(new_line)

    def write_to_file(self, text: str):
        self.f.write(text)


