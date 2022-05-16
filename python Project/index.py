from unicodedata import category
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.uic import loadUiType
import MySQLdb
import sys
import datetime
from xlsxwriter import *
from xlrd import *
from abc import ABC, abstractmethod

MainUI,_ = loadUiType('main.ui')

class Main(QMainWindow, MainUI):
    
    def __init__(self, parent=None):
        super(Main, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.UI_Changes()
        self.Handle_Buttons()
        self.DB_Connect()
        
        ######################
        self.Show_All_Categories()
        self.Show_All_Authors()
        self.Show_All_Publishers()
        self.Show_All_Books()
        self.Show_All_Students()
        self.Show_Employee()
        self.Show_All_Daily_Works()
        self.Show_History()
        
        ########## deneme
        # self.groupBox_11.setEnabled(True)
        # self.pushButton_6.setEnabled(True)
        # print(action[3])
        
        #################### DataBase 
        self.Show_Books_DataBase()
        self.Show_Students_DataBase()
        self.Show_Employees_DataBase()
        self.Show_Authors_DataBase()
        self.Show_Publishers_DataBase()
    
    
    #########################################################
    #### Connection between database and app
    def DB_Connect(self):
        self.db = MySQLdb.connect(host='localhost', user='root', password='toor', db='my_library')
        self.cur = self.db.cursor()
        print("Connection Accepted")
    #########################################################
    
    def UI_Changes(self):
        self.tabWidget.tabBar().setVisible(False)
    
    def Handle_Buttons(self):
        self.pushButton.clicked.connect(self.Open_Daily_Movement)
        self.pushButton_2.clicked.connect(self.Open_Books_Tab)
        self.pushButton_3.clicked.connect(self.Open_Students_Tab)
        self.pushButton_4.clicked.connect(self.Open_History_Tab)
        self.pushButton_5.clicked.connect(self.Open_Reports_Tab)
        self.pushButton_6.clicked.connect(self.Open_Settings_Tab)
        self.pushButton_7.clicked.connect(self.Open_Database_Tab)
        
        ################# Settings
        self.pushButton_25.clicked.connect(self.Add_Category)
        self.pushButton_26.clicked.connect(self.Add_Author)
        self.pushButton_27.clicked.connect(self.Add_Publisher)
        self.pushButton_22.clicked.connect(self.Add_Employee)
        self.pushButton_20.clicked.connect(self.Check_Employee)
        self.pushButton_23.clicked.connect(self.Edit_Employee_Data)
        self.pushButton_24.clicked.connect(self.Delete_Employee)
        self.pushButton_29.clicked.connect(self.Add_Employee_Permission)
        
        ############# Books 
        self.pushButton_9.clicked.connect(self.Add_New_Book)
        self.pushButton_10.clicked.connect(self.Book_Search)
        self.pushButton_11.clicked.connect(self.Edit_Book)
        self.pushButton_12.clicked.connect(self.Delete_Book)
        self.pushButton_8.clicked.connect(self.All_Books_Filter)
        self.pushButton_37.clicked.connect(self.Export_Books)
        
        ########### Students
        self.pushButton_14.clicked.connect(self.Add_New_Student)
        self.pushButton_15.clicked.connect(self.Search_Student)
        self.pushButton_16.clicked.connect(self.Edit_Student)
        self.pushButton_17.clicked.connect(self.Delete_Student)
        self.pushButton_13.clicked.connect(self.All_Students_Filter)
        self.pushButton_38.clicked.connect(self.Export_Students)
        
        ######### User Login
        self.pushButton_66.clicked.connect(self.User_Login_Permission)
        ######## User Logout
        self.pushButton_67.clicked.connect(self.Handle_Logout)
        
        
        self.pushButton_31.clicked.connect(self.Handle_Today_Work)
        
        ######## DataBase
        self.pushButton_36.clicked.connect(self.Export_Books_DataBase)
        self.pushButton_35.clicked.connect(self.Export_Students_DataBase)
        self.pushButton_34.clicked.connect(self.Export_Employees_DataBase)
        self.pushButton_33.clicked.connect(self.Export_Authors_DataBase)
        self.pushButton_32.clicked.connect(self.Export_Publishers_DataBase)
        
        self.pushButton_30.clicked.connect(self.Filter_History)
        
        ######## Reports
        self.pushButton_18.clicked.connect(self.Show_Books_Report)
    
    #################################################################
    ##### User Login 
    def Handle_Login(self):
        pass
    
    def Handle_Logout(self):
        self.Open_Login_Tab()
        self.groupBox_11.setEnabled(False)
        self.pushButton_67.setEnabled(False)
        # self.User_Login_Permission()
        
        ################## History
        sql = ''' INSERT INTO history(employee_id, operation_date, history_table, history_action) 
        VALUES (%s, %s, %s, %s) '''
        self.cur.execute(sql, (employee_id, datetime.datetime.now(), table[0], action[2]))
        self.db.commit()
        self.Show_History()
    
    def Handle_Reset_Password(self):
        pass
    
    def Show_All_Daily_Works(self):
        self.tableWidget_6.setRowCount(0)
        self.tableWidget_6.insertRow(0)
        
        self.cur.execute(''' SELECT book_id, type, student_id, book_from, book_to FROM daily_movement ''')
        data = self.cur.fetchall()
        
        for row, form in enumerate(data):
            for col, item in enumerate(form):
                self.tableWidget_6.setItem(row, col, QTableWidgetItem(str(item)))
                col += 1
            
            row_position = self.tableWidget_6.rowCount()
            self.tableWidget_6.insertRow(row_position)
    
    
    def Handle_Today_Work(self):
        book_title = self.lineEdit_37.text()
        student_id = self.lineEdit_52.text()
        operation_type = self.comboBox_13.currentText()
        date_from = datetime.date.today()
        dt = self.dateEdit_5.text()
        date = datetime.datetime.now()
        global employee_id
        
        #### to change date format
        dt1 = dt.replace('/', '-')
        month = dt1[:dt1.find('-')]
        if len(month)==1:
            month = '0'+month
        day = dt1[dt1.find('-')+1:dt1.find('-', 3)]
        if len(day)==1:
            day = '0'+day
        year = dt1[dt1.find('-', 3)+1:]
        date_to = f'{year}-{month}-{day}'
        # print(date_from, date_to) 
        #############################
        
        sql = ''' INSERT INTO daily_movement(book_id, student_id, type, 
        date, book_from, book_to, employee_id) Values (%s, %s, %s, %s, 
        %s, %s, %s) '''
        self.cur.execute(sql, (book_title, student_id, operation_type, 
                               date, date_from, date_to, employee_id))
        
        ################## History
        if operation_type == "Rent":
            act = action[6]
        elif operation_type == "Retreive":
            act = action[7]
        else:
            act = action[8]
        sql = ''' INSERT INTO history(employee_id, operation_date, history_table, history_action) 
        VALUES (%s, %s, %s, %s) '''
        self.cur.execute(sql, (employee_id, datetime.datetime.now(), table[8], act))
        self.Show_History()
        
        self.db.commit()
        
        self.statusBar().showMessage("Operation Added")
        self.Show_All_Daily_Works()
        
        self.lineEdit_37.clear()
        self.lineEdit_52.clear()
        self.comboBox_13.setCurrentIndex(0)
    
    def Retreive_Today_Work(self):
        pass
    
    def User_Login_Permission(self):
        username = self.lineEdit_88.text()
        password = self.lineEdit_87.text()
        
        self.cur.execute(''' SELECT national_id, name, password FROM employee ''')
        data = self.cur.fetchall()
        
        for row in data:
            if row[1] == username and row[2]==password:
                global employee_id
                employee_id = row[0]
                
                ###### Load user permissions
                self.groupBox_11.setEnabled(True)
                self.pushButton_67.setEnabled(True)
                
                self.cur.execute(''' 
                                 SELECT * FROM employee_permissions WHERE employee_name=%s 
                                 ''', [(username)])
                
                user_permissions = self.cur.fetchone()
                # print(user_permissions)
                if user_permissions[2] == 1:
                    self.pushButton_2.setEnabled(True)  # Book Tab
                if user_permissions[3] == 1:
                    self.pushButton_3.setEnabled(True)  # Student Tab
                if user_permissions[4] == 1:
                    self.pushButton_4.setEnabled(True)  # History Tab
                if user_permissions[5] == 1:
                    self.pushButton_5.setEnabled(True)  # Reports Tab
                if user_permissions[6] == 1:
                    self.pushButton_6.setEnabled(True)  # Settings Tab
                if user_permissions[7] == 1:
                    self.pushButton_7.setEnabled(True)  # Database Tab

                if user_permissions[8] == 1:
                    self.pushButton_25.setEnabled(True) # Add Category
                if user_permissions[9] == 1:
                    self.pushButton_26.setEnabled(True) # Add Author
                if user_permissions[10] == 1:
                    self.pushButton_27.setEnabled(True) # Add Publisher
                if user_permissions[11] == 1:
                    self.pushButton_22.setEnabled(True) # Add Employee
                if user_permissions[12] == 1:
                    self.pushButton_23.setEnabled(True) # Edit Employee
                if user_permissions[13] == 1:
                    self.pushButton_24.setEnabled(True) # Delete Employee
                
                if user_permissions[14] == 1:
                    self.pushButton_9.setEnabled(True)  # Add Book
                if user_permissions[15] == 1:
                    self.pushButton_11.setEnabled(True) # Edit Book
                if user_permissions[16] == 1:
                    self.pushButton_12.setEnabled(True) # Delete Book
                if user_permissions[17] == 1:
                    self.pushButton_37.setEnabled(True) # Export Book
                
                if user_permissions[18] == 1:
                    self.pushButton_14.setEnabled(True) # Add Student
                if user_permissions[19] == 1:
                    self.pushButton_16.setEnabled(True) # Edit Student
                if user_permissions[20] == 1:
                    self.pushButton_17.setEnabled(True) # Delete Student
                if user_permissions[21] == 1:
                    self.pushButton_38.setEnabled(True) # Export Student
                
                if user_permissions[22] == 1:
                    self.pushButton_29.setEnabled(True) # if Admin set Employee Permissions
                
                self.statusBar().showMessage("User Loged in")
                self.lineEdit_88.clear()
                self.lineEdit_87.clear()
                ################## History
                sql = ''' INSERT INTO history(employee_id, operation_date, history_table, history_action) 
                VALUES (%s, %s, %s, %s) '''
                self.cur.execute(sql, (employee_id, datetime.datetime.now(), table[0], action[1]))
                self.db.commit()
                self.Show_History()
        
        
        date = datetime.datetime.now()
        
        # sql = "INSERT INTO history(employee_id, table, action, date) VALUES (%s, %s, %s, %s)"
        # values = (employee_id, "ojsfd", "josjefd", date)
        # self.cur.execute(sql, values)
        # self.cur.close()
        # self.db.commit()
    
    ###############################################################
    ####### Books
    def Show_All_Books(self):
        self.tableWidget.setRowCount(0)
        self.tableWidget.insertRow(0)
        
        self.cur.execute(''' SELECT title, code, category_id, author_id, price FROM book ''')
        data = self.cur.fetchall()
        
        for row, form in enumerate(data):
            for col, item in enumerate(form):
                self.tableWidget.setItem(row, col, QTableWidgetItem(str(item)))
                col += 1
            
            row_position = self.tableWidget.rowCount()
            self.tableWidget.insertRow(row_position)
    
    def All_Books_Filter(self):
        category = self.comboBox.currentText()
        category_index = self.comboBox.currentIndex()
        
        if category_index == 0:
            sql = ''' SELECT title, code, category_id, author_id, price FROM book '''
            self.cur.execute(sql)
        else:
            sql = ''' SELECT title, code, category_id, author_id, price FROM book WHERE category_id=%s '''
            self.cur.execute(sql, [(category)])
        
        data = self.cur.fetchall()
        
        self.tableWidget.setRowCount(0)
        self.tableWidget.insertRow(0)
        
        for row, form, in enumerate(data):
            for col, item in enumerate(form):
                self.tableWidget.setItem(row, col, QTableWidgetItem(str(item)))
                col += 1
            
            row_position = self.tableWidget.rowCount()
            self.tableWidget.insertRow(row_position)
    
    def Add_New_Book(self):
        title = self.lineEdit.text()
        description = self.textEdit.toPlainText()
        code = self.lineEdit_2.text()
        category = self.comboBox_2.currentText()
        author = self.comboBox_3.currentText()
        publisher = self.comboBox_4.currentText()
        price = self.lineEdit_3.text()
        date = datetime.datetime.now()
        
        self.cur.execute('''
            INSERT INTO book(title, description, code, category_id, author_id, publisher_id, price, date)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ''', (title, description, code, category, author, publisher, price, date))
        
        # self.cur.execute('''
        #     INSERT INTO history(employee_id, date, table, action)
        #     VALUES (%s, %s, %s, %s)
        # ''', (employee_id, date, table[1], action[3]))
        
        sql = ''' INSERT INTO history(employee_id, operation_date, history_table, history_action) 
        VALUES (%s, %s, %s, %s) '''
        self.cur.execute(sql, (employee_id, date, table[1], action[3]))

        self.db.commit()
        self.statusBar().showMessage("Book Added")
        self.Show_All_Books()
        
        self.lineEdit.clear()
        self.textEdit.clear()
        self.lineEdit_2.clear()
        self.lineEdit_3.clear()
        self.comboBox_2.setCurrentIndex(0)
        self.comboBox_3.setCurrentIndex(0)
        self.comboBox_4.setCurrentIndex(0)
    
    def Book_Search(self):
        code = self.lineEdit_4.text()
        
        sql = ''' SELECT * FROM book WHERE  code=%s '''
        self.cur.execute(sql, [(code)])
        data = self.cur.fetchone()
        # print(data)
        
        self.lineEdit_5.setText(data[1])
        self.textEdit_2.setText(data[2])
        self.lineEdit_6.setText(str(data[3]))
        self.comboBox_5.setCurrentText(data[4])  
        self.comboBox_6.setCurrentText(data[5])
        self.comboBox_7.setCurrentText(data[6])
        self.lineEdit_7.setText(str(data[7]))
    
    def Edit_Book(self):
        title = self.lineEdit_5.text()
        description = self.textEdit_2.toPlainText()
        code = self.lineEdit_6.text()
        category = self.comboBox_5.currentText()
        author = self.comboBox_6.currentText()
        publisher = self.comboBox_7.currentText()
        price = self.lineEdit_7.text()
        prev_code = self.lineEdit_4.text()
        date = datetime.datetime.now()
        
        self.cur.execute(''' UPDATE book SET title=%s, description=%s, code=%s, category_id=%s, author_id=%s, publisher_id=%s, price=%s, date=%s WHERE code=%s 
                         ''', (title, description, code, category, author, publisher, price, date, prev_code))
        
        ################## History
        sql = ''' INSERT INTO history(employee_id, operation_date, history_table, history_action) 
        VALUES (%s, %s, %s, %s) '''
        self.cur.execute(sql, (employee_id, datetime.datetime.now(), table[1], action[4]))
        
        self.db.commit()
        self.statusBar().showMessage("Book Edited")
        self.Show_All_Books()
        self.Show_History()
        
        self.lineEdit_5.clear()
        self.textEdit_2.clear()
        self.lineEdit_6.clear()
        self.comboBox_5.setCurrentIndex(0)
        self.comboBox_6.setCurrentIndex(0)
        self.comboBox_7.setCurrentIndex(0)
        self.lineEdit_7.clear()
        self.lineEdit_4.clear()
    
    def Delete_Book(self):
        code = self.lineEdit_4.text()
        
        self.cur.execute(''' DELETE FROM book WHERE code=%s ''', [(code)])
        
        ################## History
        sql = ''' INSERT INTO history(employee_id, operation_date, history_table, history_action) 
        VALUES (%s, %s, %s, %s) '''
        self.cur.execute(sql, (employee_id, datetime.datetime.now(), table[1], action[5]))
        
        self.db.commit()
        self.statusBar().showMessage("Book has been deleted")
        self.Show_All_Books()
        self.Show_History()
        
        self.lineEdit_4.clear()
        self.lineEdit_5.clear()
        self.textEdit_2.clear()
        self.lineEdit_6.clear()
        self.comboBox_5.setCurrentIndex(0)
        self.comboBox_6.setCurrentIndex(0)
        self.comboBox_7.setCurrentIndex(0)
        self.lineEdit_7.clear()
    
    def Export_Books(self):
        
        sql = ''' SELECT code, title, category_id, author_id, publisher_id, price FROM book '''
        self.cur.execute(sql)
        data = self.cur.fetchall()
        
        excel_file = Workbook("books_report.xlsx")
        sheet1 = excel_file.add_worksheet()
        
        sheet1.write(0, 0, "Book Code")
        sheet1.write(0, 1, "Book Title")
        sheet1.write(0, 2, "Book Category")
        sheet1.write(0, 3, "Book Author")
        sheet1.write(0, 4, "Book Publisher")
        sheet1.write(0, 5, "Book Price")
        
        row_number = 1
        for row in data:
            col_number = 0
            for item in row:
                sheet1.write(row_number, col_number, str(item))
                col_number += 1
            row_number += 1
        
        excel_file.close()
        
        self.statusBar().showMessage("Book Report Exported Successfully")
    
    #########################################################
    #### Students
    def Show_All_Students(self):
        self.tableWidget_2.setRowCount(0)
        self.tableWidget_2.insertRow(0)
        
        self.cur.execute(''' 
                         SELECT name, student_id, phone, department, date FROM student 
                         ''')
        data = self.cur.fetchall()
        
        for row, form in enumerate(data):
            for col, item in enumerate(form):
                self.tableWidget_2.setItem(row, col, QTableWidgetItem(str(item)))
                col += 1
            
            row_position = self.tableWidget_2.rowCount()
            self.tableWidget_2.insertRow(row_position)
    
    def All_Students_Filter(self):
        src_data = self.lineEdit_8.text()
        idx = self.comboBox_8.currentIndex()
        
        if idx == 1:
            sql = ''' SELECT name, student_id, phone, department, date FROM student WHERE name=%s '''
            self.cur.execute(sql, [(src_data)])
        elif idx == 2:
            sql = ''' SELECT name, student_id, phone, department, date FROM student WHERE student_id=%s '''
            self.cur.execute(sql, [(src_data)])
        elif idx == 3:
            sql = ''' SELECT name, student_id, phone, department, date FROM student WHERE mail=%s '''
            self.cur.execute(sql, [(src_data)])
        elif idx == 4:
            sql = ''' SELECT name, student_id, phone, department, date FROM student WHERE phone=%s '''
            self.cur.execute(sql, [(src_data)])
        elif idx == 5:
            sql = ''' SELECT name, student_id, phone, department, date FROM student WHERE department=%s '''
            self.cur.execute(sql, [(src_data)])
        elif idx == 0:
            sql = ''' SELECT name, student_id, phone, department, date FROM student '''
            self.cur.execute(sql)
            self.lineEdit_8.clear()
        
        data = self.cur.fetchall()
        
        self.tableWidget_2.setRowCount(0)
        self.tableWidget_2.insertRow(0)
        
        for row, form in enumerate(data):
            for col, item in enumerate(form):
                self.tableWidget_2.setItem(row, col, QTableWidgetItem(str(item)))
                col += 1
            
            row_position = self.tableWidget_2.rowCount()
            self.tableWidget_2.insertRow(row_position)
            
    
    def Add_New_Student(self):
        name = self.lineEdit_9.text()
        mail = self.lineEdit_10.text()
        id = self.lineEdit_11.text()
        phone = self.lineEdit_12.text()
        department = self.lineEdit_25.text()
        date = datetime.datetime.now()
        
        self.cur.execute(''' 
                         INSERT INTO student(name, student_id, mail, phone, department, date)
                         VALUES (%s, %s, %s, %s, %s, %s) 
                         ''', (name, id, mail, phone, department, date))
        
        ################## History
        sql = ''' INSERT INTO history(employee_id, operation_date, history_table, history_action) 
        VALUES (%s, %s, %s, %s) '''
        self.cur.execute(sql, (employee_id, datetime.datetime.now(), table[2], action[3]))
        
        self.db.commit()
        self.statusBar().showMessage("Student Added")
        self.Show_All_Students()
        self.Show_History()
        
        self.lineEdit_9.clear()
        self.lineEdit_10.clear()
        self.lineEdit_11.clear()
        self.lineEdit_12.clear()
        self.lineEdit_25.clear()
    
    def Search_Student(self):
        src_data = self.lineEdit_13.text()
        idx = self.comboBox_9.currentIndex()
        
        if idx == 0:
            sql = (''' SELECT * FROM student WHERE name=%s ''')
            self.cur.execute(sql, [(src_data)])
        elif idx == 1:
            sql = (''' SELECT * FROM student WHERE student_id=%s ''')
            self.cur.execute(sql, [(src_data)])
        elif idx == 2:
            sql = (''' SELECT * FROM student WHERE mail=%s ''')
            self.cur.execute(sql, [(src_data)])
        elif idx == 3:
            sql = (''' SELECT * FROM student WHERE phone=%s ''')
            self.cur.execute(sql, [(src_data)])
        
        data = self.cur.fetchone()
        
        self.lineEdit_14.setText(data[1])
        self.lineEdit_15.setText(data[3])
        self.lineEdit_16.setText(str(data[2]))
        self.lineEdit_17.setText(data[4])
        self.lineEdit_24.setText(data[5])
    
    def Edit_Student(self):
        src_data = self.lineEdit_13.text()
        idx = self.comboBox_9.currentIndex()
        
        name = self.lineEdit_14.text()
        mail = self.lineEdit_15.text()
        id = self.lineEdit_16.text()
        phone = self.lineEdit_17.text()
        department = self.lineEdit_24.text()
        
        if idx == 0:
            self.cur.execute(''' 
                         UPDATE student SET name=%s, student_id=%s, mail=%s, phone=%s, department=%s WHERE name=%s 
                         ''', (name, id, mail, phone, department, src_data))
        elif idx == 1:
            self.cur.execute(''' 
                         UPDATE student SET name=%s, student_id=%s, mail=%s, phone=%s, department=%s WHERE student_id=%s 
                         ''', (name, id, mail, phone, department, src_data))
        elif idx == 2:
            self.cur.execute(''' 
                         UPDATE student SET name=%s, student_id=%s, mail=%s, phone=%s, department=%s WHERE mail=%s 
                         ''', (name, id, mail, phone, department, src_data))
        elif idx == 3:
            self.cur.execute(''' 
                         UPDATE student SET name=%s, student_id=%s, mail=%s, phone=%s, department=%s WHERE phone=%s 
                         ''', (name, id, mail, phone, department, src_data))
        
        ################## History
        sql = ''' INSERT INTO history(employee_id, operation_date, history_table, history_action) 
        VALUES (%s, %s, %s, %s) '''
        self.cur.execute(sql, (employee_id, datetime.datetime.now(), table[2], action[4]))
        
        self.db.commit()
        self.statusBar().showMessage("Student data has been Edited")
        self.Show_All_Students()
        self.Show_History()
        
        self.lineEdit_14.clear()
        self.lineEdit_15.clear()
        self.lineEdit_16.clear()
        self.lineEdit_17.clear()
        self.lineEdit_24.clear()
        
    
    def Delete_Student(self):
        src_data = self.lineEdit_13.text()
        idx = self.comboBox_9.currentIndex()
        
        if idx == 0:
            self.cur.execute(''' 
                         DELETE FROM student WHERE name=%s 
                         ''', [(src_data)])
        elif idx == 1:
            self.cur.execute(''' 
                          DELETE FROM student WHERE student_id=%s 
                         ''', [(src_data)])
        elif idx == 2:
            self.cur.execute(''' 
                          DELETE FROM student WHERE mail=%s 
                         ''', [(src_data)])
        elif idx == 3:
            self.cur.execute(''' 
                          DELETE FROM student WHERE phone=%s 
                         ''', [(src_data)])
        
        ################## History
        sql = ''' INSERT INTO history(employee_id, operation_date, history_table, history_action) 
        VALUES (%s, %s, %s, %s) '''
        self.cur.execute(sql, (employee_id, datetime.datetime.now(), table[2], action[5]))
        
        self.db.commit()
        self.statusBar().showMessage("Student data has been Deleted")
        self.Show_All_Students()
        self.Show_History()
        
        self.lineEdit_14.clear()
        self.lineEdit_15.clear()
        self.lineEdit_16.clear()
        self.lineEdit_17.clear()
        self.lineEdit_24.clear()
    
    def Export_Students(self):
        
        sql = ''' SELECT name, student_id, mail, phone, department FROM student '''
        self.cur.execute(sql)
        data = self.cur.fetchall()
        
        excel_file = Workbook("students_report.xlsx")
        sheet1 = excel_file.add_worksheet()
        
        sheet1.write(0, 0, "Student Name")
        sheet1.write(0, 1, "Student Id")
        sheet1.write(0, 2, "Student Mail")
        sheet1.write(0, 3, "Student Phone")
        sheet1.write(0, 4, "Student Department")
        
        row_number = 1
        for row in data:
            col_number = 0
            for item in row:
                sheet1.write(row_number, col_number, str(item))
                col_number += 1
            row_number += 1
        
        excel_file.close()
        
        self.statusBar().showMessage("Students Report Exported Successfully")
    
    #########################################################
    #### Tabs
    def Open_Login_Tab(self):
        self.tabWidget.setCurrentIndex(0)
        print("Login Tab")
    
    def Open_Daily_Movement(self):
        self.tabWidget.setCurrentIndex(1)
        print("Today Tab")
    
    def Open_Books_Tab(self):
        self.tabWidget.setCurrentIndex(2)
        self.tabWidget_2.setCurrentIndex(0)
        print("Books Tab")
    
    def Open_Students_Tab(self):
        self.tabWidget.setCurrentIndex(3)
        self.tabWidget_3.setCurrentIndex(0)
        print("Students Tab")
    
    def Open_History_Tab(self):
        self.tabWidget.setCurrentIndex(4)
        print("History Tab")
    
    def Open_Reports_Tab(self):
        self.tabWidget.setCurrentIndex(5)
        self.tabWidget_4.setCurrentIndex(0)
        print("Reports Tab")
    
    def Open_Settings_Tab(self):
        self.tabWidget.setCurrentIndex(6)
        self.tabWidget_5.setCurrentIndex(0)
        print("Settings Tab")
    
    def Open_Database_Tab(self):
        self.tabWidget.setCurrentIndex(7)
        self.tabWidget_6.setCurrentIndex(0)
        print("Database Tab")
    
    ########################################################
    ####### Settings
    def Add_Category(self):
        name = self.lineEdit_26.text()
        
        self.cur.execute(''' 
                         INSERT INTO category(name)
                         VALUES (%s) 
                         ''', [(name)])
        
        ################## History
        sql = ''' INSERT INTO history(employee_id, operation_date, history_table, history_action) 
        VALUES (%s, %s, %s, %s) '''
        self.cur.execute(sql, (employee_id, datetime.datetime.now(), table[4], action[3]))
        
        self.db.commit()
        self.statusBar().showMessage("Category Added")
        self.Show_All_Categories()
        self.Show_History()
        self.lineEdit_26.clear()
    
    def Add_Author(self):
        name = self.lineEdit_29.text()
        location = self.lineEdit_27.text()
        
        self.cur.execute(''' 
                         INSERT INTO author(name, location)
                         VALUES (%s, %s) 
                         ''', (name, location))
        
        ################## History
        sql = ''' INSERT INTO history(employee_id, operation_date, history_table, history_action) 
        VALUES (%s, %s, %s, %s) '''
        self.cur.execute(sql, (employee_id, datetime.datetime.now(), table[5], action[3]))
        
        self.db.commit()
        self.statusBar().showMessage("Author Added")
        self.Show_All_Authors()
        self.Show_History()
        self.lineEdit_29.clear()
        self.lineEdit_27.clear()
    
    def Add_Publisher(self):
        name = self.lineEdit_36.text()
        location = self.lineEdit_28.text()
        
        self.cur.execute(''' 
                         INSERT INTO publisher(name, location)
                         VALUES (%s, %s) 
                         ''', (name, location))
        
        ################## History
        sql = ''' INSERT INTO history(employee_id, operation_date, history_table, history_action) 
        VALUES (%s, %s, %s, %s) '''
        self.cur.execute(sql, (employee_id, datetime.datetime.now(), table[6], action[3]))
        
        self.db.commit()
        self.statusBar().showMessage("Publisher Added")
        self.Show_All_Publishers()
        self.Show_History()
        self.lineEdit_36.clear()
        self.lineEdit_28.clear()
    
    def Show_All_Categories(self):
        self.comboBox_10.clear()
        self.comboBox.clear()
        self.comboBox_2.clear()
        self.comboBox_5.clear()
        
        self.cur.execute(''' 
                         SELECT name FROM category 
                         ''')
        categories = self.cur.fetchall()
        # print(categories)
        self.comboBox.addItem("- - - - - - - - - ")
        for category in categories:
            self.comboBox_10.addItem(category[0])
            self.comboBox.addItem(category[0])
            self.comboBox_2.addItem(category[0])
            self.comboBox_5.addItem(category[0])
    
    def Show_All_Authors(self):
        self.comboBox_6.clear()
        self.comboBox_3.clear()
        
        self.cur.execute(''' 
                         SELECT name from author 
                         ''')
        authors = self.cur.fetchall()
        
        for author in authors:
            self.comboBox_6.addItem(author[0])
            self.comboBox_3.addItem(author[0])
    
    def Show_All_Publishers(self):
        self.comboBox_4.clear()
        self.comboBox_7.clear()
        
        self.cur.execute(''' 
                         SELECT name from publisher 
                         ''')
        publishers = self.cur.fetchall()
        
        for publisher in publishers:
            self.comboBox_4.addItem(publisher[0])
            self.comboBox_7.addItem(publisher[0])
    
    #######################################################
    ###### Employee
    def Show_Employee(self):
        self.comboBox_16.clear()
        self.comboBox_11.clear()
        self.cur.execute(''' 
                         SELECT name FROM employee 
                         ''')
        employees = self.cur.fetchall()
        
        self.comboBox_16.addItem("- - - - - - - -")
        for employee in employees:
            self.comboBox_11.addItem(employee[0])
            self.comboBox_16.addItem(employee[0])
    
    def Add_Employee(self):
        name = self.lineEdit_18.text()
        mail = self.lineEdit_19.text()
        id = self.lineEdit_20.text()
        phone = self.lineEdit_21.text()
        password = self.lineEdit_22.text()
        password2 = self.lineEdit_23.text()
        date = datetime.datetime.now()
        
        if password == password2:
            self.cur.execute(''' 
                         INSERT INTO employee(name, mail, password, phone, date, national_id)
                         VALUES (%s, %s, %s, %s, %s, %s) 
                         ''', (name, mail, password, phone, date, id))
            ################## History
            sql = ''' INSERT INTO history(employee_id, operation_date, history_table, history_action) 
            VALUES (%s, %s, %s, %s) '''
            self.cur.execute(sql, (employee_id, datetime.datetime.now(), table[7], action[3]))
            
            self.db.commit()
            self.statusBar().showMessage("Employee Added")
            self.Show_Employee()
            self.Show_History()
        else:
            self.statusBar().showMessage("Passwords do not match")
        self.lineEdit_18.clear()
        self.lineEdit_19.clear()
        self.lineEdit_20.clear()
        self.lineEdit_21.clear()
        self.lineEdit_22.clear()
        self.lineEdit_23.clear()
    
    def Check_Employee(self):
        name = self.lineEdit_30.text()
        password = self.lineEdit_34.text()
        
        self.cur.execute(''' SELECT * FROM employee ''')
        data = self.cur.fetchall()
        # print(data)
        for row in data:
            if row[1] == name and row[3] == password:
                self.groupBox_3.setEnabled(True)
                self.lineEdit_33.setText(row[4])
                self.lineEdit_32.setText(str(row[6]))
                self.lineEdit_31.setText(row[2])
                self.lineEdit_35.setText(row[3])
    
    def Edit_Employee_Data(self):
        name = self.lineEdit_30.text()
        mail = self.lineEdit_31.text()
        id = self.lineEdit_32.text()
        phone = self.lineEdit_33.text()
        password = self.lineEdit_35.text()
        date = datetime.datetime.now()
        
        self.cur.execute(''' 
                UPDATE employee SET mail=%s, password=%s, phone=%s, date=%s, national_id=%s WHERE name=%s 
            ''', (mail, password, phone, date, id, name))
        
        ################## History
        sql = ''' INSERT INTO history(employee_id, operation_date, history_table, history_action) 
        VALUES (%s, %s, %s, %s) '''
        self.cur.execute(sql, (employee_id, datetime.datetime.now(), table[7], action[4]))
        
        self.db.commit()
        self.Show_Employee()
        self.Show_History()
        self.statusBar().showMessage("Employee Edited")
        
        self.lineEdit_30.clear()
        self.lineEdit_31.clear()
        self.lineEdit_32.clear()
        self.lineEdit_33.clear()
        self.lineEdit_35.clear()
        self.lineEdit_34.clear()
    
    def Delete_Employee(self):
        name = self.lineEdit_30.text()
        password = self.lineEdit_34.text()
        
        sql = ''' DELETE FROM employee WHERE name=%s AND password=%s '''
        self.cur.execute(sql, (name, password))
        
        ################## History
        sql = ''' INSERT INTO history(employee_id, operation_date, history_table, history_action) 
        VALUES (%s, %s, %s, %s) '''
        self.cur.execute(sql, (employee_id, datetime.datetime.now(), table[7], action[5]))
        
        self.db.commit()
        self.statusBar().showMessage("Employee Deleted")
        self.Show_Employee()
        self.Show_History()
        
        self.lineEdit_30.clear()
        self.lineEdit_31.clear()
        self.lineEdit_32.clear()
        self.lineEdit_33.clear()
        self.lineEdit_35.clear()
        self.lineEdit_34.clear()
    
    def Add_Employee_Permission(self):
        employee_name = self.comboBox_11.currentText()
        books_tab = 0
        student_tab = 0
        history_tab = 0
        reports_tab = 0
        settings_tab = 0
        database_tab = 0
        
        add_category = 0
        add_author = 0
        add_publisher = 0
        add_employee = 0
        edit_employee = 0
        delete_employee = 0
        
        add_book = 0
        edit_book = 0
        delete_book = 0
        export_book = 0
        
        add_student = 0
        edit_student = 0
        delete_student = 0
        export_student = 0
        
        set_as_admin = 0
        
        if self.checkBox.isChecked() == True:
            books_tab = 1
        if self.checkBox_2.isChecked() == True:
            student_tab = 1
        if self.checkBox_3.isChecked() == True:
            history_tab = 1
        if self.checkBox_4.isChecked() == True:
            reports_tab = 1
        if self.checkBox_5.isChecked() == True:
            settings_tab = 1
        if self.checkBox_6.isChecked() == True:
            database_tab = 1
        
        if self.checkBox_15.isChecked() == True:
            add_category = 1
        if self.checkBox_16.isChecked() == True:
            add_author = 1
        if self.checkBox_17.isChecked() == True:
            add_publisher = 1
        if self.checkBox_18.isChecked() == True:
            add_employee = 1
        if self.checkBox_19.isChecked() == True:
            edit_employee = 1
        if self.checkBox_20.isChecked() == True:
            delete_employee = 1
        
        if self.checkBox_7.isChecked() == True:
            add_book = 1
        if self.checkBox_8.isChecked() == True:
            edit_book = 1
        if self.checkBox_9.isChecked() == True:
            delete_book = 1
        if self.checkBox_10.isChecked() == True:
            export_book = 1
        
        if self.checkBox_11.isChecked() == True:
            add_student = 1
        if self.checkBox_12.isChecked() == True:
            edit_student = 1
        if self.checkBox_13.isChecked() == True:
            delete_book = 1
        if self.checkBox_14.isChecked() == True:
            export_student = 1
        
        if self.checkBox_21.isChecked() == True:
            set_as_admin = 1
        
        self.cur.execute(''' 
                         INSERT INTO employee_permissions(employee_name, book_tab, student_tab, 
                         history_tab, report_tab, setting_tab, database_tab, add_category, add_author, 
                         add_publisher, add_employee, edit_employee, delete_employee, add_book, edit_book, 
                         delete_book, export_book, add_student, edit_student, delete_student, export_student, 
                         set_as_admin) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                         %s, %s, %s, %s, %s, %s) ''', (employee_name, books_tab, student_tab, history_tab, reports_tab, 
                                            settings_tab, database_tab, add_category, add_author, add_publisher, 
                                            add_employee, edit_employee, delete_employee, add_book, edit_book, 
                                            delete_book, export_book, add_student, edit_student, delete_student, 
                                            export_student, set_as_admin))
        self.db.commit()
        self.statusBar().showMessage("Employee Permissions Added")
    
    ################################################################
    ###### History
    def Show_History(self):
        self.tableWidget_5.setRowCount(0)
        self.tableWidget_5.insertRow(0)
        
        self.cur.execute(''' SELECT employee_id, history_action, history_table, operation_date FROM history ''')
        data = self.cur.fetchall()
        
        for row, form in enumerate(data):
            for col, item in enumerate(form):
                if col == 0:
                    self.cur.execute(''' SELECT name FROM employee WHERE national_id=%s ''', [(item)])
                    employee_name = self.cur.fetchone()
                    # print(employee_name)
                    self.tableWidget_5.setItem(row, col, QTableWidgetItem(str(employee_name[0])))
                else:
                    self.tableWidget_5.setItem(row, col, QTableWidgetItem(str(item)))
                col += 1
            
            row_position = self.tableWidget_5.rowCount()
            self.tableWidget_5.insertRow(row_position)
    
    def Filter_History(self):
        employee_name = self.comboBox_16.currentText()
        action_text = self.comboBox_12.currentText()
        table_text = self.comboBox_15.currentText()
        employee_idx = self.comboBox_16.currentIndex()
        action_idx = self.comboBox_12.currentIndex()
        table_idx = self.comboBox_15.currentIndex()
        
        if action_idx == 0:
            action_text = '- - - - - - -'
        if table_idx == 0:
            table_text = '- - - - - - -'
        if table_idx == 0 and action_idx == 0 and employee_idx == 0:
            sql = ''' SELECT employee_id, history_action, history_table, operation_date FROM history '''
            self.cur.execute(sql)
            
            self.tableWidget_5.setRowCount(0)
            self.tableWidget_5.insertRow(0)
        
            data = self.cur.fetchall()
        
            for row, form in enumerate(data):
                for col, item in enumerate(form):
                    if col == 0:
                        self.cur.execute(''' SELECT name FROM employee WHERE national_id=%s ''', [(item)])
                        employee_name = self.cur.fetchone()
                        # print(employee_name)
                        self.tableWidget_5.setItem(row, col, QTableWidgetItem(str(employee_name[0])))
                    else:
                        self.tableWidget_5.setItem(row, col, QTableWidgetItem(str(item)))
                    col += 1
            
                row_position = self.tableWidget_5.rowCount()
                self.tableWidget_5.insertRow(row_position)
        
        if employee_idx == 0:
            
            if action_idx == 0 and table_idx == 0:
                sql = ''' SELECT employee_id, history_action, history_table, operation_date FROM history '''
                self.cur.execute(sql)
            
                self.tableWidget_5.setRowCount(0)
                self.tableWidget_5.insertRow(0)
        
                data = self.cur.fetchall()
        
                for row, form in enumerate(data):
                    for col, item in enumerate(form):
                        if col == 0:
                            self.cur.execute(''' SELECT name FROM employee WHERE national_id=%s ''', [(item)])
                            employee_name = self.cur.fetchone()
                            # print(employee_name)
                            self.tableWidget_5.setItem(row, col, QTableWidgetItem(str(employee_name[0])))
                        else:
                            self.tableWidget_5.setItem(row, col, QTableWidgetItem(str(item)))
                        col += 1

                    row_position = self.tableWidget_5.rowCount()
                    self.tableWidget_5.insertRow(row_position)
            elif action_idx == 0 and table_idx != 0:
                sql = ''' SELECT employee_id, history_action, history_table, operation_date FROM history 
                WHERE history_table=%s '''
                self.cur.execute(sql, [(table_text)])

                self.tableWidget_5.setRowCount(0)
                self.tableWidget_5.insertRow(0)

                data = self.cur.fetchall()

                for row, form in enumerate(data):
                    for col, item in enumerate(form):
                        if col == 0:
                            self.cur.execute(''' SELECT name FROM employee WHERE national_id=%s ''', [(item)])
                            employee_name = self.cur.fetchone()
                            # print(employee_name)
                            self.tableWidget_5.setItem(row, col, QTableWidgetItem(str(employee_name[0])))
                        else:
                            self.tableWidget_5.setItem(row, col, QTableWidgetItem(str(item)))
                        col += 1

                    row_position = self.tableWidget_5.rowCount()
                    self.tableWidget_5.insertRow(row_position)
            elif action_idx != 0 and table_idx == 0:
                sql = ''' SELECT employee_id, history_action, history_table, operation_date FROM history 
                WHERE history_action=%s '''
                self.cur.execute(sql, [(action_text)])

                self.tableWidget_5.setRowCount(0)
                self.tableWidget_5.insertRow(0)
        
                data = self.cur.fetchall()

                for row, form in enumerate(data):
                    for col, item in enumerate(form):
                        if col == 0:
                            self.cur.execute(''' SELECT name FROM employee WHERE national_id=%s ''', [(item)])
                            employee_name = self.cur.fetchone()
                            # print(employee_name)
                            self.tableWidget_5.setItem(row, col, QTableWidgetItem(str(employee_name[0])))
                        else:
                            self.tableWidget_5.setItem(row, col, QTableWidgetItem(str(item)))
                        col += 1
                    
                    row_position = self.tableWidget_5.rowCount()
                    self.tableWidget_5.insertRow(row_position)
            elif action_idx !=0 and table_idx != 0:
                sql = ''' SELECT employee_id, history_action, history_table, operation_date FROM history 
                WHERE history_action=%s AND history_table=%s '''
                self.cur.execute(sql, (action_text, table_text))

                self.tableWidget_5.setRowCount(0)
                self.tableWidget_5.insertRow(0)

                data = self.cur.fetchall()

                for row, form in enumerate(data):
                    for col, item in enumerate(form):
                        if col == 0:
                            self.cur.execute(''' SELECT name FROM employee WHERE national_id=%s ''', [(item)])
                            employee_name = self.cur.fetchone()
                            # print(employee_name)
                            self.tableWidget_5.setItem(row, col, QTableWidgetItem(str(employee_name[0])))
                        else:
                            self.tableWidget_5.setItem(row, col, QTableWidgetItem(str(item)))
                        col += 1

                    row_position = self.tableWidget_5.rowCount()
                    self.tableWidget_5.insertRow(row_position)
            #######################################################################################
            # sql = ''' SELECT employee_id, history_action, history_table, operation_date FROM history 
            # WHERE history_table=%s AND history_action=%s '''
            # self.cur.execute(sql, (table_text, action_text))
            
            # self.tableWidget_5.setRowCount(0)
            # self.tableWidget_5.insertRow(0)
        
            # data = self.cur.fetchall()
        
            # for row, form in enumerate(data):
            #     for col, item in enumerate(form):
            #         if col == 0:
            #             self.cur.execute(''' SELECT name FROM employee WHERE national_id=%s ''', [(item)])
            #             employee_name = self.cur.fetchone()
            #             # print(employee_name)
            #             self.tableWidget_5.setItem(row, col, QTableWidgetItem(str(employee_name[0])))
            #         else:
            #             self.tableWidget_5.setItem(row, col, QTableWidgetItem(str(item)))
            #         col += 1
            
            #     row_position = self.tableWidget_5.rowCount()
            #     self.tableWidget_5.insertRow(row_position)
        elif employee_idx != 0:
            
            self.cur.execute(''' SELECT national_id FROM employee WHERE name=%s ''', [(employee_name)])
            dta = self.cur.fetchone()
            employee_national_id = dta[0]
            
            if action_idx == 0 and table_idx == 0:
                sql = ''' SELECT employee_id, history_action, history_table, operation_date FROM history 
                WHERE employee_id=%s '''
                self.cur.execute(sql, [(employee_national_id)])
            
                self.tableWidget_5.setRowCount(0)
                self.tableWidget_5.insertRow(0)
        
                data = self.cur.fetchall()
        
                for row, form in enumerate(data):
                    for col, item in enumerate(form):
                        if col == 0:
                            self.cur.execute(''' SELECT name FROM employee WHERE national_id=%s ''', [(item)])
                            employee_name = self.cur.fetchone()
                            # print(employee_name)
                            self.tableWidget_5.setItem(row, col, QTableWidgetItem(str(employee_name[0])))
                        else:
                            self.tableWidget_5.setItem(row, col, QTableWidgetItem(str(item)))
                        col += 1

                    row_position = self.tableWidget_5.rowCount()
                    self.tableWidget_5.insertRow(row_position)
            elif action_idx == 0 and table_idx != 0:
                sql = ''' SELECT employee_id, history_action, history_table, operation_date FROM history 
                WHERE history_table=%s AND employee_id=%s '''
                self.cur.execute(sql, (table_text, employee_national_id))

                self.tableWidget_5.setRowCount(0)
                self.tableWidget_5.insertRow(0)

                data = self.cur.fetchall()

                for row, form in enumerate(data):
                    for col, item in enumerate(form):
                        if col == 0:
                            self.cur.execute(''' SELECT name FROM employee WHERE national_id=%s ''', [(item)])
                            employee_name = self.cur.fetchone()
                            # print(employee_name)
                            self.tableWidget_5.setItem(row, col, QTableWidgetItem(str(employee_name[0])))
                        else:
                            self.tableWidget_5.setItem(row, col, QTableWidgetItem(str(item)))
                        col += 1

                    row_position = self.tableWidget_5.rowCount()
                    self.tableWidget_5.insertRow(row_position)
            elif action_idx != 0 and table_idx == 0:
                sql = ''' SELECT employee_id, history_action, history_table, operation_date FROM history 
                WHERE history_action=%s AND employee_id=%s '''
                self.cur.execute(sql, (action_text, employee_national_id))

                self.tableWidget_5.setRowCount(0)
                self.tableWidget_5.insertRow(0)
        
                data = self.cur.fetchall()

                for row, form in enumerate(data):
                    for col, item in enumerate(form):
                        if col == 0:
                            self.cur.execute(''' SELECT name FROM employee WHERE national_id=%s ''', [(item)])
                            employee_name = self.cur.fetchone()
                            # print(employee_name)
                            self.tableWidget_5.setItem(row, col, QTableWidgetItem(str(employee_name[0])))
                        else:
                            self.tableWidget_5.setItem(row, col, QTableWidgetItem(str(item)))
                        col += 1
                    
                    row_position = self.tableWidget_5.rowCount()
                    self.tableWidget_5.insertRow(row_position)
            elif action_idx !=0 and table_idx != 0:
                sql = ''' SELECT employee_id, history_action, history_table, operation_date FROM history 
                WHERE history_action=%s AND history_table=%s AND employee_id=%s'''
                self.cur.execute(sql, (action_text, table_text, employee_national_id))

                self.tableWidget_5.setRowCount(0)
                self.tableWidget_5.insertRow(0)

                data = self.cur.fetchall()

                for row, form in enumerate(data):
                    for col, item in enumerate(form):
                        if col == 0:
                            self.cur.execute(''' SELECT name FROM employee WHERE national_id=%s ''', [(item)])
                            employee_name = self.cur.fetchone()
                            # print(employee_name)
                            self.tableWidget_5.setItem(row, col, QTableWidgetItem(str(employee_name[0])))
                        else:
                            self.tableWidget_5.setItem(row, col, QTableWidgetItem(str(item)))
                        col += 1

                    row_position = self.tableWidget_5.rowCount()
                    self.tableWidget_5.insertRow(row_position)
    
    ################################################################
    ###### Reports
    def Show_Books_Report(self):
        dt = self.dateEdit.text()
        #### to change date format
        dt1 = dt.replace('/', '-')
        month = dt1[:dt1.find('-')]
        if len(month)==1:
            month = '0'+month
        day = dt1[dt1.find('-')+1:dt1.find('-', 3)]
        if len(day)==1:
            day = '0'+day
        year = dt1[dt1.find('-', 3)+1:]
        date_from = f'{year}-{month}-{day} 00:00:00.0'
        # print(date_from, date_to) 
        #############################
        dt2 = self.dateEdit_2.text()
        #### to change date format
        dt3 = dt2.replace('/', '-')
        month = dt3[:dt3.find('-')]
        if len(month)==1:
            month = '0'+month
        day = dt3[dt3.find('-')+1:dt3.find('-', 3)]
        if len(day)==1:
            day = '0'+day
        year = dt3[dt3.find('-', 3)+1:]
        date_to = f'{year}-{month}-{day}'
        # print(date_from, date_to) 
        #############################
        print(date_from)
        print(date_to)
        print(datetime.date.today())
        
        self.cur.execute(''' SELECT book_id FROM DATE(date)=%s ''', [(date_to)])
        data = self.cur.fetchall()
        
        print(data)
        
    ################################################################
    ###### DataBase
    def Show_Books_DataBase(self):
        self.tableWidget_7.setRowCount(0)
        self.tableWidget_7.insertRow(0)
        
        self.cur.execute(''' SELECT title, code, category_id, author_id, publisher_id, price, date, description FROM book ''')
        data = self.cur.fetchall()
        
        for row, form in enumerate(data):
            for col, item in enumerate(form):
                self.tableWidget_7.setItem(row, col, QTableWidgetItem(str(item)))
                col += 1
            
            row_position = self.tableWidget_7.rowCount()
            self.tableWidget_7.insertRow(row_position)
    
    def Export_Books_DataBase(self):
        
        sql = ''' SELECT title, code, category_id, author_id, publisher_id, price, date, description FROM book '''
        self.cur.execute(sql)
        data = self.cur.fetchall()
        
        excel_file = Workbook("books_database_report.xlsx")
        sheet1 = excel_file.add_worksheet()
        
        sheet1.write(0, 0, "Book Title")
        sheet1.write(0, 1, "Book Code")
        sheet1.write(0, 2, "Book Category")
        sheet1.write(0, 3, "Book Author")
        sheet1.write(0, 4, "Book Publisher")
        sheet1.write(0, 5, "Book Price")
        sheet1.write(0, 6, "Book Date")
        sheet1.write(0, 7, "Book Description")
        
        row_number = 1
        for row in data:
            col_number = 0
            for item in row:
                sheet1.write(row_number, col_number, str(item))
                col_number += 1
            row_number += 1
        
        excel_file.close()
        
        self.statusBar().showMessage("Books In Database Exported Successfully")
    
    def Show_Students_DataBase(self):
        self.tableWidget_8.setRowCount(0)
        self.tableWidget_8.insertRow(0)
        
        self.cur.execute(''' SELECT name, student_id, mail, phone, department, date FROM student ''')
        data = self.cur.fetchall()
        
        for row, form in enumerate(data):
            for col, item in enumerate(form):
                self.tableWidget_8.setItem(row, col, QTableWidgetItem(str(item)))
                col += 1
            
            row_position = self.tableWidget_8.rowCount()
            self.tableWidget_8.insertRow(row_position)
    
    def Export_Students_DataBase(self):
        
        sql = ''' SELECT name, student_id, mail, phone, department, date FROM student '''
        self.cur.execute(sql)
        data = self.cur.fetchall()
        
        excel_file = Workbook("students_database_report.xlsx")
        sheet1 = excel_file.add_worksheet()
        
        sheet1.write(0, 0, "Student Name")
        sheet1.write(0, 1, "Student Id")
        sheet1.write(0, 2, "Student Mail")
        sheet1.write(0, 3, "Student Phone")
        sheet1.write(0, 4, "Student Department")
        sheet1.write(0, 5, "Sutdent Date")
        
        row_number = 1
        for row in data:
            col_number = 0
            for item in row:
                sheet1.write(row_number, col_number, str(item))
                col_number += 1
            row_number += 1
        
        excel_file.close()
        
        self.statusBar().showMessage("Students In Database Exported Successfully")
    
    def Show_Employees_DataBase(self):
        self.tableWidget_9.setRowCount(0)
        self.tableWidget_9.insertRow(0)
        
        self.cur.execute(''' SELECT name, national_id, mail, phone, date FROM employee ''')
        data = self.cur.fetchall()
        
        for row, form in enumerate(data):
            for col, item in enumerate(form):
                self.tableWidget_9.setItem(row, col, QTableWidgetItem(str(item)))
                col += 1
            
            row_position = self.tableWidget_9.rowCount()
            self.tableWidget_9.insertRow(row_position)
    
    def Export_Employees_DataBase(self):
        
        sql = ''' SELECT name, national_id, mail, phone, date FROM employee '''
        self.cur.execute(sql)
        data = self.cur.fetchall()
        
        excel_file = Workbook("employees_database_report.xlsx")
        sheet1 = excel_file.add_worksheet()
        
        sheet1.write(0, 0, "Employee Name")
        sheet1.write(0, 1, "Employee Id")
        sheet1.write(0, 2, "Employee Mail")
        sheet1.write(0, 3, "Employee Phone")
        sheet1.write(0, 4, "Employee Date")
        
        row_number = 1
        for row in data:
            col_number = 0
            for item in row:
                sheet1.write(row_number, col_number, str(item))
                col_number += 1
            row_number += 1
        
        excel_file.close()
        
        self.statusBar().showMessage("Employees In Database Exported Successfully")
    
    def Show_Authors_DataBase(self):
        self.tableWidget_10.setRowCount(0)
        self.tableWidget_10.insertRow(0)
        
        self.cur.execute(''' SELECT name, location FROM author ''')
        data = self.cur.fetchall()
        
        for row, form in enumerate(data):
            for col, item in enumerate(form):
                self.tableWidget_10.setItem(row, col, QTableWidgetItem(str(item)))
                col += 1
            
            row_position = self.tableWidget_10.rowCount()
            self.tableWidget_10.insertRow(row_position)
    
    def Export_Authors_DataBase(self):
        
        sql = ''' SELECT name, location FROM author '''
        self.cur.execute(sql)
        data = self.cur.fetchall()
        
        excel_file = Workbook("author_database_report.xlsx")
        sheet1 = excel_file.add_worksheet()
        
        sheet1.write(0, 0, "Author Name")
        sheet1.write(0, 1, "Author Location")
        
        row_number = 1
        for row in data:
            col_number = 0
            for item in row:
                sheet1.write(row_number, col_number, str(item))
                col_number += 1
            row_number += 1
        
        excel_file.close()
        
        self.statusBar().showMessage("Authors In Database Exported Successfully")
    
    def Show_Publishers_DataBase(self):
        self.tableWidget_11.setRowCount(0)
        self.tableWidget_11.insertRow(0)
        
        self.cur.execute(''' SELECT name, location FROM publisher ''')
        data = self.cur.fetchall()
        
        for row, form in enumerate(data):
            for col, item in enumerate(form):
                self.tableWidget_11.setItem(row, col, QTableWidgetItem(str(item)))
                col += 1
            
            row_position = self.tableWidget_11.rowCount()
            self.tableWidget_11.insertRow(row_position)
    
    def Export_Publishers_DataBase(self):
        
        sql = ''' SELECT name, location FROM publisher '''
        self.cur.execute(sql)
        data = self.cur.fetchall()
        
        excel_file = Workbook("publisher_database_report.xlsx")
        sheet1 = excel_file.add_worksheet()
        
        sheet1.write(0, 0, "publisher Name")
        sheet1.write(0, 1, "publisher Location")
        
        row_number = 1
        for row in data:
            col_number = 0
            for item in row:
                sheet1.write(row_number, col_number, str(item))
                col_number += 1
            row_number += 1
        
        excel_file.close()
        
        self.statusBar().showMessage("Publisher In Database Exported Successfully")

######################################################################

class LibraryManagementSystem(ABC):
    
    def __init__(self, userType, userName, password):
        self.__userType = userType
        self.__userName = userName
        self.__password = password
    
    # methods 
    def logIn(self):
        pass
    def singUp(self):
        pass
    def logOut(self):
        pass

class User:
    
    def __init__(self, name, userName, email, password):
        self.__name = name
        self.__userName = userName
        self.__email = email
        self.__password = password
    
    # Methods
    def verify(self):
        pass
    def checkAccount(self):
        pass
    def getBookInfo(self):
        pass

class Librarian(User):
    
    def __init__(self, name, userName, email, password, Id, age):
        super().__init__(name, userName, email, password)
        self.__Id = Id
        self.__age = age
    
    # Methods
    def verifyLibrarian(self):
        pass

class Student(User):
    
    def __init__(self, name, userName, email, password, Id, department, year):
        super().__init__(name, userName, email, password)
        self.__Id = Id
        self.__department = department
        self.__year = year
    
    # Methods
    def searchOnBook(self):
        pass
    def borrowedBooks(self):
        pass

class Account:
    
    def __init__(self, no_borrowed_books, no_reserved_books, no_lost_books, fine_amount):
        self.__no_borrowed_books = no_borrowed_books
        self.__no_reserved_books = no_reserved_books
        self.__no_lost_books = no_lost_books
        self.__fine_amount = fine_amount
    
    # Methods
    def calculate_fine_amount(self):
        pass

class Book:
    
    def __init__(self, name, id, category, publisher, price):
        self.__name = name
        self.__id = id
        self.__cateogry = category
        self.__publisher = publisher
        self.__price = price
    
    # Methods
    def book_status(self):
        pass
    def reservation_status(self):
        pass
    def add(self):
        pass
    def delete(self):
        pass
    def update(self):
        pass

class Author:
    
    def __init__(self, name, age, phone):
        self.__name = name
        self.__age = age
        self.__phone = phone
    
    # Methods
    def author_books(self):
        pass

class Reports:
    
    def __init__(self, year, month, day):
        self.__year = year
        self.__month = month
        self.__day = day

class LMSDataBase:
    
    def __init__(self, books_list, users_list):
        self.__books_list = books_list
        self.__users_list = users_list
    
    # Methods 
    def store_books(self):
        pass
    def store_userse(self):
        pass
    def store_reports(self):
        pass
    def search(self):
        pass
    def display_all_books(self):
        pass
    def display_all_student(self):
        pass

#######################################################
global action
action = ['- - - - - - -', 'Login', 'Logout', 'Add', 'Edit', 'Delete', 'Add Rent', 'Add Retreive', 'Add Sale']
global table
table = ['- - - - - - -', 'Books', 'Students', 'History', 'Category', 'Author', 'Publisher', 'Employee', 'Daily Movement']

def main():
    app = QApplication(sys.argv)
    window = Main()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()
