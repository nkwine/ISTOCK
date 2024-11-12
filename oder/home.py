from tkinter import *
import pymysql
from tkinter import ttk,messagebox
from .purchase import purchase
from .saleorder import saleOrder

class homeo:
    def __init__(self,root,parent):
        self.root =root
        self.root.resizable(0,0)
        self.root.geometry('300x300+400+100')
        self.root.iconbitmap("employee__icon.ico")
        self.root.config(bg="#FFFFFF")
        self.root.grab_set()
        self.root.transient(parent)
        self.parent =parent
        self.root.focus_force()
        major = Frame(self.root,bg="#FFFFFF")
        major.pack(pady=100)
        self.opt1 =Button(major,text="Purchase Orders",font=("times new roman",12),width=10,cursor="hand2",bg="#0f4d7d",
                                   fg="white",command=lambda:self.majorfunction("p"))
        self.opt1.grid(row=0,column=0,padx=10,ipadx=4)
        self.opt2 =Button(major,text="Sale Orders",font=("times new roman",12),width=10,cursor="hand2",bg="#0f4d7d",
                                   fg="white",command=lambda:self.majorfunction("s"))
        self.opt2.grid(row=0,column=1,padx=10)
    def majorfunction(self,choice):
        if choice =='p':
            self.root.grab_release()
            self.root.destroy()
            pwindow = Toplevel()
            obj = purchase(pwindow,self.parent)
            pwindow.mainloop()
        else:
            self.root.grab_release()
            self.root.destroy()
            spwindow = Toplevel()
            obj = saleOrder(spwindow,self.parent)
            spwindow.mainloop()