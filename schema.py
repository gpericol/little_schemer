DEBUG = True

COMMANDS = [
    "car"
]

class Atom:
    def __init__(self, value):
        self.value = value
    
    def __repr__(self):
        return self.value
    
class CAR:
    def __init__(self, value):
        self.value = value

    def validate(self):
        if self.value is None:
            print("Error: CAR: None argument")
            exit(1)
        elif not isinstance(self.value, list):
            print("Error: CAR: argument must be a list")
            exit(1)
        elif len(self.value) == 0:
            print("Error: CAR: empty list")
            exit(1)
        
    def __repr__(self):
        return f"CAR({self.value})"
    

def debug(*args):
    if DEBUG:
        print(*args)

    
def tokenize(string):
    debug(f"Tokenizing: {string}")
    
    # if it's an atom, just return it
    if string.isalnum():
        debug(f"Atom: {string}")
        return Atom(string)
    
    # if it's not an atom, it's a list
    if not string[0] == "(" and not string[-1] == ")":
        print("Error: Invalid S-Expression")
        exit(1)
    
    # remove parethesis
    string = string[1:-1]

    # decide if it's a command
    first_element = string.split(" ")[0]
    if first_element in COMMANDS:
        debug(f"Command: {string}")
        if first_element == "car":
            return CAR(tokenize(" ".join(string.split(" ")[1:])))
    
    result_lst = []
    s_exp = ""
    i = 0
    
    while i < len(string):
        # a space is a separator
        if string[i] in " ":
            # only if the string is not empty, tokenize it
            if len(s_exp) > 0:
                debug(f"Tokenizing from space: {s_exp}")
                result_lst.append(tokenize(s_exp))
            s_exp = ""
            i += 1
        # it's an other list to parse, need to find the end of the list
        elif string[i] == "(":
            # take the "("
            s_exp += string[i]
            i += 1
            open = 1
            while open > 0:
                if string[i] == "(":
                    open += 1
                elif string[i] == ")":
                    open -= 1
                s_exp += string[i]
                i += 1
            debug(f"tokenizing from p: {s_exp}")
            result_lst.append(tokenize(s_exp))
            s_exp = ""
        else:
            # evaluating an atom
            s_exp += string[i]
            i += 1

    if len(s_exp) > 0:
        debug(f"tokenizing from end: {s_exp}")
        result_lst.append(tokenize(s_exp))

    return result_lst

def prompt():
    print("> ", end="")
    return input()
    
if __name__ == '__main__':
    #while True:
    #    value = prompt()
    #    print(tokenize(value))

    value = "(car (a a a))"
    print(value)
    print(tokenize(value))

