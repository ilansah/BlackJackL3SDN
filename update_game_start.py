#!/usr/bin/env python3
"""Script to update game start in main.py"""

# Read the file
with open(r"c:\Users\user\OneDrive\Ilan.sahraoui\École (CATHO)\L3_SDN\S1\logicielle\BlackJackL3SDN\src\main.py", 'r', encoding='utf-8') as f:
    content = f.read()

# Find and replace the game start section
old_start = """        if should_start:
            game.reset()
            game.state = GameState.INITIAL_DEAL
            game.deal_initial_cards()"""

new_start = """        if should_start:
            game.reset()
            game.state = GameState.INITIAL_DEAL
            # Utiliser le dealing multi-places si des mises sont placées sur plusieurs sièges
            if game.seat_bets:
                game.deal_initial_cards_multiseat()
            else:
                game.deal_initial_cards()"""

content = content.replace(old_start, new_start)

# Write back
with open(r"c:\Users\user\OneDrive\Ilan.sahraoui\École (CATHO)\L3_SDN\S1\logicielle\BlackJackL3SDN\src\main.py", 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated game start successfully!")
