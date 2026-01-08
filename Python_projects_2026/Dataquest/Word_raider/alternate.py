import random
import numpy as np

name = "The Word Game"
max_turns = 5
turns_made = 0
common_random_selections = []
overlaps = []
words_per_game = random.randint(3, 6)


with open("words.txt", "r") as f:
    words = [w.strip() for w in f.read().split(",") if w.strip()]

first = random.choice(words)
common_random_selections.append(first)
words.remove(first)

while words_per_game > 0 and words:
    w = random.choice(words)
    common = set(w) & set(common_random_selections[-1])

    if common:
        common_random_selections.append(w)
        overlaps.append(list(common)[0])
        words.remove(w)
        words_per_game -= 1

print("Words for the game:", common_random_selections)
print("Overlaps:", overlaps)

max_word_len = max(len(w) for w in common_random_selections)


vertical = max_word_len * 2
horizontal = max_word_len * 2

grid = np.full((vertical, horizontal), ' ', dtype='<U1')

def can_place_h(word, r, c):
    return 0 <= c and c + len(word) <= grid.shape[1]

def can_place_v(word, r, c):
    return 0 <= r and r + len(word) <= grid.shape[0]

row = vertical // 2
col = (horizontal - len(common_random_selections[0])) // 2

for i, ch in enumerate(common_random_selections[0]):
    grid[row, col + i] = ch

current_row, current_col = row, col
current_dir = 'r'


for i, word in enumerate(common_random_selections[1:]):
    overlap_char = overlaps[i]

    prev_word = common_random_selections[i]
    prev_index = prev_word.index(overlap_char)
    curr_index = word.index(overlap_char)

    if current_dir == 'r': 
        cross_row = current_row
        cross_col = current_col + prev_index

        start_r = cross_row - curr_index
        start_c = cross_col

        if not can_place_v(word, start_r, start_c):
            continue

        for j, ch in enumerate(word):
            grid[start_r + j, start_c] = ch

        current_row = start_r
        current_col = start_c
        current_dir = 'c'

    else:
        cross_row = current_row + prev_index
        cross_col = current_col

        start_r = cross_row
        start_c = cross_col - curr_index

        if not can_place_h(word, start_r, start_c):
            continue

        for j, ch in enumerate(word):
            grid[start_r, start_c + j] = ch

        current_row = start_r
        current_col = start_c
        current_dir = 'r'

print("\nCROSSWORD GRID:\n")
for r in grid:
    print(" ".join(r))
