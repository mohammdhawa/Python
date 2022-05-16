from ast import For
from contextlib import nullcontext
import datetime
from email.policy import default
from enum import unique
from pydoc import describe
from random import choices
from unicodedata import category
from xmlrpc.client import DateTime

from peewee import *

db = MySQLDatabase('my_library', user='root', password='toor',
                   host='localhost', port=3306)


class Category(Model):
    name = CharField(unique=True)
    
    class Meta:
        database = db


class Author(Model):
    name = CharField(unique=True)
    location = CharField(null=True)
    
    class Meta:
        database = db


class Publisher(Model):
    name = CharField(unique=True)
    location = CharField(null=True)
    
    class Meta:
        database = db


class Employee(Model):
    name = CharField()
    mail = CharField(unique=True)
    password = CharField()
    phone = CharField()
    date = DateTimeField(default=datetime.datetime.now)
    nationa_id = IntegerField(unique=True)
    
    class Meta:
        database = db

class Book(Model):
    title = CharField(unique=True)
    description = TextField(null=True)
    code = CharField(unique=True)
    category = ForeignKeyField(Category, backref='category', null=True)
    author = ForeignKeyField(Author, backref='author', null=True)
    publisher = ForeignKeyField(Publisher, backref='publisher', null=True)
    price = DecimalField()
    date = DateTimeField(default=datetime.datetime.now)
    
    class Meta:
        database = db

class Student(Model):
    name = CharField()
    student_id = IntegerField(unique=True)
    mail = CharField(unique=True)
    phone = CharField()
    department = CharField(null=True)
    date = DateTimeField(default=datetime.datetime.now)
    
    class Meta:
        database = db

Process_type = (
    (1, "Rent"),
    (2, "Retrieve"), 
    (3, "Sale")
)

class Daily_Movement(Model):
    book = ForeignKeyField(Book, backref='daily_book')
    student = ForeignKeyField(Student, backref='daily_Student')
    type = CharField(choices=Process_type)      # [Rent - Retrieve]
    date = DateTimeField(default=datetime.datetime.now)
    book_from = DateField(null=True)
    book_to = DateField(null=True)
    employee = ForeignKeyField(Employee, backref='daily_movement')
    
    class Meta:
        database = db

Action_type = (
    (1, 'Login'),
    (2, 'Update'), 
    (3, 'Create'),
    (4, 'Delete')
)

Table_type = (
    (1, "Book"),
    (2, "Student"),
    (3, "Employee"),
    (4, 'Category'),
    (5, "Daily Movement"),
    (6, "Publisher"),
    (7, "Author")
)

class History(Model):
    employee = ForeignKeyField(Employee, backref='history_employee')
    action = CharField(choices=Action_type)
    table = CharField(choices=Table_type)
    date = DateTimeField(default=datetime.datetime.now)
    data = CharField()
    
    class Meta:
        database = db

class Employee_Permissions(Model):
    employee_name = CharField()
    
    book_tab = IntegerField()
    student_tab = IntegerField()
    history_tab = IntegerField()
    report_tab = IntegerField()
    setting_tab = IntegerField()
    database_tab = IntegerField()
    
    add_category = IntegerField()
    add_author = IntegerField()
    add_publisher = IntegerField()
    add_employee = IntegerField()
    edit_employee = IntegerField()
    delete_employee = IntegerField()
    
    add_book = IntegerField()
    edit_book = IntegerField()
    delete_book = IntegerField()
    export_book = IntegerField()
    
    add_student = IntegerField()
    edit_student = IntegerField()
    delete_student= IntegerField()
    export_student = IntegerField()
    
    set_as_admin = IntegerField()
    
    class Meta:
        database = db



db.connect()
db.create_tables([Category, Publisher, Author, Book, Student, Employee, Daily_Movement, History, Employee_Permissions])