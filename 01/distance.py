import csv
import argparse

def load_data(file: str):
    first = []
    second = []

    with open(file) as fp:
        r = csv.reader(fp, delimiter=',')
        for row in r:
            first.append(int(row[0]))
            second.append(int(row[1]))

    first = sorted(first)
    second = sorted(second)

    return first, second

def first_part(file: str, test: bool = False):

    first, second = load_data(file)
    distance = 0

    for f, s in zip(first, second):
        distance += abs(s - f)
        if test:
            print(distance, f, s)
    print(distance)


def second_part(file: str, test: bool = False):

    first, second = load_data(file)
    unique_values = set(first)
    score_map = {}
    for value in unique_values:
        score_map[value] = second.count(value)

    if test:
        print(score_map)

    score = 0
    for entry in first:
        score += entry * score_map[entry]
        if test:
            print(score, entry, score_map[entry])

    print(score)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--test', dest='t', action='store_true', help='Run test version')
    args = parser.parse_args()

    if args.t:
        file = 'example.csv'
    else:
        file = 'lists.txt'
    print("first")
    first_part(file, args.t)
    print("second")
    second_part(file, args.t)
