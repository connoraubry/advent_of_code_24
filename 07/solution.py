import argparse

def load_data(file: str) -> list[tuple[int, list[int]]]:
    data = []
    with open(file, 'r') as fp:
        for line in fp.readlines():
            line = line.strip("\n")
            result, nums = line.split(":")
            num_list = nums.strip().split(" ")
            num_ints = [int(x) for x in num_list]
            data.append((int(result), num_ints))
    return data

def first_part(data: list[tuple[int, list[int]]]):
    total = 0
    for (result, numbers) in data:
        is_solve = solve_recursive(result, numbers)
        print(result, numbers, is_solve)
        if is_solve:
            total += result

    print(f"Sum: {total}")

def solve_recursive(result: int, numbers: list[int]) -> bool:
    if len(numbers) == 1:
        return numbers[0] == result
    operations = [
        numbers[0] + numbers[1],
        # numbers[0] - numbers[1],
        # numbers[0] / numbers[1],
        numbers[0] * numbers[1],
        int(str(numbers[0]) + str(numbers[1]))
    ]
    for op in operations:
        if solve_recursive(result, [op] + numbers[2:]):
            return True
    return False

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--test', dest='t', action='store_true', help='Run test version')
    args = parser.parse_args()

    if args.t:
        file = 'example.txt'
    else:
        file = 'input.txt'
    inputs = load_data(file)
    first_part(inputs)
