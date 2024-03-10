from S_Expressions import *

DEBUG = False

COMMANDS = [
    "car",
    "cdr"
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
        elif first_element == "cdr":
            return CDR(tokenize(" ".join(string.split(" ")[1:])))
           
    result_lst = S_List()
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
    
if __name__ == '__main__':
    value = "(car (cdr (cdr (a b c))))"
    
    if not check_parenthesis(value):
        print("Error: Invalid S-Expression")
        exit(1)

    print(value)
    print(tokenize(value).execute())