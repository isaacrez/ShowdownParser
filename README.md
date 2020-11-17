# What does it do?
The Showdown Parser will take a Showdown Replay, and generate a CSV of Pokemon stats.
Stats include:
- Direct KOs
- Indirect KOs
- Deaths

Direct KOs are a result of direct damage; all other kills are considered indirect.

It acknowledges the following as Indirect KOs:
- Hazards
- Major status conditions (i.e. Poison)
- Minor status conditions (i.e. Confusion)
- Self-KOs (from recoil or as a move side-effect; awards kill to other Pokemon on the field)
- Weather (i.e. Hail)

This has been designed primarily as a tool to facilitate Draft League management.

# To use...
  1. Run "Main.py"
  2. Download a replay match from Showdown
  3. Right-click and "Copy" to get a local link to the match
  4. Paste the link into "Read From:" and click "Parse."  You're done!
  (Note: If stats.csv does NOT appear or tabulates incorrectly, please send your Replay.  The code likely encountered an error.)

# Limitations
 Only confusion has been tested as a "volatile" status condition (Curse has not been tested)
 Deaths from trapping move chip should work, but have not been tested (ex: Whirlpool, Magma Storm)
 Deaths from traded items have not been tested (ex: trading Sticky Barb / Toxic Orb.)
  
# Suggestions?
This was intended as a one-night project; it quickly became significantly more than that.  I plan to update this frequently as I notice areas for improvement, but I cannot promise regular updates.
