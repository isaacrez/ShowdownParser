
# TO USE:
# 1. Download the replay from Showdown
# 2. Rename the replay to "matchData.txt"
# 3. Add this file to the folder containing "main.py" (this file!)
# 4. Run it!

# LIMITATIONS:
# Should credit appropriately for the following...
#   - Direct KOs
#   - KOs resulting from hazards
#   - KOs resulting from status
#   - KOs resulting from status from hazards
#
# Does not credit correctly for the following...
#   - PERISH TRAPPING
#   - Other potential edge cases

class Scrubber:

    def __init__(self, filename='matchData.txt'):
        self.f = open(filename, 'r')
        self.current_line = ""

        # Stores information on the pokemon brought
        self.party_lineup = {"p1": [], "p2": []}
        self.party_count = 0

        # Stores detailed information on pokemon used
        # "nickname": [team_id, species, KOs, dead, status_source]
        self.pokemon = {}

        # Stores information on what Pokemon last set hazards
        # ex: hazards[p1]["stealth rocks"] = "Empoleon's nickname"
        self.hazards = {"p1": {}, "p2": {}}
        self.current_pokes = {"p1": "", "p2": ""}

        self.core_loop()
        self.f.close()

        WriteLogs(self.party_lineup, self.pokemon)

    def core_loop(self):
        self.update_line()
        while self.current_line:
            if self.party_count < 12:
                self.check_for_party()
            else:
                self.check_for_switch()
                self.check_for_hazards()
                self.check_for_status()
                self.check_for_faint()
            self.update_line()

    def update_line(self):
        self.previous_line = self.current_line
        self.current_line = self.f.readline()

    def check_for_party(self):
        if self.current_line[1:5] == "poke":
            self.party_count += 1

            team = self.current_line[6:8]
            pokemon = self.parse_party()
            self.party_lineup[team].append(pokemon)

    def parse_party(self):
        pokemon_name = self.get_pokemon_name(9)
        return pokemon_name

    def check_for_switch(self):
        if self.current_line[1:7] == "switch":
            offset = 8
        elif self.current_line[1:5] == "drag":
            offset = 6
        else:
            return

        self.last_move = ""
        team = self.current_line[offset:offset + 2]
        nickname, species = self.parse_switch(offset + 1)

        self.current_pokes[team] = nickname

        if nickname not in self.pokemon.keys():
            self.pokemon[nickname] = [team, species, 0, 0, ""]

    def parse_switch(self, offset):
        nickname_end = self.current_line.find("|", offset)
        nickname = self.current_line[offset + 4:nickname_end]

        species = self.get_pokemon_name(nickname_end+1)

        return nickname, species

    def check_for_faint(self):
        if self.current_line[1:6] == "faint":
            nickname = self.current_line[12:-1]
            self.pokemon[nickname][3] = 1

            print("\n" + nickname, "was knocked out!")

            team = self.current_line[7:9]

            if self.previous_line[-3:] == "psn":
                print("It was from status!")
                self.status_KO(nickname)
            elif self.previous_line[-12:] == "Stealth Rock":
                print("It was from Rocks!")
                self.hazards_KO(team, "Stealth Rock")
            elif self.previous_line[-6:] == "Spikes":
                print("It was from Spikes!")
                self.hazards_KO(team, "Spikes")
            else:
                print("It was from an attack!")
                self.direct_KO(team)

    def direct_KO(self, team_downed):
        team_responsible = self.invert_team(team_downed)
        killer = self.current_pokes[team_responsible]
        print(killer, "is responsible!")
        self.pokemon[killer][2] += 1

    def hazards_KO(self, team_downed, hazard):
        killer = self.hazards[team_downed][hazard]
        print(killer, "is responsible!")
        self.pokemon[killer][2] += 1

    def status_KO(self, poke_downed):
        killer = self.pokemon[poke_downed][4]
        print(killer, "is responsible!")
        self.pokemon[killer][2] += 1

    def check_for_hazards(self):
        if self.is_move():
            relevant_hazards = ["Stealth Rock", "Spikes", "Toxic Spikes"]
            for hazard in relevant_hazards:
                self.check_specific_hazard(hazard)

    def check_specific_hazard(self, hazard):
        FAILED = -1
        if self.current_line.find(hazard, 6) != FAILED:
            team = self.current_line[6:8]
            team = self.invert_team(team)
            pokemon_end = self.current_line.find("|", 11)
            pokemon = self.current_line[11:pokemon_end]

            self.hazards[team] = {hazard: pokemon}

    def check_for_status(self):
        if self.current_line[2:8] == "status":
            poke_name = self.get_pokemon_name(14)
            if self.last_move == "":
                # It was from hazards
                team = self.current_line[9:11]
                self.pokemon[poke_name][4] = self.hazards[team]["Toxic Spikes"]
            else:
                # It was from another Pokemon
                self.pokemon[poke_name][4] = self.last_move

    def is_move(self):
        if self.current_line[1:5] == "move":
            self.last_move = self.get_pokemon_name(11)
            return True

    def get_pokemon_name(self, offset):
        end_index = self.current_line.find(",", offset)

        FAILED = -1
        if end_index == FAILED:
            end_index = self.current_line.find("|", offset)
        name = self.current_line[offset:end_index]
        return name

    @staticmethod
    def invert_team(team):
        if team == "p1":
            return "p2"
        else:
            return "p1"


class WriteLogs:

    def __init__(self, lineup, statistics):
        f = open("lineup.csv", "w")
        f.write("Team,\tSpecies\n")
        for player in lineup:
            for pokemon in lineup[player]:
                new_line = player + ",\t" + pokemon + "\n"
                f.write(new_line)
        f.close()

        f = open("stats.csv", "w")
        f.write("Team,\tSpecies,\tKOs,\tDeaths\n")
        for nickname in statistics:
            new_line = ""
            for i in range(0,4):
                stat = statistics[nickname][i]
                new_line = new_line + str(stat) + ",\t"
            new_line = new_line[:-2] + "\n"
            f.write(new_line)
        f.close()


Scrubber()
