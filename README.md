# Blackjack Game

A complete Blackjack game in Python with Pygame, featuring player statistics and interactive gameplay.

## Quick Start

```bash
pip install pygame
python src/main.py
```

## Game Controls
- **H** - Hit (draw a card)
- **S** - Stand (end your turn)
- **D** - Double (double bet, draw 1 card)
- **P** - Split (split a pair)
- **SPACE** - New game
- **ESC** - Quit

## How to Play

1. Start the game - you and dealer get 2 cards each
2. Choose to **Hit** (draw), **Stand** (stop), **Double** (2x bet), or **Split** (split pair)
3. Dealer auto-plays (hits on 16 or less, stands on 17+)
4. Get closer to 21 than dealer to win
5. Press SPACE for next game - your stats auto-save

## Game Rules

- **Number cards (2-10)**: Face value
- **Face cards (J, Q, K)**: 10 points
- **Ace**: 11 (or 1 if you'd bust)
- **Win**: Closer to 21 than dealer without busting
- **Blackjack**: 21 with exactly 2 cards

## Features

✅ Full blackjack rules  
✅ Player statistics (auto-saved)  
✅ Interactive gameplay (H/S/D/P)  
✅ Automatic dealer play  
✅ Win rate and profit tracking  
✅ Animated card dealing  
✅ Color-coded feedback  

## Project Structure

```
src/
├── main.py              # Game UI and main loop
└── core/
    ├── card.py          # Card class
    ├── deck.py          # Deck management
    ├── hand.py          # Hand calculation
    ├── game.py          # Game logic
    └── player.py        # Stats tracking
```

## Statistics

Your stats are saved automatically to `player_stats.json`:
- Total hands played
- Wins / Losses / Ties
- Win percentage
- Net profit/loss
- Blackjack count

## Requirements

- Python 3.11+
- Pygame 2.x

## Card Images

Place card images in `assets/cards/` (optional - game works with placeholders if missing).

Expected filenames: `ace_of_spades.png`, `king_of_hearts.png`, etc.

## License

MIT License
