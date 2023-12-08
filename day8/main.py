from math import lcm
import re


def get_num_required_steps(node, destination_check_func):
    current = node
    steps = 0
    while not destination_check_func(current):
        current = node_map[current][0 if instruction[steps % len(instruction)] == 'L' else 1]
        steps += 1
    return steps


LINE_REGEX = re.compile(r'(\w{3}) = \((\w{3}), (\w{3})')

with open('input') as f:
    lines = [l.strip() for l in f.readlines() if l.strip() != '']

instruction = lines[0]
node_map = {}
for l in lines[1:]:
    match = LINE_REGEX.search(l)
    node, left, right = match.groups()
    node_map[node] = (left, right)

print(f'Part 1: {get_num_required_steps("AAA", lambda n: n == "ZZZ")}')

required_steps = [get_num_required_steps(n, lambda n: n.endswith('Z')) for n in node_map if n.endswith('A')]
print(f'Part 2: {lcm(*required_steps)}')