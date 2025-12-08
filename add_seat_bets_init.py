#!/usr/bin/env python3
"""Script to add seat_bets initialization"""

# Read the file
with open(r"c:\Users\user\OneDrive\Ilan.sahraoui\École (CATHO)\L3_SDN\S1\logicielle\BlackJackL3SDN\src\core\game.py", 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find the line with "# Insurance (assurance)" and insert before it
insert_index = None
for i, line in enumerate(lines):
    if '# Insurance (assurance)' in line and i > 60:
        insert_index = i
        break

if insert_index is None:
    print("Could not find insertion point!")
    exit(1)

# Insert the seat_bets initialization
new_lines = [
    "        # Multi-seat betting\n",
    "        self.seat_bets = {}  # Dict {seat_index: bet_amount}\n",
    "        self.current_seat_for_betting = 0  # Place actuellement sélectionnée pour miser\n",
    "        \n"
]

# Check if it's already there
if 'self.seat_bets' not in ''.join(lines[max(0, insert_index-10):insert_index]):
    for j, new_line in enumerate(new_lines):
        lines.insert(insert_index + j, new_line)
    print("Added seat_bets initialization!")
else:
    print("seat_bets already initialized!")

# Write back
with open(r"c:\Users\user\OneDrive\Ilan.sahraoui\École (CATHO)\L3_SDN\S1\logicielle\BlackJackL3SDN\src\core\game.py", 'w', encoding='utf-8') as f:
    f.writelines(lines)
