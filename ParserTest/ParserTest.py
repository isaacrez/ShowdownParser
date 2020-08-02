
import unittest
from ParserTest.TestUtil import *

class TestParserMethods(unittest.TestCase):

    DIRECT_KOs_ID = 2
    PASSIVE_KOs_ID = 3
    DEATHS_ID = 4

    def test_direct_KO(self):
        pokemon_data = {
            "Raichu-Alola": ["p1", "Stokin' Dude!"],
            "Magikarp": ["p2", "A Karp"]
        }

        simulator = ParserSimulator(pokemon_data)
        simulator.load_all()
        simulator.switch_in_all()
        simulator.move("Stokin' Dude!", "Thunderbolt", "A Karp")
        simulator.damage("A Karp")

    def test_toxic_spikes(self):
        pokemon_data = {
            "Toxapex": ["p1", "The Worst"],
            "Magikarp": ["p2", "Sushi Incarnate"],
            "Pichu": ["p2", "Baby Pikachu"]
        }

        simulator = ParserSimulator(pokemon_data)
        simulator.load_all()
        simulator.switch_in_species("Toxapex")
        simulator.switch_in_species("Magikarp")
        simulator.move("The Worst", "Toxic Spikes", "Sushi Incarnate")
        simulator.move("Sushi Incarnate", "Splash", "The Worst")
        simulator.switch_in_species("Pichu")
        simulator.damage("Baby Pikachu", "psn")
        simulator.faint("Baby Pikachu")

    def test_stealth_rocks(self):
        pass


if __name__ == '__main__':
    unittest.main()
