from tkinter import *
from tkinter import ttk
from tkcalendar import DateEntry
from tkinter import messagebox
from add_employee import addEmployee
import pymysql
class employee:
    def __init__(self,root,parent):
        self.root =root
        self.root.resizable(0,0)
        self.root.geometry('1000x546+230+120')
        self.root.iconbitmap("D:/phone/gui/code/inventory_system/employee__icon.ico")
        self.root.config(bg="#FFFFFF")
        self.root.grab_set()
        self.root.transient(parent)
        self.root.focus_force()
        #heading
        self.titlelable =Label(self.root,text="Manage Employees",font=("times new roman",20,'bold'),bg="#0f4d7d",fg="white")
        self.titlelable.place(x=0,y=0,relwidth=1)
        #main frame
        frame = Frame(self.root,bg="white")
        frame.place(x=0,y=36,relwidth=1)
        #top frame
        self.top_frame =Frame(frame,bg="#FFFFFF",height=80)
        self.top_frame.pack(fill=X)
        self.combo_box = ttk.Combobox(self.top_frame,values=("emp_id","name","email"),font=("times new roman",12,"bold"),state="readonly")
        self.combo_box.set("Search by")
        self.combo_box.grid(row=0,column=0, padx=50,pady=15)
        #search entery
        self.search_entry = Entry(self.top_frame, font=("times new roman",12),bg="lightyellow")
        self.search_entry.grid(row=0,column=1)
        self.search_button =Button(self.top_frame,text="Search",font=("times new roman",12),width=10,cursor="hand2",bg="#0f4d7d",
                                   fg="white",command=lambda:self.majorfunction("se"))
        self.search_button.grid(row=0,column=3,padx=30)
        self.showall_button =Button(self.top_frame,text="Show all",font=("times new roman",12),width=10, cursor="hand2",bg="#0f4d7d",
                                    fg="white",command=lambda:self.majorfunction("sa"))
        self.showall_button.grid(row=0,column=4)
        self.add_employee = Button(self.top_frame, text="Add employee", bg="#0A8F36",fg="white",font=("times new roman",12),width=10,
                                   command=lambda:self.mainfunction("A"))
        self.add_employee.grid(row=0,column=5,padx=50)
        
        #middle frame
        self.middle_frame =Frame(frame)
        self.middle_frame.pack()
        #scrol bars
        horizont_scroll = Scrollbar(self.middle_frame,orient=HORIZONTAL)
        vertical_scroll = Scrollbar(self.middle_frame,orient=VERTICAL)
        #employee table
        self.employee_table =ttk.Treeview(self.middle_frame, columns=("empid",'name','contact','email','address','dob','gender','doj','employement_type',
            'workshift','education','salary','usertype'),show="headings",yscrollcommand=vertical_scroll.set,
            xscrollcommand=horizont_scroll.set,height=9)
        self.details_display()
        horizont_scroll.pack(side=BOTTOM,fill=X,padx=0)
        vertical_scroll.pack(side=RIGHT,fill=Y)
        horizont_scroll.config(command=self.employee_table.xview)
        vertical_scroll.config(command=self.employee_table.yview)
        self.employee_table.heading('empid',text='EmpId')
        self.employee_table.heading('name',text='Name')
        self.employee_table.heading('email',text='Email')
        self.employee_table.heading('contact',text='Contact')
        self.employee_table.heading('address',text='Address')
        self.employee_table.heading('gender',text='Gender')
        self.employee_table.heading('dob',text='Date of birth')
        self.employee_table.heading('employement_type',text='Employement_type')
        self.employee_table.heading('education',text='Education')
        self.employee_table.heading('workshift',text='Work_shift',)
        self.employee_table.heading('doj',text='Date of joining')
        self.employee_table.heading('salary',text='Salary')
        self.employee_table.heading('usertype',text='User_type')
        self.employee_table.pack(pady=10)
        self.employee_table.column('empid',width=80)
        self.employee_table.column('name',width=240)
        self.employee_table.column('email',width=240)
        self.employee_table.column('gender',width=80)
        self.employee_table.column('dob',width=120)
        self.employee_table.column('contact',width=120)
        self.employee_table.column('doj',width=120)
        self.employee_table.column('employement_type',width=130)
        self.employee_table.column('workshift',width=130)
        self.employee_table.column('salary',width=100)
        self.employee_table.column('usertype',width=130)
        #details frame
        self.details_frame =Frame(frame,bg="navajo white")
        #empid
        empid = Label(self.details_frame,text="Emp_id",font=("times new roman",11,"bold"),bg="navajo white")
        empid.grid(row=0,column=0,sticky=W,pady=8)
        self.empid = Entry(self.details_frame, font=("times new roman",12),bg="lightyellow")
        self.empid.grid(row=0,column=1)
        #name
        name= Label(self.details_frame,text="Name",font=("times new roman",11,"bold"),bg="navajo white")
        name.grid(row=1,column=0,sticky=W)
        self.name = Entry(self.details_frame, font=("times new roman",12),bg="lightyellow")
        self.name.grid(row=1,column=1)
        #email
        email = Label(self.details_frame,text="Email",font=("times new roman",11,"bold"),bg="navajo white")
        email.grid(row=2,column=0,sticky=W,pady=8)
        self.email = Entry(self.details_frame, font=("times new roman",12),bg="lightyellow")
        self.email.grid(row=2,column=1)
        #contact
        contact = Label(self.details_frame,text="Contact",font=("times new roman",11,"bold"),bg="navajo white")
        contact.grid(row=3,column=0,sticky=W)
        self.contact = Entry(self.details_frame, font=("times new roman",12),bg="lightyellow")
        self.contact.grid(row=3,column=1,pady=16)
        #address
        address= Label(self.details_frame,text="Address",font=("times new roman",11,"bold"),bg="navajo white")
        address.grid(row=0,column=2,rowspan=2,sticky=W)
        self.address = Text(self.details_frame, font=("times new roman",12),width=19,height=3,bg="lightyellow")
        self.address.grid(row=0,column=3,sticky=W,rowspan=2)
        #date of joining
        doj= Label(self.details_frame,text="Joining date",font=("times new roman",11,"bold"),bg="navajo white")
        doj.grid(row=2,column=2,sticky=W)
        self.doj = DateEntry(self.details_frame,bg="lightyellow",width=17,font=("times new roman",11,"bold"))
        self.doj.grid(row=2,column=3,sticky=W)
        #gender
        gender = Label(self.details_frame,text="Gender",font=("times new roman",11,"bold"),bg="navajo white")
        gender.grid(row=3,column=2,sticky=W)
        self.gender = ttk.Combobox(self.details_frame, values=("Male","Female"), font=("times new roman",12),state="readonly",width=17)
        self.gender.grid(row=3,column=3,sticky=W)
         #date of birth
        dob = Label(self.details_frame,text="Date of birth",font=("times new roman",11,"bold"),bg="navajo white")
        dob.grid(row=0,column=4,sticky=W)
        self.dob = DateEntry(self.details_frame, font=("times new roman",12),width=17,bg="lightyellow")
        self.dob.grid(row=0,column=5,sticky=W)
        #employment type
        emp_type = Label(self.details_frame,text="Employment type",font=("times new roman",11,"bold"),bg="navajo white")
        emp_type.grid(row=1,column=4,sticky=W)
        self.emp_type = Entry(self.details_frame, font=("times new roman",12),bg="lightyellow")
        self.emp_type.grid(row=1,column=5)
        #shift
        shift = Label(self.details_frame,text="Shift",font=("times new roman",11,"bold"),bg="navajo white")
        shift.grid(row=2,column=4,sticky=W)  
        self.shift = ttk.Combobox(self.details_frame, values=("Morning","Evening","Day","Night"), font=("times new roman",12),
                                  state="readonly",width=17)
        self.shift.grid(row=2,column=5)
        #education
        education= Label(self.details_frame,text="Education",font=("times new roman",11,"bold"),bg="navajo white")
        education.grid(row=3,column=4,sticky=W)
        self.education =  ttk.Combobox(self.details_frame, values=("None","Degree","High school","Primary"), font=("times new roman",12),
                                       state="readonly",width=17)
        self.education.grid(row=3,column=5)
        #salary
        salary= Label(self.details_frame,text="Salary",font=("times new roman",11,"bold"),bg="navajo white")
        salary.grid(row=0,column=6,sticky=W)
        self.salary = Entry(self.details_frame, font=("times new roman",12),bg="lightyellow")
        self.salary.grid(row=0,column=7)
        #user type
        user_type= Label(self.details_frame,text="User type",font=("times new roman",11,"bold"),bg="navajo white")
        user_type.grid(row=1,column=6,sticky=W)
        self.user_type = ttk.Combobox(self.details_frame,values=("Admin","Manager","Cashier","Not a user"),state="readonly",
                                      font=("times new roman",12),width=17)
        self.user_type.grid(row=1,column=7)
        #bottom frame
        self.bottom_frame = Frame(frame, bg="white")
        self.bottom_frame.pack( )
        self.update = Button(self.bottom_frame, text="Update", bg="#0A8F36",fg="white",font=("times new roman",12),
                             command=lambda:self.majorfunction("u"),width=10,state="disabled")
        self.update.grid(row=0,column=0,padx=10,pady=4)
        self.delet= Button(self.bottom_frame, text="Delete", bg="#A80808",fg="white",font=("times new roman",12),width=10,
                           command=lambda:self.majorfunction("d"),state="disabled")
        self.delet.grid(row=0,column=1,padx=10,pady=4)
        self.employee_table.bind("<<TreeviewSelect>>",self.show)
    #functions
    def close(self):
        self.root.protocol("WM_DELET_WINDOW",self.on_close)
    def on_close(self):
        self.root.grab_release()
        self.root.destroy()
        self.parent.focus_set()
        
    #open add employee window
    def mainfunction(self,choice):
         if choice =="A":
             root = Toplevel()
             obj = addEmployee(root,self.root,self.details_display)
             root.mainloop()
    def connection(self):
        return pymysql.connect(host="localhost",user="root",password="1996",database="inventory")
        
    def details_display(self):
        try:
            con= self.connection()
            mycursor = con.cursor()
            mycursor.execute("SELECT*FROM employee_data")
            employee_record = mycursor.fetchall()
            self.employee_table.delete(*self.employee_table.get_children())
            for record in employee_record:
                self.employee_table.insert("",END,values = record)
            con.close()
        except:
            messagebox.showerror("Error","Something went wrong",parent=self.root)
    def show(self,event):
        y =self.employee_table.focus()
        data = self.employee_table.item(y,"values")
        if data!='':  
            self.empid.delete(0,END)
            self.empid.insert(0,data[0])
            self.name.delete(0,END)
            self.name.insert(0,data[1])
            self.email.delete(0,END)
            self.email.insert(0,data[3])
            self.contact.delete(0,END)
            self.contact.insert(0,data[2])
            self.address.delete(1.0,END)
            self.address.insert(END,data[4])
            self.doj.delete(0,END)
            self.doj.insert(0,data[7])
            self.gender.delete(0,END)
            self.gender.set(data[6])
            self.dob.delete(0,END)
            self.dob.insert(0,data[5])
            self.emp_type.delete(0,END)
            self.emp_type.insert(0,data[8])
            self.shift.delete(0,END)
            self.shift.set(data[9])
            self.education.delete(0,END)
            self.education.set(data[10])
            self.salary.delete(0,END)
            self.salary.insert(0,data[11])
            self.user_type.delete(0,END)
            self.user_type.set(data[12])
            self.details_frame.pack(before=self.bottom_frame)
            self.update.config(state="normal")
            self.delet.config(state="normal")
        else:
            self.details_frame.pack_forget()
            self.update.config(state="disabled")
            self.delet.config(state="disabled")
    def majorfunction(self,choice):
        con = self.connection()
        mycursor = con.cursor()
        if choice == "d":
            y =self.employee_table.focus()
            data = self.employee_table.item(y,"values")
            todelet = data[0]
            action ="DELETE FROM employee_data WHERE emp_id = %s"
            mycursor.execute(action,todelet)
            if messagebox.askyesnocancel("","Once the record is deleted, it can not be recovered\nAre you sure you want to delete this record",parent=self.root):
                con.commit()
                messagebox.showinfo("","Record successfully deleted",parent=self.root)
                con.close()
                self.details_display()
                return
            else:
                con.close()
                return
            print(todelet)  
        elif choice == "u":
            y =self.employee_table.focus()
            data = self.employee_table.item(y,"values")
            toupdate = data[0]
            action ='''UPDATE employee_data SET name=%s,contact=%s,email=%s,address=%s,date_of_birth=%s,gender=%s,date_of_joining=%s,
            employee_type=%s,shift=%s,education=%s,salary=%s,user_type=%s WHERE emp_id=%s'''
            mycursor.execute(action,(self.name.get(),self.contact.get(),self.email.get(),self.address.get(1.0,END),self.dob.get(),
            self.gender.get(),self.doj.get(),self.emp_type.get(),self.shift.get(),self.education.get(),self.salary.get(),
            self.user_type.get(),toupdate))
            if messagebox.askyesnocancel("Update",f"Are you sure you want to update the data of {self.name.get()}",parent=self.root):
                con.commit()
                messagebox.showinfo("","Record successfully deleted",parent=self.root)
                con.close()
                self.details_display()
                return
        elif choice == "sa":
            self.details_display()
        else:
            if self.search_entry.get()!='':
                if self.combo_box.get()=="emp_id":
                    query = '''SELECT*FROM employee_data WHERE emp_id LIKE %s
                    '''
                    mycursor.execute(query,f"%{self.search_entry.get()}%")
                    search =mycursor.fetchall()
                    if len(search)==0:
                        messagebox.showerror("Search error",f"No employee with id {self.search_entry.get()}!",parent=self.root)
                    else:
                        self.employee_table.delete(*self.employee_table.get_children())
                        for row in search:
                            self.employee_table.insert("",END,values = row)
                            con.close()
                elif self.combo_box.get()=="name":
                    query = '''SELECT*FROM employee_data WHERE name LIKE %s
                    '''
                    mycursor.execute(query,f"%{self.search_entry.get()}%")
                    search =mycursor.fetchall()
                    if len(search)==0:
                        messagebox.showerror("Search error",f"No employee with name {self.search_entry.get()}!",parent=self.root)
                    else:
                        self.employee_table.delete(*self.employee_table.get_children())
                        for row in search:
                            self.employee_table.insert("",END,values = row)
                            con.close()
                elif self.combo_box.get()=="email":
                    query = '''SELECT*FROM employee_data WHERE email LIKE %s
                    '''
                    mycursor.execute(query,f"%{self.search_entry.get()}%")
                    search =mycursor.fetchall()
                    if len(search)==0:
                        messagebox.showerror("Search error",f"No employee with email {self.search_entry.get()}!",parent=self.root)
                    else:
                        self.employee_table.delete(*self.employee_table.get_children())
                        for row in search:
                            self.employee_table.insert("",END,values = row)
                            con.close()
                else:
                  messagebox.showerror("Search error","You did not specify search creteria!",parent=self.root)      
            else:
                messagebox.showerror("Search error","The search entry is empty!",parent=self.root)    
            