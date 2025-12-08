#!/usr/bin/env python3
"""Script to update money processing for multi-seat"""

# Read the file
with open(r"c:\Users\user\OneDrive\Ilan.sahraoui\École (CATHO)\L3_SDN\S1\logicielle\BlackJackL3SDN\src\main.py", 'r', encoding='utf-8') as f:
    content = f.read()

# Find and replace money processing
old_money = """        if game.state == GameState.RESULT_SCREEN and not getattr(game, \"money_processed\", False):
            game.money_processed = True
            if game.has_surrendered: player.lose_hand(game.player_bet // 2)
            elif len(game.hands) > 1:
                for i, h in enumerate(game.hands):
                    res = game.hand_results[i]; bet = game.hand_bets[i]
                    if res == GameResult.PLAYER_WIN:
                        mult = 1.5 if h.is_blackjack() else 1.0
                        player.win_hand(int(bet * mult))
                    elif res == GameResult.DEALER_WIN: player.lose_hand(bet)
                    else: player.push_hand()
            else:
                res = game.result
                if res == GameResult.PLAYER_WIN:
                    mult = 1.5 if game.hands[0].is_blackjack() else 1.0
                    player.win_hand(int(game.hand_bets[0] * mult))
                elif res == GameResult.DEALER_WIN: player.lose_hand(game.hand_bets[0])
                else: player.push_hand()
            player.save()"""

new_money = """        if game.state == GameState.RESULT_SCREEN and not getattr(game, \"money_processed\", False):
            game.money_processed = True
            
            # Multi-seat: traiter chaque place active
            if game.active_seats:
                for seat_idx in game.active_seats:
                    res = game.seat_results[seat_idx]
                    bet = game.seat_bets[seat_idx]
                    hand = game.seat_hands[seat_idx]
                    
                    if res == GameResult.PLAYER_WIN:
                        mult = 1.5 if hand.is_blackjack() else 1.0
                        player.win_hand(int(bet * mult))
                    elif res == GameResult.DEALER_WIN:
                        player.lose_hand(bet)
                    else:
                        player.push_hand()
            elif game.has_surrendered:
                player.lose_hand(game.player_bet // 2)
            elif len(game.hands) > 1:
                for i, h in enumerate(game.hands):
                    res = game.hand_results[i]; bet = game.hand_bets[i]
                    if res == GameResult.PLAYER_WIN:
                        mult = 1.5 if h.is_blackjack() else 1.0
                        player.win_hand(int(bet * mult))
                    elif res == GameResult.DEALER_WIN: player.lose_hand(bet)
                    else: player.push_hand()
            else:
                res = game.result
                if res == GameResult.PLAYER_WIN:
                    mult = 1.5 if game.hands[0].is_blackjack() else 1.0
                    player.win_hand(int(game.hand_bets[0] * mult))
                elif res == GameResult.DEALER_WIN: player.lose_hand(game.hand_bets[0])
                else: player.push_hand()
            player.save()"""

content = content.replace(old_money, new_money)

# Write back
with open(r"c:\Users\user\OneDrive\Ilan.sahraoui\École (CATHO)\L3_SDN\S1\logicielle\BlackJackL3SDN\src\main.py", 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated money processing for multi-seat!")
