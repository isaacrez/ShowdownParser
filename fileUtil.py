
class _CSVFileWriter:

    FILENAME = "INVALID"

    def __init__(self, data):
        self.data = data

        self.f = open(self.FILENAME, "w")
        self.writeHeader()
        self.populateData()
        self.f.close()

    def writeHeader(self):
        pass

    def populateData(self):
        pass

    def writeToFile(self, text: str):
        self.f.write(text)


class LineupFile(_CSVFileWriter):

    FILENAME = "lineup.csv"

    def writeHeader(self):
        self.writeToFile("Team,\tSpecies\n")

    def populateData(self):
        for player in self.data:
            for pokemon in self.data[player]:
                self.writeToFile(player + ",\t" + pokemon + "\n")


class StatsFile(_CSVFileWriter):

    FILENAME = "stats.csv"

    def writeHeader(self):
        self.writeToFile("Team,\tSpecies,\tKOs,\tDeaths\n")

    def populateData(self):
        for nickname in self.data:
            new_line = ""
            for i in range(0, 4):
                stat = self.data[nickname][i]
                new_line = new_line + str(stat) + ",\t"
            new_line = new_line[:-2] + "\n"
            self.writeToFile(new_line)
