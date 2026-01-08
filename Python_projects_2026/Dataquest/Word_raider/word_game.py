import random
import numpy as np

name = 'The word game'
words = []
misplaced = []
incorrect = []
common_random_selections = []
overlaps = []

max_turns = 5
turns_made = 0
words_per_game = random.randint(3, 8)

with open('words.txt', 'r') as f:
    words = [w.strip() for w in f.read().split(',')]

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

direction = ['r', 'c']
selected_dir = random.choice(direction)
original_dir=selected_dir
horizontal_right = []
horizontal_left = []
vertical_up = []
vertical_down = []

for i, ch in enumerate(overlaps):
    next_word = common_random_selections[i + 1]
    pos = next_word.index(ch) + 1

    if selected_dir == 'r':
        horizontal_right.append(pos)
        horizontal_left.append(len(next_word) - pos)
        selected_dir = 'c'
    else:
        vertical_up.append(pos)
        vertical_down.append(len(next_word) - pos)
        selected_dir = 'r'

vertical = max(vertical_up, default=0) + max(vertical_down, default=0)
horizontal = max(horizontal_left, default=0) + max(horizontal_right, default=0)

max_word_len = max(len(w) for w in common_random_selections)

vertical = max(vertical, max_word_len + 2)
horizontal = max(horizontal, max_word_len + 2)


matrix = np.zeros((vertical, horizontal), dtype=int)
print(matrix)



print(f'Welcome to {name}, player!')

while max_turns:
    print(f'You have currently {max_turns-turns_made} turns left to guess')
    the_word=random.choice(common_random_selections)
    encrypt_word=the_word
    encrypt_word_len=random.choice([i for i in range(1, len(the_word)-(len(the_word)//2))])
    print(encrypt_word_len)
    for en in range(encrypt_word_len):        
        encrypt_word=encrypt_word.replace(f'{encrypt_word[en]}', '_')
    print(encrypt_word)
    print(f'Guess the following word: ' )
    the_guess=input('What is your guess?: ').lower()
    if the_guess.isalpha():
        if the_guess==the_word:
            print('Correct!!!')
        elif set(the_guess).intersection(the_word):
            matching_letters=[]
            for g in list(set(the_guess).intersection(the_word)):
                matching_letters.append(list(the_word).index(g))
            for m in matching_letters:
                the_guess.replace(the_guess[m], f'{the_word[m]}')
            print(the_guess)
    else:
        print('No numbers! Please retry.')
