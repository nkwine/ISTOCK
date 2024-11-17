from tkinter import *
from tkcalendar import DateEntry
from tkinter import messagebox,ttk
import re
import pymysql
class addsupplier:
    def __init__(self,root,parent,on_clos=None):
        self.parent = parent
        self.root =root
        self.on_clos =on_clos
        self.root.geometry('800x560+300+50')
        self.root.iconbitmap("D:/phone/gui/code/inventory_system/employee__icon.ico")
        self.root.resizable(0,0)
        self.root.config(bg="white")
        self.root.grab_set()
        self.root.transient(parent)
        self.root.bind("<Destroy>",self.on_close)
        #heading
        self.titlelable =Label(self.root,text="Add New Supplier",font=("times new roman",20,'bold'),bg="#0f4d7d",fg="white")
        self.titlelable.place(x=0,y=0,relwidth=1)
        #main frame
        frame = Frame(self.root,bg="white")
        frame.place(x=30,y=40,relwidth=1)
        #name
        name= Label(frame,text="Name",font=("times new roman",11,"bold"),bg="white")
        name.grid(row=0,column=0,sticky=W,pady=12)
        self.name = Entry(frame, font=("times new roman",12),bg="lightyellow",width=30)
        self.name.grid(row=0,column=1,padx=20)
        #address
        address = Label(frame,text="Address",font=("times new roman",12,"bold"),bg="white")
        address.grid(row=1,column=0,sticky=W,rowspan=2)
        self.address = Text(frame,font=("times new roman",12),bg="lightyellow",width=30,height=5)
        self.address.grid(row=1,column=1,rowspan=2,padx=20,pady=10)
        #contact_person
        contact_person = Label(frame,text="Contact_person",font=("times new roman",13,"bold"),bg="white")
        contact_person.grid(row=3,column=0,sticky=W,)
        self.contact_person = Entry(frame, font=("times new roman",12),bg="lightyellow",width=30)
        self.contact_person.grid(row=3,column=1,sticky=W,padx=20,pady=10)
        #contact
        contact = Label(frame,text="Contact",font=("times new roman",12,"bold"),bg="white")
        contact.grid(row=4,column=0,sticky=W)
        self.contact =Entry(frame, font=("times new roman",12),bg="lightyellow",fg="grey",width=30)
        self.contact.grid(row=4,column=1,sticky=W,padx=20,pady=10)
        self.contact.insert(0,"07...")
        self.contact.bind("<FocusIn>",self.focus_in)
        self.contact.bind("<FocusOut>",self.focus_out)
        #email
        email = Label(frame,text="Email(optional)",font=("times new roman",12,"bold"),bg="white")
        email.grid(row=5,column=0,sticky=W,)
        self.email = Entry(frame, font=("times new roman",12),bg="lightyellow",width=30)
        self.email.grid(row=5,column=1,sticky=W,padx=20,pady=10)
        # products
        product_outer_frame = Frame(frame,bg="white")
        product_outer_frame.grid(row=0,column=2,rowspan=6,pady=20) 
        product_frame = Frame(product_outer_frame,bg="white")
        product_frame.pack()       
        products = Label(product_frame,text="Products\nClick on a product to select it",font=("times new roman",12,"bold"),bg="white")
        products.pack()
        yscroll = Scrollbar(product_frame,orient=VERTICAL)
        xscroll = Scrollbar(product_frame,orient=HORIZONTAL)
        self.products = Listbox(product_frame,bg="lightyellow",fg="black",yscrollcommand=yscroll.set,xscrollcommand=xscroll.set,
            height=13,width=30,selectmode=MULTIPLE)
        yscroll.pack(side=RIGHT,fill=Y)
        xscroll.pack(side=BOTTOM,fill=X)
        yscroll.config(command=self.products.yview)
        xscroll.config(command=self.products.xview)
        self.products.pack()
        # more_products = Label(product_outer_frame,text="In the space below, list any extra products,\nuse a coma(,) to seperate products",
        #                       font=("times new roman",12,"bold"),bg="white")
        # more_products.pack()
        # self.more_products = Text(product_outer_frame, font=("times new roman",12),bg="lightyellow",width=25,height=4)
        # self.more_products.pack()
         #bottom frame
        self.bottom_frame = Frame(self.root, bg="white")
        self.bottom_frame.place( x=200,y=480)
        self.save = Button(self.bottom_frame, text="Save", bg="#0A8F36",fg="white",font=("times new roman",12),width=10,
            command=lambda:self.add_supplier(self.name.get(),self.address.get(1.0,END),self.contact_person.get(),self.contact.get(),self.email.get()))
        self.save.pack(padx=100)
        self.produt_list()
         
    #functions
    #when window is closed
    def database_connection(self,pas):
        try:
            return pymysql.connect(host="localhost",user="root",password=f"{pas}",database="inventory")
        except Exception as e:
            messagebox.showerror("Error",f"Failed connection {e}",parent=self.root) 
    def produt_list(self):
        con = self.database_connection(1996)
        mycursor = con.cursor()
        query = "SELECT* FROM products"
        self.products.delete(0,END)
        mycursor.execute(query)
        for itme in mycursor.fetchall():
            self.products.insert(END,itme[1])
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
    def add_supplier(self,name,address,contact_person,contact,email):
        li =[]
        y =self.products.curselection()
        for k in y:
            li.append(self.products.get(k))
        # a =self.more_products.get("1.0",END).strip()
        # if len(a)>0:
        #     a=a.split(",")
        #     for value in a:
        #         if value not in li:
        #             li.append(value)
        final = ",".join(li)
        try:
            if name.strip() == '' or address == '\n'or contact_person.strip()  == '' or contact.strip()  == '' or contact.strip()=='07...':
                messagebox.showerror("Error","name ,  address,contact person , contact, product must be provided!",parent=self.root)
                return
            if len(final)==0:
                messagebox.showerror("Error","Provide products for this supplier please",parent=self.root) 
                return 
            if len(contact)!=10 or contact[0]!="0":
                messagebox.showerror("Error","Invalid contact",parent=self.root)
                return
            if email !='':
                partern =r"^[a-z,A-Z,0-9]+\S[a-z,A-Z,0-9]+\S@(gmail|yahoo)\.com$"
                if re.search(partern,email):
                    pass
                else:
                    messagebox.showerror("Error","Invalid email address",parent=self.root)
                    return
                 
            
    
            try:
                number = int(contact)
                pass
            except:
                messagebox.showerror("Error","Invalid contact",parent=self.root)
                return
            
            try:
                con = self.database_connection(1996)
                mycursor = con.cursor()
                table = '''CREATE TABLE IF NOT EXISTS suppliers(s_id VARCHAR(20) PRIMARY KEY,name VARCHAR(30) NOT NULL,
                address VARCHAR(200) NOT NULL,contact_person VARCHAR(200) NOT NULL,contact VARCHAR(15) NOT NULL,
                email VARCHAR(30),products VARCHAR(1000) NOT NULL)'''
                mycursor.execute(table)
                mycursor.execute("SELECT*FROM suppliers WHERE name = %s",name.lower())
                if len(mycursor.fetchall())>=1:
                        messagebox.showerror("Error","The spplier already eists!",parent=self.root)
                        con.close()
                        return
                id = "SELECT MAX(SUBSTR(s_id,4))FROM suppliers"
                mycursor.execute(id)
                max_id = mycursor.fetchone()[0]
                initial = name[0].capitalize()
                if max_id is None:
                    new_id = f"{initial}-0001"
                else:
                    max_id = int(max_id)
                    new_id =f"{initial}-{str(max_id+1).zfill(4)}"
                query = "INSERT INTO suppliers VALUES(%s,%s,%s,%s,%s,%s,%s)"
                values =(new_id,name.strip().lower(),address.strip(),contact_person.strip().capitalize(),contact,email,final)
                mycursor.execute(query,values)
                if messagebox.askyesnocancel("","Are you sure you want to save this supplier data?",parent=self.root):
                    con.commit()
                    messagebox.showinfo("","Supplier data saved successfully!",parent=self.root)
                    self.root.destroy()
                    self.parent.focus_set()
                    self.parent.grab_set() 
                con.close()
            except Exception as e:
                messagebox.showerror("Error",e,parent=self.root)
                return
        except:
            return        

            