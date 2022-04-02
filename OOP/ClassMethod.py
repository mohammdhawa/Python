from datetime import date

class Person:
    
    def __init__(self, name, age):
        self.name = name
        self.age = age
        
    @classmethod
    def fromBirthYear(cls, name, birthYear):
        return cls(name, date.today().year-birthYear)
    
    def display(self):
        print(f"{self.name}'s age is: {str(self.age)}")
        
person = Person("Adam", 19)
person.display()

person1 = Person.fromBirthYear("Mohammad", 1999)
person1.display()
