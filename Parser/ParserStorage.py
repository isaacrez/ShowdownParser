
class ParserStorage:

    def __init__(self):
        self.reset()

    def reset(self):
        self.pokemon = {}
        self.pokemon_present = []
        self.species_to_teams = {}
        self.species_to_nickname = {}
        self.weather_set_by = ""
        self.last_move_by = ""

        # ex: WishWashFish directly hits BoomBoomMonkey (Uses nicknames)
        # damaged_by["BoomBoomMonkey"] = ["WishWashFish", "direct"]
        self.damaged_by = {}

        # ex: TuxBirb sets up Stealth Rocks onto p1's side (Uses nickname)
        # ex: hazards[p1]["Stealth Rocks"] = "TuxBirb"
        self.hazards = {"p1": {}, "p2": {}}

        self.current_pokes = {"p1": "", "p2": ""}

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
                              "minor sts src": {}}

    def add_nickname(self, species, nickname):
        self.species_to_nickname[species] = nickname

    def get_nickname(self, species):
        return self.species_to_nickname[species]

    def update_field(self, nickname):
        team = self.pokemon[nickname]["team"]
        self.pokemon[nickname]["minor sts src"] = {}
        self.damaged_by.pop(self.current_pokes[team], "")
        self.last_move_by = ""
        self.current_pokes[team] = nickname

    def update_hazards(self, setter, hazard):
        pass

    def update_damage(self, damaged, src):
        DAMAGE_TYPE = {
            "direct": "other",
            "Recoil": "other",
            "psn": "status",
            "brn": "status",
            "Hail": "weather",
            "Sandstorm": "weather",
            "confusion": "volatile status"
        }

        DMG_HAZARDS = ["Stealth Rock", "Spikes"]

        if src in DAMAGE_TYPE:

            if DAMAGE_TYPE[src] == "other":
                damage_src = self.other_field_pokemon(damaged)

            elif DAMAGE_TYPE[src] == "status":
                damage_src = self.pokemon[damaged]["major sts src"]

            elif DAMAGE_TYPE[src] == "weather":
                damage_src = self.weather_set_by

            else: # Volatile Status
                damage_src = self.pokemon[damaged]["minor sts src"]["confusion"]

        elif src in DMG_HAZARDS:
            team = self._team_from_field(damaged)
            damage_src = self.hazards[team][src]

        else:
            print("UNKNOWN DAMAGE SOURCE:", src)
            print("Assume the other guy's responsible!")
            damage_src = self.other_field_pokemon(damaged)

        self.damaged_by[damaged] = [damage_src]
        if src == "direct":
            self.damaged_by[damaged].append("direct")
        else:
            self.damaged_by[damaged].append("indirect")

    def other_field_pokemon(self, nickname):
        other_team = "p1"
        if self.current_pokes[other_team] == nickname:
            other_team = "p2"
        return self.current_pokes[other_team]

    def _team_from_field(self, nickname):
        for team in self.current_pokes:
            if self.current_pokes[team] == nickname:
                return team

    @staticmethod
    def _other_team(team):
        if team == "p1":
            return "p2"
        else:
            return "p1"
