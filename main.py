from tkinter import *
from tkinter import messagebox
import time
from employee import employee
from product import product
from category import category
# from sales import sales
from order import order
from supplier import supplier
from oder.home import homeo
from sale.sales import sales

class inventory:
    def __init__(self,root):
        self.root =root
        self.root.title("ISTOCK")
        self.root.geometry("1240x669+10+0")
        self.root.resizable(0,0)
        self.root.config(bg="white")
        self.root.iconbitmap("maini.ico")
        self.bgimage = PhotoImage(file="shop.png")
        #head section
        titlelable =Label(self.root,image=self.bgimage,compound=LEFT,text="\tInventory Management System",font=("times new roman",30,'bold'),
                          bg="#010c48",fg="gold",anchor=W,padx=30,)
        titlelable.place(x=0,y=0,relwidth=1)
        logoutbtn = Button(self.root,text="Logout",font=("times new roman",20,'bold'),fg="#010c48",bg="white",cursor="hand2")
        logoutbtn.place(x=1100,y=5)
        self.subtitlelable = Label(self.root,text=f"Welcome Admin\t\tDate: {time.strftime("%Y:%m:%d")}\t\tTime: 12:32:08",
                                   font=("times new roman",15,'bold'),bg="#4d636d",fg="white")
        self.subtitlelable.place(x=0,y=60,relwidth=1,)
        self.currentTime()
        #leftframe
        leftframe =Frame(self.root,bg="wheat")
        leftframe.place(x=0,y=89,width=200,height=600)
        #leftimage
        self.frameimage =PhotoImage(file="friend.png")
        imagelable = Label(leftframe,image=self.frameimage,borderwidth=0,bg="bisque",height=99)
        imagelable.pack(fill=X)
        #menu
        menulable = Label(leftframe,text="Menu",font=("times new roman",20,'bold'),bg="#009688")
        menulable.pack(fill=X)
        #left buttons
         #employees
        self.employimage = PhotoImage(file="employees.png")
        employeebtn =Button(leftframe,image=self.employimage,compound=LEFT,text="Employees",font=("times new roman",17,'bold'),
                            anchor=W,height=48,padx=10,bg="white",command=lambda:self.windoCall("E"))
        employeebtn.pack(fill=X)
        #supplier
        self.supplierimage = PhotoImage(file="supplier.png")
        supplierbtn =Button(leftframe,image=self.supplierimage,compound=LEFT,text="Suppliers",font=("times new roman",17,'bold'),
                            anchor=W,height=48,padx=10,bg="white",command=lambda:self.windoCall("Su"))
        supplierbtn.pack(fill=X)
        #sales
        self.salesimage = PhotoImage(file="sales.png")
        salesbtn =Button(leftframe,image=self.salesimage,compound=LEFT,text="Sales",font=("times new roman",17,'bold'),
                         anchor=W,height=48,padx=10,bg="white",command=lambda:self.windoCall("Sa"))
        salesbtn.pack(fill=X)
        #categories
        self.categoryimage = PhotoImage(file="category.png")
        categorybtn =Button(leftframe,image=self.categoryimage,compound=LEFT,text="Categories",font=("times new roman",17,'bold'),
                            anchor=W,height=48,padx=10,bg="white",command=lambda:self.windoCall("C"))
        categorybtn.pack(fill=X)
        #products
        self.productimage = PhotoImage(file="product.png")
        productbtn =Button(leftframe,image=self.productimage,compound=LEFT,text="Products",font=("times new roman",17,'bold'),
                           anchor=W,height=48,padx=10,bg="white",command=lambda:self.windoCall("P"))
        productbtn.pack(fill=X)
        #orders
        #products
        self.orderimage = PhotoImage(file="orders.png")
        orderbtn =Button(leftframe,image=self.orderimage,compound=LEFT,text="Orders",font=("times new roman",17,'bold'),
                           anchor=W,height=48,padx=10,bg="white",command=lambda:self.windoCall("O"))
        orderbtn.pack(fill=X)
        #exit
        self.exitimage = PhotoImage(file="exit.png")
        exitbtn =Button(leftframe,image=self.exitimage,compound=LEFT,text="Exit",font=("times new roman",17,'bold'),
                        anchor=W,height=48,padx=10,bg="white",command=lambda:self.windoCall("Ex"))
        exitbtn.pack(fill=X)
        #employee frame
        #total employees
        self.total_employImage = PhotoImage(file="totalemployees.png")
        emp_frame = Frame(self.root,bg="#2C3E50",bd=3,relief=RIDGE)
        emp_frame.place(x=300,y=125,height=170,width=280)
        total_empl_icon =Label(emp_frame,bg="#2C3E50", image=self.total_employImage)
        total_empl_icon.pack(pady=10)
        
        total_empl_lable =Label(emp_frame,bg="#2C3E50",fg="white", text="Total Employees",font=("times new roman",14,'bold'))
        total_empl_lable.pack()
        #total
        self.total_empl_number =Label(emp_frame,bg="#2C3E50",fg="white", text="10",font=("times new roman",30,'bold'))
        self.total_empl_number.pack()
        
        #products frame
        #total products
        product_frame = Frame(self.root,bg="#8E44AD",bd=3,relief=RIDGE)
        product_frame.place(x=600,y=125,height=170,width=280)
        total_product_icon =Label(product_frame,bg="#8E44AD", image=self.employimage)
        total_product_icon.pack(pady=10)
        
        total_product_lable =Label(product_frame,bg="#8E44AD",fg="white", text="Total Products",font=("times new roman",14,'bold'))
        total_product_lable.pack()
        #total
        self.total_product_number =Label(product_frame,bg="#8E44AD",fg="white", text="10",font=("times new roman",30,'bold'))
        self.total_product_number.pack()
        
        #categories frame
        #total categories
        category_frame = Frame(self.root,bg="#5744AD",bd=3,relief=RIDGE)
        category_frame.place(x=900,y=125,height=170,width=280)
        total_category_icon =Label(category_frame,bg="#5744AD", image=self.employimage)
        total_category_icon.pack(pady=10)
        
        total_category_lable =Label(category_frame,bg="#5744AD",fg="white", text="Product Categorie",font=("times new roman",14,'bold'))
        total_category_lable.pack()
        #total
        self.total_category_number =Label(category_frame,bg="#5744AD",fg="white", text="10",font=("times new roman",30,'bold'))
        self.total_category_number.pack()
        
        #suppliers frame
        #total suppliers
        supplier_frame = Frame(self.root,bg="#27AE60",bd=3,relief=RIDGE)
        supplier_frame.place(x=300,y=330,height=170,width=280)
        total_supplier_icon =Label(supplier_frame,bg="#27AE60", image=self.employimage)
        total_supplier_icon.pack(pady=10)
        
        total_supplier_lable =Label(supplier_frame,bg="#27AE60",fg="white", text="Total Suppliers",font=("times new roman",14,'bold'))
        total_supplier_lable.pack()
        #total
        self.total_supplier_number =Label(supplier_frame,bg="#27AE60",fg="white", text="10",font=("times new roman",30,'bold'))
        self.total_supplier_number.pack()
        
        #orders frame
        #total orders
        order_frame = Frame(self.root,bg="#E7B311",bd=3,relief=RIDGE)
        order_frame.place(x=600,y=330,height=170,width=280)
        total_order_icon =Label(order_frame,bg="#E7B311", image=self.employimage)
        total_order_icon.pack(pady=10)
        
        total_order_lable =Label(order_frame,bg="#E7B311",fg="white", text="Total Pedding Orders",font=("times new roman",14,'bold'))
        total_order_lable.pack()
        #total
        self.total_order_number =Label(order_frame,bg="#E7B311",fg="white", text="10",font=("times new roman",30,'bold'))
        self.total_order_number.pack()
        
        #sales frame
        #total sales
        sale_frame = Frame(self.root,bg="#E77111",bd=3,relief=RIDGE)
        sale_frame.place(x=900,y=330,height=170,width=280)
        total_sale_icon =Label(sale_frame,bg="#E77111", image=self.employimage)
        total_sale_icon.pack(pady=10)
        
        total_sale_lable =Label(sale_frame,bg="#E77111",fg="white", text="Total Sales",font=("times new roman",14,'bold'))
        total_sale_lable.pack()
        #total
        self.total_sale_number =Label(sale_frame,bg="#E77111",fg="white", text="10",font=("times new roman",30,'bold'))
        self.total_sale_number.pack()
        
    #mehod call
        
        #metthods
    def windoCall(self,window):
        if window =="E":
            empwindow = Toplevel()
            empobj=employee(empwindow,self.root)
            empwindow.mainloop()
            return
        elif window =="P":
            prowindow = Toplevel()
            probj=product(prowindow,self.root)
            prowindow.mainloop()
            return
        elif window =="Sa":
            swindow = Toplevel()
            sobj=sales(swindow,self.root)
            swindow.mainloop()
            return
        elif window =="Su":
            supwindow = Toplevel()
            supobj=supplier(supwindow,self.root)
            supwindow.mainloop()
            return
        elif window =="O":
           ordwindow = Toplevel()
           obj = homeo(ordwindow,self.root)
           ordwindow.mainloop()
           return
        elif window =="C":
            catwindow = Toplevel()
            catobj=category(catwindow,self.root)
            catwindow.mainloop()
            return
        elif window == "Ex":
            if messagebox.askyesno("Exit","Are your sure you want to close the application",parent=self.root):
                self.root.destroy()
                return
            else:
                return
    def currentTime(self):
        self.subtitlelable.config(text=f"Welcome Admin\t\tDate: {time.strftime("%Y:%m:%d")}\t\tTime: {time.strftime("%H:%M:%S")}")
        self.subtitlelable.after(1000,self.currentTime)
            
        
        
        
        
root =Tk()
obj = inventory(root)
root.mainloop()