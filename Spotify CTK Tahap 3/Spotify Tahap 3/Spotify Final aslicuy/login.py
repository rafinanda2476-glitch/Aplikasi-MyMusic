# login page - jgn diutak atik
import customtkinter as ctk
from tkinter import messagebox,StringVar

class PageLogin(ctk.CTkFrame):
    def __init__(self,parent,cb_login,c):
        super().__init__(parent,fg_color="#FFFFFF")
        self.cb=cb_login;self.c=c;self.my_pin=StringVar()
        self.grid_columnconfigure(0,weight=1);self.grid_columnconfigure(1,weight=1);self.grid_rowconfigure(0,weight=1)
        self.kiri();self.kanan()

    def kiri(self):
        f=ctk.CTkFrame(self,fg_color=self.c["primary"],corner_radius=0);f.grid(row=0,column=0,sticky="nsew")
        x=ctk.CTkFrame(f,fg_color="transparent");x.pack(expand=True)
        ctk.CTkLabel(x,text="⚡",font=("Segoe UI",100)).pack(pady=10)
        ctk.CTkLabel(x,text="MyMusic",font=("Segoe UI",36,"bold"),text_color="white").pack()
        ctk.CTkLabel(x,text="Electric Edition",font=("Segoe UI",16),text_color="#E0EFFF").pack(pady=5)

    def kanan(self):
        f=ctk.CTkFrame(self,fg_color="#FFFFFF",corner_radius=0);f.grid(row=0,column=1,sticky="nsew")
        xx=ctk.CTkFrame(f,fg_color="transparent");xx.pack(expand=True,fill="x",padx=50)
        ctk.CTkLabel(xx,text="Akses Cepat",font=("Segoe UI",28,"bold"),text_color=self.c["text_head"]).pack(pady=(0,10))
        self.inp=ctk.CTkEntry(xx,placeholder_text="• • • •",height=60,width=200,font=("Consolas",32,"bold"),justify="center",show="•",textvariable=self.my_pin,border_color=self.c["primary"])
        self.inp.pack(pady=(0,20))
        b=ctk.CTkButton(xx,text="BUKA KUNCI",height=50,fg_color=self.c["primary"],hover_color=self.c["hover"],font=("Segoe UI",14,"bold"),command=self.cek_login);b.pack(fill="x",pady=10)
        h=ctk.CTkFrame(xx,fg_color="#F5F9FF",corner_radius=5);h.pack(fill="x",pady=20)
        ctk.CTkLabel(h,text="🔑 Admin: 0000  |  👤 User: 9999",text_color="#555",font=("Consolas",12)).pack(pady=10)
        self.inp.bind("<Return>",lambda e:self.cek_login());self.inp.focus()

    def cek_login(self):
        p=self.my_pin.get().strip()
        if p=="0000":self.cb("admin")
        elif p=="9999":self.cb("user")
        else:print("salah");messagebox.showerror("Error","PIN Salah!");self.my_pin.set("")