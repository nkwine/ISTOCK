from tkinter import *
import pymysql,os,platform,sys
from tkinter import ttk,messagebox
from tkcalendar import DateEntry
from .addorder import addOrder
class purchase:
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
        self.titlelable =Label(self.root,text="Manage Purchase Orders",font=("times new roman",20,'bold'),bg="#0f4d7d",fg="white")
        self.titlelable.place(x=0,y=0,relwidth=1)
        #main frame
        frame = Frame(self.root,bg="white")
        frame.place(x=0,y=36,relwidth=1)
         #top frame
        self.top_frame =Frame(frame,bg="#FFFFFF",height=80)
        self.top_frame.pack(fill=X)
        self.combo_box = ttk.Combobox(self.top_frame,values=("Order_No","date","supplier","status"),font=("times new roman",12,"bold"),state="readonly")
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
        self.status = ttk.Combobox(self.top_frame,values=("waiting","partially delivered","delivered","over due","canceled"),font=("times new roman",12,"bold"),state="readonly")
        self.status.set("Select")
        self.search_button =Button(self.top_frame,text="Search",font=("times new roman",12),width=10,cursor="hand2",bg="#0f4d7d",
                                   fg="white",command=lambda:self.majorfunction("se"))
        self.search_button.grid(row=0,column=3,padx=30)
        self.showall_button =Button(self.top_frame,text="Show all",font=("times new roman",12),width=10, cursor="hand2",bg="#0f4d7d",
                                    fg="white",command=lambda:self.majorfunction("sa"))
        self.showall_button.grid(row=0,column=4)
        self.add_oder = Button(self.top_frame, text="Add order", bg="#0A8F36",fg="white",font=("times new roman",12),width=10,
                                   command=lambda:self.mainfunction("A"))
        self.add_oder.grid(row=0,column=5,padx=50)
        #middle frame
        self.middle_frame =Frame(frame)
        self.middle_frame.pack()
        #scrol bars
        horizont_scroll = Scrollbar(self.middle_frame,orient=HORIZONTAL)
        vertical_scroll = Scrollbar(self.middle_frame,orient=VERTICAL)
        #oder table
        self.oder_table =ttk.Treeview(self.middle_frame, columns=("oder_no",'date',"oder","bill",'deposite','balance',"duedate","status"
            ),show="headings",yscrollcommand=vertical_scroll.set,xscrollcommand=horizont_scroll.set,height=9)
        # self.details_display()
        horizont_scroll.pack(side=BOTTOM,fill=X,padx=0)
        vertical_scroll.pack(side=RIGHT,fill=Y)
        horizont_scroll.config(command=self.oder_table.xview)
        vertical_scroll.config(command=self.oder_table.yview)
        self.oder_table.heading('oder_no',text='Oder_no')
        self.oder_table.heading('date',text='Date')
        self.oder_table.heading('oder',text='Supplier')
        self.oder_table.heading('bill',text='Bill')
        self.oder_table.heading('deposite',text='Deposit')
        self.oder_table.heading('balance',text='Balance')
        self.oder_table.heading('duedate',text='Due date')
        self.oder_table.heading('status',text='Status')
        self.oder_table.pack(pady=10)
        self.oder_table.column('oder_no',width=80)
        self.oder_table.column('date',width=100)
        self.oder_table.column('oder',width=240)
        self.oder_table.column('bill',width=180)
        self.oder_table.column('deposite',width=150)
        self.oder_table.column('balance',width=180)
        self.oder_table.column('duedate',width=100)
        self.oder_table.column('status',width=100)
        #bottom frame
        self.bottom_frame =Frame(frame,bg="white")
        self.bottom_frame.pack(pady=15)
        self.delete = Button(self.bottom_frame, text="delete", bg="#860404",fg="white",font=("times new roman",12),width=10,
                                   state=DISABLED,command=lambda:self.mainfunction("d"))
        self.delete.grid(row=0,column=0,padx=50)
        self.cancelm = Button(self.bottom_frame, text="cancel", bg="#8F0A4D",fg="white",font=("times new roman",12),width=10,
                                   state=DISABLED,command=lambda:self.mainfunction("c"))
        self.cancelm.grid(row=0,column=1,padx=50)
        self.confirm = Button(self.bottom_frame, text="confirm", bg="#0A8F36",fg="white",font=("times new roman",12),width=10,
                                   state=DISABLED,command=lambda:self.mainfunction("co"))
        self.confirm.grid(row=0,column=2,padx=50)
        self.view= Button(self.bottom_frame, text="View", bg="#0f4d7d",fg="white",font=("times new roman",12),width=10,
                                   state=DISABLED,command=lambda:self.mainfunction("v"))
        self.view.grid(row=0,column=3,padx=50)
        self.oder_table.bind("<<TreeviewSelect>>",self.select)
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
            query = "SELECT*FROM purchase_ordder"
            mycursor.execute(query)
            data = mycursor.fetchall()
            self.oder_table.delete(*self.oder_table.get_children())
            for value in data:
                self.oder_table.insert("",END,values=value)
            self.delete.config(state=DISABLED)
            self.cancelm.config(state=DISABLED)
            self.confirm.config(state=DISABLED)
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
                if self.combo_box.get()=="Order_No":
                    if self.search_entry.get()!='':
                        query = '''SELECT*FROM purchase_ordder WHERE o_id LIKE %s'''
                        mycursor.execute(query,f"%{self.search_entry.get()}%")
                        search =mycursor.fetchall()
                        if len(search)==0:
                            messagebox.showerror("Search error",f"No order with number {self.search_entry.get()}!",parent=self.root)
                        else:
                            self.oder_table.delete(*self.oder_table.get_children())
                            for value in search:
                                self.oder_table.insert("",END,values=value)
                            con.close()
                            return
                    else:
                        messagebox.showerror("Search error","The search entry is empty!",parent=self.root)
                elif self.combo_box.get()=="supplier":
                    if self.search_entry.get()!='':
                        query = '''SELECT*FROM purchase_ordder WHERE supplier LIKE %s'''
                        mycursor.execute(query,f"%{self.search_entry.get()}%")
                        search =mycursor.fetchall()
                        if len(search)==0:
                            messagebox.showerror("Search error",f"No supplier named {self.search_entry.get()}!",parent=self.root)
                        else:
                            self.oder_table.delete(*self.oder_table.get_children())
                            for value in search:
                                self.oder_table.insert("",END,values=value)
                            con.close()
                            return
                    else:
                        messagebox.showerror("Search error","The search entry is empty!",parent=self.root)   
                     
                elif self.combo_box.get()=="date":
                        query = '''SELECT*FROM purchase_ordder WHERE date = %s'''
                        mycursor.execute(query,f"{str(self.date.get_date().strftime('%m/%d/%Y'))}")
                        search =mycursor.fetchall()
                        if len(search)==0:
                            messagebox.showerror("Search error",f"No order was made on {str(self.date.get_date().strftime('%m/%d/%Y'))}!",parent=self.root)
                        else:
                            self.oder_table.delete(*self.oder_table.get_children())
                            for value in search:
                                self.oder_table.insert("",END,values=value)
                            con.close()
                            return
                elif self.combo_box.get()=="status":
                    if self.status.get()!="Select":
                        query = '''SELECT*FROM purchase_ordder WHERE status = %s'''
                        mycursor.execute(query,f"{str(self.status.get().strip())}")
                        search =mycursor.fetchall()
                        if len(search)==0:
                            messagebox.showerror("Search error",f"No order with status {self.status.get().strip()}!",parent=self.root)
                            return
                        else:
                            self.oder_table.delete(*self.oder_table.get_children())
                            for value in search:
                                self.oder_table.insert("",END,values=value)
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
        if self.oder_table.focus()!="":
            self.delete.config(state=NORMAL)
            self.cancelm.config(state=NORMAL)
            self.confirm.config(state=NORMAL)
            self.view.config(state=NORMAL)
      
        return
    def mainfunction(self,choice):
        if choice =='A':
            aowindow = Toplevel()
            obj = addOrder(aowindow,self.root,self.details_display)
            aowindow.mainloop()
        elif choice =='c':
            con = self.database_connection(1996)
            mycursor = con.cursor()
            y = self.oder_table.focus()
            y = self.oder_table.item(y,"values")
            a=y[0]
            b =y[7]
            if b!="canceled" and b!="delivered" and b!="partially delivered":
                query1 = "UPDATE purchase_ordder SET status =%s WHERE o_id = %s"
                if messagebox.askyesnocancel("","Are you sure you want to cancel this ordder?",parent=self.root):
                    value =("canceled",a)
                    mycursor.execute(query1,value)
                    messagebox.showinfo("","Order canceled!",parent=self.root)
                    con.commit()
                    self.details_display()
                    return 
            else:
                messagebox.showerror("Error","You can only cancel an order that has not been delivered or canceled already!",parent=self.root)
                return
        elif choice == "co":
            global tab_value
            global info
            info ={}
            self.root1 = Toplevel(self.root)
            self.root1.geometry("800x560+350+100")
            self.root1.title("confirm oder")
            self.root1.grab_set()
            self.root1.focus_force()
            self.root1.transient(self.root)
            self.root1.config(bg="white")
            self.root1.resizable(0,0)
            self.root1.bind("<Destroy>",lambda event:self.on_close(self.root1))
            titlelable =Label(self.root1,text="Comfirm delivered products",font=("times new roman",20,'bold'),bg="#0f4d7d",fg="white")
            titlelable.pack(fill=X)
            y = self.oder_table.focus()
            oder = self.oder_table.item(y,"values")
            lable =Label(self.root1,text=f"Supplier: {oder[2]}",font=("times new roman",20,'bold'))
            lable.pack(fill=X)
            tab_value = oder[0]
            con = self.database_connection(1996)
            mycursor =  con.cursor()
            mycursor.execute("SELECT*FROM ordered WHERE o_id =%s",oder[0])
            records = mycursor.fetchall()
            for record in records:
                mycursor.execute("SELECT name,u_measure FROM products WHERE p_id =%s",record[1])
                itme = mycursor.fetchone()
                found = LabelFrame(self.root1,text= itme[0],bg="white",font=("times new roman",12))
                Label(found,text=f"Qty ordered({itme[1]})",bg="white").grid(row=0,column=0)
                self.ordered=Entry(found,width=16,bg="lightyellow",font=("times new roman",12))
                self.ordered.grid(row=0,column=1)
                self.ordered.insert(0,f"{int(record[3]):,}")
                self.ordered.config(state=DISABLED)
                Label(found,text="Qty recieved",bg="white").grid(row=0,column=2)
                self.recieved=Entry(found,width=16,bg="lightyellow",font=("times new roman",12))
                self.recieved.grid(row=0,column=3)
                # self.recieved.insert(0,f"{int(record[4]):,}")
                Label(found,text="Balance",bg="white").grid(row=0,column=4)
                self.qtyre=Entry(found,width=16,bg="lightyellow",font=("times new roman",12))
                self.qtyre.grid(row=0,column=5)
                self.qtyre.insert(0,f"{int(record[5]):,}")
                self.qtyre.config(state=DISABLED)
                info[itme[0]]=[record[1],record[2]]
                found.pack(pady=15,anchor=W,padx=12)
            fram = Frame(self.root1,bg="white")
            Label(fram,text=f"Bill",bg="white").grid(row=0,column=0,pady=8)
            self.bill=Entry(fram,width=16,bg="lightyellow",font=("times new roman",12))
            self.bill.grid(row=0,column=1,pady=8)
            self.bill.insert(0,oder[3])
            self.bill.config(state=DISABLED)
            Label(fram,text=f"Deposit",bg="white").grid(row=0,column=2,pady=8)
            self.deposit=Entry(fram,width=16,bg="lightyellow",font=("times new roman",12))
            self.deposit.grid(row=0,column=3,pady=8)
            self.deposit.insert(0,oder[4])
            self.deposit.config(state=DISABLED)
            Label(fram,text=f"Balance",bg="white").grid(row=0,column=4)
            self.balance=Entry(fram,width=16,bg="lightyellow",font=("times new roman",12))
            self.balance.grid(row=0,column=5)
            self.balance.insert(0,oder[5])
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
            self.save = Button(fram2, text="Save", bg="#0f4d7d",fg="white",font=("times new roman",12),width=10,
                                   command=lambda:self.control(self.root1,"s"))
            self.save.grid(row=0,column=0,padx=50)
            self.cancel= Button(fram2, text="Cancel", bg="#7C0707",fg="white",font=("times new roman",12),width=10,
                                    command=lambda:self.control(self.root1,"ca"))
            self.cancel.grid(row=0,column=1,padx=50)
            fram2.pack()
            self.root1.mainloop()
        elif choice == "d":
            y = self.oder_table.focus()
            oder = self.oder_table.item(y,"values")
            tab= oder[0]
            if oder[7] == "delivered" or oder[7] == "canceled":
                if messagebox.askyesno("","Are you sure you want to permanently delete this order",parent=self.root):
                    try:
                        con =self.database_connection(1996)
                        mycursor = con.cursor()
                        mycursor.execute("DELETE FROM ordered WHERE o_id =%s",tab)
                        con.commit()
                        mycursor.execute("DELETE FROM purchase_ordder WHERE o_id =%s",tab)
                        con.commit()
                        partions = [f for f in os.listdir('/mnt')if os.path.isdir(os.path.join('/mnt',f))]if platform.system()=='Linux'else[f for f in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'if os.path.exists(f+":")]
                        os_partition = sys.executable.split("\\")[0].rstrip(":").upper()
                        non_os_partition = [p for p in partions if p!=os_partition]
                        non_os_partition = non_os_partition[0] if non_os_partition is not None else None
                        path = f"{non_os_partition}:/inventory/purchase_order"
                        if os.path.exists(path):
                            for item in os.listdir(path):
                                if os.path.isfile(os.path.join(path,item)) and item.split(".")[0]==tab:
                                    os.remove(os.path.join(path,item))
                                    messagebox.showinfo("Deleted",f"Order successfully deleted",parent=self.root)
                                    self.details_display()
                    except Exception as e:
                        messagebox.showerror("Error",f"Some thing went wrong{e}",parent=self.root)
            else:
                messagebox.showerror("Error","You can only delete an order that has been delivered or canceled",parent=self.root)
                    
        elif choice == "v":
            aroot = Toplevel(self.root)
            aroot.geometry("500x520+350+100")
            aroot.title("Odre details")
            aroot.grab_set()
            aroot.focus_force()
            aroot.transient(self.root)
            aroot.config(bg="white")
            aroot.resizable(0,0)
            aroot.bind("<Destroy>",lambda event:self.on_close(aroot))
            self.texta = Text(aroot)
            self.texta.pack()
            y = self.oder_table.focus()
            oder = self.oder_table.item(y,"values")
            tab= oder[0]
            partions = [f for f in os.listdir('/mnt')if os.path.isdir(os.path.join('/mnt',f))]if platform.system()=='Linux'else[f for f in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'if os.path.exists(f+":")]
            os_partition = sys.executable.split("\\")[0].rstrip(":").upper()
            non_os_partition = [p for p in partions if p!=os_partition]
            non_os_partition = non_os_partition[0] if non_os_partition is not None else None
            path = f"{non_os_partition}:/inventory/purchase_order"
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
        elif choice == "s":
            if messagebox.askyesno("","Do you really want to save change",parent=root):
                try:
                    for child in self.root1.winfo_children():
                        if isinstance(child,LabelFrame):
                            val = []
                            for grand in child.winfo_children():
                                if isinstance(grand,Entry):
                                    val.append(grand.get().strip())
                            for key,value in info.items():
                                if key == child.cget("text"):
                                    if len(value)==3:
                                        value[2]=val
                                    else:
                                        value.append(val)
                    for key,value in info.items():
                        if value[2][1]=="":
                            value[2][1]=0
                    try:
                        for key,value in info.items():
                            int(value[2][1])
                            if self.paid.get().strip()!="":
                                int(self.paid.get().strip().replace(",",""))
                    except:
                        messagebox.showerror("Error","Only digits are allowed",parent=root)
                        return
                    count = 0
                    for key,value in info.items():
                        con = self.database_connection(1996)
                        mycursor = con.cursor()
                        mycursor.execute("SELECT id,recieved,balance from ordered WHERE p_id=%s AND o_id=%s",(value[0],value[1]))
                        fetch = mycursor.fetchone()
                        if int(fetch[2])<=0 and int(value[2][1])!=0:
                            messagebox.showerror("Error",f"All {key} odered were/was delivered",parent=root)
                            return
                        elif int(value[2][1])>int(fetch[2]):
                            messagebox.showerror("Error",f"The qty of {key} you entered is morethan the qty expected",parent=root)
                            return
                        else:   
                            reciev = int(value[2][1])+int(fetch[1])
                            bal = int(fetch[2])- int(value[2][1])
                            count+=bal
                            mycursor.execute("UPDATE ordered SET recieved=%s,balance=%s WHERE id =%s",(str(reciev),str(bal),fetch[0]))
                        mycursor.execute("SELECT qty from products WHERE p_id=%s",value[0])
                        fetch = mycursor.fetchone()
                        val =int(fetch[0])+int(value[2][1])
                        mycursor.execute("UPDATE products SET qty=%s WHERE p_id =%s",(val,value[0]))
                        con.commit()
                        
                    if count == 0:
                        status = "delivered"
                    else:
                        status = "partially delivered"
                    if self.paid.get().strip()=="":
                        new =0
                    else: new = int(self.paid.get().strip().replace(",",""))
                    mycursor.execute("SELECT balance,deposit FROM purchase_ordder WHERE o_id=%s",tab_value)
                    fetch = mycursor.fetchone()
                    if new >int(fetch[0].replace(",","")):
                        messagebox.showerror("Error",f"You entered more money than the expected",parent=root)
                        return
                    to_in = int(fetch[0].replace(",",""))-new
                    depo =new+int(fetch[1].replace(",",""))
                    mycursor.execute("UPDATE purchase_ordder SET deposit=%s,balance=%s,status=%s WHERE o_id =%s",(f"{depo:,}",f"{to_in:,}",status,tab_value))
                    con.commit()
                    messagebox.showinfo("","Data successful saved",parent=root)
                    self.root1.destroy()
                    self.details_display()
                    return 
                except Exception as e:
                    messagebox.showerror("Error",f"Some thing went wrong {e}",parent=root)
                    return
            return
    def focus_in(self,event):
        if self.paid.get()=="0":
            self.paid.delete(0,END)
            self.paid.config(fg="black")
    def focus_out(self,event):
        if self.paid.get()=="":
            self.paid.insert(0,"0")
    def on_close(self,event):
        self.root.focus_get()
        self.root.grab_set()
        self.details_display()
    def on_closev(self,event):
        self.root.focus_get()
        self.root.grab_set()
        self.details_display()
        return
