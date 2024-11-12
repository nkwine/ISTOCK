from tkinter import *
from tkcalendar import DateEntry
from tkinter import messagebox,ttk
import re
import pymysql, datetime,os,sys,platform
from tkcalendar import DateEntry
class sale_odder:
    def __init__(self,root,parent,on_clos=None):
        self.parent = parent
        self.root =root
        self.on_clos =on_clos
        self.root.geometry('1000x630+230+35')
        self.root.iconbitmap("employee__icon.ico")
        self.root.resizable(0,0)
        self.root.config(bg="white")
        self.root.grab_set()
        self.root.transient(parent)
        self.root.bind("<Destroy>",self.on_close)
        #heading
        self.titlelable =Label(self.root,text="Add a sale Order",font=("times new roman",20,'bold'),bg="#0f4d7d",fg="white")
        self.titlelable.place(x=0,y=0,relwidth=1)
        #main frame
        frame = Frame(self.root,bg="white")
        frame.place(x=2,y=40,relwidth=1)
        #first frame
        topframe =Frame(frame,bg="white")
        topframe.pack(fill=X)
        leftframe =Frame(topframe,bg="white",width=640)
        leftframe.grid(row=0,column=0)
        headl = Frame(leftframe,bg="white")
        headl.pack()
        name = Label(headl,text="Customer name",font=("times new roman",14,"bold"),bg="white")
        name.grid(row =0,column =0,padx=5)
        self.name = Entry(headl,font=("times new roman",12,"bold"),bg="lightyellow",width=25)
        self.name.grid(row =0,column =1,padx=5)
        contact = Label(headl,text="Contact",font=("times new roman",14,"bold"),bg="white")
        contact.grid(row =0,column =2,padx=5)
        self.contact = Entry(headl,font=("times new roman",12,"bold"),bg="lightyellow")
        self.contact.grid(row =0,column =3,padx=5)
        #middle
        middle = Frame(leftframe,height=500,bg="white")
        middle.pack(fill=X)
        sproducts = Label(middle,text="Selected Products",font=("times new roman",12,"bold"),bg="white")
        sproducts.pack(pady=10)
        self.pframe = Frame(middle,bg="white")
        self.base =Label(self.pframe,bg="white",)
        self.base.pack()
        self.pframe.pack()
        #Bill Details
        self.detail = Frame(middle, bg="white")
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
        
        
        #bottom
        bottom = Frame(self.root,bg="white")
        bottom.place(x=30,y=550)
        
        self.finish = Button(bottom, text="Finish", bg="#0f4d7d",fg="white",font=("times new roman",12),width=10,
                                   state=DISABLED,command=lambda:self.finishup())
        self.finish.grid(row=0,column=0,padx=7)
        self.bill_invoice = Button(bottom, text="Bill", bg="#0f4d7d",fg="white",font=("times new roman",12),width=10,
                                   state=DISABLED,command=lambda:self.billup())
        self.bill_invoice.grid(row=0,column=1,padx=7)
        self.save = Button(bottom, text="Save",bg="#0f4d7d",fg="white",font=("times new roman",12),width=10,
                                   state=DISABLED,command=lambda:self.inserti())
        self.save.grid(row=0,column=2,padx=7)
        self.print = Button(bottom,text="Print", bg="#0f4d7d",fg="white",font=("times new roman",12),width=10,
                                   state=DISABLED,command=lambda:self.mainfunction("co"))
        self.print.grid(row=0,column=3,padx=7)
        self.cancel= Button(bottom,text="Cancel", bg="#720505",fg="white",font=("times new roman",12),width=10,
                            command=self.go)
        self.cancel.grid(row=0,column=4,padx=10)
        
        rightframe =Frame(topframe,bg="white",width=420)
        rightframe.grid(row=0,column=1,rowspan=10)
        headr = Frame(rightframe,bg="white")
        headr.pack(anchor=E)
        self.search = Entry(headr,font=("times new roman",12,"bold"),bg="lightyellow",fg="grey")
        self.search.insert(0,"serch a product") 
        self.search.grid(row =0,column =0,padx=5,sticky=E)
        self.search.bind("<FocusIn>",self.focus_In)
        self.search.bind("<FocusOut>",self.focus_Out)
        button = Button(headr,text ="Search",bg="#0f4d7d",font=("times new roman",14,"bold"),fg="white",command=self.research)
        button.grid(row =0,column =1,padx=5,sticky=NE,ipadx=4)
        button = Button(headr,text ="Show all",bg="#0f4d7d",font=("times new roman",14,"bold"),fg="white",command=self.produt_list)
        button.grid(row =0,column =2,padx=5,sticky=NE,ipadx=4)
        #product frame
        product_frame = Frame(rightframe,bg="white")
        product_frame.pack() 
        scrolly = Scrollbar(product_frame,orient=VERTICAL)
        scrollx = Scrollbar(product_frame,orient=HORIZONTAL)
        products = Label(product_frame,text="Products, Click to select or deselect",font=("times new roman",12,"bold"),bg="white")
        products.pack()
        self.products = Listbox(product_frame,bg="lightyellow",fg="black",yscrollcommand=scrolly.set,xscrollcommand=scrollx.set,
            height=9,width=60,selectmode=MULTIPLE)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.config(command=self.products.yview)
        scrollx.config(command=self.products.xview)
        self.products.pack()
        self.products.bind("<Button-1>",self.show)
        #invoice
        bill_frame = Frame(rightframe,bg="white")
        bill_frame.pack() 
        y = Scrollbar(bill_frame,orient=VERTICAL)
        x = Scrollbar(bill_frame,orient=HORIZONTAL)
        bill = Label(bill_frame,text="Bill",font=("times new roman",12,"bold"),bg="white")
        bill.pack()
        self.bill = Text(bill_frame,bg="lightyellow",fg="black",yscrollcommand=y.set,xscrollcommand=x.set,
            height=18,width=45,)
        y.pack(side=RIGHT,fill=Y)
        x.pack(side=BOTTOM,fill=X)
        y.config(command=self.bill.yview)
        x.config(command=self.bill.xview)
        self.bill.pack()
        
        self.produt_list()
    #methods
    def database_connection(self,pas):
         try:
             return pymysql.connect(host="localhost",user="root",password=f"{pas}",database="inventory")
         except Exception as e:
             messagebox.showerror("Error",f"Failed connection {e}")
    def produt_list(self):
        con = self.database_connection(1996)
        mycursor = con.cursor()
        query = "SELECT* FROM products"
        self.products.delete(0,END)
        mycursor.execute(query)
        for itme in mycursor.fetchall():
            self.products.insert(END,itme[1])
    def research(self):
        if self.search.get().strip()=="serch a product" or self.search.get().strip()=="":
            messagebox.showerror("Error",f"You did not enter anything in the search entry")
            self.produt_list()
            return
        else:
            con = self.database_connection(1996)
            mycursor = con.cursor()
            mycursor.execute("SELECT* FROM products WHERE name LIKE %s",f"%{self.search.get().strip()}%") 
            record = mycursor.fetchall()
            if len(record)==0:
                 messagebox.showinfo("",f"You do not have {self.search.get().strip()} in your store")
                 self.produt_list()
            else:
                self.products.delete(0,END)
                for item in record:
                    self.products.insert(END,item[1]) 
        return      
    def show(self,event):
        con = self.database_connection(1996)
        mycursor = con.cursor()
        index = self.products.nearest(event.y)
        # if self.sup is not None:
        count=0
        number =0
        for child in self.pframe.winfo_children():
            if isinstance(child,LabelFrame) and child.cget("text")==self.products.get(index):
                self.root.unbind("<Destroy>")
                child.destroy()
                self.root.bind("<Destroy>",self.on_close)
                count+=1
        if count == 0:
            number=1
            self.new =LabelFrame(self.pframe,text=self.products.get(index),bg="white",font=("times new roman",15,"bold"))
            mycursor.execute("SELECT p_id,u_measure,unit_price FROM products WHERE name =%s",self.products.get(index).strip())
            record = mycursor.fetchone()
            # print(record[0],record[1],record[2])
            Label(self.new,text=f"Qty({record[1]})",bg="white").grid(row=0,column=0)
            e1=Entry(self.new,width=14,bg="lightyellow",font=("times new roman",12,"bold"))
            e1.grid(row=0,column=1)
            e1.bind("<FocusIn>",self.leave)
            Label(self.new,text="Unit price(UGX)",bg="white").grid(row=0,column=2)
            e2=Entry(self.new,width=14,bg="lightyellow",font=("times new roman",12,"bold"))
            e2.grid(row=0,column=3)
            e2.insert(0,f"{int(record[2]):,}")
            e2.config(state=DISABLED)
            Label(self.new,text="Total(UGX)",bg="white").grid(row=0,column=4)
            e3=Entry(self.new,width=14,bg="lightyellow",state=DISABLED,font=("times new roman",12,"bold"))
            e3.grid(row=0,column=5)
            e3.bind("<FocusIn>",self.leave2)
            self.new.pack(before=self.base,anchor=W)
        self.finish.config(state=DISABLED)
        self.bill_invoice.config(state=DISABLED)
        self.save.config(state=DISABLED)
        self.print.config(state=DISABLED)
        self.detail.pack_forget()
        self.bill.delete(1.0,END)
        self.check()
        return
       
    def check(self):
        try:
            counter=0
            for child in self.pframe.winfo_children():
                if isinstance(child,LabelFrame):
                    counter=1
                elif isinstance(child,Frame):
                    self.root.unbind("<Destroy>")
                    child.destroy()
                    self.root.bind("<Destroy>",self.on_close)
                    
            if counter>0:
                action = Frame(self.pframe,bg="white")
                action.pack()
                self.cont = Button(action, text="Continue", bg="#0C0A8F",fg="white",font=("times new roman",12),width=10,
                command=lambda:self.enable())
                self.cont.grid(row=0,column=0,padx=7)
                self.clear = Button(action, text="Clear", bg="#0C0A8F",fg="white",font=("times new roman",12),width=10,
                command=lambda:self.clea())
                self.clear.grid(row=0,column=1)
        except:
            pass
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
                                inner.append(grand.get().replace(",",""))
                            elif count>=3:
                                obj=grand
                                obj.config(state=NORMAL)
                    obj.delete(0,END)
                    obj.insert(0,f"{int(inner[0])*int(inner[1]):,}")
                    info[child.cget("text")]=inner
        con = self.database_connection(1996)
        mycursor = con.cursor()
        for key,value in info.items():
            mycursor.execute("SELECT qty,u_measure FROM products WHERE name  =%s",key)
            y = mycursor.fetchone()
            if int(y[0].replace(",",""))<int(value[0].replace(",","")):
                messagebox.showerror("",f"There are only {y[0]} {y[1]}(s) of {key} !",parent=self.root)
                return       
        self.finish.config(state=NORMAL)
        self.save.config(state=DISABLED) 
        self.print.config(state=DISABLED)
        self.bill_invoice.config(state=DISABLED)
        self.detail.pack_forget()
        self.root.focus_force()
    def clea(self):
        for child in self.pframe.winfo_children():
            if isinstance(child,LabelFrame) or isinstance(child,Frame):
                child.destroy()
        self.produt_list()
        return
    def finishup(self):
        global info1
        info1 ={}
        for child in self.pframe.winfo_children():
                if isinstance(child,LabelFrame):
                    inner =[]
                    for grand in child.winfo_children():
                        if isinstance(grand,Entry):
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
                    info1[child.cget("text")]=inner
                    
        count =0
        for key,value in info1.items():
            count+=int(value[2].replace(",",""))
        self.total_amount.config(state=NORMAL)
        self.total_amount.delete(0,END)
        self.total_amount.insert(0,f"{count:,}")
        self.total_amount.config(state=DISABLED)
        self.detail.pack(pady=6)
        self.bill_invoice.config(state=NORMAL) 
        self.root.focus_force()
    def billup(self):
        if self.name.get().strip()=="":
            messagebox.showerror("","Customer name can not be empty!",parent=self.root)
            return
        if self.contact.get().strip()==""or len(self.contact.get().strip())!=10 or self.contact.get().strip()[0]!="0":
            messagebox.showerror("","Invalid contact!",parent=self.root)
            return
        try:
            int(self.contact.get().strip())
            pass
        except:
            messagebox.showerror("","Invalid contact!",parent=self.root)
            return
        if self.total_deposit.get().strip()=="":
            depo = 0
        else:
            depo = self.total_deposit.get().strip().replace(",","")
        try:
            int(depo)
            pass
        except:
            messagebox.showerror("","Invalid input in the deposit entry",parent=self.root)
            return
                
        self.root.focus_force()
        con = self.database_connection(1996)
        mycursor = con.cursor()
        global info1
        info1 ={}
        for child in self.pframe.winfo_children():
            if isinstance(child,LabelFrame):
                    inner =[]
                    for grand in child.winfo_children():
                        if isinstance(grand,Entry):
                            inner.append(grand.get().replace(",",""))
                    info1[child.cget("text")] = inner
        self.bill.delete(1.0,END)
        self.bill.insert(END,f"Customer Name: {self.name.get()}\nCustomer Contact: {self.contact.get()}\n")
        self.bill.insert(END,f"\t\tItems\n")
        self.bill.insert(END,f" Item\t     Qty\t      Price(UGX)\tTotla(UGX)\n")
        self.bill.insert(END,f"*********\t   ****\t     **********\t**********\n")
        for key,value in info1.items():
            mycursor.execute("SELECT u_measure FROM products WHERE name  =%s",key)
            record = mycursor.fetchone()
            value.insert(0,record[0])
            unit =f"{int(value[2]):,}"
            am=f"{int(value[3]):,}"
            mea =f"{value[1]}{value[0]}"
            self.bill.insert(END,f"{key:<13}{mea:<10}{unit:<11}{am}\n")
        amount = self.total_amount.get().replace(",","")
        if int(depo)>int(amount):
            messagebox.showerror("","Deposit cannot be more than total bill!",parent=self.root)
            return   
        bal = int(amount)-int(depo)
        bal = f"{bal:,}"
        amount = f"{int(amount):,}"
        depo = f"{int(depo):,}"
        date = self.due.get_date()
        self.bill.insert(END,f"\t\tOther details\n")
        self.bill.insert(END,f"Total bill\t   Deposit(UGX)\t  Balance(UGX)\n")
        self.bill.insert(END,f"**********\t   ************\t  ************\n")
        self.bill.insert(END,f"{amount:<14}{depo:<15}{bal}\n")
        self.bill.insert(END,f"Due date: {date}\n")
        
        table = '''CREATE TABLE IF NOT EXISTS sale_order(o_id VARCHAR(20) PRIMARY KEY,date VARCHAR(30) NOT NULL,
        customer VARCHAR(200) NOT NULL,bill VARCHAR(200) NOT NULL,deposit VARCHAR(15) NOT NULL,
        balance VARCHAR(30),due_date VARCHAR(1000) NOT NULL,status VARCHAR(1000) NOT NULL)'''
        mycursor.execute(table)
        id = "SELECT MAX(SUBSTR(o_id,1))FROM sale_order"
        mycursor.execute(id)
        global to_insert_list
        to_insert_list  =[]
        max_id = mycursor.fetchone()[0]
        if max_id is None:
            new_id = f"0000001"
            to_insert_list.append(new_id)
        else:
            max_id = int(max_id)
            new_id =f"{str(max_id+1).zfill(7)}"
            to_insert_list.append(new_id)
        to_insert_list.append(amount)
        to_insert_list.append(depo)
        to_insert_list.append(bal)
        to_insert_list.append(date)
        self.bill.insert(1.0,f"Order Number: {new_id}\n")
        self.save.config(state=NORMAL) 
        self.print.config(state=NORMAL)    
    
    def inserti(self):
        con = self.database_connection(1996)
        mycursor = con.cursor()
        try:
            query = "INSERT INTO sale_order VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"
            values =(to_insert_list[0],datetime.datetime.now().strftime("%m/%d/%Y"),self.name.get(),to_insert_list[1],to_insert_list[2],
                    to_insert_list[3],to_insert_list[4],"pendding")
            if messagebox.askyesno("","Do you want to save this order"):
                mycursor.execute(query,values)
            else:
                return
            con.commit()
            table = '''CREATE TABLE IF NOT EXISTS ordered_sale(id INT PRIMARY KEY AUTO_INCREMENT,p_id VARCHAR(20) NOT NULL,
            o_id VARCHAR(20) NOT NULL,qty VARCHAR(200) NOT NULL,recieved VARCHAR(200) DEFAULT "0",balance VARCHAR(200) NOT NULL,FOREIGN KEY(p_id)REFERENCES products(p_id),
            FOREIGN KEY(o_id)REFERENCES sale_order(o_id))
                    '''
            mycursor.execute(table)
            for key,value in info1.items():
                mycursor.execute("SELECT qty,p_id FROM products WHERE name =%s",key)
                record = mycursor.fetchone()
                query ="INSERT INTO ordered_sale(p_id,o_id,qty,balance) VALUES((SELECT p_id FROM products WHERE name =%s),%s,%s,%s)"
                mycursor.execute(query,(key,to_insert_list[0],value[1],value[1]))
                record1=int(record [0].replace(",",""))
                new =record1-int(value[1].replace(",",""))
                mycursor.execute("UPDATE products SET qty= %s WHERE p_id=%s",(new,record[1]))
            con.commit()
            con.close()
            partions = [f for f in os.listdir('/mnt')if os.path.isdir(os.path.join('/mnt',f))]if platform.system()=='Linux'else[f for f in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'if os.path.exists(f+":")]
            os_partition = sys.executable.split("\\")[0].rstrip(":").upper()
            non_os_partition = [p for p in partions if p!=os_partition]
            non_os_partition = non_os_partition[0] if non_os_partition is not None else None
            if not os.path.exists(f"{non_os_partition}:/inventory/sale_order"):
                os.makedirs(f"{non_os_partition}:/inventory/sale_order")
            file = open(f"{non_os_partition}:/inventory/sale_order/{to_insert_list[0]}.txt",'w')
            file.write(self.bill.get(1.0,END))
            file.close()
            messagebox.showinfo("",f"Order saved successfuly",parent=self.root) 
            self.root.destroy()
            self.parent.focus_set()
            self.parent.grab_set() 
        except Exception as e:
            messagebox.showerror("Error",f"Something went wrong**{e}",parent=self.root)       

    def leave(self,evvent):
        self.finish.config(state=DISABLED)
        self.bill_invoice.config(state=DISABLED)
        self.save.config(state=DISABLED)
        self.print.config(state=DISABLED)
        self.detail.pack_forget()
        self.bill.delete(1.0,END)
    def leave2(self,evvent):
        self.bill_invoice.config(state=DISABLED)
        self.save.config(state=DISABLED)
        self.print.config(state=DISABLED)
        self.detail.pack_forget()
        self.bill.delete(1.0,END)
    def focus_in(self,event):
        if self.total_deposit.get()=="0":
            self.total_deposit.delete(0,END)
            self.total_deposit.config(fg="black")
        self.bill.delete(1.0,END)
        # self.bill_invoice.config(state=DISABLED)
        self.save.config(state=DISABLED) 
        self.print.config(state=DISABLED)
            
    def focus_out(self,event):
        if self.total_deposit.get()=="":
            self.total_deposit.insert(0,"0")
            self.total_deposit.config(fg="grey")
    def focus_In(self,event):
        if self.search.get()=="serch a product":
            self.search.delete(0,END)
            self.search.config(fg="black")
    def focus_Out(self,event):
        if self.search.get()=="":
            self.search.insert(0,"serch a product")
            self.search.config(fg="grey")
    def go(self):
        if messagebox.askyesno("","Do you really want to cancel",parent=self.root):
            self.root.destroy()
    def on_close(self,event):
        if self.on_clos:
            self.on_clos()
        self.root.grab_release()
        self.parent.focus_force()
        self.parent.grab_set()
        return
