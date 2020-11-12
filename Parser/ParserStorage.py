
class ParserStorage:
    pokemon = {}
    pokemon_present = []
    species_to_teams = {}
    species_to_nickname = {}
    last_move_by = ""

    # Stores information on what Pokemon last set hazards
    # ex: hazards[p1]["stealth rocks"] = "Empoleon's nickname"
    hazards = {"p1": {}, "p2": {}}
    current_pokes = {"p1": "", "p2": ""}

    def update_lineup(self, pokemon, team):
        self.pokemon_present.append(pokemon)
        self.species_to_teams[pokemon] = team

    def initialize_pokemon(self, name, team, species):
        self.pokemon[name] = {"team": team,
                              "species": species,
                              "direct KOs": 0,
                              "indirect KOs": 0,
                              "deaths": 0,
                              "major sts src": "",
                              "minor sts src": ""}

    def add_nickname(self, species, nickname):
        self.species_to_nickname[species] = nickname

    def get_nickname(self, species):
        return self.species_to_nickname[species]

    def update_field(self, species):
        team = self.species_to_teams[species]
        nickname = self.get_nickname(species)
        self.current_pokes[team] = nickname

    def update_hazards(self, setter, hazard):
        pass

    def _team_of(self, pokemon):
        pass


