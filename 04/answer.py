import argparse

class StateMachine():
    def __init__(self):
        self.state = ''

    def update(self, new_state: str) -> int:
        return_val = 0
        if new_state == 'X':
            self.state = 'X'
        elif self.state == 'X' and new_state == 'M':
            self.state = 'M'
        elif self.state == 'M' and new_state == 'A':
            self.state = 'A'
        elif self.state == 'A' and new_state == 'S':
            self.state = ''
            return_val = 1
        else:
            self.state = ''

        return return_val

class XmasTable():
    def __init__(self, input: list[list[str]]):
        self.table = input

    def search_all(self) -> int:
        count = 0
        count += self.horizontal_search_all()
        count += self.vertical_search_all()
        count += self.diagonal_search_all()
        return count

    def horizontal_search_all(self) -> int:
        count = 0
        for line in self.table:
            count += self.horizontal_search(line)
        for line in self.table:
            count += self.horizontal_search_reverse(line)
        return count

    def vertical_search_all(self) -> int:
        count = 0
        states = [StateMachine() for _ in self.table[0]]
        for row in self.table:
            for letter, state in zip(row, states):
                count += state.update(letter)

        states = [StateMachine() for _ in self.table[0]]
        for row in self.table[::-1]:
            for letter, state in zip(row, states):
                count += state.update(letter)
        return count

    def diagonal_search_all(self) -> int:
        count = 0
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        for dir in directions:
            for start_x in range(len(self.table[0])):
                count += self.diagonal_generic((start_x, 0), dir)
                count += self.diagonal_generic((start_x, len(self.table) - 1), dir)
            for start_y in range(1, len(self.table) - 1):  #don't want to double count corners
                count += self.diagonal_generic((0, start_y), dir)
                count += self.diagonal_generic((len(self.table[0]) - 1, start_y), dir)

        return count

    def diagonal_generic(self, start: tuple[int, int], dir: tuple[int, int]) -> int:
        state = StateMachine()
        count = 0

        while self.in_bounds(start):
            count += state.update(self.table[start[1]][start[0]])
            start = (start[0] + dir[0], start[1] + dir[1])

        return count

    def search_x_mas(self) -> int:
        count = 0
        for y_idx, row in enumerate(self.table):
            for x_idx, char in enumerate(row):
                if char != 'A':
                    continue

                tl = (x_idx - 1, y_idx - 1)
                br = (x_idx + 1, y_idx + 1)
                if not self.in_bounds(tl) or not self.in_bounds(br):
                    continue
                top_left = self.get_value(tl)
                bottom_right = self.get_value(br)
                if not ((top_left == 'M' and bottom_right == 'S') or (top_left == 'S' and bottom_right == 'M')):
                    continue

                tr = (x_idx + 1, y_idx - 1)
                bl = (x_idx - 1, y_idx + 1)
                if not self.in_bounds(tr) or not self.in_bounds(bl):
                    continue
                top_right = self.get_value(tr)
                bottom_left = self.get_value(bl)
                if not ((top_right == 'M' and bottom_left == 'S') or (top_right == 'S' and bottom_left == 'M')):
                    continue
                count += 1
        return count

    def get_value(self, location: tuple[int, int]) -> str:
        return self.table[location[1]][location[0]]

    def in_bounds(self, loc: tuple[int, int]) -> bool:
        if loc[0] < 0 or loc[1] < 0 or loc[0] >= len(self.table[0]) or loc[1] >= len(self.table):
            return False
        return True

    @staticmethod
    def horizontal_search(line: list[str]) -> int:
        state = StateMachine()
        count = 0
        for letter in line:
            count += state.update(letter)
        return count

    @staticmethod
    def horizontal_search_reverse(line: list[str]) -> int:
        state = StateMachine()
        count = 0
        for letter in line[::-1]:
            count += state.update(letter)
        return count

def load_data(file: str) -> XmasTable:
    obj: list[list[str]] = []
    with open(file) as fp:
        obj = [[x for x in line.strip("\n")] for line in fp.readlines()]
    return XmasTable(input=obj)

def first_part(file: str, test: bool = False):
    xmas = load_data(file)

    # print(xmas.horizontal_search_all())
    # print(xmas.vertical_search_all())
    # print(xmas.diagonal_search_all())
    print("First part:", xmas.search_all())

def second_part(file: str, test: bool = False):
    xmas = load_data(file)
    print("Second part:", xmas.search_x_mas())

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--test', dest='t', action='store_true', help='Run test version')
    # parser.add_argument('-d', '--do', dest='d', action='store_true', help='Run do() enabled')
    args = parser.parse_args()

    if args.t:
        file = 'example.txt'
        # if args.d:
        #     file = 'example_2.txt'
    else:
        file = 'input.txt'
    first_part(file, args.t)
    second_part(file, args.t)
