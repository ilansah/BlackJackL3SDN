#!/usr/bin/env python3
"""Script to update _determine_winner for multi-seat"""

# Read the file
with open(r"c:\Users\user\OneDrive\Ilan.sahraoui\École (CATHO)\L3_SDN\S1\logicielle\BlackJackL3SDN\src\core\game.py", 'r', encoding='utf-8') as f:
    content = f.read()

# Find and replace _determine_winner
old_determine = """    def _determine_winner(self) -> None:
        \"\"\"Compare les mains et détermine le gagnant.\"\"\"
        dealer_value = self.dealer_hand.get_value()
        dealer_bust = dealer_value > 21
        
        # Si on a plusieurs mains (split), calculer le résultat pour chaque main
        if len(self.hands) > 1:
            for i, hand in enumerate(self.hands):
                if self.hand_results[i] is not None:
                    # Résultat déjà déterminé (bust)
                    continue
                
                player_value = hand.get_value()
                
                if dealer_bust:
                    self.hand_results[i] = GameResult.PLAYER_WIN
                elif player_value > dealer_value:
                    self.hand_results[i] = GameResult.PLAYER_WIN
                elif dealer_value > player_value:
                    self.hand_results[i] = GameResult.DEALER_WIN
                else:
                    self.hand_results[i] = GameResult.PUSH
            
            # Déterminer le résultat global (pour l'affichage)
            wins = sum(1 for r in self.hand_results if r == GameResult.PLAYER_WIN)
            losses = sum(1 for r in self.hand_results if r == GameResult.DEALER_WIN)
            if wins > losses:
                self.result = GameResult.PLAYER_WIN
            elif losses > wins:
                self.result = GameResult.DEALER_WIN
            else:
                self.result = GameResult.PUSH
        else:
            # Une seule main
            player_value = self.hands[0].get_value()
            
            if dealer_bust:
                self.result = GameResult.PLAYER_WIN
            elif player_value > 21:
                self.result = GameResult.DEALER_WIN
            elif player_value > dealer_value:
                self.result = GameResult.PLAYER_WIN
            elif dealer_value > player_value:
                self.result = GameResult.DEALER_WIN
            else:
                self.result = GameResult.PUSH
            
            self.hand_results[0] = self.result
        
        # Gérer l'assurance
        if self.has_insurance and self.dealer_hand.is_blackjack():
            # Le joueur gagne l'assurance (paiement 2:1)
            pass  # Sera géré dans le calcul des gains
        
        self.state = GameState.RESULT_SCREEN"""

new_determine = """    def _determine_winner(self) -> None:
        \"\"\"Compare les mains et détermine le gagnant.\"\"\"
        dealer_value = self.dealer_hand.get_value()
        dealer_bust = dealer_value > 21
        
        # Multi-seat: calculer le résultat pour chaque place active
        if self.active_seats:
            for seat_idx in self.active_seats:
                if self.seat_results[seat_idx] is not None:
                    # Résultat déjà déterminé (bust ou blackjack)
                    continue
                
                hand = self.seat_hands[seat_idx]
                player_value = hand.get_value()
                
                if dealer_bust:
                    self.seat_results[seat_idx] = GameResult.PLAYER_WIN
                elif player_value > dealer_value:
                    self.seat_results[seat_idx] = GameResult.PLAYER_WIN
                elif dealer_value > player_value:
                    self.seat_results[seat_idx] = GameResult.DEALER_WIN
                else:
                    self.seat_results[seat_idx] = GameResult.PUSH
            
            # Déterminer le résultat global
            wins = sum(1 for r in self.seat_results.values() if r == GameResult.PLAYER_WIN)
            losses = sum(1 for r in self.seat_results.values() if r == GameResult.DEALER_WIN)
            if wins > losses:
                self.result = GameResult.PLAYER_WIN
            elif losses > wins:
                self.result = GameResult.DEALER_WIN
            else:
                self.result = GameResult.PUSH
        elif len(self.hands) > 1:
            # Mode split (fallback)
            for i, hand in enumerate(self.hands):
                if self.hand_results[i] is not None:
                    continue
                player_value = hand.get_value()
                if dealer_bust:
                    self.hand_results[i] = GameResult.PLAYER_WIN
                elif player_value > dealer_value:
                    self.hand_results[i] = GameResult.PLAYER_WIN
                elif dealer_value > player_value:
                    self.hand_results[i] = GameResult.DEALER_WIN
                else:
                    self.hand_results[i] = GameResult.PUSH
            wins = sum(1 for r in self.hand_results if r == GameResult.PLAYER_WIN)
            losses = sum(1 for r in self.hand_results if r == GameResult.DEALER_WIN)
            if wins > losses:
                self.result = GameResult.PLAYER_WIN
            elif losses > wins:
                self.result = GameResult.DEALER_WIN
            else:
                self.result = GameResult.PUSH
        else:
            # Une seule main (fallback)
            player_value = self.hands[0].get_value()
            if dealer_bust:
                self.result = GameResult.PLAYER_WIN
            elif player_value > 21:
                self.result = GameResult.DEALER_WIN
            elif player_value > dealer_value:
                self.result = GameResult.PLAYER_WIN
            elif dealer_value > player_value:
                self.result = GameResult.DEALER_WIN
            else:
                self.result = GameResult.PUSH
            self.hand_results[0] = self.result
        
        # Gérer l'assurance
        if self.has_insurance and self.dealer_hand.is_blackjack():
            # Le joueur gagne l'assurance (paiement 2:1)
            pass  # Sera géré dans le calcul des gains
        
        self.state = GameState.RESULT_SCREEN"""

content = content.replace(old_determine, new_determine)

# Write back
with open(r"c:\Users\user\OneDrive\Ilan.sahraoui\École (CATHO)\L3_SDN\S1\logicielle\BlackJackL3SDN\src\core\game.py", 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated _determine_winner for multi-seat!")
