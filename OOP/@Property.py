

class Member:
    
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def sayHello(self):
        return f"Hello {self.name}"
    
    @property
    def age_in_days(self):
        return self.age*365
    

one = Member("Mohammad", 23)

print(one.name)
print(one.age)
print(one.sayHello())
print(one.age_in_days)


