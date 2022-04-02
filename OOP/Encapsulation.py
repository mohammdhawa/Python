

class Member:
    
    def __init__(self, name, age, id):
        self.name = name    # Public
        self._age = age     # Protected
        self.__id = id      # Private
        
    def say(self):
        return f"Id: {self.__id}"

one = Member("Mohmmad", 23, 190290622)
print(one.name)
print(one._age)
print(one.say())

print(one._Member__id)
