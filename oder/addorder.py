from tkinter import *
from tkcalendar import DateEntry
from tkinter import messagebox,ttk
import re
import pymysql, datetime,os,sys,platform
from tkcalendar import DateEntry
class addOrder:
    def __init__(self,root,parent,on_clos=None):
        self.parent = parent
        self.root =root
        self.on_clos =on_clos
        self.root.geometry('800x610+300+25')
        self.root.iconbitmap("employee__icon.ico")
        self.root.resizable(0,0)
        self.root.config(bg="white")
        self.root.grab_set()
        self.root.transient(parent)
        self.root.bind("<Destroy>",self.on_close)
        #heading
        self.titlelable =Label(self.root,text="Add a New Ordder",font=("times new roman",20,'bold'),bg="#0f4d7d",fg="white")
        self.titlelable.place(x=0,y=0,relwidth=1)
        #main frame
        frame = Frame(self.root,bg="white")
        frame.place(x=30,y=40,relwidth=1)
        #name
        head = Frame(frame,bg="white",width=400)
        head.grid(row=0,column=0,sticky=W)
        name= Label(head,text="Supplier",font=("times new roman",11,"bold"),bg="white")
        name.grid(row=0,column=0,sticky=W,pady=20)
        self.name = Entry(head, font=("times new roman",12),bg="lightyellow",width=50)
        self.name.grid(row=0,column=1,padx=20,pady=20)
        pro= Label(head,text="Products\n (you can manually enter the total amount spent on each product)\nNote: Plaese know that you can only enter digits hen you are filling",font=("times new roman",11),bg="white")
        pro.grid(row=1,column=0,columnspan=2)
        #product frame
        self.pframe = Frame(frame,bg="white",padx=10,)
        self.pframe.grid(row=1,column=0,sticky=EW)
        self.base =Label(self.pframe,bg="white")
        self.base.pack()
        #draft button  
        # supplier
        product_outer_frame = Frame(frame,bg="white",padx=30)
        product_outer_frame.grid(row=0,column=2,rowspan=6) 
        product_frame = Frame(product_outer_frame,bg="white")
        product_frame.pack()       
        supplier = Label(product_frame,text="Suppliers\nClick on a supplier to select ",font=("times new roman",12,"bold"),bg="white")
        supplier.pack()
        # products
        yscroll = Scrollbar(product_frame,orient=VERTICAL)
        xscroll = Scrollbar(product_frame,orient=HORIZONTAL)
        self.suppliers = Listbox(product_frame,bg="lightyellow",fg="black",yscrollcommand=yscroll.set,xscrollcommand=xscroll.set,
            height=9,width=30)
        yscroll.pack(side=RIGHT,fill=Y)
        xscroll.pack(side=BOTTOM,fill=X)
        yscroll.config(command=self.suppliers.yview)
        xscroll.config(command=self.suppliers.xview)
        self.suppliers.pack()
        self.suppliers.bind("<<ListboxSelect>>",lambda event:self.show("s",event))
        
        
        product_frame1 = Frame(product_outer_frame,bg="white")
        product_frame1.pack() 
        scrolly = Scrollbar(product_frame1,orient=VERTICAL)
        scrollx = Scrollbar(product_frame1,orient=HORIZONTAL)
        products = Label(product_frame1,text="Products",font=("times new roman",12,"bold"),bg="white")
        products.pack()
        self.products = Listbox(product_frame1,bg="lightyellow",fg="black",yscrollcommand=scrolly.set,xscrollcommand=scrollx.set,
            height=9,width=30,selectmode=MULTIPLE)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.config(command=self.products.yview)
        scrollx.config(command=self.products.xview)
        self.products.pack()
        self.products.bind("<Button-1>",self.showp)
        #Bill frame
        self.detail = Frame(self.root, bg="white")
        #self.detail.place( x=110,y=500)
        total_amount = Label(self.detail,text="Total Bill(UGX):",bg="white")
        total_amount.grid(row=0,column=0)
        self.total_amount =Entry(self.detail,width=18,bg="lightyellow")
        self.total_amount.grid(row=0,column=1)
        total_deposit = Label(self.detail,text="Total deposit(UGX):",bg="white")
        total_deposit.grid(row=0,column=2)
        self.total_deposit =Entry(self.detail,width=18,bg="lightyellow",fg="grey")
        self.total_deposit.grid(row=0,column=3)
        self.total_deposit.insert(0,"0")
        self.total_deposit.bind("<FocusIn>",self.focus_in)
        self.total_deposit.bind("<FocusOut>",self.focus_out)
        due = Label(self.detail,text="Due date:",bg="white")
        due.grid(row=0,column=4)
        self.due =DateEntry(self.detail,width=18,bg="lightyellow")
        self.due.grid(row=0,column=5)
         #bottom frame
        self.bottom_frame = Frame(self.root, bg="white")
        self.bottom_frame.place( x=150,y=540)
        self.finish = Button(self.bottom_frame, text="Finish", bg="#0f4d7d",fg="white",font=("times new roman",12),width=10,state=DISABLED,
            command=lambda:self.finishup())
        self.finish.grid(row=0,column=0,padx=20)
        self.view = Button(self.bottom_frame, text="View", bg="#0f4d7d",fg="white",font=("times new roman",12),width=10,state=DISABLED,
            command=lambda:self.final_step("V"))
        self.view.grid(row=0,column=1,padx=20)
        self.save = Button(self.bottom_frame, text="Save", bg="#0f4d7d",fg="white",font=("times new roman",12),width=10,state=DISABLED,
            command=lambda:self.final_step("S"))
        self.save.grid(row=0,column=2,padx=20)
        self.cancel = Button(self.bottom_frame, text="Cancel", bg="#810404",fg="white",font=("times new roman",12),width=10,
            command=lambda:self.majorfunction("C"))
        self.cancel.grid(row=0,column=3,padx=20)
        self.supplier_list()
        self.sup = None
         
    #functions
    #when window is closed
    def database_connection(self,pas):
        try:
            return pymysql.connect(host="localhost",user="root",password=f"{pas}",database="inventory")
        except Exception as e:
            messagebox.showerror("Error",f"Failed connection {e}") 
    def supplier_list(self):
        con = self.database_connection(1996)
        mycursor = con.cursor()
        query = "SELECT* FROM suppliers"
        self.suppliers.delete(0,END)
        mycursor.execute(query)
        global detail ,selected,fastitem
        selected = None
        fastitem = None
        detail={}
        for itme in mycursor.fetchall():
            detail[itme[1]]=itme[0]
            self.suppliers.insert(END,itme[1])
    def produt_list(self):
        con = self.database_connection(1996)
        mycursor = con.cursor()
        query = "SELECT* FROM products"
        self.products.delete(0,END)
        mycursor.execute(query)
        for itme in mycursor.fetchall():
            self.products.insert(END,itme[1])
    def show(self,choice,event):
        if choice =="s":
            if len(self.suppliers.curselection())>0:
                y = self.suppliers.curselection()[0]
                y = self.suppliers.get(y)
                self.sup = y
                self.name.delete(0,END)
                self.name.insert(0,y)
                self.products.delete(0,END)
                item = ""
                for key,value in detail.items():
                    if key == y.strip():
                        item = value
                        self.keep(key)
                        break
                con = self.database_connection(1996)
                mycursor = con.cursor()
                mycursor.execute("SELECT products FROM suppliers WHERE s_id = %s",item)
                newlist =mycursor.fetchone()
                for k in newlist:
                    k = k.split(",")
                    for a in k:
                        self.products.insert(END,a) 
                
                if selected is None or selected !=y.strip():
                    for child in self.pframe.winfo_children():
                        if isinstance(child,LabelFrame):
                            child.destroy() 
                    try:
                        self.draft.destroy()
                        self.finish.config(state=DISABLED)
                        self.view.config(state=DISABLED) 
                        self.save.config(state=DISABLED)
                        self.detail.place_forget()
                    except:
                        pass                  
        return
    def showp(self,event):
        con =self.database_connection(1996)
        mycursor = con.cursor()
        index = self.products.nearest(event.y)
        if self.sup is not None:
            count=0
            for child in self.pframe.winfo_children():
                if isinstance(child,LabelFrame) and child.cget("text")==self.products.get(index):
                    self.root.unbind("<Destroy>")
                    child.destroy()
                    self.root.bind("<Destroy>",self.on_close)
                    count+=1
            if count == 0:
                global selected
                selected =fastitem
                self.new =LabelFrame(self.pframe,text=self.products.get(index),bg="white")
                self.new.pack(before=self.base,pady=5,anchor=W)
                mycursor.execute("SELECT u_measure FROM products WHERE name=%s",self.products.get(index).strip())
                record =mycursor.fetchone()
                Label(self.new,text=f"Qty({record[0]})",bg="white").grid(row=0,column=0)
                e1=Entry(self.new,width=16,bg="lightyellow")
                e1.grid(row=0,column=1)
                e1.bind("<FocusIn>",self.leave)
                Label(self.new,text="Unit price(UGX)",bg="white").grid(row=0,column=2)
                e2=Entry(self.new,width=16,bg="lightyellow")
                e2.grid(row=0,column=3)
                e2.bind("<FocusIn>",self.leave)
    
                Label(self.new,text="Total(UGX)",bg="white").grid(row=0,column=4)
                e3=Entry(self.new,width=16,bg="lightyellow",state=DISABLED)
                e3.grid(row=0,column=5)
                e3.bind("<FocusIn>",self.leave2)
                con.close()
        self.check()
        # self.draft.config(state=DISABLED)
        self.view.config(state=DISABLED) 
        self.save.config(state=DISABLED)
        self.finish.config(state=DISABLED)
        self.detail.place_forget()
        return
    #keeping truck of selected spplier           
    def keep(self,value):
        global fastitem
        fastitem =value
    def check(self):
        try:
            counter=0
            for child in self.pframe.winfo_children():
                if isinstance(child,LabelFrame):
                    counter=1
                elif isinstance(child,Button):
                    self.root.unbind("<Destroy>")
                    child.destroy()
                    self.root.bind("<Destroy>",self.on_close)
            if counter>0:
                self.draft = Button(self.pframe, text="Draft", bg="#0C0A8F",fg="white",font=("times new roman",12),width=10,
                command=lambda:self.enable())
                self.draft.pack() 
        except:
            pass
    def leave(self,evvent):
        self.finish.config(state=DISABLED)
        self.view.config(state=DISABLED)
        self.save.config(state=DISABLED)
        self.detail.place_forget()
    def leave2(self,evvent):
        #yself.finish.config(state=DISABLED)
        self.view.config(state=DISABLED)
        self.save.config(state=DISABLED)
        self.detail.place_forget()
    def enable(self):
        info ={}
        for child in self.pframe.winfo_children():
                if isinstance(child,LabelFrame):
                    inner =[]
                    count =0
                    obj = None
                    for grand in child.winfo_children():
                        if isinstance(grand,Entry):
                            count+=1
                            if count<3:
                                if grand.get().strip()=="":
                                    messagebox.showerror("","Some entries are empty!",parent=self.root)
                                    return
                                try:
                                    int(grand.get().replace(",",""))
                                    pass
                                except:
                                    messagebox.showerror("","Only digits are allowed!",parent=self.root)
                                    return  
                                inner.append(grand.get())
                            elif count>=3:
                                obj=grand
                                obj.config(state=NORMAL)
                    obj.delete(0,END)
                    obj.insert(0,int(inner[0])*int(inner[1]))
                    info[child.cget("text")]=inner
        self.finish.config(state=NORMAL)
        self.view.config(state=DISABLED) 
        self.save.config(state=DISABLED)
        self.detail.place_forget()
        self.root.focus_force()
        
    def finishup(self):
        global info1
        info1 ={}
        for child in self.pframe.winfo_children():
                if isinstance(child,LabelFrame):
                    inner =[]
                    # count =0
                    # obj = None
                    for grand in child.winfo_children():
                        if isinstance(grand,Entry):
                            # count+=1
                            # if count<3:
                            if grand.get().strip()=="":
                                messagebox.showerror("","Some entries are empty!",parent=self.root)
                                return
                            try:
                                int(grand.get())
                                pass
                            except:
                                messagebox.showerror("","Only digits are allowed!",parent=self.root)
                                return  
                            inner.append(grand.get())
                    info1[child.cget("text")]=inner
                    
        count =0
        for key,value in info1.items():
            count+=int(value[2])
        self.total_amount.config(state=NORMAL)
        self.total_amount.delete(0,END)
        self.total_amount.insert(0,f"{count:,}")
        self.total_amount.config(state=DISABLED)
        self.detail.place( x=110,y=460)
        self.view.config(state=NORMAL) 
        self.save.config(state=NORMAL)
        self.root.focus_force()    
        
    def majorfunction(self,choice):
        if choice == "C":
            if messagebox.askyesno("","Are you sure you want to cancel?",parent=self.root):
                self.root.destroy()
    def final_step(self,choice):
        self.root.focus_force()
        con = self.database_connection(1996)
        mycursor = con.cursor()
        s_id = None
        for key,value in detail.items():
            if key ==self.name.get():
                s_id =value
        mycursor.execute("SELECT*FROM suppliers where s_id =%s",s_id)
        fetch = mycursor.fetchone()
        supplier ={}
        supplier["Suppier Number:"]=fetch[0]
        supplier["Suppier Name:"]=fetch[1]
        supplier["Location:"]=fetch[2]
        supplier["Contact person:"]=fetch[3]
        supplier["Contact:"]=fetch[4]
        supplier["Email:"]=fetch[5]
        try:
            global deposit,total,balance,date
            deposit =int(self.total_deposit.get().strip().replace(",",""))
            total =int(self.total_amount.get().replace(",",""))
            if deposit>total:
                messagebox.showerror("","Deposit cannot be more than total bill!",parent=self.root)
                return     
            balance = total-deposit
            date = self.due.get()
            total = f"{total:,}"
            deposit =f"{deposit:,}"
            balance =f"{balance:,}"
        except:
            messagebox.showerror("","Only digits are allowed in the deposit entry!",parent=self.root)
            return
        root = Toplevel(self.root)
        root.geometry("500x520+350+100")
        root.title("Odre details")
        root.config(bg="white")
        root.resizable(0,0)
        self.text = Text(root,width=60,height=40)
        self.text.insert(1.14,"\t\tSupplier Details\n")
        count =2
        for key1,value1 in supplier.items():
            self.text.insert(f"{count}.0",f"{key1:<20}{value1}\n")
            # self.text.insert(f"{count}.30",f"{value1}\n")
            count+=1
            
        self.text.insert(END,"\n\n\t\tProducts Details\n")
        self.text.insert(END,"Product\t\tQty\tUnit cost(UGX)\t\tTotal(UGX)\n")
        self.text.insert(END,"*******\t\t***\t**************\t\t**********\n")
        for key1,value1 in info1.items():
            self.text.insert(END,f"{key1:<16}{value1[0]:<9}{value1[1]:<15}{value1[2]}\n")
        self.text.insert(END,"\n\n\t\tOther Details\n")
        self.text.insert(END,"Total bill\t\tDeposit(UGX)\t\tBalance(UGX)\t\tDue date\n")
        self.text.insert(END,"**********\t\t************\t\t************\t\t********\n")
        self.text.insert(END,f"{total:<16}{deposit:<16}{balance:<16}{date}\n")
        d ="Made on"
        A ="Authorised by"
        self.text.insert(END,f"\n\n{d:<16}: {datetime.datetime.now().strftime("%m/%d/%Y")}\n")
        self.text.insert(END,f"{A:<16}: Muli Isaac\n")
        self.text.pack()
        if choice =="V":
            root.grab_set()
            root.focus_force()
            root.transient(self.root)
            root.mainloop()
        else:
            root.grab_release()
            root.withdraw()
            self.root.focus_force()
            self.root.grab_set()
            self.root.transient(self.parent)
            table = '''CREATE TABLE IF NOT EXISTS purchase_ordder(o_id VARCHAR(20) PRIMARY KEY,date VARCHAR(30) NOT NULL,
            supplier VARCHAR(200) NOT NULL,bill VARCHAR(200) NOT NULL,deposit VARCHAR(15) NOT NULL,
            balance VARCHAR(30),due_date VARCHAR(1000) NOT NULL,status VARCHAR(1000) NOT NULL)'''
            mycursor.execute(table)
            id = "SELECT MAX(SUBSTR(o_id,1))FROM purchase_ordder"
            mycursor.execute(id)
            max_id = mycursor.fetchone()[0]
            if max_id is None:
                new_id = f"0000001"
            else:
                max_id = int(max_id)
                new_id =f"{str(max_id+1).zfill(7)}"
                if int(total.replace(",",""))<int(deposit.replace(",","")):
                    messagebox.showerror("","Deposit cannot be more than total bill!",parent=self.root)
                    return   
            query = "INSERT INTO purchase_ordder VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"
            values =(new_id,datetime.datetime.now().strftime("%m/%d/%Y"),supplier["Suppier Name:"],total,deposit.strip(),
                    balance,date,"waiting")
            # if messagebox.askyesnocancel("","Are you sure you want to save this ordder?",parent=self.root):
            mycursor.execute(query,values)
            partions = [f for f in os.listdir('/mnt')if os.path.isdir(os.path.join('/mnt',f))]if platform.system()=='Linux'else[f for f in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'if os.path.exists(f+":")]
            os_partition = sys.executable.split("\\")[0].rstrip(":").upper()
            non_os_partition = [p for p in partions if p!=os_partition]
            non_os_partition = non_os_partition[0] if non_os_partition is not None else None
            if not os.path.exists(f"{non_os_partition}:/inventory/purchase_order"):
                os.makedirs(f"{non_os_partition}:/inventory/purchase_order")
            file = open(f"{non_os_partition}:/inventory/purchase_order/{new_id}.txt",'w')
            file.write(self.text.get(1.0,END))
            file.close()
            table = '''CREATE TABLE IF NOT EXISTS ordered(id INT PRIMARY KEY AUTO_INCREMENT,p_id VARCHAR(20) NOT NULL,o_id VARCHAR(20) NOT NULL,qty VARCHAR(200) NOT NULL,
            FOREIGN KEY(p_id)REFERENCES products(p_id),FOREIGN KEY(o_id)REFERENCES purchase_ordder(o_id))
            '''
            mycursor.execute(table)
            for key,vaue in info1.items():
                query ="INSERT INTO ordered(p_id,o_id,qty,balance) VALUES((SELECT p_id FROM products WHERE name =%s),%s,%s,%s)"
                mycursor.execute(query,(key,new_id,vaue[0],vaue[0]))
            con.commit()
            con.close()
            messagebox.showinfo("","Ordder saved successfully!",parent=self.root)
            self.root.destroy()
            self.parent.focus_set()
            self.parent.grab_set() 
            return
        
            # except Exception as e:
            #     messagebox.showerror("Error",e,parent=self.root)
            #     return
        #else:return

    def final_step1(self,choice):
        self.root.focus_force()
        con = self.database_connection(1996)
        mycursor = con.cursor()
        s_id = None
        for key,value in detail.items():
            if key ==self.name.get():
                s_id =value
        mycursor.execute("SELECT*FROM suppliers where s_id =%s",s_id)
        fetch = mycursor.fetchone()
        supplier ={}
        supplier["Suppier Number:"]=fetch[0]
        supplier["Suppier Name:"]=fetch[1]
        supplier["Location:"]=fetch[2]
        supplier["Contact person:"]=fetch[3]
        supplier["Contact:"]=fetch[4]
        supplier["Email:"]=fetch[5]
        try:
            global deposit,total,balance,date
            deposit =int(self.total_deposit.get().strip().replace(",",""))
            total =int(self.total_amount.get().replace(",",""))
            balance = total-deposit
            date = self.due.get()
            total = f"{total:,}"
            deposit =f"{deposit:,}"
            balance =f"{balance:,}"
        except:
            messagebox.showerror("","Only digits are allowed in the deposit entry!",parent=self.root)
            return
        
        if choice=="S":
            if messagebox.askyesnocancel("","Are you sure you want to save this ordder?",parent=self.root):
                # try:
                con = self.database_connection(1996)
                mycursor = con.cursor()
            #     table = '''CREATE TABLE IF NOT EXISTS purchase_ordder(o_id VARCHAR(20) PRIMARY KEY,date VARCHAR(30) NOT NULL,
            #     supplier VARCHAR(200) NOT NULL,bill VARCHAR(200) NOT NULL,deposit VARCHAR(15) NOT NULL,
            #     balance VARCHAR(30),due_date VARCHAR(1000) NOT NULL,status VARCHAR(1000) NOT NULL)'''
            #     mycursor.execute(table)
            #     id = "SELECT MAX(SUBSTR(o_id,1))FROM purchase_ordder"
            #     mycursor.execute(id)
            #     max_id = mycursor.fetchone()[0]
            #     if max_id is None:
            #         new_id = f"0000001"
            #     else:
            #         max_id = int(max_id)
            #         new_id =f"{str(max_id+1).zfill(7)}"
            #         if int(total.replace(",",""))<int(deposit.replace(",","")):
            #             messagebox.showerror("","Deposit cannot be more than total bill!",parent=self.root)
            #             return   
            #     query = "INSERT INTO purchase_ordder VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"
            #     values =(new_id,datetime.datetime.now().strftime("%m/%d/%Y"),supplier["Suppier Name:"],total,deposit.strip(),
            #             balance,date,"waiting")
            #     # if messagebox.askyesnocancel("","Are you sure you want to save this ordder?",parent=self.root):
            #     mycursor.execute(query,values)
            #     partions = [f for f in os.listdir('/mnt')if os.path.isdir(os.path.join('/mnt',f))]if platform.system()=='Linux'else[f for f in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'if os.path.exists(f+":")]
            #     os_partition = sys.executable.split("\\")[0].rstrip(":").upper()
            #     non_os_partition = [p for p in partions if p!=os_partition]
            #     non_os_partition = non_os_partition[0] if non_os_partition is not None else None
            #     if not os.path.exists(f"{non_os_partition}:/inventory/purchase_order"):
            #         os.makedirs(f"{non_os_partition}:/inventory/purchase_order")
            #     file = open(f"{non_os_partition}:/inventory/purchase_order/{new_id}.txt",'w')
            #     file.write(self.text.get(1.0,END))
            #     messagebox.showinfo("","Ordder saved successfully!",parent=self.root)
            #     table = '''CREATE TABLE IF NOT EXISTS ordered(id INT PRIMARY KEY AUTO_INCREMENT,p_id VARCHAR(20) NOT NULL,o_id VARCHAR(20) NOT NULL,qty VARCHAR(200) NOT NULL,
            #     FOREIGN KEY(p_id)REFERENCES products(p_id),FOREIGN KEY(o_id)REFERENCES purchase_ordder(o_id))
            #     '''
            #     mycursor.execute(table)
            #     for key,vaue in info1.items():
            #         query ="INSERT INTO ordered(p_id,o_id,qty,balance) VALUES((SELECT p_id FROM products WHERE name =%s),%s,%s,%s)"
            #         mycursor.execute(query,(key,new_id,vaue[0],vaue[0]))
            #     con.commit()
            #     con.close()
            #     self.root.destroy()
            #     self.parent.focus_set()
            #     self.parent.grab_set() 
            
            #     # except Exception as e:
            #     #     messagebox.showerror("Error",e,parent=self.root)
            #     #     return
            # else:return

    ################
    
    def on_close(self,event):
        if self.on_clos:
            self.on_clos()
        self.root.grab_release()
        self.parent.focus_set()
        self.parent.grab_set()
    def focus_in(self,event):
        if self.total_deposit.get()=="0":
            self.total_deposit.delete(0,END)
            self.total_deposit.config(fg="black")
    def focus_out(self,event):
        if self.total_deposit.get()=="":
            self.total_deposit.insert(0,"0")
            self.total_deposit.config(fg="grey")
  

            