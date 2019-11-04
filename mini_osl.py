import sqlite3
import tkinter as tk
import tkinter.messagebox as tkMessageBox
from sqlite3 import Error
from sqlite3 import IntegrityError
from tkinter import *
from tkinter import Frame
from tkinter import font
from tkinter import ttk
import os
from database_connection import *

global database
database = "emp_info.db"
# functions
global JobPosition
JobPosition = ('Manager','Employee')


def delete3():
    screen4.destroy()


def delete4():
    screen5.destroy()


def login_sucess(user):
    if user=='admin':screen1.withdraw()
    screen2.withdraw()
    name=''
    department=''
    if(user!='admin'):
        conn = create_connection(database)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM data where employee_id="+user)
        fetch = cursor.fetchall()
        for data in fetch:
            name=data[1]
            department=data[9]
        cursor.close()
        conn.close()
        print(name+"  "+department)

    # window start
    global window
    window = Toplevel(screen)
    if(user=='admin'):window.title('ADMIN PANEL')
    else:window.title('WELCOME '+name+" DEPARTMENT "+department)

    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    width = 1320
    height = 525
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)
    window.geometry("%dx%d+%d+%d" % (width,height,x,y))
    window.resizable(0,0)
    # ==================================FRAME==============================================

    Top = Frame(window,width=900,height=30,bd=10,bg="#8C8C8C",relief=RIDGE)
    Top.pack(side=TOP)
    Left = Frame(window,width=300,height=500,relief=RIDGE)
    Left.pack(side=LEFT)

    Forms = Frame(Left,width=50,height=500,bd=10,relief=RIDGE)
    Forms.pack(side=TOP)
    BUTTON = Frame(Left,width=50,height=500,relief=RIDGE)
    BUTTON.pack(side=BOTTOM)
    result = Frame(BUTTON)
    result.pack(side=TOP)
    Right = Frame(window,width=700,height=500,bd=8,relief=RIDGE)
    Right.pack(side=RIGHT)

    txt_result = Label(BUTTON,font=('Segoe UI Black','13'),border=2,)
    txt_result.pack(side=TOP)

    def get_data():
        employee_name = name.get()
        employee_id = IDText.get()
        gender = str(var.get())
        b_date = str(month.get() + "-" + date.get() + "-" + year.get())
        email = emailText.get()
        qualification = Qualification.get()
        work_exp = workExp.get()
        mob_num = mobileText.get()
        job_title = jobtitleText.get()
        job_des = jobDepartmentText.get()
        work_num = WorkPhoneText.get()
        work_loc = WorkLocationText.get()
        salary = salaryText.get()
        address = AddressText.get()
        project = [employee_id,employee_name,gender,b_date
            ,email,qualification,work_exp,mob_num,job_title,job_des
            ,work_num,work_loc,salary,address]
        return project

    def read():
        conn = create_connection(database)
        cursor = conn.cursor()
        tree.delete(*tree.get_children())
        if(user=='admin'):
            cursor.execute("SELECT * FROM data")
        else:
            cursor.execute("SELECT * FROM data WHERE job_des='"+department+"'")

        fetch = cursor.fetchall()
        for data in fetch:
            tree.insert('','end',values=(data[0],data[1],data[2],data[3],data[4],data[5],data[6]
                                         ,data[7],data[8],data[9],data[10],data[11],data[12],data[13]))
        cursor.close()
        conn.close()
    def Exit():
        if user != 'admin':
            result = tkMessageBox.askquestion('Exit','Are you sure you want to exit?',icon="warning")
            if result == 'yes':
                window.destroy()
        else:
            window.destroy()
            adminPanel()


    def update():
        conn = create_connection(database)
        if not tree.selection():
            print("ERROR")
        else:
            curItem = tree.focus()
            contents = (tree.item(curItem))

            selecteditem = contents['values']
            if check():
                try:
                    data = get_data()
                    sql = ''' UPDATE data SET
                                  employee_id = ? ,
                                  employee_name= ? ,
                                  gender= ? ,
                                  b_date= ? ,
                                  email= ? ,
                                  qualification= ?,
                                  work_exp= ?,
                                  mob_num= ?,
                                  job_title= ?,
                                  job_des= ? ,
                                  work_num= ?,
                                  work_loc= ?,
                                  salary= ?,
                                  address= ?
                                  WHERE employee_id = ?'''
                    data.append(selecteditem[0])
                    cur = conn.cursor()
                    cur.execute(sql,data)
                    conn.commit()
                    print(selecteditem)

                    if data[8] == 'Manager':
                        username_info = selecteditem[1]
                        id_info = selecteditem[0]
                        dep=selecteditem[9]
                        manager_data = [id_info,username_info,dep]
                        sql_create_projects_table = """ CREATE TABLE IF NOT EXISTS manager(manager_id INTEGER PRIMARY KEY NOT NULL,
                                                                                                        manager_name  TEXT NOT NULL,
                                                                                                        job_des TEXT NOT NULL
                                                                                                    ); """
                        # create a database connection

                        if conn is not None:
                            # create projects table
                            create_table(conn,sql_create_projects_table)
                        else:
                            print("Error! cannot create the database connection.")
                        with conn:
                            try:
                                cursor.execute("SELECT * FROM manager where manager_name='" + username_info + "'")
                                fetch=cursor.fetchall()
                                if(fetch):
                                    manager_data.append(id_info)
                                    sql = ''' UPDATE manager SET manager_id = ?,
                                                                 manager_name = ?,
                                                                 job_des= ?
                                                                 WHERE manager_id = ?'''
                                    print('jere')
                                    cur = conn.cursor()
                                    cur.execute(sql,manager_data)
                                    conn.commit()
                                    print('here')
                                else:
                                    sql = ''' INSERT INTO manager(manager_id,manager_name,job_des)
                                                                              VALUES(?,?,?) '''
                                    print('jere')
                                    create_project(conn,manager_data,sql)
                                    print('here')
                            except IntegrityError:
                                print('err')
                    cur.close()
                    conn.close()
                    txt_result.config(text="Successfully updated the data",fg="green")
                    Clear()
                    read()
                except IntegrityError:
                    txt_result.config(text="ID alreday existis",fg="green")

    def delete():
        conn = create_connection(database)
        cursor = conn.cursor()
        if not tree.selection():
            txt_result.config(text="Please select an item first",fg="red")
            print("ERROR")
        else:
            result = tkMessageBox.askquestion("Delete",'Are you sure you want to delete this record?',
                                              icon="warning")
            if result == 'yes':
                curItem = tree.focus()
                contents = (tree.item(curItem))
                selecteditem = contents['values']

                tree.delete(curItem)
                cursor.execute("DELETE FROM data WHERE employee_id = ?",(selecteditem[0],))
                conn.commit()
                cursor.close()
                conn.close()
                txt_result.config(text="Successfully deleted the data",fg="black")
                Clear()
                read()

    def nameck(self):
        if not nameText.get():
            txt_result.config(text="Please complete the required field!: NAME",fg="red")
        else:
            txt_result.config(text=" ")
            return True
        return False

    def IDck(self):
        if not IDText.get() or not IDText.get().isdigit():
            txt_result.config(text="Please complete the required field!: ID",fg="red")
        else:
            txt_result.config(text=" ")
            return True
        return False

    def dobck(self):
        if date.get() == '1' and month.get() == 'Null' and year.get() == '0':
            txt_result.config(text="Please complete the required field!: BIRTH-DATE",fg="red")
        else:
            txt_result.config(text=" ")
            return True
        return False

    def genderck(self):
        if not var.get():
            txt_result.config(text="Please complete the required field!: GENDER",fg="red")
        else:
            txt_result.config(text=" ")
            return True
        return False

    def emailck(self):
        if not emailText.get() or not re.match("^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$",emailText.get(),
                                               re.IGNORECASE):
            txt_result.config(text="Please complete the required field!: EMAIL ADDRESS",fg="red")
        else:
            txt_result.config(text=" ")
            return True
        return False

    def mobileck(self):
        if not mobileText.get() or not re.match("(0/91)?[7-9][0-9]{9}",str(mobileText.get())):
            txt_result.config(text="Please complete the required field!: MOBILE NUMBER ",fg="red")
        else:
            txt_result.config(text=" ")
            return True
        return False

    def workexpck(self):
        if not workExp.get() or not workExp.get().isdigit():
            txt_result.config(text="Please complete the required field!: WORK EXPERIENCE ",fg="red")
        else:
            txt_result.config(text=" ")
            return True
        return False

    def Qualificationck(self):
        if not Qualification.get():
            txt_result.config(text="Please complete the required field!: QUALIFICATION",fg="red")
        else:
            txt_result.config(text=" ")
            return True
        return False

    def jobdepartck():
        conn = create_connection(database)
        cursor = conn.cursor()
        cursor.execute("SELECT department_name FROM department")
        fetch = cursor.fetchall()
        Department = []
        for data in fetch:
            Department.append(data[0])
        cursor.close()
        conn.close()
        print()
        if not jobDepartmentText.get():
            txt_result.config(text="Please complete the required field!: JOB DEPARTMENT",fg="red")
        elif not Department.__contains__(jobDepartmentText.get()):
            txt_result.config(text="Please Select From The Given Options!: JOB DEPARTMENT",fg="red")
        else:
            txt_result.config(text=" ")
            return True
        return False

    def jobtitleck(self):
        if not jobtitleText.get():
            txt_result.config(text="Please complete the required field!: JOB TITLE",fg="red")
        elif not JobPosition.__contains__(jobtitleText.get()):
            txt_result.config(text="Please Select From The Given Options!: JOB TITLE",fg="red")
        else:
            txt_result.config(text=" ")
            return True
        return False

    def worklocack(self):
        if not WorkLocationText.get():
            txt_result.config(text="Please complete the required field!: WORK LOCATION",fg="red")
        else:
            txt_result.config(text=" ")
            return True
        return False

    def workPhoneck(self):
        if not WorkPhoneText.get() or not re.match("(0/91)?[7-9][0-9]{9}",str(WorkPhoneText.get())):
            txt_result.config(text="Please complete the required field!: WORK NUMBER",fg="red")
        else:
            txt_result.config(text=" ")
            return True
        return False

    def addressck(self):
        if not AddressText.get():
            txt_result.config(text="Please complete the required field!: ADDRESS",fg="red")
        else:
            txt_result.config(text=" ")
            return True
        return False

    def salaryck(self):
        if not salaryText.get() or not salaryText.get().isdigit():
            txt_result.config(text="Please complete the required field!: SALARY",fg="red")
        else:
            txt_result.config(text=" ")
            return True
        return False

    def check():
        if not nameText.get():
            txt_result.config(text="Please complete the required field!: NAME",fg="red")
        elif not IDText.get() or not IDText.get().isdigit():
            txt_result.config(text="Please complete the required field!: ID",fg="red")
        elif date.get() == 'DD' and month.get() == 'MM' and year.get() == 'YYYY':
            txt_result.config(text="Please complete the required field!: BIRTH-DATE",fg="red")
        elif not var.get():
            txt_result.config(text="Please complete the required field!: GENDER",fg="red")
        elif not emailText.get() or not re.match("^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$",emailText.get(),
                                                 re.IGNORECASE):
            txt_result.config(text="Please complete the required field!: EMAIL ADDRESS",fg="red")
        elif not mobileText.get() or not mobileText.get().isdigit() or not re.match("(0/91)?[7-9][0-9]{9}",
                                                                                    str(mobileText.get())):
            txt_result.config(text="Please complete the required field!: MOBILE NUMBER ",fg="red")
        elif not workExp.get() or not workExp.get().isdigit():
            txt_result.config(text="Please complete the required field!: WORK EXPERIENCE ",fg="red")
        elif not Qualification.get():
            txt_result.config(text="Please complete the required field!: QUALIFICATION",fg="red")
        elif not jobdepartck():
            txt_result.config(text="Please complete the required field!: JOB DEPARTMENT",fg="red")
        elif not jobtitleText.get():
            txt_result.config(text="Please complete the required field!: JOB TITLE",fg="red")
        elif not WorkLocationText.get():
            txt_result.config(text="Please complete the required field!: WORK LOCATION",fg="red")
        elif not WorkPhoneText.get() or not re.match("(0/91)?[7-9][0-9]{9}",str(WorkPhoneText.get())):
            txt_result.config(text="Please complete the required field!: WORK NUMBER",fg="red")
        elif not AddressText.get():
            txt_result.config(text="Please complete the required field!: ADDRESS",fg="red")
        elif not salaryText.get() or not salaryText.get().isdigit():
            txt_result.config(text="Please complete the required field!: SALARY",fg="red")
        else:
            return True
        return False

    def Clear():
        nameText.delete(0,'end')
        IDText.delete(0,'end')
        str(var.set(" "))
        date.set('DD')
        month.set("MM")
        year.set("YYYY")
        emailText.delete(0,'end')
        Qualification.set('Select Qualification')
        mobileText.delete(0,'end')
        jobtitleText.delete(0,'end')
        jobDepartmentText.delete(0,'end')
        WorkPhoneText.delete(0,'end')
        WorkLocationText.delete(0,'end')
        salaryText.delete(0,'end')
        AddressText.delete(0,'end')
        workExperienceText.delete(0,'end')

    def submit() -> object:
        sql_create_projects_table = """ CREATE TABLE IF NOT EXISTS data (employee_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                                                                                employee_name  TEXT NOT NULL,
                                                                                gender TEXT NOT NULL,
                                                                                b_date TEXT NOT NULL,
                                                                                email TEXT NOT NULL,
                                                                                qualification TEXT NOT NULL,
                                                                                work_exp TEXT NOT NULL,
                                                                                mob_num INTEGER NOT NULL,
                                                                                job_title TEXT NOT NULL,
                                                                                job_des TEXT NOT NULL,
                                                                                work_num INTEGER NOT NULL,
                                                                                work_loc TEXT NOT NULL,
                                                                                salary INTEGER NOT NULL,
                                                                                address TEXT NOT NULL
                                                                            ); """

        # create a database connection
        conn = create_connection(database)
        cursor = conn.cursor()
        if check():

            data = get_data()
            print(data)
            if conn is not None:
                # create projects table
                create_table(conn,sql_create_projects_table)
            else:
                print("Error! cannot create the database connection.")

            with conn:
                try:

                    sql = ''' INSERT INTO data(employee_id,employee_name,gender,b_date
                               ,email,qualification,work_exp,mob_num,job_title,job_des
                               ,work_num,work_loc,salary,address)
                              VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?) '''
                    create_project(conn,data,sql)
                    if data[8] == 'Manager':
                        username_info = data[1]
                        id_info = data[0]
                        print(id_info)
                        manager_data=[id_info,username_info,data[9]]
                        sql_create_projects_table = """ CREATE TABLE IF NOT EXISTS manager(manager_id INTEGER PRIMARY KEY NOT NULL,
                                                                                                        manager_name  TEXT NOT NULL,
                                                                                                        job_des TEXT NOT NULL
                                                                                                    ); """
                        # create a database connection

                        if conn is not None:
                            # create projects table
                            create_table(conn,sql_create_projects_table)
                        else:
                            print("Error! cannot create the database connection.")
                        with conn:
                            try:
                                sql = ''' INSERT INTO manager(manager_id,manager_name,job_des)
                                          VALUES(?,?,?) '''
                                print('jere')
                                create_project(conn,manager_data,sql)
                                print('here')

                            except IntegrityError:
                                print('err')


                    tree.delete(*tree.get_children())
                    if (user == 'admin'):
                        cursor.execute("SELECT * FROM data")
                    else:
                        cursor.execute("SELECT * FROM data WHERE job_des='" + department+"'")
                    fetch = cursor.fetchall()
                    for data in fetch:
                        tree.insert('','end',values=(data[0],data[1],data[2],data[3],data[4],data[5],data[6]
                                                     ,data[7],data[8],data[9],data[10],data[11],data[12],data[13]))
                    txt_result.config(text="YOUR RESPONSE SUCCESSFULLY SAVED",fg="green")




                except IntegrityError:
                    txt_result.config(text="ID alreday existis",fg="green")

        cursor.close()

        conn.close()

    def enter(selecteditem):
        Clear()
        id.set(selecteditem[0])
        name.set(selecteditem[1])
        dob = " ".join(str(x) for x in str(selecteditem[3]).split("-"))
        dob = list(dob.split(" "))
        year.set(dob[2])
        month.set(dob[0])
        date.set(dob[1])
        if selecteditem[2] == 'Male':
            male.select()
        else:
            female.select()
        email.set(selecteditem[4])
        Qualification.set(selecteditem[5])
        workExp.set(selecteditem[6])
        mob_num.set(selecteditem[7])
        jobtitleText.set(selecteditem[8])
        jobDepartmentText.set(selecteditem[9])
        workphone.set(selecteditem[10])
        workloc.set(selecteditem[11])
        salary.set(selecteditem[12])
        address.set(selecteditem[13])

    def find(Variable):
        Clear()
        conn = create_connection(database)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM `data`")
        fetch = cursor.fetchall()
        found = False
        for data in fetch:
            if str(data[0]) == str(Variable):
                txt_result.config(text="Data Found",fg="green")
                found = True
                enter(data)
        if not found:
            txt_result.config(text="Data Not Found",fg="red")
        cursor.close()
        conn.close()

    def sel(self):
        curItem = tree.focus()
        contents = (tree.item(curItem))
        selecteditem = contents['values']
        try:
            enter(selecteditem)
        except IndexError:
            pass

    # variables
    name = StringVar()
    id = StringVar()
    email = StringVar()
    workExp = StringVar()
    mob_num = StringVar()
    jobtitle = StringVar()
    jobdes = StringVar()
    workphone = StringVar()
    workloc = StringVar()
    salary = StringVar()
    address = StringVar()
    var1 = BooleanVar()
    var1.set(True)
    var2 = BooleanVar()
    var2.set(True)
    var3 = BooleanVar()
    var3.set(True)
    var4 = BooleanVar()
    var4.set(True)
    var = StringVar()
    studyYear = StringVar()
    pre = ["Mrs","Mr","Miss"]
    months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    dates = [int(a) for a in range(1,32)]
    years = [int(a) for a in range(1950,2050)]

    # TOP
    if(user=='admin'):
        txt_title = Label(Top,width=900,font=('Segoe UI Black',24),text="ADMIN PANNEL")

    else:
        txt_title = Label(Top,width=900,font=('Segoe UI Black',24),text=department.upper())
    txt_title.pack()
    # for NAME
    nameLabel = Label(Forms,font=('Segoe UI Black','13'),border=2,text="Full Name:")
    nameLabel.grid(row=0,column=0,sticky=W,pady=1,padx=2)
    nameText = Entry(Forms,font=('Segoe UI Black','13'),border=2,bd=5,textvariable=name)
    nameText.grid(row=0,column=1,columnspan=2,sticky=W,pady=1,padx=2)
    nameText.bind('<FocusOut>',nameck)

    # for ID
    IDLabel = Label(Forms,font=('Segoe UI Black','13'),border=2,text="Employee ID:")
    IDLabel.grid(row=1,column=0,sticky=W,pady=1,padx=2)
    IDText = Entry(Forms,font=('Segoe UI Black','13'),textvariable=id,border=2,bd=5)
    IDText.grid(row=1,column=1,sticky=W,pady=1,padx=2)
    IDText.bind('<FocusOut>',IDck)

    # for BD
    birthDate = Label(Forms,font=('Segoe UI Black','13'),border=2,text="Birth Date").grid(row=2,column=0,sticky=W,
                                                                                          pady=1,
                                                                                          padx=2)
    month = ttk.Combobox(Forms,font=('Segoe UI Black','13'),values=months,width=6,text="Select month")
    month.grid(row=2,column=1,padx=3,sticky=W,pady=1)
    month.set('MM')
    month.bind("<<ComboboxSelected>>",dobck)
    date = ttk.Combobox(Forms,font=('Segoe UI Black','13'),values=dates,width=6)
    date.set('DD')
    date.grid(row=2,column=2,padx=3,sticky=W,pady=1)

    date.bind("<<ComboboxSelected>>",dobck)
    year = ttk.Combobox(Forms,font=('Segoe UI Black','13'),values=years,text="Select year",width=6)
    year.grid(row=2,column=3,padx=3,sticky=W,pady=1)
    year.set('YYYY')
    year.bind("<<ComboboxSelected>>",dobck)

    # gender
    gender = Label(Forms,font=('Segoe UI Black','13'),border=2,text="Gender").grid(row=3,column=0,sticky=W,pady=1,
                                                                                   padx=2)
    male = Radiobutton(Forms,font=('Segoe UI Black','13'),border=2,text="Male",padx=20,variable=var,value="Male")
    male.deselect()
    female = Radiobutton(Forms,font=('Segoe UI Black','13'),border=2,text="Female",padx=20,variable=var,value="Female")
    female.deselect()
    male.grid(row=3,column=1)
    female.grid(row=3,column=2)
    male.bind('<FocusOut>',genderck)
    female.bind('<FocusOut>',genderck)

    # for email
    emailLabel = Label(Forms,font=('Segoe UI Black','13'),border=2,text="Email:")
    emailLabel.grid(row=4,column=0,sticky=W,pady=1,padx=2)
    emailText = Entry(Forms,font=('Segoe UI Black','13'),border=2,bd=5,textvariable=email)
    emailText.grid(row=4,column=1,sticky=W,pady=1,padx=2)
    emailText.bind('<FocusOut>',emailck)

    # #  mobile number
    mobileLabel = Label(Forms,font=('Segoe UI Black','13'),border=2,text="Mobile Number")
    mobileLabel.grid(row=4,column=2,sticky=W,pady=1,padx=2)
    mobileText = Entry(Forms,font=('Segoe UI Black','13'),textvariable=mob_num,border=2,bd=5,)
    # mobileText.config(validate="all",validatecommand=(mobcheck,'%P'))
    mobileText.bind('<FocusOut>',mobileck)

    mobileText.grid(row=4,column=3)

    #  qualifications

    Qualifications = ['SSC','HSC','DIPLOMA','B.E','BSC IT','M.E','PHD']
    nameQualification = Label(Forms,font=('Segoe UI Black','13'),border=2,text="Qualification")
    nameQualification.grid(row=5,column=0,sticky=W,pady=1,padx=2)
    Qualification = ttk.Combobox(Forms,font=('Segoe UI Black','13'),values=Qualifications,width=18,
                                 text="Select Qualification")
    Qualification.bind("<<ComboboxSelected>>",Qualificationck)
    Qualification.set('Select Qualification')
    Qualification.grid(row=5,column=1)
    # for workExperience
    workExperienceLabel = Label(Forms,font=('Segoe UI Black','13'),border=2,text="Work Experience:")
    workExperienceLabel.grid(row=5,column=2,sticky=W,pady=1,padx=2)
    workExperienceText = Entry(Forms,font=('Segoe UI Black','13'),border=2,bd=5,textvariable=workExp)
    workExperienceText.grid(row=5,column=3,sticky=W,pady=1,padx=2)
    workExperienceText.bind('<FocusOut>',workexpck)

    # for jobtitle

    jobtitleLabel = Label(Forms,font=('Segoe UI Black','13'),border=2,text="Job Position")
    jobtitleLabel.grid(row=6,column=0,sticky=W,pady=1,padx=2)
    jobtitleText = ttk.Combobox(Forms,font=('Segoe UI Black','13'),values=JobPosition,width=18,
                                text="Select Job Position")
    jobtitleText.bind("<<ComboboxSelected>>",jobtitleck)
    jobtitleText.set('Select Job Position')
    jobtitleText.grid(row=6,column=1,sticky=W,pady=1,padx=2)

    # for jobDepartment
    conn = create_connection(database)
    cursor = conn.cursor()
    cursor.execute("SELECT department_name FROM department")
    Department = cursor.fetchall()

    jobDepartmentLabel = Label(Forms,font=('Segoe UI Black','13'),border=2,text="Department")
    jobDepartmentLabel.grid(row=6,column=2,sticky=W,pady=1,padx=2)
    jobDepartmentText = ttk.Combobox(Forms,font=('Segoe UI Black','13'),values=Department,width=18,
                                     text="Select Department")
    jobDepartmentText.bind("<<ComboboxSelected>>",jobdepartck)
    jobDepartmentText.set('Select Department')
    jobDepartmentText.grid(row=6,column=3,sticky=W,pady=1,padx=2)

    #  work number
    WorkPhoneLabel = Label(Forms,font=('Segoe UI Black','13'),border=2,text="Work Phone: ")
    WorkPhoneLabel.grid(row=7,column=0,sticky=W,pady=1,padx=2)
    WorkPhoneText = Entry(Forms,font=('Segoe UI Black','13'),textvariable=workphone,border=2,bd=5)
    WorkPhoneText.grid(row=7,column=1)
    WorkPhoneText.bind('<FocusOut>',workPhoneck)

    #  mobile number
    WorkLocationLabel = Label(Forms,font=('Segoe UI Black','13'),border=2,text="Work Location: ")
    WorkLocationLabel.grid(row=7,column=2,sticky=W,pady=1,padx=2)
    WorkLocationText = Entry(Forms,font=('Segoe UI Black','13'),textvariable=workloc,border=2,bd=5)
    WorkLocationText.grid(row=7,column=3)
    WorkLocationText.bind('<FocusOut>',worklocack)

    #  salary
    salaryLabel = Label(Forms,font=('Segoe UI Black','13'),border=2,text="Salary")
    salaryLabel.grid(row=8,column=0,sticky=W,pady=1,padx=2)
    salaryText = Entry(Forms,font=('Segoe UI Black','13'),textvariable=salary,border=2,bd=5)
    salaryText.grid(row=8,column=1)
    salaryText.bind('<FocusOut>',salaryck)

    # for address
    AddressLabel = Label(Forms,font=('Segoe UI Black','13'),border=2,text="Address:")
    AddressLabel.grid(row=9,column=0,sticky=W,pady=1,padx=2)
    AddressText = Entry(Forms,font=('Segoe UI Black','13'),border=2,width=57,bd=5,textvariable=address)
    AddressText.grid(row=9,column=1,columnspan=3,sticky=W,pady=1,padx=2)
    AddressText.bind('<FocusOut>',addressck)

    # list
    # =======================================================
    searchid = StringVar()
    searchTop = Frame(Right,width=300,height=3,relief=RIDGE)
    searchTop.pack(side=BOTTOM)

    searchLable = Label(searchTop,font=('Segoe UI Black','13'),border=2,text="Enter Employee ID to search:")
    searchLable.grid(row=1,column=0,sticky=W,pady=1,padx=2)
    searchText = Entry(searchTop,font=('Segoe UI Black','13'),textvariable=searchid,border=2,bd=5)
    searchText.grid(row=1,column=1,sticky=W,pady=1,padx=2)
    searchbutton = tk.Button(searchTop,text="Search",font=('Segoe UI Black','13'),width=20,border=8,height=1,pady=10,
                             command=lambda: find(searchid.get()))
    searchbutton.grid(row=2,column=0,columnspan=2,sticky=N,pady=1,padx=2)
    # ====================================================
    yscroll = Scrollbar(Right)
    yscroll.pack(side=RIGHT,fill=Y)

    xscroll = Scrollbar(Right,orient="horizontal")
    xscroll.pack(side=BOTTOM,fill=X)
    style = ttk.Style()
    style.configure("mystyle.Treeview",highlightthickness=0,bd=0,font=('Calibri',11))  # Modify the font of the body
    style.configure("mystyle.Treeview.Heading",font=('Calibri',13,'bold'))  # Modify the font of the headings
    style.layout("mystyle.Treeview",[('mystyle.Treeview.treearea',{'sticky': 'nswe'})])  # Remove the borders
    # set ttk theme to "clam" which support the fieldbackground option
    # set ttk theme to "clam" which support the fieldbackground option

    style.theme_use("alt")
    style = ttk.Style()

    style.layout("Custom.Treeview.Heading",[
        ("Custom.Treeheading.cell",{'sticky': 'nswe'}),
        ("Custom.Treeheading.border",{'sticky': 'nswe','children': [
            ("Custom.Treeheading.padding",{'sticky': 'nswe','children': [
                ("Custom.Treeheading.image",{'side': 'right','sticky': ''}),
                ("Custom.Treeheading.text",{'sticky': 'we'})
            ]})
        ]}),
    ])
    style.configure("Custom.Treeview.Heading",
                    background="#BFBFBF",foreground="#0D0D0D",relief="flat")
    style.map("Custom.Treeview.Heading",
              relief=[('active','flat'),('pressed','sunken')])
    tree = ttk.Treeview(Right,style="Custom.Treeview",selectmode="browse",height=100,yscrollcommand=yscroll.set,
                        xscrollcommand=xscroll.set)
    tree.pack(side='left')
    yscroll.config(command=tree.yview)
    xscroll.config(command=tree.xview)

    tree["columns"] = ("EMPLOYEE ID","EMPLOYEE NAME","Gender","DOB","EMPLOYEE EMAIL","QUALIFICATION"
                       ,"WORK EXPERIENCE","MOBILE NUMBER","JOB TITLE","JOB DEPARTMENT","WORK PHONE"
                       ,"WORK LOCATION","EMPLOYEE  SALARY","EMPLOYEE  ADDRESS")
    tree['show'] = 'headings'

    tree.heading('EMPLOYEE NAME',text="EMPLOYEE NAME",anchor=W)
    tree.heading('EMPLOYEE ID',text="EMPLOYEE ID",anchor=W)
    tree.heading('DOB',text="DOB",anchor=W)
    tree.heading('Gender',text="Gender",anchor=W)
    tree.heading('EMPLOYEE EMAIL',text="EMPLOYEE EMAIL",anchor=W)
    tree.heading('QUALIFICATION',text="QUALIFICATION",anchor=W)
    tree.heading('WORK EXPERIENCE',text="WORK EXPERIENCE",anchor=W)
    tree.heading('MOBILE NUMBER',text="MOBILE NUMBER",anchor=W)
    tree.heading('JOB TITLE',text="JOB TITLE",anchor=W)
    tree.heading('JOB DEPARTMENT',text="JOB DEPARTMENT",anchor=W)
    tree.heading('WORK PHONE',text="WORK PHONE",anchor=W)
    tree.heading('WORK LOCATION',text="WORK LOCATION",anchor=W)
    tree.heading('EMPLOYEE  SALARY',text="EMPLOYEE  SALARY",anchor=W)
    tree.heading('EMPLOYEE  ADDRESS',text="EMPLOYEE  ADDRESS",anchor=W)
    tree.column('#0',stretch=NO,minwidth=0,width=
    0)
    tree.column('#1',stretch=NO,minwidth=0,width=120)
    tree.column('#2',stretch=NO,minwidth=0,width=120)
    tree.column('#3',stretch=NO,minwidth=0,width=120)
    tree.column('#4',stretch=NO,minwidth=0,width=120)
    tree.column('#5',stretch=NO,minwidth=0,width=120)
    tree.column('#7',stretch=NO,minwidth=0,width=120)
    tree.column('#8',stretch=NO,minwidth=0,width=120)
    tree.column('#9',stretch=NO,minwidth=0,width=120)
    tree.column('#10',stretch=NO,minwidth=0,width=120)
    tree.column('#11',stretch=NO,minwidth=0,width=120)
    tree.column('#12',stretch=NO,minwidth=0,width=120)
    tree.column('#13',stretch=NO,minwidth=0,width=120)
    tree.column('#14',stretch=NO,minwidth=0,width=120)
    tree.bind('<ButtonRelease-1>',sel)
    read()
    # tButton
    submitButton = tk.Button(BUTTON,text="Add",font=('Segoe UI Black','10'),width=12,border=8,
                             height=2,pady=10,command=submit).pack(side=LEFT)
    update = tk.Button(BUTTON,text="Update",font=('Segoe UI Black','10'),width=12,border=8,height=2,
                       pady=10,command=update).pack(side=LEFT)

    delete = tk.Button(BUTTON,text="Delete",font=('Segoe UI Black','10'),width=12,border=8,height=2,
                       pady=10,command=delete).pack(side=LEFT)
    clear = tk.Button(BUTTON,text="Clear",font=('Segoe UI Black','10'),width=12,border=8,height=2,
                      pady=10,command=Clear).pack(side=LEFT)
    exit = tk.Button(BUTTON,text="Exit",font=('Segoe UI Black','10'),width=12,border=8,height=2,
                     pady=10,command=Exit).pack(side=LEFT)
    window.mainloop()


