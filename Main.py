from Parser import Parser
from Writer import StatsWriter

MATCH_FILENAME = "matchData.txt"

parser = Parser.Parser()
parser.start(MATCH_FILENAME)
writer = StatsWriter.StatsWriter(parser.get_data())


