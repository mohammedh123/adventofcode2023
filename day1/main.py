import re


DIGIT_WORDS_TO_VALUE = {
    'one': 1,
    'two': 2,
    'three': 3,
    'four': 4,
    'five': 5,
    'six': 6,
    'seven': 7,
    'eight': 8,
    'nine': 9,
    '1': 1,
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5,
    '6': 6,
    '7': 7,
    '8': 8,
    '9': 9,
}

p1_result = 0
p2_result = 0

with open('input') as f:
    for l in f.readlines():
        l = l.strip()

        p1_digits = []
        for i, c in enumerate(l):
            if ord('0') <= ord(c) <= ord('9'):
                p1_digits.append(int(c))

        p1_result += int(str(p1_digits[0]) + str(p1_digits[-1]))

        p2_digits = []
        for digit, val in DIGIT_WORDS_TO_VALUE.items():
            for m in re.finditer(digit, l):
                p2_digits.append((m.start(), val))

        p2_digits.sort()
        p2_result += int(str(p2_digits[0][1]) + str(p2_digits[-1][1]))

print(f'Part 1: {p1_result}')
print(f'Part 2: {p2_result}')