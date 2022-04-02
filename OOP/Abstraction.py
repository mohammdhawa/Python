

# -ABC module in python provides infrastructure for defining custom Abstract Base classes

from abc import ABCMeta, abstractclassmethod


class Programming(metaclass=ABCMeta):  # Abstract class 
    
    @abstractclassmethod
    def has_OOP(self):
        pass

class Python(Programming):
    
    def has_OOP(self):
        return "Yes"
    
class Pascal(Programming):
    
    def has_OOP(self):
        return "No"
    
one = Python()
print(one.has_OOP())



