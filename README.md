# What does it do?
The Showdown Parser will take a Showdown Replay, and generate a CSV of Pokemon stats.

It acknowledges the following as Direct KOs:
- Direct Damage
- Perish Song

It acknowledges the following as Indirect KOs:
- Hazards
- Major status conditions (i.e. Poison)
- Minor status conditions (i.e. Confusion)
- Self-KOs (from recoil or as a move side-effect; awards kill to other Pokemon on the field)

This has been designed primarily as a tool to facilitate Draft League management.

# To use...
  1. Download a replay of the match you want tabulated from Showdown
  2. Rename the replay to "matchData.txt"
  3. Add this file to the folder containing "Main.py"
  4. Double click "Main.py" to run it
  5. Open "stats.csv"
  (Note: If stats.csv does NOT appear, please send your Replay.  The code likely encountered an error.)

# Limitations
  Currently has not been tested for any "minor" status conditions besides confusion.
  Curse and partial trapping chip are not included.
  Deaths due to damage from trading items are not included (i.e. trading a Sticky Barb / Toxic Orb.)
  
# Suggestions?
This was intended as a one-night project; it quickly became significantly more than that.  I plan to update this frequently as notice areas for improvement, but I cannot promise regular updates.
