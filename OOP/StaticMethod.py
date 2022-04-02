

class Employee:
    
    def __init__(self, name, salary, project_name):
        self.name = name
        self.salary = salary
        self.project_name = project_name
        
    @staticmethod
    def gather_requirement(project_name):
        if project_name == "ABC Project":
            requirement = ["Task_1", "Task_2", "Task_3"]
        else:
            requirement = ["Task_1"]
        return requirement

    @staticmethod
    def Say():
        return "Yup"
    
    # instance method 
    def work(self):
        # call static method from instance method
        requirement = self.gather_requirement(self.project_name)
        for task in requirement:
            print("Completed", task)
            
emp = Employee("Mohammad", 12000, "ABC Project")
emp.work()

print(Employee.Say())
