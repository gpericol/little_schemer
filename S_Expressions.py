class Atom:
    def __init__(self, value):
        self.value = value
    
    def __repr__(self):
        return repr(self.value)
    
    def execute(self):
        return self.value

class S_List(list):
    def execute(self):
        return S_List(item.execute() if hasattr(item, 'execute') else item for item in self)

class ListOperation:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"{self.__class__.__name__}({self.value})"
    
    def execute(self):
        executed_value = self.value.execute() if hasattr(self.value, 'execute') else self.value
        
        if not isinstance(executed_value, list):
            print(f"Error: {self.__class__.__name__}: argument must be a list")
            exit(1)

        return self.operation(executed_value)

class CAR(ListOperation):
    def operation(self, executed_value):
        return executed_value[0]

class CDR(ListOperation):
    def operation(self, executed_value):
        return executed_value[1:]
