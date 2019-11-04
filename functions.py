global database
database = "emp_info.db"
# functions
def delete3():
  screen4.destroy()

def delete4():
  screen5.destroy()
# functions


def create_project(conn,project):
    sql = ''' INSERT INTO data(employee_id,employee_name,gender,b_date
               ,email,qualification,work_exp,mob_num,job_title,job_des
               ,work_num,work_loc,salary,address)
              VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql,project)
    return cur.lastrowid

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
    cursor.execute("SELECT * FROM `data`")
    fetch = cursor.fetchall()
    for data in fetch:
        tree.insert('','end',values=(data[0],data[1],data[2],data[3],data[4],data[5],data[6]
                                     ,data[7],data[8],data[9],data[10],data[11],data[12],data[13]))
    cursor.close()
    conn.close()

def Exit():
    result = tkMessageBox.askquestion('Exit','Are you sure you want to exit?',icon="warning")
    if result == 'yes':
        window.destroy()

def update():
    conn = create_connection(database)
    if not tree.selection():
        print("ERROR")
    else:
        curItem = tree.focus()
        contents = (tree.item(curItem))
        selecteditem = contents['values']
        print(selecteditem)
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        if check():
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
            cur.close()
            conn.close()
            txt_result.config(text="Successfully updated the data",fg="green")
            Clear()
            read()

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
    print("work=",workExp.get())
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

def jobdepartck(self):
    if not jobDepartmentText.get():
        txt_result.config(text="Please complete the required field!: JOB DEPARTMENT",fg="red")
    else:
        txt_result.config(text=" ")
        return True
    return False

def jobtitleck(self):
    if not jobtitleText.get():
        txt_result.config(text="Please complete the required field!: JOB TITLE",fg="red")
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
        print(var.get())
        txt_result.config(text="Please complete the required field!: GENDER",fg="red")
    elif not emailText.get() or not re.match("^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$",emailText.get(),
                                             re.IGNORECASE):
        txt_result.config(text="Please complete the required field!: EMAIL ADDRESS",fg="red")
    elif not mobileText.get() or not mobileText.get().isdigit() or not re.match("(0/91)?[7-9][0-9]{9}",
                                                                                str(mobileText.get())):
        txt_result.config(text="Please complete the required field!: MOBILE NUMBER ",fg="red")
    elif not workExp.get() or not workExp.get().isdigit():
        print("work=",workExp.get())
        txt_result.config(text="Please complete the required field!: WORK EXPERIENCE ",fg="red")
    elif not Qualification.get():
        txt_result.config(text="Please complete the required field!: QUALIFICATION",fg="red")
    elif not jobDepartmentText.get():
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
        if conn is not None:
            # create projects table
            create_table(conn,sql_create_projects_table)
        else:
            print("Error! cannot create the database connection.")

        with conn:
            try:
                create_project(conn,data)
                tree.delete(*tree.get_children())
                cursor.execute("SELECT * FROM `data`")
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
    jobtitle.set(selecteditem[8])
    jobdes.set(selecteditem[9])
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