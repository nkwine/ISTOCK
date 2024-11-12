from tkinter import *
from tkcalendar import DateEntry
from tkinter import messagebox,ttk
import re
import pymysql
class addEmployee:
    def __init__(self,root,parent,on_clos=None):
        self.parent = parent
        self.root =root
        self.on_clos = on_clos
        self.root.geometry('800x500+300+50')
        self.root.iconbitmap("employee__icon.ico")
        self.root.resizable(0,0)
        self.root.config(bg="white")
        self.root.grab_set()
        self.root.transient(parent)
        self.root.bind("<Destroy>",self.on_close)
        #heading
        self.titlelable =Label(self.root,text="Add New Employee",font=("times new roman",20,'bold'),bg="#0f4d7d",fg="white")
        self.titlelable.place(x=0,y=0,relwidth=1)
        #main frame
        frame = Frame(self.root,bg="white")
        frame.place(x=30,y=40,relwidth=1)
        #name
        name= Label(frame,text="Name",font=("times new roman",11,"bold"),bg="white")
        name.grid(row=0,column=0,sticky=W,pady=12)
        self.name = Entry(frame, font=("times new roman",12),bg="lightyellow")
        self.name.grid(row=0,column=1,padx=20)
        #email
        email = Label(frame,text="Email",font=("times new roman",11,"bold"),bg="white")
        email.grid(row=1,column=0,sticky=W,pady=12)
        self.email = Entry(frame, font=("times new roman",12),bg="lightyellow")
        self.email.grid(row=1,column=1,padx=20)
        #contact
        contact = Label(frame,text="Contact",font=("times new roman",13,"bold"),bg="white")
        contact.grid(row=2,column=0,sticky=W)
        self.contact = Entry(frame, font=("times new roman",12),bg="lightyellow",fg="grey")
        self.contact.grid(row=2,column=1,pady=12,padx=20)
        self.contact.insert(0,"07...")
        self.contact.bind("<FocusIn>",self.focus_in)
        self.contact.bind("<FocusOut>",self.focus_out)
        #address
        address= Label(frame,text="Address",font=("times new roman",11,"bold"),bg="white")
        address.grid(row=3,column=0,rowspan=3,sticky=W)
        self.address = Text(frame, font=("times new roman",12),width=20,height=3,bg="lightyellow")
        self.address.grid(row=3,column=1,sticky=W,rowspan=3,padx=20)
        #date of joining
        doj= Label(frame,text="Joining date",font=("times new roman",11,"bold"),bg="white")
        doj.grid(row=6,column=0,sticky=W,pady=12)
        self.doj = DateEntry(frame,bg="lightyellow",width=17,font=("times new roman",11,"bold"))
        self.doj.grid(row=6,column=1,sticky=W,padx=20)
        #gender
        gender = Label(frame,text="Gender",font=("times new roman",11,"bold"),bg="white")
        gender.grid(row=0,column=2,sticky=W)
        self.gender = ttk.Combobox(frame, values=("Male","Female"), font=("times new roman",12),state="readonly",width=17)
        self.gender.grid(row=0,column=3,sticky=W,padx=20)
         #date of birth
        dob = Label(frame,text="Date of birth",font=("times new roman",11,"bold"),bg="white")
        dob.grid(row=1,column=2,sticky=W)
        self.dob = DateEntry(frame, font=("times new roman",12),width=17,bg="lightyellow")
        self.dob.grid(row=1,column=3,sticky=W,padx=20)
        #employment type
        emp_type = Label(frame,text="Employment type",font=("times new roman",11,"bold"),bg="white")
        emp_type.grid(row=2,column=2,sticky=W)
        self.emp_type = Entry(frame, font=("times new roman",12),bg="lightyellow")
        self.emp_type.grid(row=2,column=3,padx=20)
        #shift
        shift = Label(frame,text="Shift",font=("times new roman",11,"bold"),bg="white")
        shift.grid(row=3,column=2,sticky=W)  
        self.shift = ttk.Combobox(frame, values=("Morning","Evening","Day","Night"), font=("times new roman",12),
                                  state="readonly",width=17)
        self.shift.grid(row=3,column=3,padx=20,pady=16)
        #education
        education= Label(frame,text="Education",font=("times new roman",11,"bold"),bg="white")
        education.grid(row=4,column=2,sticky=W)
        self.education =  ttk.Combobox(frame, values=("None","Degree","High school","Primary"), font=("times new roman",12),
                                       state="readonly",width=17)
        self.education.grid(row=4,column=3,padx=20)
        #salary
        salary= Label(frame,text="Salary",font=("times new roman",11,"bold"),bg="white")
        salary.grid(row=5,column=2,sticky=W)
        self.salary = Entry(frame, font=("times new roman",12),bg="lightyellow",fg="grey")
        self.salary.grid(row=5,column=3,padx=20,pady=16)
        self.salary.insert(0,"digits only, e.g 789000")
        self.salary.bind("<FocusIn>", self.safocus_in)
        self.salary.bind("<FocusOut>", self.safocus_out)
        #user type
        user_type= Label(frame,text="User type",font=("times new roman",11,"bold"),bg="white")
        user_type.grid(row=6,column=2,sticky=W)
        self.user_type = ttk.Combobox(frame,values=("Admin","Manager","Cashier","Not a user"),state="readonly",
                                      font=("times new roman",12),width=17)
        self.user_type.grid(row=6,column=3,padx=20)
        #bottom frame
        self.bottom_frame = Frame(self.root, bg="white")
        self.bottom_frame.place( x=200,y=370)
        self.save = Button(self.bottom_frame, text="Save", bg="#0A8F36",fg="white",font=("times new roman",12),width=10,
            command=lambda:self.add_employee(self.name.get(),self.contact.get(),self.email.get(),self.address.get(1.0,END),self.doj.get(),
            self.gender.get(),self.dob.get(),self.emp_type.get(),self.shift.get(),self.education.get(),self.salary.get(),self.user_type.get()))
        self.save.pack(padx=100)
         
    #functions
    #when window is closed
    def on_close(self,event):
        if self.on_clos:
            self.on_clos()
        self.root.grab_release()
        self.parent.focus_set()
        self.parent.grab_set()
    def focus_in(self,event):
        if self.contact.get()=="07...":
            self.contact.delete(0,END)
            self.contact.config(fg="black")
    def focus_out(self,event):
        if self.contact.get()=="":
            self.contact.insert(0,"07...")
            self.contact.config(fg="grey")
    def safocus_in(self,event):
        if self.salary.get()=="digits only, e.g 789000":
            self.salary.delete(0,END)
            self.salary.config(fg="black")
    def safocus_out(self,event):
        if self.salary.get()=="":
            self.salary.insert(0,"digits only, e.g 789000")
            self.salary.config(fg="grey")
    def add_employee(self,name,contact,email,address,doj,gender,dob,emptype,shift,education,salary,usertype):
        try:
            if name == '' or contact == '' or address == '\n' or salary == '' or usertype == '':
                messagebox.showerror("Error","name , contact, address, salary, and usertype must be provided ",parent=self.root)
                return
            elif email !='':
                partern =r"[a-z,A-Z,0-9]+.+@gmail|yahoo\.com$"
                if re.search(partern,email):
                    pass
                else:
                    messagebox.showerror("Error","Invalid email address",parent=self.root)
                    return 
            try:
                number = int(contact)
                if len(contact)!=10 or contact[0]!="0":
                    messagebox.showerror("Error","Invalid contact",parent=self.root)
                    return
            except:
                messagebox.showerror("Error","Invalid contact",parent=self.root)
                return
            try:
                amount = int(salary)
            except:
                messagebox.showerror("Error","Invalid salary amount",parent=self.root)
                return
            try:
                con = pymysql.connect(host="localhost",user="root",password="1996")
                mycoursor = con.cursor()
                database = "use inventory"
                mycoursor.execute(database)
                table = '''CREATE TABLE IF NOT EXISTS employee_data(emp_id VARCHAR(20) PRIMARY KEY,name VARCHAR(30) NOT NULL,
                    contact VARCHAR(15) NOT NULL,email VARCHAR(30),address VARCHAR(200) NOT NULL,date_of_birth VARCHAR(10),gender VARCHAR(10),
                    date_of_joining VARCHAR(10),employee_type VARCHAR(15), shift VARCHAR(10),education VARCHAR(10),salary VARCHAR(10) NOT NULL,
                    user_type VARCHAR(10) NOT NULL)'''
                mycoursor.execute(table)
                id = "SELECT MAX(SUBSTR(emp_id,4))FROM employee_data"
                mycoursor.execute(id)
                max_id = int(mycoursor.fetchone()[0])
                initial = name[0:2].capitalize()
                if max_id is None:
                    new_id = f"{initial}-000001"
                else:
                    new_id =f"{initial}-{str(max_id+1).zfill(6)}"
                query = "INSERT INTO employee_data VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                values =(new_id,name,contact,email,address,dob,gender,doj,emptype,shift,education,salary,usertype)
                mycoursor.execute(query,values)
                if messagebox.askyesnocancel("","Are you sure you want to save this employee data?",parent=self.root):
                    con.commit()
                    messagebox.showinfo("","Employee data saved successfully!",parent=self.root)
                    self.root.destroy()
                    self.parent.focus_set()
                    self.parent.grab_set() 
                con.close()
            except Exception as e:
                messagebox.showerror("Error",e,parent=self.root)
        except:
            return        

            