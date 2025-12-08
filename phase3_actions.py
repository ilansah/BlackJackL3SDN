#!/usr/bin/env python3
"""Script to add _switch_to_next_seat helper and update player actions"""

# Read the file
with open(r"c:\Users\user\OneDrive\Ilan.sahraoui\École (CATHO)\L3_SDN\S1\logicielle\BlackJackL3SDN\src\core\game.py", 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find where to insert _switch_to_next_seat (before player_hit)
insert_index = None
for i, line in enumerate(lines):
    if 'def player_hit(self)' in line:
        insert_index = i
        break

if insert_index is None:
    print("Could not find player_hit!")
    exit(1)

# Add the helper method
helper_method = '''    def _switch_to_next_seat(self) -> None:
        """Passe à la place suivante dans le jeu multi-places."""
        self.current_seat_playing += 1
        if self.current_seat_playing >= len(self.active_seats):
            # Toutes les places ont été jouées, le croupier joue
            self.state = GameState.DEALER_REVEAL
    
'''

lines.insert(insert_index, helper_method)

# Now update player_hit
# Find player_hit method
content = ''.join(lines)

old_hit = """    def player_hit(self) -> None:
        \"\"\"Le joueur tire une carte.\"\"\"
        if not self.can_hit():
            return
        
        current_hand = self.hands[self.current_hand_index]
        current_hand.add_cards(self.deck.draw(1))
        self.last_action_time = self.frame_counter
        
        # Vérifier si la main a bust
        if current_hand.is_bust():
            self.hand_results[self.current_hand_index] = GameResult.DEALER_WIN
            # Passer à la main suivante ou terminer
            if not self.switch_to_next_hand():
                # Toutes les mains ont été jouées
                self.state = GameState.DEALER_REVEAL"""

new_hit = """    def player_hit(self) -> None:
        \"\"\"Le joueur tire une carte.\"\"\"
        if not self.can_hit():
            return
        
        # Multi-seat: utiliser la place active actuelle
        if self.active_seats:
            seat_idx = self.active_seats[self.current_seat_playing]
            current_hand = self.seat_hands[seat_idx]
            current_hand.add_cards(self.deck.draw(1))
            self.last_action_time = self.frame_counter
            
            # Vérifier si la main a bust
            if current_hand.is_bust():
                self.seat_results[seat_idx] = GameResult.DEALER_WIN
                # Passer à la place suivante
                self._switch_to_next_seat()
        else:
            # Fallback pour le mode single-seat
            current_hand = self.hands[self.current_hand_index]
            current_hand.add_cards(self.deck.draw(1))
            self.last_action_time = self.frame_counter
            
            # Vérifier si la main a bust
            if current_hand.is_bust():
                self.hand_results[self.current_hand_index] = GameResult.DEALER_WIN
                # Passer à la main suivante ou terminer
                if not self.switch_to_next_hand():
                    # Toutes les mains ont été jouées
                    self.state = GameState.DEALER_REVEAL"""

content = content.replace(old_hit, new_hit)

# Update player_stand
old_stand = """    def player_stand(self) -> None:
        \"\"\"Le joueur s'arrête et passe à la main suivante ou au croupier.\"\"\"
        if not self.can_stand():
            return
        
        # Passer à la main suivante ou au croupier
        if not self.switch_to_next_hand():
            # Toutes les mains ont été jouées, le croupier joue
            self.state = GameState.DEALER_REVEAL
        
        self.last_action_time = self.frame_counter"""

new_stand = """    def player_stand(self) -> None:
        \"\"\"Le joueur s'arrête et passe à la main suivante ou au croupier.\"\"\"
        if not self.can_stand():
            return
        
        # Multi-seat: passer à la place suivante
        if self.active_seats:
            self._switch_to_next_seat()
        else:
            # Fallback pour le mode single-seat
            # Passer à la main suivante ou au croupier
            if not self.switch_to_next_hand():
                # Toutes les mains ont été jouées, le croupier joue
                self.state = GameState.DEALER_REVEAL
        
        self.last_action_time = self.frame_counter"""

content = content.replace(old_stand, new_stand)

# Write back
with open(r"c:\Users\user\OneDrive\Ilan.sahraoui\École (CATHO)\L3_SDN\S1\logicielle\BlackJackL3SDN\src\core\game.py", 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated player actions for multi-seat!")
