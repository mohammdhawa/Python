
class GrandFather:
    
    def __init__(self, grandFatherName):
        self.granFatherName = grandFatherName
        
class Father(GrandFather):
    
    def __init__(self, fatherName, grandFatherName):
        super().__init__(grandFatherName)
        self.fatherName = fatherName
        
class Son(Father):
    
    def __init__(self, sonName, fatherName, grandFatherName):
        super().__init__(fatherName, grandFatherName)
        self.sonName = sonName
        
    def display(self):
        print(f"Grandfather Name: {self.granFatherName}")
        print(f"Father Name: {self.fatherName}")
        print(f"Son Name: {self.sonName}")
        

s1 = Son("Mohammad", "Enes", "Ahmed")
print(s1.granFatherName)
s1.display()
