from tkinter import *
from tkinter import ttk,messagebox
from add_supplier import addsupplier
from update_supplier import updatesupplier
import pymysql
class supplier:
    def __init__(self,root,parent):
        self.root =root
        self.root.resizable(0,0)
        self.root.geometry('1000x546+230+120')
        self.root.iconbitmap("employee__icon.ico")
        self.root.config(bg="#FFFFFF")
        self.root.grab_set()
        self.root.transient(parent)
        self.root.focus_force()
        
        #heading
        self.titlelable =Label(self.root,text="Manage Suppliers",font=("times new roman",20,'bold'),bg="#0f4d7d",fg="white")
        self.titlelable.place(x=0,y=0,relwidth=1)
        #main frame
        frame = Frame(self.root,bg="white")
        frame.place(x=0,y=36,relwidth=1)
        #top frame
        self.top_frame =Frame(frame,bg="#FFFFFF",height=80)
        self.top_frame.pack(fill=X)
        self.combo_box = ttk.Combobox(self.top_frame,values=("sup_id","name","email"),font=("times new roman",12,"bold"),state="readonly")
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
        self.add_supplier = Button(self.top_frame, text="Add supplier", bg="#0A8F36",fg="white",font=("times new roman",12),width=10,
                                   command=lambda:self.mainfunction("A"))
        self.add_supplier.grid(row=0,column=5,padx=50)
        
         #middle frame
        self.middle_frame =Frame(frame)
        self.middle_frame.pack()
        #scrol bars
        horizont_scroll = Scrollbar(self.middle_frame,orient=HORIZONTAL)
        vertical_scroll = Scrollbar(self.middle_frame,orient=VERTICAL)
        #supplier table
        self.supplier_table =ttk.Treeview(self.middle_frame, columns=("supid",'compname',"address","contact_person",'contact','email',
            'products'),show="headings",yscrollcommand=vertical_scroll.set,xscrollcommand=horizont_scroll.set,height=9)
        # self.details_display()
        horizont_scroll.pack(side=BOTTOM,fill=X,padx=0)
        vertical_scroll.pack(side=RIGHT,fill=Y)
        horizont_scroll.config(command=self.supplier_table.xview)
        vertical_scroll.config(command=self.supplier_table.yview)
        self.supplier_table.heading('supid',text='supplier_Id')
        self.supplier_table.heading('compname',text='Name')
        self.supplier_table.heading('address',text='Address')
        self.supplier_table.heading('contact_person',text='Contact_person')
        self.supplier_table.heading('contact',text='Contact')
        self.supplier_table.heading('email',text='Email')
        self.supplier_table.heading('products',text='Products')
        self.supplier_table.pack(pady=10)
        self.supplier_table.column('supid',width=80)
        self.supplier_table.column('compname',width=240)
        self.supplier_table.column('address',width=240)
        self.supplier_table.column('products',width=280)
       
        #details frame
        self.details_frame =Frame(frame,bg="navajo white")
        #supid
        supid = Label(self.details_frame,text="sup_id",font=("times new roman",12,"bold"),bg="navajo white")
        supid.grid(row=0,column=0,sticky=W,pady=8)
        self.supid = Entry(self.details_frame, font=("times new roman",12),bg="lightyellow",width=30)
        self.supid.grid(row=0,column=1)
        #company name
        compname= Label(self.details_frame,text="Company_name",font=("times new roman",12,"bold"),bg="navajo white")
        compname.grid(row=1,column=0,sticky=W)
        self.compname = Entry(self.details_frame, font=("times new roman",12),bg="lightyellow",width=30)
        self.compname.grid(row=1,column=1)
        #address
        address= Label(self.details_frame,text="Address",font=("times new roman",12,"bold"),bg="navajo white")
        address.grid(row=2,column=0,rowspan=2,sticky=W)
        self.address = Text(self.details_frame, font=("times new roman",12),width=30,height=3,bg="lightyellow")
        self.address.grid(row=2,column=1,sticky=W,rowspan=2,pady=8)
        #contact person
        contact_person = Label(self.details_frame,text="Contact_person",font=("times new roman",11,"bold"),bg="navajo white")
        contact_person.grid(row=0,column=2,sticky=W)
        self.contact_person = Entry(self.details_frame, font=("times new roman",12),bg="lightyellow",width=25)
        self.contact_person.grid(row=0,column=3,pady=16)
        #contact
        contact= Label(self.details_frame,text="Contact",font=("times new roman",12,"bold"),bg="navajo white")
        contact.grid(row=1,column=2,sticky=W)
        self.contact = Entry(self.details_frame, font=("times new roman",12),bg="lightyellow",width=25)
        self.contact.grid(row=1,column=3,sticky=W)
        #Email
        email= Label(self.details_frame,text="Email",font=("times new roman",11,"bold"),bg="navajo white")
        email.grid(row=2,column=2,sticky=W)
        self.email = Entry(self.details_frame,bg="lightyellow",width=25,font=("times new roman",12,"bold"))
        self.email.grid(row=2,column=3,sticky=W)
        #products
        products = Label(self.details_frame,text="Products",font=("times new roman",12,"bold"),bg="navajo white")
        products.grid(row=0,column=4,sticky=W)
        self.products =Text(self.details_frame, font=("times new roman",12),width=30,height=3,bg="lightyellow")
        self.products.grid(row=0,column=5,rowspan=2,pady=8)
        #bottom frame
        self.bottom_frame = Frame(frame, bg="white")
        self.bottom_frame.pack( )
        self.update = Button(self.bottom_frame, text="Update", bg="#0A8F36",fg="white",font=("times new roman",12),
                             command=lambda:self.majorfunction("u"),width=10,state="disabled")
        self.update.grid(row=0,column=0,padx=10,pady=4)
        self.delet= Button(self.bottom_frame, text="Delete", bg="#A80808",fg="white",font=("times new roman",12),width=10,
                            command=lambda:self.majorfunction("d"),state="disabled")
        self.delet.grid(row=0,column=1,padx=10,pady=4)
        self.supplier_table.bind("<<TreeviewSelect>>",self.show)
        self.details_display()
        
    #functions
    def mainfunction(self,choice):
         if choice =="A":
             root = Toplevel()
             obj = addsupplier(root,self.root,self.details_display)
             root.mainloop()
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
             obj = addsupplier(root,self.root,self.details_display)
             root.mainloop()
    def connection(self):
        return pymysql.connect(host="localhost",user="root",password="1996",database="inventory")
        
    def details_display(self):
        try:
            con= self.connection()
            mycursor = con.cursor()
            mycursor.execute("SELECT*FROM suppliers")
            supplier_record = mycursor.fetchall()
            self.supplier_table.delete(*self.supplier_table.get_children())
            for record in supplier_record:
                self.supplier_table.insert("",END,values = record)
            con.close()
        except:
            messagebox.showerror("Error",f"Something went wrong",parent=self.root)
    def show(self,event):
        y =self.supplier_table.focus()
        data = self.supplier_table.item(y,"values")
        if data!='':  
            self.supid.delete(0,END)
            self.supid.insert(0,data[0])
            self.compname.delete(0,END)
            self.compname.insert(0,data[1])
            self.address.delete(1.0,END)
            self.address.insert(END,data[2])
            self.contact_person.delete(0,END)
            self.contact_person.insert(0,data[3])
            self.contact.delete(0,END)
            self.contact.insert(0,data[4])
            self.email.delete(0,END)
            self.email.insert(0,data[5])
            self.products.delete(1.0,END)
            self.products.insert(END,data[6])
            self.update.config(state="normal")
            self.delet.config(state="normal")
            self.details_frame.pack(after= self.middle_frame)
        else:
            self.details_frame.pack_forget()
            self.update.config(state="disabled")
            self.delet.config(state="disabled")
    def database_connection(self,pas):
        try:
            return pymysql.connect(host="localhost",user="root",password=f"{pas}",database="inventory")
        except:
            messagebox.showerror("Error",f"Failed connection",parent=self.root) 
    def majorfunction(self,choice):
        con = self.database_connection(1996)
        mycursor = con.cursor()
        if choice == "d":
            y =self.supplier_table.focus()
            data = self.supplier_table.item(y,"values")
            todelet = data[0]
            action ="DELETE FROM suppliers WHERE s_id = %s"
            if messagebox.askyesnocancel("","Once the record is deleted, it can not be recovered\nAre you sure you want to delete this record",parent=self.root):
                mycursor.execute(action,todelet)
                con.commit()
                messagebox.showinfo("","Record successfully deleted",parent=self.root)
                con.close()
                self.details_display()
                return
            else:
                con.close()
                return 
        elif choice == "u":
            try:
                y =self.supplier_table.focus()
                data = self.supplier_table.item(y,"values")
                toupdate = data[0]
                root = Toplevel()
                obj = updatesupplier(root,self.root,toupdate,self.details_display)
                root.mainloop()
                # y =self.supplier_table.focus()
                # data = self.supplier_table.item(y,"values")
                # toupdate = data[0]
                # action ='''UPDATE suppliers SET name=%s,address=%s,contact_person=%s,contact=%s,email=%s,products=%s WHERE s_id=%s'''
                # if messagebox.askyesnocancel("Update",f"Are you sure you want to update the data of supplier {self.compname.get()}",parent=self.root):
                #     mycursor.execute(action,(self.compname.get().lower(),self.address.get(1.0,END),self.contact_person.get().capitalize(),self.contact.get(),
                #                             self.email.get(),self.products.get('1.0',END),toupdate))
                #     con.commit()
                #     messagebox.showinfo("","Record successfully updated",parent=self.root)
                #     con.close()
                #     self.details_display()
                #     return
            except Exception as e:
                messagebox.showerror("Error",f"Something went wrong{e}",parent=self.root)
        elif choice == "sa":
            self.details_display()
        else:
            try:
                if self.search_entry.get()!='':
                    if self.combo_box.get()=="sup_id":
                        query = '''SELECT*FROM suppliers WHERE s_id LIKE %s
                        '''
                        mycursor.execute(query,f"%{self.search_entry.get()}%")
                        search =mycursor.fetchall()
                        if len(search)==0:
                            messagebox.showerror("Search error",f"No supplier with id {self.search_entry.get()}!")
                        else:
                            self.supplier_table.delete(*self.supplier_table.get_children())
                            for row in search:
                                self.supplier_table.insert("",END,values = row)
                                con.close()
                    elif self.combo_box.get()=="name":
                        query = '''SELECT*FROM suppliers WHERE name LIKE %s
                        '''
                        mycursor.execute(query,f"%{self.search_entry.get()}%")
                        search =mycursor.fetchall()
                        if len(search)==0:
                            messagebox.showerror("Search error",f"No supplier with name {self.search_entry.get()}!",parent=self.root)
                        else:
                            self.supplier_table.delete(*self.supplier_table.get_children())
                            for row in search:
                                self.supplier_table.insert("",END,values = row)
                                con.close()
                    elif self.combo_box.get()=="email":
                        query = '''SELECT*FROM suppliers WHERE email LIKE %s
                        '''
                        mycursor.execute(query,f"%{self.search_entry.get()}%")
                        search =mycursor.fetchall()
                        if len(search)==0:
                            messagebox.showerror("Search error",f"No supplier with email {self.search_entry.get()}!",parent=self.root)
                        else:
                            self.supplier_table.delete(*self.supplier_table.get_children())
                            for row in search:
                                self.supplier_table.insert("",END,values = row)
                                con.close()
                    else:
                        messagebox.showerror("Search error","You did not specify search creteria!",parent=self.root)      
                else:
                    messagebox.showerror("Search error","The search entry is empty!",parent=self.root)    
            except:
                messagebox.showerror("Error",f"Something went wrong{e}",parent=self.root)
         