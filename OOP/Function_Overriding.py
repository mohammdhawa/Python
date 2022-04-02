
class Animal:
    
    def Walk(self):
        print("HellO, I am the parent class")
        
class Dog(Animal):
    
    def Walk(self):
        print("Hello, I am the child class")
        
print("The method walk here is overridden in the code")

# invoking child class through object r

r = Dog();
r.Walk()

# invoking parent class through object r

r = Animal()
r.Walk()
