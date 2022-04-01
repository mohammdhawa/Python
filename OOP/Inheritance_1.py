
# parent class
class Person:
    
    def __init__(self, name, id):
        self.name = name
        self.id = id
        
    def display(self):
        print(self.name)
        print(self.id)
        
    def details(self):
        print(f"My name is {self.name}")
        print(f"ID: {self.id}")


# child class      
class Employee(Person):
    
    def __init__(self, name, id, salary, post):
        # invoking the constructor of parent class
        super().__init__(name, id)
        
        self.salary = salary
        self.post = post
        
    def details(self):
        # invoking the details instance method
        super().details()
        print(f"Salary: {self.salary}")
        print(f"Post: {self.post}")
        
# creation of an object variables or an intance
a = Employee("Mohammad", 190290622, 5000, "Aleppo")

a.display()
print("*"*20)
a.details()
        
        
        
        
