from tkinter import *
import pymysql,os,platform,sys,datetime
from tkinter import ttk,messagebox
from tkcalendar import DateEntry
from .makesale import make_sale
class sales:
    def __init__(self,root,parent):
        self.root =root
        self.parent = parent
        self.root.resizable(0,0)
        self.root.geometry('1000x546+230+120')
        self.root.iconbitmap("employee__icon.ico")
        self.root.config(bg="#FFFFFF")
        self.root.grab_set()
        self.root.focus_force()
        self.root.transient(parent)
        self.titlelable =Label(self.root,text="Manage Sales",font=("times new roman",20,'bold'),bg="#0f4d7d",fg="white")
        self.titlelable.place(x=0,y=0,relwidth=1)
        #main frame
        frame = Frame(self.root,bg="white")
        frame.place(x=0,y=36,relwidth=1)
         #top frame
        self.top_frame =Frame(frame,bg="#FFFFFF",height=80)
        self.top_frame.pack(fill=X)
        self.combo_box = ttk.Combobox(self.top_frame,values=("sale_No","date","customer","status"),font=("times new roman",12,"bold"),state="readonly")
        self.combo_box.set("Search by")
        self.combo_box.grid(row=0,column=0, padx=50,pady=15)
        self.combo_box.bind("<<ComboboxSelected>>",lambda event:self.search_select())
        #search entery
        #op1
        self.search_entry = Entry(self.top_frame, font=("times new roman",12),width=17,bg="lightyellow")
        self.search_entry.grid(row=0,column=1)
        #op2
        self.date = DateEntry(self.top_frame,bg="lightyellow",width=17,font=("times new roman",11,"bold"))
        #op3
        self.status = ttk.Combobox(self.top_frame,values=("cleared","outstanding balance"),font=("times new roman",12,"bold"),state="readonly")
        self.status.set("Select")
        self.search_button =Button(self.top_frame,text="Search",font=("times new roman",12),width=10,cursor="hand2",bg="#0f4d7d",
                                   fg="white",command=lambda:self.majorfunction("se"))
        self.search_button.grid(row=0,column=3,padx=30)
        self.showall_button =Button(self.top_frame,text="Show all",font=("times new roman",12),width=10, cursor="hand2",bg="#0f4d7d",
                                    fg="white",command=lambda:self.majorfunction("sa"))
        self.showall_button.grid(row=0,column=4)
        self.add_sales = Button(self.top_frame, text="Make sale", bg="#0A8F36",fg="white",font=("times new roman",12),width=10,
                                   command=lambda:self.mainfunction("A"))
        self.add_sales.grid(row=0,column=5,padx=50)
        #middle frame
        self.middle_frame =Frame(frame)
        self.middle_frame.pack()
        #scrol bars
        horizont_scroll = Scrollbar(self.middle_frame,orient=HORIZONTAL)
        vertical_scroll = Scrollbar(self.middle_frame,orient=VERTICAL)
        #sales table
        self.sales_table =ttk.Treeview(self.middle_frame, columns=("sales_no",'date',"customer","bill",'deposite','balance',"status"
            ),show="headings",yscrollcommand=vertical_scroll.set,xscrollcommand=horizont_scroll.set,height=9)
        # self.details_display()
        horizont_scroll.pack(side=BOTTOM,fill=X,padx=0)
        vertical_scroll.pack(side=RIGHT,fill=Y)
        horizont_scroll.config(command=self.sales_table.xview)
        vertical_scroll.config(command=self.sales_table.yview)
        self.sales_table.heading('sales_no',text='sales_no')
        self.sales_table.heading('date',text='Date')
        self.sales_table.heading('customer',text='Customer')
        self.sales_table.heading('bill',text='Bill')
        self.sales_table.heading('deposite',text='Deposit')
        self.sales_table.heading('balance',text='Balance')
        self.sales_table.heading('status',text='Status')
        self.sales_table.pack(pady=10)
        self.sales_table.column('sales_no',width=80)
        self.sales_table.column('date',width=100)
        self.sales_table.column('customer',width=240)
        self.sales_table.column('bill',width=180)
        self.sales_table.column('deposite',width=150)
        self.sales_table.column('balance',width=180)
        self.sales_table.column('status',width=100)
        #bottom frame
        self.bottom_frame =Frame(frame,bg="white")
        self.bottom_frame.pack(pady=15)
        self.delete = Button(self.bottom_frame, text="delete", bg="#860404",fg="white",font=("times new roman",12),width=10,
                                   state=DISABLED,command=lambda:self.mainfunction("d"))
        self.delete.grid(row=0,column=0,padx=50)
        self.clear = Button(self.bottom_frame, text="Clear", bg="#0A8F36",fg="white",font=("times new roman",12),width=10,
                                   state=DISABLED,command=lambda:self.mainfunction("co"))
        self.clear.grid(row=0,column=2,padx=50)
        self.view= Button(self.bottom_frame, text="View", bg="#0f4d7d",fg="white",font=("times new roman",12),width=10,
                                   state=DISABLED,command=lambda:self.mainfunction("v"))
        self.view.grid(row=0,column=3,padx=50)
        self.sales_table.bind("<<TreeviewSelect>>",self.select)
        self.details_display()
    #methods
    def database_connection(self,pas):
        try:
            return pymysql.connect(host="localhost",user="root",password=f"{pas}",database="inventory")
        except:
            messagebox.showerror("Error",f"Failed connection") 
    def details_display(self):
        try:
            con = self.database_connection(1996)
            mycursor = con.cursor()
            query = "SELECT*FROM sales"
            mycursor.execute(query)
            data = mycursor.fetchall()
            self.sales_table.delete(*self.sales_table.get_children())
            for value in data:
                self.sales_table.insert("",END,values=value)
            self.delete.config(state=DISABLED)
            # self.cancelm.config(state=DISABLED)
            self.clear.config(state=DISABLED)
            self.view.config(state=DISABLED)
        except Exception as e:
            messagebox.showerror("Error",f"Something went wrong***{e}",parent=self.root)          
    def search_select(self):
        if self.combo_box.get()=="date":
            self.search_entry.grid_forget()
            self.status.grid_forget()
            self.date.grid(row=0,column=1,sticky=W)
        elif self.combo_box.get()=="status":
            self.search_entry.grid_forget()
            self.date.grid_forget()
            self.status.grid(row=0,column=1,sticky=W)
        else:
            self.date.grid_forget()
            self.status.grid_forget()
            self.search_entry.grid(row=0,column=1,sticky=W)    
    def majorfunction(self,choice):
        con = self.database_connection(1996)
        mycursor = con.cursor()
        if choice == "sa":
            self.details_display()
        else:
            if self.combo_box.get()!="Search by":
                if self.combo_box.get()=="sale_No":
                    if self.search_entry.get()!='':
                        query = '''SELECT*FROM sales WHERE s_id LIKE %s'''
                        mycursor.execute(query,f"%{self.search_entry.get()}%")
                        search =mycursor.fetchall()
                        if len(search)==0:
                            messagebox.showerror("Search error",f"No sale with number {self.search_entry.get()}!",parent=self.root)
                        else:
                            self.sales_table.delete(*self.sales_table.get_children())
                            for value in search:
                                self.sales_table.insert("",END,values=value)
                            con.close()
                            return
                    else:
                        messagebox.showerror("Search error","The search entry is empty!",parent=self.root)
                elif self.combo_box.get()=="customer":
                    if self.search_entry.get()!='':
                        query = '''SELECT*FROM sales WHERE customer LIKE %s'''
                        mycursor.execute(query,f"%{self.search_entry.get()}%")
                        search =mycursor.fetchall()
                        if len(search)==0:
                            messagebox.showerror("Search error",f"No customer named {self.search_entry.get()}!",parent=self.root)
                        else:
                            self.sales_table.delete(*self.sales_table.get_children())
                            for value in search:
                                self.sales_table.insert("",END,values=value)
                            con.close()
                            return
                    else:
                        messagebox.showerror("Search error","The search entry is empty!",parent=self.root)   
                     
                elif self.combo_box.get()=="date":
                        query = '''SELECT*FROM sales WHERE date = %s'''
                        mycursor.execute(query,f"{str(self.date.get_date().strftime('%m/%d/%Y'))}")
                        search =mycursor.fetchall()
                        if len(search)==0:
                            messagebox.showerror("Search error",f"No sale was made on {str(self.date.get_date().strftime('%m/%d/%Y'))}!",parent=self.root)
                        else:
                            self.sales_table.delete(*self.sales_table.get_children())
                            for value in search:
                                self.sales_table.insert("",END,values=value)
                            con.close()
                            return
                elif self.combo_box.get()=="status":
                    if self.status.get()!="Select":
                        query = '''SELECT*FROM sales WHERE status = %s'''
                        mycursor.execute(query,f"{str(self.status.get().strip())}")
                        search =mycursor.fetchall()
                        if len(search)==0:
                            messagebox.showerror("Search error",f"No sale with status {self.status.get().strip()}!",parent=self.root)
                            return
                        else:
                            self.sales_table.delete(*self.sales_table.get_children())
                            for value in search:
                                self.sales_table.insert("",END,values=value)
                            con.close()
                            return
                    else:
                        messagebox.showerror("Search error",f"No status was specified{self.search_entry.get()}!",parent=self.root)
                        return                    
                         
            else:
                messagebox.showerror("Search error","You did not specify search creteria!",parent=self.root)
                return
    def on_close(self,event,window):
        window.grab_release()
        self.root.focus_force()
        self.root.grab_set()
        self.details_display()  
            
    def select(self,event):
        if self.sales_table.focus()!="":
            self.delete.config(state=NORMAL)
            self.clear.config(state=NORMAL)
            self.view.config(state=NORMAL)
      
        return
    def mainfunction(self,choice):
        if choice =='A':
            swindow = Toplevel()
            obj = make_sale(swindow,self.root,self.details_display)
            swindow.mainloop()
        elif choice == "co":
            global tab_value
            self.root1 = Toplevel(self.root)
            self.root1.geometry("950x640+250+30")
            self.root1.title("clear sales")
            self.root1.grab_set()
            self.root1.focus_force()
            self.root1.transient(self.root)
            self.root1.config(bg="white")
            self.root1.resizable(0,0)
            self.root1.bind("<Destroy>",lambda event:self.on_close(self.root1))
            titlelable =Label(self.root1,text="Clear Payments",font=("times new roman",20,'bold'),bg="#0f4d7d",fg="white")
            titlelable.pack(fill=X)
            y = self.sales_table.focus()
            global sales
            sales = self.sales_table.item(y,"values")
            lable =Label(self.root1,text=f"customer: {sales[2]}",font=("times new roman",20,'bold'))
            lable.pack(fill=X)
            outer = Frame(self.root1,bg="white")
            outer.pack(fill=X)
            self.left = Frame(outer,bg="white",width=300)
            self.left.grid(row=0,column=0,sticky=N)
            right =Frame(outer,bg="white")
            right.grid(row=0,column=1,pady=15,sticky=NE)
            tab_value = sales[0]
            con = self.database_connection(1996)
            mycursor =  con.cursor()
            mycursor.execute("SELECT*FROM sale_items WHERE s_id =%s",sales[0])
            records = mycursor.fetchall()
            for record in records:
                mycursor.execute("SELECT name,u_measure FROM products WHERE p_id =%s",record[1])
                itme = mycursor.fetchone()
                found = LabelFrame(self.left,text= itme[0],bg="white",font=("times new roman",12))
                Label(found,text=f"Qty bought({itme[1]})",bg="white").grid(row=0,column=0)
                self.sale_items=Entry(found,width=16,bg="lightyellow",font=("times new roman",12))
                self.sale_items.grid(row=0,column=1)
                self.sale_items.insert(0,f"{int(record[3]):,}")
                self.sale_items.config(state=DISABLED)
                found.pack(pady=9,anchor=W,padx=40)
            # reciept =Text(right,width=60,height=20)
            # reciept.pack(anchor=E)
            y = Scrollbar(right,orient=VERTICAL)
            x = Scrollbar(right,orient=HORIZONTAL)
            reciept = Label(right,text="Reciept",font=("times new roman",12,"bold"),bg="white")
            reciept.pack()
            self.reciept = Text(right,bg="lightyellow",fg="black",yscrollcommand=y.set,xscrollcommand=x.set,
                width=60,height=20,)
            y.pack(side=RIGHT,fill=Y)
            x.pack(side=BOTTOM,fill=X)
            y.config(command=self.reciept.yview)
            x.config(command=self.reciept.xview)
            self.reciept.pack(anchor=E)

            fram = Frame(self.left,bg="white")
            Label(fram,text=f"Bill",bg="white").grid(row=0,column=0,pady=8)
            self.bill=Entry(fram,width=12,bg="lightyellow",font=("times new roman",12))
            self.bill.grid(row=0,column=1,pady=8)
            self.bill.insert(0,sales[3])
            self.bill.config(state=DISABLED)
            Label(fram,text=f"Deposit",bg="white").grid(row=0,column=2,pady=8)
            self.deposit=Entry(fram,width=12,bg="lightyellow",font=("times new roman",12))
            self.deposit.grid(row=0,column=3,pady=8)
            self.deposit.insert(0,sales[4])
            self.deposit.config(state=DISABLED)
            Label(fram,text=f"Balance",bg="white").grid(row=0,column=4)
            self.balance=Entry(fram,width=12,bg="lightyellow",font=("times new roman",12))
            self.balance.grid(row=0,column=5)
            self.balance.insert(0,sales[5])
            self.balance.config(state=DISABLED)
            
            fram.pack()
            fram1 = Frame(self.root1 ,bg="white")
            Label(fram1,text=f"Paid",bg="white").grid(row=1,column=1,pady=8)
            self.paid=Entry(fram1,width=16,bg="lightyellow",font=("times new roman",12))
            self.paid.grid(row=1,column=2,pady=8)
            self.paid.insert(0,"0")
            self.paid.bind("<FocusIn>",self.focus_in)
            self.paid.bind("<FocusOut>",self.focus_out)
            fram1.pack()
            fram2 = Frame(self.root1,bg="white")
            self.fin= Button(fram2, text="Continue", bg="#0f4d7d",fg="white",font=("times new roman",12),width=10,
                                   command=lambda:self.control(self.root1,"cont"))
            self.fin.grid(row=0,column=0,padx=30)
            self.save = Button(fram2, text="Save", bg="#0f4d7d",fg="white",font=("times new roman",12),width=10,
                                   command=lambda:self.control(self.root1,"s"),state=DISABLED)
            self.save.grid(row=0,column=1,padx=30)
            self.prin = Button(fram2, text="Print", bg="#0f4d7d",fg="white",font=("times new roman",12),width=10,
                                   command=lambda:self.control(self.root1,"p"),state=DISABLED)
            self.prin.grid(row=0,column=2,padx=30)
            self.cancel= Button(fram2, text="Cancel", bg="#7C0707",fg="white",font=("times new roman",12),width=10,
                                    command=lambda:self.control(self.root1,"ca"))
            self.cancel.grid(row=0,column=3,padx=30)
            fram2.pack()
            self.root1.mainloop()
        elif choice == "d":
            y = self.sales_table.focus()
            sales = self.sales_table.item(y,"values")
            tab= sales[0]
            if sales[6] == "cleared":
                if messagebox.askyesno("","Are you sure you want to permanently delete this sale",parent=self.root):
                    try:
                        con =self.database_connection(1996)
                        mycursor = con.cursor()
                        mycursor.execute("DELETE FROM sale_items WHERE s_id =%s",tab)
                        con.commit()
                        mycursor.execute("DELETE FROM sales WHERE s_id =%s",tab)
                        con.commit()
                        partions = [f for f in os.listdir('/mnt')if os.path.isdir(os.path.join('/mnt',f))]if platform.system()=='Linux'else[f for f in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'if os.path.exists(f+":")]
                        os_partition = sys.executable.split("\\")[0].rstrip(":").upper()
                        non_os_partition = [p for p in partions if p!=os_partition]
                        non_os_partition = non_os_partition[0] if non_os_partition is not None else None
                        path = f"{non_os_partition}:/inventory/purchase_sale"
                        if os.path.exists(path):
                            for item in os.listdir(path):
                                if os.path.isfile(os.path.join(path,item)) and item.split(".")[0]==tab:
                                    os.remove(os.path.join(path,item))
                                    messagebox.showinfo("Deleted",f"sale successfully deleted",parent=self.root)
                                    self.details_display()
                    except Exception as e:
                        messagebox.showerror("Error",f"Some thing went wrong{e}",parent=self.root)
            else:
                messagebox.showerror("Error",f"You can only delete a sale that has been cleared",parent=self.root)                
        elif choice == "v":
            aroot = Toplevel(self.root)
            aroot.geometry("500x520+350+100")
            aroot.title("Sale details")
            aroot.grab_set()
            aroot.focus_force()
            aroot.transient(self.root)
            aroot.config(bg="white")
            aroot.resizable(0,0)
            aroot.bind("<Destroy>",lambda event:self.on_close(aroot))
            self.texta = Text(aroot)
            self.texta.pack()
            y = self.sales_table.focus()
            sales = self.sales_table.item(y,"values")
            tab= sales[0]
            partions = [f for f in os.listdir('/mnt')if os.path.isdir(os.path.join('/mnt',f))]if platform.system()=='Linux'else[f for f in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'if os.path.exists(f+":")]
            os_partition = sys.executable.split("\\")[0].rstrip(":").upper()
            non_os_partition = [p for p in partions if p!=os_partition]
            non_os_partition = non_os_partition[0] if non_os_partition is not None else None
            path = f"{non_os_partition}:/inventory/sales"
            if os.path.exists(path):
                for item in os.listdir(path):
                    if os.path.isfile(os.path.join(path,item)) and item.split(".")[0]==tab:
                        file = open(os.path.join(path,item),"r")
                        self.texta.delete(1.0,END)
                        for value in file:
                            self.texta.insert(END,value)

            aroot.mainloop() 
    def control(self,root,choice):
        if choice =="ca":
            if messagebox.askyesno("","Do you really want to cancel",parent=root):
                root.destroy()
                return
        elif choice =="cont":
            con =self.database_connection(1996)
            mycursor = con.cursor()
            self.root1.focus_force()
            if self.paid.get().strip()!="0":
                try:
                    newv = int(self.paid.get().strip().replace(",",""))
                    mycursor.execute("SELECT balance,deposit,bill FROM sales WHERE s_id=%s",tab_value)
                    fetch = mycursor.fetchone()
                    if newv >int(fetch[0].replace(",","")):
                        messagebox.showerror("Error",f"You entered more money than the expected",parent=root)
                        return
                    else:
                        global old,current,bal,tob,depo
                        old =fetch[0].replace(",","")
                        old =f"{int(old):,}"
                        current =  f"{newv:,}"
                        bal =int(fetch[0].replace(",",""))-newv
                        bal = f"{bal:,}"
                        tob = fetch[2].replace(",","")
                        tob =f"{int(tob):,}"
                        depo =int(fetch[1].replace(",",""))+newv
                        depo =f'{depo:,}'
                    dic = {}
                    for child in self.left.winfo_children():
                        if isinstance(child,LabelFrame):
                            li =[]
                            for grand in child.winfo_children():
                                if isinstance(grand,Entry):
                                    li.append(grand.get().strip().replace(",",""))
                            dic[child.cget("text")]=li
                    self.reciept.insert(END,f"\t\tIsaac HardWare\n\t\t   Reciept\n")
                    self.reciept.insert(END,f"\nCusomer name: {sales[2]}\n")
                    self.reciept.insert(END,f"      Item\t\t    QTY\t   Price(UGX)\t  TOtal(UGX)\n")
                    self.reciept.insert(END,f"******************\t*****\t  **********\t  **********\n")
                    for key,value in dic.items():
                        mycursor.execute("SELECT unit_price FROM products WHERE name =%s",key)
                        rais = mycursor.fetchone()
                        rais =rais[0].replace(",","")
                        money =int(value[0])*int(rais)
                        money =f"{money:,}"
                        rais =f"{int(rais):,}"                        
                        self.reciept.insert(END,f"{key:<18} {value[0]:<8}{rais:<13}{money}\n")
                    self.reciept.insert(END,f"\nTotal bill(UGX)\t Prev_balance(UGX)\tPaid(UGX)\t  Balance(UGX)\n")
                    self.reciept.insert(END,f"************\t    ****************\t *********\t  ************\n")
                    self.reciept.insert(END,f"{tob:<17}{old:<18}{current:<12} {bal}\n\n")
                    self.reciept.insert(END,f"Issued by: ..........................\n\nDate: {datetime.date.today()}  Signature: ..............\n")
                    self.prin.config(state=NORMAL)
                    self.save.config(state=NORMAL)
                except Exception as e:
                    messagebox.showerror("Error",f"Only digits are allowed {e}",parent=root)
                    return
            else:
                messagebox.showerror("Error","You did not make any payments!",parent=root)
                return
                
        elif choice == "s":
            con = self.database_connection(1996)
            mycursor =con.cursor()
            if messagebox.askyesno("","Do you really want to save",parent=root):
                try:
                    if bal =="0":
                        status ="cleared"
                    else:
                        status = "outstanding balance"
                    mycursor.execute("UPDATE sales SET deposit =%s,balance =%s,status =%s WHERE s_id =%s",(depo,bal,status,tab_value))
                    table ="CREATE TABLE IF NOT EXISTS reciepts(r_id VARCHAR(20) PRIMARY KEY,date VARCHAR(30) NOT NULL,customer VARCHAR(200) NOT NULL)"
                    mycursor.execute(table)
                    id = "SELECT MAX(SUBSTR(r_id,1))FROM reciepts"
                    mycursor.execute(id)
                    max_id = mycursor.fetchone()[0]
                    if max_id is None:
                        new_id = f"0000001"
                    else:
                        max_id = int(max_id)
                        new_id =f"{str(max_id+1).zfill(7)}"
                    query ="INSERT INTO reciepts VALUES(%s,%s,%s)"
                    self.reciept.insert(1.0,f"Sale Number: {new_id}\n")
                    partions = [f for f in os.listdir('/mnt')if os.path.isdir(os.path.join('/mnt',f))]if platform.system()=='Linux'else[f for f in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'if os.path.exists(f+":")]
                    os_partition = sys.executable.split("\\")[0].rstrip(":").upper()
                    non_os_partition = [p for p in partions if p!=os_partition]
                    non_os_partition = non_os_partition[0] if non_os_partition is not None else None
                    if not os.path.exists(f"{non_os_partition}:/inventory/reciepts"):
                        os.makedirs(f"{non_os_partition}:/inventory/reciepts")
                    file = open(f"{non_os_partition}:/inventory/reciepts/{new_id}.txt",'w')
                    file.write(self.reciept.get(1.0,END))
                    file.close()
                    mycursor.execute(query,(new_id,f"{datetime.date.today()}",sales[2]))
                    con.commit()
                    con.close()
                    messagebox.showinfo("",f"Sale saved successfuly",parent=self.root1)
                    self.root1.destroy()
                except Exception as e:
                    messagebox.showerror("Error",f"Something went wrong",parent=root)
                    return                
          
    def focus_in(self,event):
        if self.paid.get()=="0":
            self.paid.delete(0,END)
            self.paid.config(fg="black")
        self.prin.config(state=DISABLED)
        self.save.config(state=DISABLED)
        self.reciept.delete(1.0,END)
        
    def focus_out(self,event):
        if self.paid.get()=="":
            self.paid.insert(0,"0")
    def on_close(self,event):
        self.root.focus_force()
        self.root.grab_set()
        self.details_display()
