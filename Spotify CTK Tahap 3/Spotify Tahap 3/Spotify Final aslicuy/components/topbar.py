# topbar component
import customtkinter as ctk

def TopBar(p,cb_out,c,on_search=None):
    f=ctk.CTkFrame(p,fg_color="white",height=60,corner_radius=0)
    ctk.CTkLabel(f,text="MyMusic",font=("Segoe UI",18,"bold"),text_color=c["primary"]).pack(side="left",padx=20)
    if on_search:
        s_cont=ctk.CTkFrame(f,fg_color="transparent");s_cont.pack(side="left",expand=True,padx=20)
        ctk.CTkLabel(s_cont,text="🔍",font=("Segoe UI",16)).pack(side="left",padx=(0,8))
        s_var=ctk.StringVar()
        ent=ctk.CTkEntry(s_cont,textvariable=s_var,placeholder_text="Cari lagu atau artis...",width=400,height=35,fg_color="#F5F5F5",border_width=0);ent.pack(side="left")
        def ganti(*a):on_search(s_var.get())
        s_var.trace('w',ganti)
        def ok(e=None):on_search(s_var.get().strip())
        ent.bind("<Return>",ok)
    ctk.CTkButton(f,text="Keluar",width=80,fg_color="#FFEEED",text_color="red",hover_color="#FFDDD9",command=cb_out).pack(side="right",padx=20,pady=10)
    return f
