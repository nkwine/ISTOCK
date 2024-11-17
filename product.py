from tkinter import *
from tkinter import ttk,messagebox,simpledialog
from updateProduct import updateProduct
import pymysql

class product:
    def __init__(self,root,parent):
        self.root =root
        self.root.resizable(0,0)
        self.root.geometry('1027x546+215+120')
        self.root.iconbitmap("D:/phone/gui/code/inventory_system/employee__icon.ico")
        self.root.config(bg="#FFFFFF")
        self.root.grab_set()
        self.root.transient(parent)
        self.root.focus_force()
        #heading
        self.titlelable =Label(self.root,text="Manage Products",font=("times new roman",20,'bold'),bg="#0f4d7d",fg="white")
        self.titlelable.place(x=0,y=0,relwidth=1)
        #left frame
        left_frame = Frame(self.root,bg="white",width=280,height=300)
        left_frame.place(x=6,y=60)
        title =Label(left_frame,text="Create New Products",font=("times new roman",15,'bold'),bg="#0f4d7d",fg="white")
        title.pack(fill=X)
        #inner framr
        inner_frame =Frame(left_frame,highlightbackground="grey",highlightthickness=2,bg="white")
        inner_frame.pack(fill=BOTH,expand=True)
        #name
        name = Label(inner_frame,text="Product Name",font=("times new roman",12,"bold"),bg="white")
        name.grid(row=0,column=0,sticky=W,pady=20)
        self.name = Entry(inner_frame, font=("times new roman",12),bg="lightyellow",width=23)
        self.name.grid(row=0,column=1,sticky=W,padx=10)
        data = self.categoryData()
        self.items=[]
        for y in data:
            self.items.append(y[1])
        self.items.append("None")
        self.items=tuple(self.items)
        category =Label(inner_frame,text="Category",font=("times new roman",12,"bold"),bg="white")
        category.grid(row=1,column=0,sticky=W,pady=20)
        self.category = ttk.Combobox(inner_frame, values=self.items, font=("times new roman",12),state="readonly",width=21)
        self.category.grid(row=1,column=1,sticky=W,padx=10)
        self.category.set("Select")
        #unit measuer
        unit =Label(inner_frame,text="Unit of measurement",font=("times new roman",12,"bold"),bg="white")
        unit.grid(row=2,column=0,pady=20)
        self.unit = Entry(inner_frame, font=("times new roman",12),bg="lightyellow",width=23, fg="grey")
        self.unit.grid(row=2,column=1,sticky=W,padx=10)
        self.unit.insert(0,"eg kg, box, piece, bundle etc")
        #bidding
        self.unit.bind("<FocusIn>",lambda val:self.focus_in(val,"u"))
        self.unit.bind("<FocusOut>",lambda val:self.focus_out(val,"u"))
        qty =Label(inner_frame,text="Quantity Available",font=("times new roman",12,"bold"),bg="white")
        qty.grid(row=3,column=0,sticky=W,pady=20)
        self.qty = Entry(inner_frame, font=("times new roman",12),bg="lightyellow",width=23, fg="grey")
        self.qty.grid(row=3,column=1,sticky=W,padx=10)
        self.qty.insert(0,"use digits eg 7")
        #bidding
        self.qty.bind("<FocusIn>",lambda val:self.focus_in(val,"q"))
        self.qty.bind("<FocusOut>",lambda val:self.focus_out(val,"q"))
        #price
        price =Label(inner_frame,text="Price Per Unit(UGX)",font=("times new roman",12,"bold"),bg="white")
        price.grid(row=4,column=0,pady=20,sticky=W)
        self.price = Entry(inner_frame, font=("times new roman",12),bg="lightyellow",width=23, fg="grey")
        self.price.grid(row=4,column=1,sticky=W,padx=10)
        self.price.insert(0,"use digits eg 10")
        #bidding
        self.price.bind("<FocusIn>",lambda val:self.focus_in(val,"p"))
        self.price.bind("<FocusOut>",lambda val:self.focus_out(val,"p"))
        bottom_frame =Frame(inner_frame,bg="white")
        bottom_frame.grid(row=5,column=0,columnspan=2)
        #add button
        self.add = Button(bottom_frame, text="Add", bg="#0f4d7d",fg="white",font=("times new roman",12),
                             command=lambda:self.majorfunction("A"),width=10)
        self.add.grid(row=0,column=0,padx=58,pady=24)
        #clear button
        self.clear = Button(bottom_frame, text="Clear", bg="#0f4d7d",fg="white",font=("times new roman",12),
                             command=lambda:self.majorfunction("C"),width=10)
        self.clear.grid(row=0,column=1,padx=28,pady=24)
        
        #right frame
        right_frame = Frame(self.root,bg="white")
        right_frame.place(x=390,y=50)
        #Search frame
        serch = LabelFrame(right_frame,text="Search Products",font=("times new roman",12),bg="white")
        serch.pack(fill=X)
        self.combo_box = ttk.Combobox(serch,values=("p_id","name","category"),font=("times new roman",12,"bold"),state="readonly",width=13)
        self.combo_box.set("Search by")
        self.combo_box.grid(row=0,column=0,padx=13)
        #search entery
        self.search_entry = Entry(serch, font=("times new roman",12),bg="lightyellow",width=25)
        self.search_entry.grid(row=0,column=1)
        self.search_button =Button(serch,text="Search",font=("times new roman",12),width=7,cursor="hand2",bg="#0f4d7d",
                                   fg="white",command=lambda:self.edit("S"))
        self.search_button.grid(row=0,column=3,padx=17,pady=8)
        self.showall_button =Button(serch,text="Show all",font=("times new roman",12),width=7, cursor="hand2",bg="#0f4d7d",
                                    fg="white",command=lambda:self.edit("sa"))
        self.showall_button.grid(row=0,column=4,padx=17)
        
        rinner_frame = Frame(right_frame,bg="white")
        rinner_frame.pack(fill=BOTH,expand=False)
        horizont_scroll = Scrollbar(rinner_frame,orient=HORIZONTAL)
        vertical_scroll = Scrollbar(rinner_frame,orient=VERTICAL)
        self.products_table = ttk.Treeview(rinner_frame,columns=("p_id","name","category","u_m","qty","price","status"),show="headings",
            yscrollcommand=vertical_scroll.set,xscrollcommand=horizont_scroll.set,height=13)
        horizont_scroll.pack(side=BOTTOM,fill=X)
        vertical_scroll.pack(side=RIGHT,fill=Y)
        horizont_scroll.config(command=self.products_table.xview)
        self.products_table.heading('p_id',text='P_Id')
        self.products_table.heading('name',text='Name')
        self.products_table.heading('category',text='Category')
        self.products_table.heading('u_m',text='Measurement')
        self.products_table.heading('qty',text='Qty')
        self.products_table.heading('price',text='Unit price')
        self.products_table.heading('status',text='Status')
        self.products_table.column('p_id',width=60)
        self.products_table.column('name',width=130)
        self.products_table.column('category',width=130)
        self.products_table.column('u_m',width=100)
        self.products_table.column('qty',width=50)
        self.products_table.column('price',width=60)
        self.products_table.column('status',width=80)
        self.products_table.pack(fill=X,expand=0,anchor=NW)
        self.products_table.bind("<<TreeviewSelect>>",self.show)
        #buttons
        rbottom_frame =Frame(right_frame,bg="white")
        rbottom_frame.pack()
        self.update = Button(rbottom_frame, text="Update product details", bg="#0A581B",fg="white",font=("times new roman",12),
                             command=lambda:self.edit("U"),width=16,state=DISABLED)
        self.update.grid(row=0,column=0,padx=50,pady=24)
        self.delete = Button(rbottom_frame, text="Delete", bg="#750707",fg="white",font=("times new roman",12),
                             command=lambda:self.edit("D"),width=10,state=DISABLED)
        self.delete.grid(row=0,column=1,padx=28,pady=24)
        self.add_stock = Button(rbottom_frame, text="Add stock", bg="#0f4d7d",fg="white",font=("times new roman",12),
                             command=lambda:self.edit("AD"),width=10,state=DISABLED)
        self.add_stock.grid(row=0,column=2,padx=28,pady=24)
        self.details_display()
        
    #functions
    
    def database_connection(self,pas):
        try:
            return pymysql.connect(host="localhost",user="root",password=f"{pas}",database="inventory")
        except:
            messagebox.showerror("Error",f"Failed connection",parent=self.root) 
    def details_display(self):
        self.update.config(state=DISABLED)
        self.delete.config(state=DISABLED)
        self.products_table.selection_clear()  
        try:
            con= self.database_connection(1996)
            mycursor = con.cursor()
            mycursor.execute("SELECT*FROM products")
            product = mycursor.fetchall()
            self.products_table.delete(*self.products_table.get_children())
            for record in product:
                to_add = []
                staus = "enoug"
                for item in record:
                    to_add.append(item)
                if int(record[4])>=100:
                    staus = "much"
                elif int(record[4])>=60 and int(record[4])<100:
                     staus = "enough"
                elif int(record[4])>=30 and int(record[4])<60:
                     staus = "low"
                else:
                    staus = "Running out"
                to_add.append(staus)
                self.products_table.insert("",END,values = to_add)
            self.indicate()
            con.close()
        except:
            messagebox.showerror("Error","Something wrong hapenned",parent=self.root)
    #running out stock
    def indicate(self):
        for items in self.products_table.get_children():
            value = self.products_table.item(items,"values")[6]
            if value == "Running out":
                self.products_table.item(items,tags =("red",))
        self.products_table.tag_configure("red",foreground ="red")
    #enable items
    def show(self,event):
        if self.products_table.selection():
            self.update.config(state="normal")
            self.delete.config(state="normal")
            self.add_stock.config(state="normal")
    #retriev category from database
    def edit(self,choice):
        con = self.database_connection(1996)
        mycursor = con.cursor()
        if choice =="D":
            value = self.products_table.focus()
            to_delete = self.products_table.item(value,"values")[0]
            query = "DELETE FROM products WHERE p_id = %s"
            if messagebox.askyesno("","Deleted records can not be recovered\nAre you sure?",parent=self.root):
                mycursor.execute(query,to_delete)
                con.commit()
                messagebox.showinfo("","Product successfully deleted",parent=self.root)
                con.close()
                self.details_display()
                self.products_table.selection_clear()
        elif choice == "sa":
            self.details_display()
        elif choice == "S":
            if self.search_entry.get().strip()!='':
                if self.combo_box.get()=="p_id":
                    query = '''SELECT*FROM products WHERE p_id LIKE %s
                    '''
                    mycursor.execute(query,f"%{self.search_entry.get()}%")
                    search =mycursor.fetchall()
                    if len(search)==0:
                        messagebox.showerror("Search error",f"No product with id {self.search_entry.get()}!")
                    else:
                        self.products_table.delete(*self.products_table.get_children())
                        for record in search:
                            to_add = []
                            staus = "enoug"
                            for item in record:
                                to_add.append(item)
                            if int(record[4])>=100:
                                staus = "much"
                            elif int(record[4])>=60 and int(record[4])<100:
                                staus = "enough"
                            elif int(record[4])>=30 and int(record[4])<60:
                                staus = "low"
                            else:
                                staus = "Running out"
                            to_add.append(staus)
                            self.products_table.insert("",END,values = to_add)
                            con.close()
                elif self.combo_box.get()=="name":
                    query = '''SELECT*FROM products WHERE name LIKE %s
                    '''
                    mycursor.execute(query,f"%{self.search_entry.get()}%")
                    search =mycursor.fetchall()
                    if len(search)==0:
                        messagebox.showerror("Search error",f"No product with name {self.search_entry.get()}!",parent=self.root)
                    else:
                        self.products_table.delete(*self.products_table.get_children())
                        for record in search:
                            to_add = []
                            staus = "enoug"
                            for item in record:
                                to_add.append(item)
                            if int(record[4])>=100:
                                staus = "much"
                            elif int(record[4])>=60 and int(record[4])<100:
                                staus = "enough"
                            elif int(record[4])>=30 and int(record[4])<60:
                                staus = "low"
                            else:
                                staus = "Running out"
                            to_add.append(staus)
                            self.products_table.insert("",END,values = to_add)
                            con.close()
                elif self.combo_box.get()=="category":
                    query = '''SELECT*FROM products WHERE category LIKE %s
                    '''
                    mycursor.execute(query,f"%{self.search_entry.get()}%")
                    search =mycursor.fetchall()
                    if len(search)==0:
                        messagebox.showerror("Search error",f"No product with category {self.search_entry.get()}!",parent=self.root)
                    else:
                        self.products_table.delete(*self.products_table.get_children())
                        for record in search:
                            to_add = []
                            staus = "enoug"
                            for item in record:
                                to_add.append(item)
                            if int(record[4])>=100:
                                staus = "much"
                            elif int(record[4])>=60 and int(record[4])<100:
                                staus = "enough"
                            elif int(record[4])>=30 and int(record[4])<60:
                                staus = "low"
                            else:
                                staus = "Running out"
                            to_add.append(staus)
                            self.products_table.insert("",END,values = to_add)
                        con.close()
                else:
                  messagebox.showerror("Search error","You did not specify search creteria!",parent=self.root)
                  return    
            else:
                messagebox.showerror("Search error","The search entry is empty!",parent=self.root)  
                return  
                
        elif choice =="U":
            value = self.products_table.focus()
            root = Toplevel()
            obj = updateProduct(root,self.root,self.products_table.item(value,"values")[0],self.products_table.item(value,"values")[1],
                self.products_table.item(value,"values")[2],self.products_table.item(value,"values")[3],self.products_table.item(value,
                "values")[4],self.products_table.item(value,"values")[5],self.details_display)
            root.mainloop()
            return
        elif choice =="AD":
            option = self.products_table.focus()
            to_update = self.products_table.item(option,"values")
            try:
                 new_value = simpledialog.askinteger("Input",f"Enter the qty of {to_update[1]} in {to_update[3]}(s)",parent=self.root)
                 self.root.grab_set()
                 #self.root.transient(self.parent)
                 if str(new_value).strip()=='':
                     messagebox.showerror("Error","You did not anything",parent=self.root)
                     return
                 elif new_value is None:
                     messagebox.showerror("","Process canceled",parent=self.root)
                     return
            except Exception as e:
                 messagebox.showerror("Error",f"Something went wrong {e}",parent=self.root)
            try:
                 query = "UPDATE products SET qty = %s WHERE p_id = %s"
                 old =int(to_update[4])
                 new =old+new_value
                 new = str(new)
                 mycursor.execute(query,(new,to_update[0],))
                 messagebox.showinfo("","Quantity added",parent=self.root)
                 con .commit()
                 con.close()
                 self.details_display()                 
            except:
                 messagebox.showerror("Error",f"Failed to update the record",parent=self.root)
                 return
    def categoryData(self):
        con = self.database_connection(1996)
        mycursor=con.cursor() 
        query = "SELECT* FROM product_category"
        mycursor.execute(query)
        values = []
        for y in mycursor.fetchall():
            values.append(y)
        con.close()
        return values  
    def focus_in(self,event,v):
        if v =="u":
            if self.unit.get()=="eg kg, box, piece, bundle etc":
                self.unit.delete(0,END)
                self.unit.config(fg="black")
        elif v == "q":
            if self.qty.get()=="use digits eg 7":
                self.qty.delete(0,END)
                self.qty.config(fg="black")
        elif v == "p":
            if self.price.get()=="use digits eg 10":
                self.price.delete(0,END)
                self.price.config(fg="black")
    def focus_out(self,event,v):
        if v =="u":
            if len(self.unit.get().strip())==0:
                self.unit.insert(0,"eg kg, box, piece, bundle etc")
                self.unit.config(fg="grey")
        elif v == "q":
            if len(self.qty.get().strip())==0:
                self.qty.insert(0,"use digits eg 7")
                self.qty.config(fg="grey")
        elif v == "p":
            if len(self.price.get().strip())==0:
                self.price.insert(0,"use digits eg 10")
                self.price.config(fg="grey")
    def majorfunction(self,choice):
        con = self.database_connection(1996)
        mycursor = con.cursor()
        if choice == "A":
            if self.name.get().strip()=='':
                messagebox.showerror("Error","Product name must be provided",parent=self.root)
                return
            elif self.category.get()=="Select":
                messagebox.showerror("Error","No product category was selected",parent=self.root)
                return
            elif self.unit.get().strip() =="eg kg, box, piece, bundle etc" or self.unit.get().strip()=='':
                messagebox.showerror("Error","Provide the unit of measuerment please",parent=self.root)
                return                
            elif self.qty.get().strip() =="eg kg, box, piece, bundle etc" or self.qty.get().strip()=='':
                messagebox.showerror("Error","The quantity of the product availabe must be provided",parent=self.root)
                return
            elif self.price.get().strip() =="eg kg, box, piece, bundle etc" or self.price.get().strip()=='':
                messagebox.showerror("Error","The unit price of the product availabe must be provided",parent=self.root)
                return
            else:
                try:
                    int(self.unit.get().strip())
                    messagebox.showerror("Error","The unit of measuerment can not be a digit please!",parent=self.root)
                    con.close()
                    return
                except:
                    pass
                try:
                    int(self.qty.get().strip())
                    pass
                except:
                    messagebox.showerror("Error","The quantity of the product availabe must be a digit",parent=self.root)
                    con.close()
                    return
                try:
                    int(self.price.get().strip())
                    pass
                except:
                    messagebox.showerror("Error","The unit price of the  must be a digit",parent=self.root)
                    con.close()
                    return
                try:
                    table = '''CREATE TABLE IF NOT EXISTS products(p_id VARCHAR(20) PRIMARY KEY NOT NULL,name VARCHAR(30) NOT NULL UNIQUE,
                    category VARCHAR(15) NOT NULL,u_measure VARCHAR(30) NOT NULL,qty VARCHAR(200) NOT NULL,unit_price VARCHAR(10) NOT NULL)
                   '''
                    mycursor.execute(table)
                    mycursor.execute("SELECT*FROM products WHERE name = %s",self.name.get().lower())
                    if len(mycursor.fetchall())>=1:
                        messagebox.showerror("Error","The product already eists!",parent=self.root)
                        con.close()
                        return
                    else:
                        mycursor.execute("SELECT*FROM products WHERE name LIKE %s",f"%{self.name.get().lower()}%")
                        g=mycursor.fetchall()
                        if len(g)>=1:
                            y=[]
                            for k in g:
                                y.append(k[1])
                            if not messagebox.askyesno("",f"The product named enter is like {y} which is already in the system\nDo you still want to save",parent=self.root):
                                messagebox.showinfo("","Process canceled",parent=self.root)
                                con.close()
                                return
                        
                        
                        my_id = "SELECT MAX(SUBSTR(p_id,3))FROM products"
                        mycursor.execute(my_id)
                        max_id = mycursor.fetchone()[0]
                        initial = "p"
                        if max_id is None:
                            new_id =f"{initial}-000001"
                        else:
                            max_id = int(max_id)
                            new_id = f"{initial}-{str(max_id+1).zfill(6)}"
                        try:
                            query = "INSERT INTO products VALUES(%s,%s,%s,%s,%s,%s)"
                            values =(new_id,self.name.get().lower(),self.category.get(),self.unit.get().lower(),self.qty.get(),self.price.get())
                            if messagebox.askyesno("","Do you really want to save this product?",parent=self.root):
                                mycursor.execute(query,values)
                                messagebox.showinfo("","Product successfuly added",parent=self.root)
                                con .commit()
                                con.close()
                                self.details_display()
                                return
                        except:
                            messagebox.showerror("Error",f"Something went wrong try again!",parent=self.root)
                            con.close()
                            return
                except:
                    messagebox.showerror("Error",f"Something wrong happened",parent=self.root)
                    con.close()
                    return
        elif choice == "C":
            self.name.delete(0,END)
            self.category.set("Select")
            self.unit.delete(0,END)
            self.unit.insert(0,"eg kg, box, piece, bundle etc")
            self.unit.config(fg="grey")
            self.qty.delete(0,END)   
            self.qty.insert(0,"use digits eg 7")
            self.qty.config(fg="grey")
            self.price.delete(0,END)
            self.price.insert(0,"use digits eg 10")
            self.price.config(fg="grey")
            self.root.focus_set()
        return
    