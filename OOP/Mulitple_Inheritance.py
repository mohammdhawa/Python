# Base class 1
class Mother:
    
    motherName = ""
    
    def mother(self):
        print(self.motherName)
        
# Base class 2
class Father:
    
    fatherName = ""
    
    def father(self):
        print(self.fatherName)
        
# Derived class
class Son(Mother, Father):
    
    def Parents(self):
        print(f"Father: {self.fatherName}")
        print(f"Mother: {self.motherName}")
        
s1 = Son()
s1.fatherName = "Ned"
s1.motherName = "Katlen"

s1.Parents()
