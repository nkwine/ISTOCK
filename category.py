from tkinter import *
from tkinter import ttk,messagebox,simpledialog
import pymysql
class category:
    def __init__(self,root,parent):
        self.root =root
        self.root.resizable(0,0)
        self.root.geometry('1000x546+230+120')
        self.root.iconbitmap("employee__icon.ico")
        self.root.config(bg="#FFFFFF")
        self.root.grab_set()
        self.parent = parent
        self.root.transient(parent)
        self.root.focus_force()
        
        #heading
        self.titlelable =Label(self.root,text="Manage Product Categories",font=("times new roman",20,'bold'),bg="#0f4d7d",fg="white")
        self.titlelable.place(x=0,y=0,relwidth=1)
        #main frame
        frame = Frame(self.root,bg="white")
        frame.place(x=0,y=36,relwidth=1)
        #left frame
        left_frame =Frame(frame,bg="#FFFFFF",height=80)
        left_frame.grid(row=0,column=0,padx=20,pady=20)
        title= Label(left_frame,text="Enter A new Category Name",font=("times new roman",16,"bold"),bg="white")
        title.grid(row=0,column=0,padx=20)
        self.name = Entry(left_frame,bg="lightyellow",font=("times new roman",12),width=30)
        self.name.grid(row=1,column=0,padx=10,pady=20)
        self.add = Button(left_frame, text="Add", bg="#0f4d7d",fg="white",font=("times new roman",12),
            command=lambda:self.mainfunction("A"),width=7)
        self.add.grid(row=1,column=1)
        self.update = Button(left_frame, text="Update", bg="#0A8F36",fg="white",font=("times new roman",12),
            command=lambda:self.mainfunction("U"),width=7,state="disabled")
        self.update.grid(row=1,column=2,padx=20)
        self.delet = Button(left_frame, text="Delet", bg="#6E0606",fg="white",font=("times new roman",12),
            command=lambda:self.mainfunction("D"),width=7,state="disabled")
        self.delet.grid(row=1,column=3)
        #right frame
        right_frame = Frame(frame,bg="white")
        right_frame.grid(row=0,column=1,pady=20,rowspan=10)
        categories =Label(right_frame,text="Available Categories ",font=("times new roman",16,"bold"),bg="white")
        categories.pack(padx=30)
        yscroll = Scrollbar(right_frame,orient=VERTICAL)
        xscroll = Scrollbar(right_frame,orient=HORIZONTAL)
        self.ava_category =ttk.Treeview(right_frame,columns=("cid","name"),show="headings",height=18,yscrollcommand=yscroll.set,xscrollcommand=xscroll.set)
        yscroll.pack(side=RIGHT,fill=Y)
        xscroll.pack(side=BOTTOM,fill=X)
        yscroll.config(command=self.ava_category.yview)
        xscroll.config(command=self.ava_category.xview)
        self.ava_category.heading("cid",text='Category_Id')
        self.ava_category.heading("name",text="Category Name")
        self.ava_category.pack(padx=5)
        self.ava_category.column("cid",width=110)
        self.ava_category.column("name",width=245)
        self.details_display()
       
        self.ava_category.bind("<<TreeviewSelect>>",self.show)
        
        
    #functions
    def database_connection(self,pas):
        try:
            return pymysql.connect(host="localhost",user="root",password=f"{pas}",database="inventory")
        except:
            messagebox.showerror("Error",f"Failed connection",parent=self.root)
            
    def mainfunction(self,choice):
        con = self.database_connection(1996)
        mycursor =con.cursor()
        if choice =="A":
             if self.name.get()=='':
                 messagebox.showerror("Error","Enter the category name please",parent=self.root)
                 return
             try:
                comand ='''CREATE TABLE IF NOT EXISTS product_category(c_id INT(8) PRIMARY KEY NOT NULL,category_name VARCHAR(20) NOT NULL)
                '''
                mycursor.execute(comand)
                mycursor.execute("SELECT*FROM product_category WHERE category_name = %s",self.name.get().lower())
                if len(mycursor.fetchall())>=1:
                    messagebox.showerror("Error","The category already eists!",parent=self.root)
                    return
                else:
                    my_id = "SELECT MAX(SUBSTR(c_id,3))FROM product_category"
                    mycursor.execute(my_id)
                    max_id = mycursor.fetchone()[0]
                    initial = "C"
                    if max_id is None:
                        new_id =f"{initial}-000001"
                    else:
                        max_id = int(max_id)
                        new_id = f"{initial}-{str(max_id+1).zfill(6)}"
                        
                    try:
                        query = "INSERT INTO product_category VALUES(%s,%s)"
                        values =(new_id,self.name.get().lower())
                        mycursor.execute(query,values)
                        messagebox.showinfo("","Category successfuly added",parent=self.root)
                        con .commit()
                        con.close()
                        self.details_display()
                    except:
                        messagebox.showerror("Error",f"Something went wrong try again!",parent=self.root)
                
                return
             except:
                 messagebox.showerror("Error","Something went wrong try again!",parent=self.root)
        elif choice =="U":
             option = self.ava_category.focus()
             to_update = self.ava_category.item(option,"values")
             try:
                 new_value = simpledialog.askstring("Input","Enter new category name",parent=self.root)
                 self.root.grab_set()
                 #self.root.transient(self.parent)
                 if str(new_value).strip()=='':
                     messagebox.showerror("Error","Enter a new category please",parent=self.root)
                     return
                 elif new_value is None:
                     messagebox.showerror("","Process canceled",parent=self.root)
                     return
             except:
                 messagebox.showerror("Error",f"Something went wrong",parent=self.root)
             try:
                 query = "UPDATE product_category SET category_name = %s WHERE c_id = %s"
                 mycursor.execute(query,(new_value,to_update[0],))
                 messagebox.showinfo("","Record updated successfuly",parent=self.root)
                 con .commit()
                 con.close()
                 self.details_display()                 
             except:
                 messagebox.showerror("Error",f"Failed to update the record",parent=self.root)
                 return
        else:
            option = self.ava_category.focus()
            to_delete = self.ava_category.item(option,"values")
            try:
                query = "DELETE FROM product_category WHERE c_id =%s"
                if messagebox.askokcancel("Delete",f"Your about to permanently delete the category {to_delete[1]},are you sure?",
                                          parent=self.root):
                    mycursor.execute(query,to_delete[0])
                    messagebox.showinfo("","Category successfuly deleted",parent=self.root)
                    con .commit()
                    con.close()
                    self.details_display()
                else:
                 messagebox.showinfo("","Process canceled",parent=self.root)
                 return
            except:
                 messagebox.showerror("Error","Something went wrong",parent=self.root)
        return
            
             
            
    def details_display(self):
        try:
            self.update.config(state="disabled")
            self.delet.config(state="disabled")
            con= self.database_connection(1996)
            mycursor = con.cursor()
            mycursor.execute("SELECT*FROM product_category")
            category_record = mycursor.fetchall()
            self.ava_category.delete(*self.ava_category.get_children())
            for record in category_record:
                self.ava_category.insert("",END,values = record)
            con.close()
        except:
            messagebox.showerror("Error","There is an error",parent=self.root)  
    def show(self,event):
        if self.ava_category.selection():
            self.update.config(state="normal")
            self.delet.config(state="normal")

             
       
         