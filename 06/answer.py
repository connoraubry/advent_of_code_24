import argparse
from tqdm import tqdm

class Map():
    def __init__(self):
        self.map = []
        self.curr_pos = (-1, -1)
        self.num_change = 0
        self.direction = (0, -1)
        self.start_pos = (-1, -1)

    def print(self):
        for row in self.map:
            print(row)

    def reset(self):
        for ridx, row in enumerate(self.map):
            for cidx, char in enumerate(row):
                if char == '#':
                    continue
                self.map[ridx][cidx] = '.'
        self.map[self.start_pos[1]][self.start_pos[0]] = '^'
        self.curr_pos = self.start_pos
        self.num_change = 0
        self.direction = (0, -1)

    def has_loop(self) -> bool:
        maxIter = len(self.map) * len(self.map[1])
        count = 0

        while count < maxIter and self.in_bounds(self.curr_pos):
            count += 1
            if self.map[self.curr_pos[1]][self.curr_pos[0]] not in ['-', '|', '+']:
                count += 1
            self.update_curr_pos_on_map()
            next_pos = (self.curr_pos[0] + self.direction[0], self.curr_pos[1] + self.direction[1])
            if not self.in_bounds(next_pos):
                self.curr_pos = next_pos
                break
            # turn, will move on next loop
            if self.map[next_pos[1]][next_pos[0]] == '#':
                self.update_direction()
                continue
            self.curr_pos = next_pos
        return count >= maxIter

    def get_count(self):
        count = 0

        while self.in_bounds(self.curr_pos):
            if self.map[self.curr_pos[1]][self.curr_pos[0]] not in ['-', '|', '+']:
                count += 1
            self.update_curr_pos_on_map()
            next_pos = (self.curr_pos[0] + self.direction[0], self.curr_pos[1] + self.direction[1])
            if not self.in_bounds(next_pos):
                self.curr_pos = next_pos
                break
            # turn, will move on next loop
            if self.map[next_pos[1]][next_pos[0]] == '#':
                self.update_direction()
                continue
            self.curr_pos = next_pos
        return count

    def update_direction(self):
        if self.direction == (0, -1):
            self.direction = (1, 0)
        elif self.direction == (1, 0):
            self.direction = (0, 1)
        elif self.direction == (0, 1):
            self.direction = (-1, 0)
        elif self.direction == (-1, 0):
            self.direction = (0, -1)

    def in_bounds(self, pos):
        x, y = pos
        if x >= 0 and y >= 0 and x < len(self.map[0]) and y < len(self.map):
            return True
        return False

    def update_curr_pos_on_map(self):
        now = self.map[self.curr_pos[1]][self.curr_pos[0]]
        # if now == '+':
        #     return
        if now == '-':
            if self.direction[1] != 0:
                self.map[self.curr_pos[1]][self.curr_pos[0]] = '+'
        elif now == '|':
            if self.direction[0] != 0:
                self.map[self.curr_pos[1]][self.curr_pos[0]] = '+'
        else:
            if self.direction[0] != 0:
                self.map[self.curr_pos[1]][self.curr_pos[0]] = '-'
            else:
                self.map[self.curr_pos[1]][self.curr_pos[0]] = '|'


def load_data(file: str) -> Map:
    m = Map()
    with open(file) as fp:
        for y_idx, line in enumerate(fp.readlines()):
            line = line.strip("\n")
            m.map.append([x for x in line])

            x_pos = line.find("^")
            if x_pos != -1:
                m.curr_pos = (x_pos, y_idx)
                m.start_pos = (x_pos, y_idx)

    return m

def first_part(file: str, verbose: bool = False):
    update = load_data(file)
    print("First part:", update.get_count())
    if verbose:
        for row in update.map:
            print(row)

def second_part(file: str, verbose: bool = False):
    m = load_data(file)

    m2 = load_data(file)
    m2.get_count()

    count = 0
    for ridx in tqdm(range(len(m.map))):
        row = m.map[ridx]
        for cidx, char in enumerate(row):
            if char == '#' or char == '^':
                continue

            #check if it hits the path normall
            if m2.map[ridx][cidx] not in ['-', '|', '+']:
                continue

            m.map[ridx][cidx] = '#'

            if m.has_loop():
                count += 1

            m.map[ridx][cidx] = '.'
            m.reset()
            if verbose:
                print(f"Completed ({ridx}, {cidx})")
                m.print()
    print(f"Second part: {count}")


# def second_part(file: str, verbose: bool = False):
#     update = load_data(file)
#     update.verbose = verbose
#
#     print("Second part:", update.get_invalid_update_middles())

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
