
def check_start_for(text, full_line):
    i = 0
    j = i + len(text)

    if full_line[i:j] == text:
        return True
    else:
        return False

def check_line_end_for(text, full_line):
    line_end_symbol_offset = -1
    j = line_end_symbol_offset
    i = j - len(text)

    if full_line[i:j] == text:
        return True
    else:
        return False

def invert_teams(team):
    if team == "p1":
        return "p2"
    elif team == "p2":
        return "p1"
