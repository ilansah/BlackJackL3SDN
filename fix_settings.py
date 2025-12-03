import re

# Read the file
with open(r"c:\Users\user\OneDrive\Ilan.sahraoui\École (CATHO)\L3_SDN\S1\logicielle\BlackJackL3SDN\src\main.py", 'r', encoding='utf-8') as f:
    content = f.read()

# Find and replace the corrupted section
# Pattern to match from line 538 to 543
old_pattern = r"    controls\.append\(\('button', 'reset_stats', reset_rect\)\)és\r?\n    prob_rect = pygame\.Rect\(x_center, y_start \+ y_spacing \* 2, control_width, control_height\)\r?\n    prob_on = config\.get\('features\.show_probabilities', False\)\r?\n    prob_hover = prob_rect\.collidepoint\(mouse_pos\)\r?\n    draw_toggle_button\(screen, prob_rect, prob_on, \"Probabilités\", prob_hover\)\r?\n    controls\.append\(\('toggle', 'features\.show_probabilities', prob_rect\)\)\r?\n"

new_text = """    controls.append(('button', 'reset_stats', reset_rect))
"""

content = re.sub(old_pattern, new_text, content)

# Write back
with open(r"c:\Users\user\OneDrive\Ilan.sahraoui\École (CATHO)\L3_SDN\S1\logicielle\BlackJackL3SDN\src\main.py", 'w', encoding='utf-8') as f:
    f.write(content)

print("File fixed successfully!")
