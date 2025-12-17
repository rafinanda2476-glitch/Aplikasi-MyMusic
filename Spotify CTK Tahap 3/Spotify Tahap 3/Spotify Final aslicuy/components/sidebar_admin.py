# sidebar admin
import customtkinter as ctk

def SidebarAdmin(p,c,cb_d,cb_s,cb_a,cb_i,cur="dashboard"):
    f=ctk.CTkFrame(p,width=240,fg_color=c["bg_sidebar"],corner_radius=0)
    ctk.CTkLabel(f,text="ADMIN PANEL",font=("Segoe UI",16,"bold"),text_color=c["primary"]).pack(pady=(30,10),padx=20,anchor="w")
    ctk.CTkLabel(f,text="Manage Music",font=("Segoe UI",12),text_color="gray").pack(pady=(0,20),padx=20,anchor="w")
    def btn(txt,ic,cmd,id):
        act=(cur==id)
        b=ctk.CTkButton(f,text=f"{ic}   {txt}",anchor="w",font=("Segoe UI",13,"bold" if act else "normal"),fg_color=c["primary"] if act else "transparent",text_color="white" if act else "#E0E0E0",hover_color=c["hover"],height=38,width=210,command=cmd)
        b.pack(pady=2,padx=10)
    btn("Dashboard","📊",cb_d,"dashboard");btn("Database Lagu","💿",cb_s,"songs");btn("Tambah Baru","➕",cb_a,"add");btn("Import Folder","📂",cb_i,"import")
    return f