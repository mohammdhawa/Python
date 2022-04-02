

class MyClass:
    
    # hidden member of myclass
    __hiddenVariable = 0
    
    def add(self, increment):
        self.__hiddenVariable += increment
        
    def display(self):
        print(self.__hiddenVariable)
        
myObj = MyClass()
myObj.add(2)
myObj.add(5)

myObj.display()

# to access to hidden member attribute
print(myObj._MyClass__hiddenVariable)
