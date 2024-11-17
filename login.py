from tkinter import *
from tkinter import messagebox
import time,pymysql


class login:
    def __init__(self,root):
        self.root =root
        self.root.title("ISTOCK")
        self.root.geometry("500x300+390+160")
        self.root.resizable(0,0)
        self.root.config(bg="#003e53")
        self.root.iconbitmap("D:/phone/gui/code/inventory_system/maini.ico")
        self.bgimage = PhotoImage(file="D:/phone/gui/code/inventory_system/shop.png")
        self.frame = Frame(self.root,bg="#003e53")
        self.frame.pack(padx=10,pady=80)
        user = Label(self.frame,text="Username:",bg="#003e53",fg="white",font=("times new roman",14))
        user.grid(row=0,column=0)
        self.user = Entry(self.frame,bg="white",width=25,font=("times new roman",11,"bold"))
        self.user.grid(row=0,column=1)
        passw = Label(self.frame,text="Password:",bg="#003e53",fg="white",font=("times new roman",14))
        passw.grid(row=1,column=0)
        self.pas = Entry(self.frame,bg="white",width=25,font=("times new roman",11,"bold"),show="*")
        self.pas.grid(row=1,column=1)
        self.info = Button(self.root,text="Login",bg="white",fg="#003e53",font=("times new roman",14,"bold"),command=self.grant)
        self.info.pack()
        #method
    def grant(self):
        try:
            if self.user.get().strip() == "inno" and self.pas.get().strip() == "1996":
                self.root.destroy()
                import main
            else:
                messagebox.showerror("Error","Wrong credentials\nCheck your username and password and try again!")
        except Exception as e:
            messagebox.showerror("Error",f"Something went wrong",parent=self.root)
root = Tk()
obj = login(root)
root.mainloop()