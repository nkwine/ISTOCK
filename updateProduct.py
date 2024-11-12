from tkinter import*
from tkinter import messagebox, ttk
import pymysql

class updateProduct:
    def __init__(self,root,parent,pid,pname,pcategory,punit,pqty,uprice,on_clos=None):
        self.parent = parent
        self.root =root
        self.pname = pname
        self.pcategory = pcategory
        self.punit = punit
        self.pqty = pqty
        self.uprice = uprice
        self.pid = pid
        self.on_clos = on_clos
        self.root.geometry('500x450+300+170')
        self.root.iconbitmap("employee__icon.ico")
        self.root.resizable(0,0)
        self.root.config(bg="white")
        self.root.grab_set()
        self.root.transient(parent)
        self.root.bind("<Destroy>",self.on_close)
        
        #widgets
        self.titlelable =Label(self.root,text="Update Products",font=("times new roman",16,'bold'),bg="#0f4d7d",fg="white")
        self.titlelable.place(x=0,y=0,relwidth=1)
        #left frame
        frame = Frame(self.root,bg="white",width=600,height=300)
        frame.place(x=50,y=30)
        #inner framr
        inner_frame =Frame(frame,highlightbackground="grey",highlightthickness=2,bg="white")
        inner_frame.pack(fill=BOTH,expand=True)
        #name
        name = Label(inner_frame,text="Product Name",font=("times new roman",12,"bold"),bg="white")
        name.grid(row=0,column=0,sticky=W,pady=20)
        self.name = Entry(inner_frame, font=("times new roman",12),bg="lightyellow",width=23)
        self.name.grid(row=0,column=1,sticky=W,padx=10)
        self.name.insert(0,pname)
        #category
        data = self.categoryData()
        self.items=[]
        for y in data:
            self.items.append(y[1])
        self.items.append("None")
        self.items=tuple(self.items)
        category =Label(inner_frame,text="Category",font=("times new roman",12,"bold"),bg="white")
        category.grid(row=1,column=0,sticky=W,pady=20)
        self.category = ttk.Combobox(inner_frame, values=self.items, font=("times new roman",12),state="readonly",width=20)
        self.category.grid(row=1,column=1,sticky=W,padx=10)
        self.category.set(pcategory)
        #unit measuer
        unit =Label(inner_frame,text="Unit of measurement",font=("times new roman",12,"bold"),bg="white")
        unit.grid(row=2,column=0,pady=20)
        self.unit = Entry(inner_frame, font=("times new roman",12),bg="lightyellow",width=23,)
        self.unit.grid(row=2,column=1,sticky=W,padx=10)
        self.unit.insert(0,punit)
        #bidding
        # self.unit.bind("<FocusIn>",lambda val:self.focus_in(val,"u"))
        # self.unit.bind("<FocusOut>",lambda val:self.focus_out(val,"u"))
        qty =Label(inner_frame,text="Quantity Available",font=("times new roman",12,"bold"),bg="white")
        qty.grid(row=3,column=0,sticky=W,pady=20)
        self.qty = Entry(inner_frame, font=("times new roman",12),bg="lightyellow",width=23,)
        self.qty.grid(row=3,column=1,sticky=W,padx=10)
        self.qty.insert(0,pqty)
        #bidding
        # self.qty.bind("<FocusIn>",lambda val:self.focus_in(val,"q"))
        # self.qty.bind("<FocusOut>",lambda val:self.focus_out(val,"q"))
        #price
        price =Label(inner_frame,text="Price Per Unit(UGX)",font=("times new roman",12,"bold"),bg="white")
        price.grid(row=4,column=0,pady=20,sticky=W)
        self.price = Entry(inner_frame, font=("times new roman",12),bg="lightyellow",width=23,)
        self.price.grid(row=4,column=1,sticky=W,padx=10)
        self.price.insert(0,uprice)
        #bidding
        # self.price.bind("<FocusIn>",lambda val:self.focus_in(val,"p"))
        # self.price.bind("<FocusOut>",lambda val:self.focus_out(val,"p"))
        bottom_frame =Frame(inner_frame,bg="white")
        bottom_frame.grid(row=5,column=0,columnspan=2)
        #add button
        self.add = Button(bottom_frame, text="Save", bg="#065735",fg="white",font=("times new roman",12),
                             command=lambda:self.majorfunction("A"),width=7)
        self.add.grid(row=0,column=0,padx=20,pady=24)
        #clear button
        self.clear = Button(bottom_frame, text="Clear", bg="#0f4d7d",fg="white",font=("times new roman",12),
                             command=lambda:self.majorfunction("C"),width=7)
        self.clear.grid(row=0,column=1,padx=1,pady=24)
        self.cancel = Button(bottom_frame, text="Cancel", bg="#8A0B0B",fg="white",font=("times new roman",12),
                             command=lambda:self.majorfunction("Ca"),width=7)
        self.cancel.grid(row=0,column=2,padx=20,pady=24)
        
    def database_connection(self,pas):
        try:
            return pymysql.connect(host="localhost",user="root",password=f"{pas}",database="inventory")
        except Exception as e:
            messagebox.showerror("Error",f"Failed connection {e}") 
    def on_close(self,event):
        self.root.grab_release()
        self.root.destroy()
        self.parent.focus_set()
        self.parent.grab_set()
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
    def majorfunction(self,choice):
        con = self.database_connection(1996)
        mycursor = con.cursor()
        if choice == "A":
            if self.name.get().strip()=='':
                messagebox.showerror("Error","Product name must be provided",parent=self.root)
                return
            elif self.unit.get().strip()=='':
                messagebox.showerror("Error","Provide the unit of measuerment please",parent=self.root)
                return                
            elif self.qty.get().strip()=='':
                messagebox.showerror("Error","The quantity of the product availabe must be provided",parent=self.root)
                return
            elif self.price.get().strip()=='':
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
                    messagebox.showerror("Error","The quantity of the product availabe must be a digit!",parent=self.root)
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
                    mycursor.execute("SELECT*FROM products WHERE name = %s",self.name.get().lower())
                    y =mycursor.fetchall()
                    if len(y)>=1:
                        counter = 0
                        for item in y:
                            if item[1]==self.name.get().lower() and item[0]!=self.pid:
                                counter+=1
                        if counter>0:
                            messagebox.showerror("Error","The product name already eists!",parent=self.root)
                            con.close()
                            return
                    
                    mycursor.execute("SELECT*FROM products WHERE name LIKE %s",f"%{self.name.get().lower()}%")
                    g=mycursor.fetchall()
                    if len(g)>=1:
                        y=[]
                        for k in g:
                            if k[0] != self.pid:
                                y.append(k[1])
                        if len(y)>0:
                            if not messagebox.askyesno("",f"The product named enter is like {y} which is already in the system\nDo you still want to save",
                                                       parent=self.root):
                                messagebox.showinfo("","Process canceled",parent=self.root)
                                con.close()
                                return
                    try:
                        table = "UPDATE products SET name =%s,category =%s,u_measure =%s,qty =%s,unit_price =%s WHERE p_id =%s"
                        values = (self.name.get().lower(),self.category.get(),self.unit.get().lower(),self.qty.get(),self.price.get(),self.pid)
                        if messagebox.askyesno("","Do you really want to save this product?",parent=self.root):
                            mycursor.execute(table,values)
                            messagebox.showinfo("","Product successfuly updated",parent=self.root)
                            con .commit()
                            con.close()
                            self.root.destroy()
                            return
                        else:
                            messagebox.showinfo("","Process canceled",parent=self.root)
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
            self.name.insert(0,self.pname)
            self.category.set(self.pcategory)
            self.unit.delete(0,END)
            self.unit.insert(0,self.punit)
            self.qty.delete(0,END)   
            self.qty.insert(0,self.pqty)
            self.price.delete(0,END)
            self.price.insert(0,self.uprice)
            self.root.focus_set()
            return
        elif choice =="Ca":
            if messagebox.askyesno("","Do you really want to cancel this process",parent=self.root):
                self.root.destroy()
    def on_close(self,event):
        if self.on_clos:
            self.on_clos()
        self.root.grab_release()
        #self.root.destroy()
        self.parent.focus_set()
        self.parent.grab_set()
            
    
    