
class Skill:
    
    def __init__(self):
        self.skills = ["Html", 'Cass', "JS"]
    
    # Magic methods
    def __str__(self):
        return f"This is my skills => {self.skills}"
    
    def __len__(self):
        return len(self.skills)
        
    
profile = Skill()
print(profile)
print(len(profile))

profile.skills.append("PHP")
profile.skills.append("MySQL")

print(len(profile))
