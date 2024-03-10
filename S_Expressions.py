class Atom:
    def __init__(self, value):
        self.value = value

    def is_numeric(self):
        return self.value.isnumeric()
    
    def __repr__(self):
        return repr(f"Atom({self.value})")
    

class S_List():
    def __init__(self, items):
        self.items = items

    def __repr__(self):
        return f"{self.__class__.__name__}({self.items})"

    def execute(self):
        return S_List([item.execute() if hasattr(item, 'execute') else item for item in self.items])

class ListOperation:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"{self.__class__.__name__}({self.value})"
    
    def execute(self):
        executed_value = self.value.execute() if hasattr(self.value, 'execute') else self.value
        
        if not isinstance(executed_value, S_List):
            print(f"Error: {self.__class__.__name__}: argument must be a list")
            exit(1)

        return self.operation(executed_value)

class CAR(ListOperation):
    def operation(self, executed_value):
        return executed_value.items[0]

class CDR(ListOperation):
    def operation(self, executed_value):
        return S_List(executed_value.items[1:])
    
class CONS(ListOperation):
    def __init__(self, value1, value2):
        self.value1 = value1
        self.value2 = value2

    def __repr__(self):
        return f"{self.__class__.__name__}({self.value1}, {self.value2})"

    def execute(self):
        executed_value1 = self.value1.execute() if hasattr(self.value1, 'execute') else self.value1
        executed_value2 = self.value2.execute() if hasattr(self.value2, 'execute') else self.value2
        
        if not isinstance(executed_value2, S_List):
            print(f"Error: {self.__class__.__name__}: secondo argomento deve essere una lista")
            exit(1)
       
        new_items = [executed_value1] + executed_value2.items
        
        return S_List(new_items)
    
class NULL(ListOperation):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"NULL({self.value})"

    def execute(self):
        executed_value = self.value.execute() if hasattr(self.value, 'execute') else self.value

        if not isinstance(executed_value, S_List):
            print("Error: NULL: argument must be a list")
            exit(1)

        return len(executed_value.items) == 0


class IS_ATOM:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"IS_ATOM({self.value})"

    def execute(self):
        executed_value = self.value.execute() if hasattr(self.value, 'execute') else self.value

        return isinstance(executed_value, Atom)
    
class EQ:
    def __init__(self, value1, value2):
        self.value1 = value1
        self.value2 = value2

    def __repr__(self):
        return f"EQ({self.value1}, {self.value2})"

    def execute(self):
        executed_value1 = self.value1.execute() if hasattr(self.value1, 'execute') else self.value1
        executed_value2 = self.value2.execute() if hasattr(self.value2, 'execute') else self.value2

        if not isinstance(executed_value1, Atom) or not isinstance(executed_value2, Atom):
            print("Error: two parameters must be atoms")
            exit(1)
        
        # one or more atoms are numeric
        if executed_value1.is_numeric() or executed_value2.is_numeric():
            return False

        return executed_value1.value == executed_value2.value