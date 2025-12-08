#!/usr/bin/env python3
"""Script to add deal_initial_cards_multiseat method"""

# Read the file
with open(r"c:\Users\user\OneDrive\Ilan.sahraoui\École (CATHO)\L3_SDN\S1\logicielle\BlackJackL3SDN\src\core\game.py", 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find the line after deal_initial_cards method ends
insert_index = None
for i, line in enumerate(lines):
    if line.strip() == "self.state = GameState.PLAYER_TURN" and i > 390:
        insert_index = i + 1
        break

if insert_index is None:
    print("Could not find insertion point!")
    exit(1)

# New method to insert
new_method = '''
    def deal_initial_cards_multiseat(self) -> None:
        """Distribue les 2 cartes initiales à toutes les places actives et au croupier."""
        # Identifier les places actives (celles avec des mises)
        self.active_seats = sorted([seat for seat, bet in self.seat_bets.items() if bet > 0])
        
        if not self.active_seats:
            return
        
        # Initialiser les mains pour chaque place active
        for seat_idx in self.active_seats:
            self.seat_hands[seat_idx] = Hand()
            self.seat_results[seat_idx] = None
        
        # Distribution alternée: 1 carte à chaque place, puis 1 au croupier, puis 2ème carte à chaque place, puis 2ème au croupier
        for seat_idx in self.active_seats:
            self.seat_hands[seat_idx].add_cards(self.deck.draw(1))
        
        self.dealer_hand.add_cards(self.deck.draw(1))
        
        for seat_idx in self.active_seats:
            self.seat_hands[seat_idx].add_cards(self.deck.draw(1))
        
        self.dealer_hand.add_cards(self.deck.draw(1))
        
        # Vérifier les blackjacks
        dealer_bj = self.dealer_hand.is_blackjack()
        
        # Vérifier chaque place pour les blackjacks
        all_done = True
        for seat_idx in self.active_seats:
            player_bj = self.seat_hands[seat_idx].is_blackjack()
            
            if player_bj and dealer_bj:
                self.seat_results[seat_idx] = GameResult.PUSH
            elif player_bj:
                self.seat_results[seat_idx] = GameResult.PLAYER_WIN
            elif dealer_bj:
                self.seat_results[seat_idx] = GameResult.DEALER_WIN
            else:
                all_done = False
        
        # Si tous ont des blackjacks ou le croupier a un blackjack, terminer
        if dealer_bj or all_done:
            self.state = GameState.RESULT_SCREEN
        else:
            # Commencer à jouer la première place
            self.current_seat_playing = 0
            self.state = GameState.PLAYER_TURN
'''

# Insert the new method
lines.insert(insert_index, new_method)

# Write back
with open(r"c:\Users\user\OneDrive\Ilan.sahraoui\École (CATHO)\L3_SDN\S1\logicielle\BlackJackL3SDN\src\core\game.py", 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("Added deal_initial_cards_multiseat() method successfully!")
