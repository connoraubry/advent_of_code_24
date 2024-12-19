import argparse
from flask import Flask, render_template

app = Flask(__name__)

global_update = 0

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/update')
def get_update():
    global global_update
    global g
    g.step()
    global_update += 1
    return format_string()

@app.route('/backwards')
def go_backwards():
    global global_update
    global g
    g.step(-1)
    global_update -= 1
    return format_string()

@app.route('/until_line')
def until_line():
    global global_update
    global g
    g.step(1)
    global_update += 1
    while g.longest_line() < 10:
        g.step(1)
        global_update += 1

    return format_string()


def format_string():
    global global_update
    global g
    s = f'''
    test: {global_update}
    <br>

    <code>
    {g.save_string()}
    </code>
    '''
    return s

MAX_INT = 70 * 70 * 70

class Robot():
    def __init__(self, x: int, y: int, dx: int, dy: int):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy

    def __str__(self):
        return f"Robot(x={self.x}, y={self.y}, dx={self.dx}, dy={self.dy})"

    def get_final_position(self, moves: int, x_bound: int, y_bound: int):
        newX = (self.x + (self.dx * moves)) % x_bound
        newY = (self.y + (self.dy * moves)) % y_bound
        return newX, newY

    def update(self, x_bound: int, y_bound: int):
        self.x = (self.x + (self.dx)) % x_bound
        self.y = (self.y + (self.dy)) % y_bound

    def update_multiple(self, moves: int, x_bound: int, y_bound: int):
        self.x = (self.x + (self.dx * moves)) % x_bound
        self.y = (self.y + (self.dy * moves)) % y_bound

class Grid():
    def __init__(self, robots: [Robot], max_x: int, max_y: int):
        self.robots = robots
        self.max_x = max_x
        self.max_y = max_y

    def step(self, moves: int = 1):
        for robot in self.robots:
            robot.update_multiple(moves, self.max_x, self.max_y)

    def longest_line(self):
        graph = [['.' for _ in range(self.max_x)] for _ in range(self.max_y)]
        for r in self.robots:
            pastChar = graph[r.y][r.x]
            if pastChar != '.':
                graph[r.y][r.x] = str(int(pastChar) + 1)
            else:
                graph[r.y][r.x] = '1'

        longest = 0
        for line in graph:
            curr = 0
            for elem in line:
                if elem != '.':
                    curr += 1
                else:
                    curr = 0
                longest = max(longest, curr)

        return longest

    def print(self):
        graph = [['.' for _ in range(self.max_x)] for _ in range(self.max_y)]
        for r in self.robots:
            pastChar = graph[r.y][r.x]
            if pastChar != '.':
                graph[r.y][r.x] = str(int(pastChar) + 1)
            else:
                graph[r.y][r.x] = '1'

        for line in graph:
            for cha in line:
                print(cha, end="")

            print("\n")

    def save_string(self) -> str:
        graph = [['.' for _ in range(self.max_x)] for _ in range(self.max_y)]
        for r in self.robots:
            pastChar = graph[r.y][r.x]
            if pastChar != '.':
                graph[r.y][r.x] = str(int(pastChar) + 1)
            else:
                graph[r.y][r.x] = '1'

        final_string = ""
        for line in graph:
            final_string += f"{''.join(line)}\n"
        return final_string

    def save(self, output_file: str):
        graph = [['.' for _ in range(self.max_x)] for _ in range(self.max_y)]
        for r in self.robots:
            pastChar = graph[r.y][r.x]
            if pastChar != '.':
                graph[r.y][r.x] = str(int(pastChar) + 1)
            else:
                graph[r.y][r.x] = '1'
        with open(output_file, 'w') as fp:
            for line in graph:
                for cha in line:
                    fp.write(cha)
                    # print(cha, end="")
                fp.write("\n")

                # print("\n")


def load_data(file: str) -> list[Robot]:
    result = []
    with open(file, 'r') as fp:
        for line in fp.readlines():
            line = line.strip("\n")
            p, v = line.split(" ")
            x, y = p.split("=")[1].split(",")
            dx, dy = v.split("=")[1].split(",")
            r = Robot(int(x), int(y), int(dx), int(dy))
            result.append(r)
    return result

def first_part(robots: list[Robot], moves: int, dimension: tuple[int, int]):
    results = [0, 0, 0, 0]

    x_half = (dimension[0] - (dimension[0] % 2)) / 2
    y_half = (dimension[1] - (dimension[1] % 2)) / 2

    for r in robots:
        print(r)
        finalX, finalY = r.get_final_position(moves, dimension[0], dimension[1])
        if finalX < x_half:
            if finalY < y_half:
                results[0] += 1
            elif finalY > y_half:
                results[1] += 1
        elif finalX > x_half:
            if finalY < y_half:
                results[2] += 1
            elif finalY > y_half:
                results[3] += 1
    print(results)
    res = 1
    for q in results:
        res *= q
    print(res)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--test', dest='t', action='store_true', help='Run test version')
    parser.add_argument('-s', '--step', dest='s', action='store_true', help='Run step version')
    args = parser.parse_args()

    file = 'example.txt'
    if args.t:
        file = 'example.txt'
        moves = 100
        dimension = (11, 7)
    else:
        file = 'input.txt'
        moves = 100
        dimension = (101, 103)
    inputs = load_data(file)

    if args.s:
        g = Grid(inputs, max_x=dimension[0], max_y=dimension[1])
        app.run(debug=True)
    else:
        first_part(inputs, moves, dimension)
