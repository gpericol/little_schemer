from S_Expressions import *

DEBUG = False

COMMANDS = [
    "car",
    "cdr",
    "cons",
    "null?",
    "atom?",
    "eq?"
]    

def debug(*args):
    if DEBUG:
        print(*args)

def check_parenthesis(string):
    open = 0
    for c in string:
        if c == "(":
            open += 1
        elif c == ")":
            open -= 1
        if open < 0:
            return False
    return open == 0


def tokenize_parameters(string):
    parameters = []
    depth = 0
    start_index = 0

    for i, char in enumerate(string):
        if char == '(':
            depth += 1
        elif char == ')':
            depth -= 1
        elif char == ' ' and depth == 0:
            parameter = string[start_index:i].strip()
            if parameter:
                parameters.append(tokenize(parameter))
            start_index = i + 1

    # Add last parameter
    last_parameter = string[start_index:].strip()
    
    if last_parameter:
        parameters.append(tokenize(last_parameter))

    return parameters

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
        if first_element in COMMANDS:
            parameters = tokenize_parameters(" ".join(string.split(" ")[1:]))
            if first_element == "car":
                if len(parameters) != 1:
                    print("Error: car: takes only one argument")
                    exit(1)
                return CAR(parameters[0])
            elif first_element == "cdr":
                if len(parameters) != 1:
                    print("Error: cdr: takes only one argument")
                    exit(1)
                return CDR(parameters[0])
            elif first_element == "cons":
                if len(parameters) != 2:
                    print("Error: cdr: takes two arguments")
                    exit(1)
                return CONS(parameters[0], parameters[1])
            elif first_element == "null?":
                if len(parameters) != 1:
                    print("Error: null?: takes only one argument")
                    exit(1)
                return NULL(parameters[0])
            elif first_element == "atom?":
                if len(parameters) != 1:
                    print("Error: atom?: takes only one argument")
                    exit(1)
                return IS_ATOM(parameters[0])
            elif first_element == "eq?":
                if len(parameters) != 2:
                    print("Error: eq?: takes two arguments")
                    exit(1)
                return EQ(parameters[0], parameters[1])
           
    result_lst = S_List([])
    s_exp = ""
    i = 0
    
    while i < len(string):
        # a space is a separator
        if string[i] in " ":
            # only if the string is not empty, tokenize it
            if len(s_exp) > 0:
                debug(f"Tokenizing from space: {s_exp}")
                result_lst.items.append(tokenize(s_exp))
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
            result_lst.items.append(tokenize(s_exp))
            s_exp = ""
        else:
            # evaluating an atom
            s_exp += string[i]
            i += 1

    if len(s_exp) > 0:
        debug(f"tokenizing from end: {s_exp}")
        result_lst.items.append(tokenize(s_exp))

    return result_lst
    
if __name__ == '__main__':
    value = "(eq? (car (a a b)) (car (cdr (a a b))))"
    
    if not check_parenthesis(value):
        print("Error: Invalid S-Expression")
        exit(1)

    print(value)
    print(tokenize(value))
    print(tokenize(value).execute())