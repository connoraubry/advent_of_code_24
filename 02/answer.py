import argparse

def load_data(file: str) -> list[list[int]]:
    all_nums = []
    with open(file) as fp:
        all_nums = [[int(x) for x in line.strip("\n").split()] for line in fp.readlines()]
    return all_nums

def first_part(file: str, test: bool = False):
    nums = load_data(file)

    count = 0
    for line in nums:
        if is_safe(line):
            count += 1
    print(f"first: {count}")

def second_part(file: str, test: bool = False):
    nums = load_data(file)
    count = 0
    for line in nums:
        if is_safe_2(line):
            count += 1
        else:
            if is_safe(line[1:]):
                count += 1
            else:
                if test:
                    print(line)
    print(f"second: {count}")

def is_safe(line: list[int]) -> bool:
    first = line[0]
    second = line[1]
    increasing = first < second

    past = first

    good = True

    for entry in line[1:]:

        diff = abs(entry - past)
        if diff > 3 or diff < 1:
            good = False
        if increasing:
            if entry < past:
                good = False
        else:
            if past < entry:
                good = False
        past = entry
    return good

def is_safe_2(line: list[int], test=False) -> bool:
    if test:
        print(f"testing {line}")
    increasing = 0
    decreasing = 0

    past = line[0]
    for entry in line[1:]:
        if entry > past:
            increasing += 1
        elif past > entry:
            decreasing += 1
        past = entry

    if increasing >= 2 and decreasing >= 2:
        return False

    is_increasing = True
    if decreasing > increasing:
        is_increasing = False

    if test:
        print(f"increasing?: {is_increasing}")

    strikes = 0
    past = line[0]
    for entry in line[1:]:
        if test:
            print(past, entry, abs(entry-past), strikes)
        diff = abs(entry - past)
        if diff > 3 or diff < 1:
            strikes += 1
            if strikes > 1:
                return False
            continue
        if is_increasing:
            if entry < past:
                strikes += 1
                if strikes > 1:
                    return False
                continue
        else:
            if past < entry:
                strikes += 1
                if strikes > 1:
                    return False
                continue
        past = entry
    return True

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--test', dest='t', action='store_true', help='Run test version')
    args = parser.parse_args()

    if args.t:
        file = 'example.txt'
    else:
        file = 'input.txt'
    first_part(file, args.t)
    second_part(file, args.t)
