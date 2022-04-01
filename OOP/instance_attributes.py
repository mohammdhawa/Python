class Dog:
    
    # class attribute
    attr1 = "mammal"
    
    # constructor
    def __init__(self, name):
        # intstance attribute
        self.name = name
        
    # instance attribute
    def sayHi(self):
        print("Hi")
        
tommy = Dog("Tommy")

# Access class attribute
print("Toommy is also a {}".format(tommy.__class__.attr1))

# Access instance attribute
print("My name is {}".format(tommy.name))