def password_not_recognised():
    global screen4
    screen4 = Toplevel(screen)
    screen4.title("Success")
    screen4.geometry("150x100")
    Label(screen4,text="Password Error").pack()
    Button(screen4,text="OK",command=delete3).pack()


def user_not_found():
    global screen5
    screen5 = Toplevel(screen)
    screen5.title("Success")
    screen5.geometry("150x100")
    Label(screen5,text="User Not Found").pack()
    Button(screen5,text="OK",command=delete4).pack()





def login_verify():
    username1 = username_verify.get()
    password1 = password_verify.get()
    username_entry1.delete(0,END)
    password_entry1.delete(0,END)
    if username1 == 'admin':
        if password1=='admin':
            adminPanel()
        else:
            password_not_recognised()

    else:
        conn = create_connection(database)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM manager where manager_name='"+username1+"'")
        fetch=cursor.fetchall()
        if(fetch):
            print(fetch)
            for data in fetch:
                if data[1]==username1:
                    print(data[1],data[0])
                    if data[0]==int(password1):
                        login_sucess(password1)
                    else:
                        password_not_recognised()


        else:
            user_not_found()
            print('not found')
        cursor.close()
        conn.close()
        #list_of_files = os.listdir()
        # if username1 in list_of_files:
        #     file1 = open(username1,"r")
        #     verify = file1.read().splitlines()
        #     if password1 in verify:
        #         if username1 == 'admin':
        #             register()
        #         else:
        #             login_sucess(password1)
        #     else:
        #         password_not_recognised()
        #
        # else:
        #     user_not_found()


