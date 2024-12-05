import argparse
from collections import defaultdict
import sys

class PageTable():
    def __init__(self, verbose=False):
        self.depends_on = defaultdict(list)
        self.verbose = verbose

        self.updates = []

    def add_dependency(self, num: int, dependency: int):
        self.depends_on[num].append(dependency)

    def add_update(self, update: list[int]):
        self.updates.append(update)

    def get_valid_update_middles(self) -> int:
        count = 0
        for entry in self.updates:
            if self.is_update_valid(entry):
                middle = (len(entry) - (len(entry) % 2)) // 2
                count += entry[middle]
        return count

    def is_update_valid(self, update) -> bool:
        if self.verbose:
            print(f"Validating entry {update}")

        update_set = set(update)
        found_set: set[int] = set()
        for entry in update:
            if self.verbose:
                print(f"Testing entry: {entry} and dependencies: {self.depends_on[entry]}")
            dependencies = self.depends_on[entry]
            for dep in dependencies:
                if dep not in found_set and dep in update_set:
                    if self.verbose:
                        print(f"Dependency {dep} not found in {found_set}")
                    return False
            found_set.add(entry)
        return True

    def get_invalid_update_middles(self) -> int:
        count = 0
        for entry in self.updates:
            if self.is_update_valid(entry):
                continue

            new_update = self.make_update_valid(entry)
            middle = (len(new_update) - (len(new_update) % 2)) // 2
            count += new_update[middle]
        return count

    def make_update_valid(self, update: list[int]) -> list[int]:
        update_set = set(update)
        depends_on = {}

        new_update_list = []

        for entry in update_set:
            depends_on[entry] = set([x for x in self.depends_on[entry] if x in update_set])

        iters = 0
        while len(update_set) > 0:
            for entry in update_set:
                if len(depends_on[entry]) != 0:
                    continue
                new_update_list.append(entry)
                update_set.remove(entry)
                for inner_entry in update_set:
                    depends_on[inner_entry].remove(entry)
                break

            #don't want infinite loop
            iters += 1
            if iters > len(update) * 2:
                print("something went wrong")
                sys.exit(1)

        return new_update_list

def load_data(file: str) -> PageTable:
    pt = PageTable()

    state = "first"
    with open(file) as fp:
        for line in fp.readlines():
            line = line.strip("\n")
            if line == "":
                state = "second"
                continue

            if state == "first":
                first, second = line.split("|")
                pt.add_dependency(int(second), int(first))
            elif state == "second":
                update = [int(x) for x in line.split(",")]
                pt.add_update(update)
    return pt

def first_part(file: str, verbose: bool = False):
    update = load_data(file)
    update.verbose = verbose

    # print(xmas.horizontal_search_all())
    # print(xmas.vertical_search_all())
    # print(xmas.diagonal_search_all())
    print("First part:", update.get_valid_update_middles())


def second_part(file: str, verbose: bool = False):
    update = load_data(file)
    update.verbose = verbose

    print("Second part:", update.get_invalid_update_middles())

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--test', dest='t', action='store_true', help='Run test version')
    parser.add_argument('-v', '--verbose', dest='v', action='store_true', help='Verbose output')
    # parser.add_argument('-d', '--do', dest='d', action='store_true', help='Run do() enabled')
    args = parser.parse_args()

    if args.t:
        file = 'example.txt'
        # if args.d:
        #     file = 'example_2.txt'
    else:
        file = 'input.txt'
    first_part(file, args.v)
    second_part(file, args.v)
