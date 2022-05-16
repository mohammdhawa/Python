


class Author:
    __name = ''
    __location = ''
    
    def Show_Authors(self):
        pass
    
    def Add_Author(self, name, location):
        pass

class Publisher:
    __name = ''
    __location = ''
    
    def Show_Publishers(self):
        pass
    
    def Add_Publisher(self, name, location):
        pass

class Category:
    __name = 'Hello'
    
    def Show_Categories(self):
        pass
    
    def Add_Cateogry(self, name):
        self.__name = name
    
    def show(self):
        print(self.__name)

class Reports:
    __day = 0
    __month = 0
    __year = 0
    
    def Daily_Reports(self):
        pass
    
    def Monthly_Reports(self):
        pass
    
    def Yearly_Reports(self):
        pass

class DataBase:
    ###### Composition Relation Between Reports and DataBase
    reports = Reports()
    
    def Show_Books(self, books):
        pass
    
    def Export_Books(self, books):
        pass
    
    def Show_Students(self, students):
        pass
    
    def Export_Students(self, students):
        pass
    
    def Show_Employees(self, employees):
        pass
    
    def Export_Employees(self, employees):
        pass
    
    ######## those needs some modifications
    def Show_Authors(self):
        pass
    
    def Export_Authors(self):
        pass
    
    def Show_Publishers(self):
        pass
    
    def Export_Publishers(self):
        pass

class Staff:
    __name = ''
    __mail = ''
    __national_id = ''
    __phone = ''
    __password = ''
    
    def Show(self):
        pass
    
    def Add(self, name, mail, national_id, phone, password):
        self.__name = name
        self.__mail = mail
        self.__national_id = national_id
        self.__phone = phone
        self.__password = password
    
    def Edit(self, name, mail, national_id, phone, password):
        self.__name = name
        self.__mail = mail
        self.__national_id = national_id
        self.__phone = phone
        self.__password = password
    
    def Delete(self):
        pass
    
    def Check(self):
        pass

class Librarian(Staff):
    
    def Add_Employee_Permissions(self):
        pass

class Employee(Staff):
    
    def Login(self):
        pass

class Students:
    __name = ''
    __mail = ''
    __student_id = ''
    __phone = ''
    __department = ''
    
    def Show_Students(self, database):
        pass
    
    def Add_Student(self, name, mail, student_id, phone, department):
        self.__name = name
        self.__mail = mail
        self.__student_id = student_id
        self.__phone = phone
        self.__department = department
    
    def Edit_Student(self, name, mail, student_id, phone, department):
        self.__name = name
        self.__mail = mail
        self.__student_id = student_id
        self.__phone = phone
        self.__department = department
    
    def Delete_Student(self):
        pass
    
    def Search(self):
        pass
    
    def Filter_Students(self):
        pass
    
    def Export_Students(self, database):
        pass

class Books:
    __title = ''
    __description = ''
    __code = ''
    __category = ''
    __author = ''
    __publisher = ''
    __price = ''
    
    ####### Coposition relation between Authors and Books
    authors = Author()
    ###### Composition relation between Publishers and Books
    publishers = Publisher()
    ###### Composition relation between Categories and Books
    categories = Category()

    def Show_Books(self, database):
        pass
    
    def Add_Book(self, title, description, code, category, author, publisher, price):
        self.__title = title
        self.__description = description
        self.__code = code
        self.__category = category
        self.__author = author
        self.__publisher = publisher
        self.__price = price
    
    def Edit_Book(self, title, description, code, category, author, publisher, price):
        self.__title = title
        self.__description = description
        self.__code = code
        self.__category = category
        self.__author = author
        self.__publisher = publisher
        self.__price = price
    
    def Delete_Book(self):
        pass
    
    def Export_Books(self database):
        pass

class LibraryManagementSystem:
    
    ###### Composition relation between Students and LMS
    students = Students()
    ###### Composition relation between Books and LMS
    books = Books()
    ###### Composition relation between Staff and LMS
    staff = Staff()
    
    def Login(self):
        pass
    
    def Logout(self):
        pass
