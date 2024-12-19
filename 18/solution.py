import argparse
import heapq

MAX_INT = 70 * 70 * 70

def load_data(file: str) -> list[tuple[int, int]]:
    result = []
    with open(file, 'r') as fp:
        for line in fp.readlines():
            line = line.strip("\n")
            x, y = line.split(",")
            result.append((int(x), int(y)))
    return result

def first_part(inputs: list[tuple[int, int]], dimension: int, num_blockers: int):
    map = [[120341231 for _ in range(dimension + 1)] for _ in range(dimension + 1)]
    for byt in inputs[:num_blockers]:
        map[byt[1]][byt[0]] = -1
    print_map(map)

    path_length = get_min_path_length(map, dimension, num_blockers)
    print_map(map)
    print(f"First part: {path_length}")

def first_part_quiet(inputs: list[tuple[int, int]], dimension: int, num_blockers: int) -> int:
    map = [[MAX_INT for _ in range(dimension + 1)] for _ in range(dimension + 1)]
    for byt in inputs[:num_blockers]:
        map[byt[1]][byt[0]] = -1

    path_length = get_min_path_length(map, dimension, num_blockers)
    return path_length

def second_part(inputs: list[tuple[int, int]], dimension: int):
    #binary search for last open path
    l_bound = 0
    r_bound = len(inputs) - 1
    while l_bound < r_bound:
        half = (l_bound + r_bound) // 2
        res = first_part_quiet(inputs, dimension, half)
        if res == MAX_INT:
            r_bound = half - 1
        else:
            l_bound = half + 1

    res = first_part_quiet(inputs, dimension, l_bound)
    print(f"l bound: {l_bound} - {res}")
    print(f"coordinate: {inputs[l_bound]}")

def get_min_path_length(map: list[list[int]], dimension: int, num_blockers: int) -> int:
    heap = []
    heapq.heappush(heap, (calc_distance(0, 0, dimension), (0, 0)))
    map[0][0] = 0
    while len(heap) > 0:
        _, (currX, currY) = heapq.heappop(heap)
        score = map[currY][currX]
        directions = get_valid_directions(currX, currY, dimension)
        for (newX, newY) in directions:
            # if newX == dimension and newY == dimension:
            #     return score + 1
            if map[newY][newX] >= 0 and score + 1 < map[newY][newX]:
                map[newY][newX] = score + 1
                newCost = calc_distance(newX, newY, dimension)
                heapTuple = (newCost, (newX, newY))
                heapq.heappush(heap, heapTuple)
    return map[dimension][dimension]

def get_valid_directions(x: int, y: int, dimension: int) -> list[tuple[int, int]]:
    directions = []
    if x - 1 >= 0:
        directions.append((x - 1, y))
    if x + 1 <= dimension:
        directions.append((x + 1, y))
    if y - 1 >= 0:
        directions.append((x, y - 1))
    if y + 1 <= dimension:
        directions.append((x, y + 1))
    return directions

def calc_distance(x: int, y: int, dimension: int):
    return (dimension - x) + (dimension - y)

def print_map(map: list[list[int]]):
    for entry in map:
        print(entry)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--test', dest='t', action='store_true', help='Run test version')
    args = parser.parse_args()

    file = 'example.txt'
    dimension = 6
    count = 0
    if args.t:
        file = 'example.txt'
        dimension = 6
        count = 12
    else:
        file = 'input.txt'
        dimension = 70
        count = 1024
    inputs = load_data(file)

    first_part(inputs, dimension, count)
    second_part(inputs, dimension)