def back_to_main_register():
    screen2.destroy()
    screen.deiconify()



def add_department():
    global add_department_screen
    global new_department
    global new_department_id
    new_department_id = StringVar()
    new_department = StringVar()
    conn = create_connection(database)
    cursor = conn.cursor()
    cursor.execute("SELECT Department_name FROM department")
    fetch = \
        cursor.fetchall()
    add_department_screen = Toplevel(screen)
    add_department_screen.title("Add departments")
    add_department_screen.geometry("600x400")
    Top = Frame(add_department_screen,width=600,height=400,bd=10,relief=RIDGE)
    Top.pack(side=TOP)
    Bottom = Frame(add_department_screen,width=600,height=200,bd=10,relief=RIDGE)
    Bottom.pack(side=BOTTOM)
    # for ID
    IDLabel = Label(Top,font=('Segoe UI Black','13'),border=2,width=200,text="Department ID:")
    IDLabel.pack()
    IDText = Entry(Top,font=('Segoe UI Black','13'),textvariable=new_department_id,border=2,bd=5)
    IDText.pack()
    department_name = Label(Top,font=('Segoe UI Black','13'),width=200,border=2,text="Name of Department:")
    department_name.pack()
    department_name_entry = Entry(Top,font=('Segoe UI Black','13'),border=2,bd=5,
                                  textvariable=new_department)
    department_name_entry.pack()

    Button(Top,text="Add",font=('Segoe UI Black','10'),width=20,border=8,
                     pady=10,command=add_new_department).pack()
    global department_tree
    department_tree = ttk.Treeview(Bottom,style="Custom.Treeview",selectmode="browse",height=50)
    department_tree.pack()

    department_tree["columns"] = ("Department ID","Department NAME")
    department_tree['show'] = 'headings'
    department_tree.heading('Department NAME',text="Department NAME",anchor=W)
    department_tree.heading('Department ID',text="Department ID",anchor=W)
    read_department_tree()

