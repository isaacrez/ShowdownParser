
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
        columns = ["team", "species", "direct KOs", "indirect KOs", "deaths"]
        self.writeable_data = []

        for species in self.data.pokemon_present:
            entry = []
            try:
                nickname = self.data.get_nickname(species)
                for col in columns:
                    entry.append(self.data.pokemon[nickname][col])
            except KeyError:
                team = self.data.species_to_teams[species]
                entry = [team, species, 0, 0, 0]

            self.writeable_data.append(entry)

    def write_header(self):
        self.write_to_file("Team,Species,Direct KOs,Passive KOs,Deaths\n")

    def populate_data(self):
        for entry in self.writeable_data:
            new_line = ",".join(map(str, entry)) + "\n"
            self.write_to_file(new_line)

    def write_to_file(self, text: str):
        self.f.write(text)


