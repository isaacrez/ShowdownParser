
class ParserStorage:

    party_lineup = {"p1": [], "p2": []}
    species_to_nickname = {}
    last_move_by = ""

    # Stores detailed information on pokemon used
    # "nickname":
    #  0. [team_id,
    #  1. species,
    #  2. Direct KOs,
    #  3. Passive KOs,
    #  4. Deaths,
    #  5. Major Status Source,
    #  6. {Minor Status: Source}]
    pokemon = {}

    # Stores information on what Pokemon last set hazards
    # ex: hazards[p1]["stealth rocks"] = "Empoleon's nickname"
    hazards = {"p1": {}, "p2": {}}
    current_pokes = {"p1": "", "p2": ""}