def read_department_tree():
    department_tree.delete(*department_tree.get_children())

    conn = create_connection(database)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM department")
    fetch = cursor.fetchall()
    print(fetch)
    for data in fetch:
        department_tree.insert('','end',values=(data[0],data[1]))
    cursor.close()
    conn.close()


def add_new_department():
    sql_create_projects_table = """ CREATE TABLE IF NOT EXISTS department (Department_id INTEGER PRIMARY KEY  NOT NULL,
                                                                           Department_name TEXT NOT NULL
                                                                            ); """
    data = [new_department_id.get(),new_department.get()]
    # create a database connection
    conn = create_connection(database)
    cursor = conn.cursor()

    if conn is not None:
        # create projects table
        create_table(conn,sql_create_projects_table)
    else:
        print("Error! cannot create the database connection.")

    with conn:
        try:
            sql = ''' INSERT INTO Department(Department_id,Department_name)
                      VALUES(?,?) '''
            create_project(conn,data,sql)
        except IntegrityError:
            print(IntegrityError)
    cursor.close()

    conn.close()
    read_department_tree()


def adminLogin():
    screen.withdraw()
    global screen2
    screen2 = Toplevel(screen)
    screen2.title("Login")
    screen2.geometry("300x300")
    Top = Frame(screen2,width=300,bd=5,relief=RIDGE)
    Top.pack(side=TOP)
    Label(Top,text="ADMIN LOGIN",font=('Segoe UI Black','12')).pack()

    global username_verify
    global password_verify

    username_verify = StringVar()
    password_verify = StringVar()

    global username_entry1
    global password_entry1

    Label(screen2,text="Username * ",font=('Segoe UI Black','12'),width=100).pack()
    username_entry1 = Entry(screen2,border=2,bd=5,width=30,textvariable=username_verify)
    username_entry1.pack()
    Label(screen2,text="").pack()

    Label(screen2,text="Password * ",font=('Segoe UI Black','12'),width=100).pack()
    password_entry1 = Entry(screen2,border=2,bd=5,width=30,textvariable=password_verify)
    password_entry1.pack()
    Label(screen2,text="").pack()

    Button(screen2,text="Login",font=('Segoe UI Black','10'),width=100,border=4,
                     pady=10,command=login_verify).pack()
    Button(screen2,text="Back to Main Screen ",font=('Segoe UI Black','10'),width=100,border=4,
                     pady=10,command=back_to_main_login).pack(side=BOTTOM)


