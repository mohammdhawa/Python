
class Bird:
    
    def intro(self):
        print("Ther are many types of birds.")
        
    def flight(self):
        print("Most of the birds can fly but som cannot.")
        
class Sparrow(Bird):
    
    def flight(self):
        print("Sparrows can fly.")
        
class Ostrich(Bird):
    
    def flight(self):
        print("Ostriches cannot fly.")
        
#####################################################

obj_bird = Bird()
obj_spr = Sparrow()
obj_ost = Ostrich()

obj_bird.intro()
obj_bird.flight()

print("#"*30)

obj_spr.intro()
obj_spr.flight()

print("#"*30)

obj_ost.intro()
obj_ost.flight()
        
        
        
