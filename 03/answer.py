import argparse

def load_data(file: str) -> str:
    obj = ""
    with open(file) as fp:
        obj = fp.read()

    return obj

def first_part(file: str, do: bool = False, test: bool = False):
    data = load_data(file)

    ml = MulState(test, do)
    count = 0
    for char in data:
        count += ml.update_state(char)
    print(count)

class MulState:
    def __init__(self, test=False, do=False):
        self.state = "start"
        self.test = test

        self.do = do
        self.do_enabled = True

        self.first_num = ''
        self.second_num = ''

    def update_state(self, char: str):
        return_val = 0
        if self.test:
            print(f"Char: {char}, state = {self.state}, first = {self.first_num}, second = {self.second_num}")
        if char == 'd':
            self.state = 'd'
        elif self.state == 'd' and char == 'o':
            self.state = 'do'
        elif self.state == 'do' and char == 'n':
            self.state = 'don'
        elif self.state == 'do' and char == '(':
            self.state = 'do('
        elif self.state == 'do(' and char == ')':
            self.do_enabled = True
            self.state = ''
        elif self.state == 'don' and char == '\'':
            self.state = 'don\''
        elif self.state == "don'" and char == 't':
            self.state = 'dont'
        elif self.state == 'dont' and char == '(':
            self.state = 'dont('
        elif self.state == 'dont(' and char == ')':
            self.do_enabled = False
            self.state = ''
            self.reset_state()
        elif char == 'm':
            self.state = char
        elif self.state == 'm' and char == 'u':
            self.state = char
        elif self.state == 'u' and char == 'l':
            self.state = char
        elif self.state == 'l' and char == '(':
            self.state = char
        elif self.state == '(' and char.isdigit():
            self.first_num = char
            self.state = 'first'
        elif self.state == 'first' and char.isdigit():
            self.first_num += char
        elif self.state == 'first' and char == ',':
            self.state = ','
        elif self.state == ',' and char.isdigit():
            self.second_num = char
            self.state = 'second'
        elif self.state == 'second' and char.isdigit():
            self.second_num += char
        elif self.state == 'second' and char == ')':
            first = int(self.first_num)
            second = int(self.second_num)
            return_val = first * second
            self.reset_state()
        else:
            self.reset_state()

        if self.do:
            if self.do_enabled:
                return return_val
            return 0
        return return_val

    def reset_state(self):
        self.state = ''
        self.first_num = ''
        self.second_num = ''

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--test', dest='t', action='store_true', help='Run test version')
    parser.add_argument('-d', '--do', dest='d', action='store_true', help='Run do() enabled')
    args = parser.parse_args()

    if args.t:
        file = 'example.txt'
        if args.d:
            file = 'example_2.txt'
    else:
        file = 'input.txt'
    first_part(file, args.d, args.t)