def adminPanel():

    screen2.withdraw()
    global screen1
    screen1 = Toplevel(screen)
    screen1.title("Register")
    screen1.geometry("500x300")
    Top = Frame(screen1,width=500,height=100,bd=10,relief=RIDGE)
    Top.pack(side=TOP)
    Bottom = Frame(Top,width=500,height=100,bd=10,relief=RIDGE)
    Bottom.pack(side=BOTTOM)
    # add department
    Label(Top,font=('Segoe UI Black','13'),border=2,text="ADMIN PANNEL").pack()
    Button(Top,text="Add Department ",font=('Segoe UI Black','10'),width=300,border=8,height=2,
                     pady=10,command=add_department).pack()

    Button(Top,text="View-edit-employes",font=('Segoe UI Black','10'),width=300,border=8,height=2,
                     pady=10,command=lambda: login_sucess('admin')).pack()

    Button(Bottom,text="Back to Main Screen ",font=('Segoe UI Black','10'),width=300,border=8,height=2,
                     pady=10,command=back_to_main_register).pack()


def back_to_main_register():
    screen1.destroy()
    screen.deiconify()

def back_to_main_login():
    screen2.destroy()
    screen.deiconify()


def login():
    screen.withdraw()
    global screen2
    screen2 = Toplevel(screen)
    screen2.title("Login")
    screen2.geometry("300x300")
    Top = Frame(screen2,width=300,bd=5,relief=RIDGE)
    Top.pack(side=TOP)
    Label(Top,text="MANAGER LOGIN",font=('Segoe UI Black','12')).pack()

    global username_verify
    global password_verify

    username_verify = StringVar()
    password_verify = StringVar()

    global username_entry1
    global password_entry1

    Label(screen2,text="Username * ",font=('Segoe UI Black','12'),width=100).pack()
    username_entry1 = Entry(screen2,textvariable=username_verify,border=2,bd=5,width=30)
    username_entry1.pack()
    Label(screen2,text="").pack()

    Label(screen2,text="Manager ID * ",font=('Segoe UI Black','12'),width=100).pack()
    password_entry1 = Entry(screen2,border=2,bd=5,width=30,textvariable=password_verify)
    password_entry1.pack()
    Label(screen2,text="").pack()

    Button(screen2,text="Login",font=('Segoe UI Black','10'),width=100,border=4,
                     pady=10,command=login_verify).pack()
    Button(screen2,text="Back to Main Screen ",font=('Segoe UI Black','10'),width=100,border=4,
                     pady=10,command=back_to_main_login).pack(side=BOTTOM)


from PIL import ImageTk,Image


def main_screen():
    global screen
    screen = Tk()
    screen.geometry("500x300")
    screen.title("Notes 1.0")
    Top = Frame(screen,width=300,bd=10,relief=RIDGE)
    Top.pack(side=TOP)
    # img = ImageTk.PhotoImage(Image.open(r"C:\Users\Dell\Desktop\a.png"))
    # image=Label(screen,image=img)
    # image.pack()
    Label(Top,text="DEPARTMENT RECORDS",bg="grey",width="300",height="2",font=("Calibri",13)).pack()
    Label(text="").pack()
    Button(text="Manager Login",font=('Segoe UI Black','10'),width=20,border=8,height=2,
                     pady=10,command=login).pack()
    Label(text="").pack()
    Button(text="Administrator",font=('Segoe UI Black','10'),width=20,border=8,height=2,
                     pady=10,command=adminLogin).pack()

    screen.mainloop()

main_screen()
