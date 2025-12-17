# create playlist page
import customtkinter as ctk
from tkinter import messagebox

def render_create_playlist(p,pm,c,cb_suc):
    scr=ctk.CTkScrollableFrame(p,fg_color="transparent");scr.pack(expand=True,fill="both",padx=20,pady=20)
    cnt=ctk.CTkFrame(scr,fg_color="transparent");cnt.pack(expand=True,fill="both",pady=50)
    card=ctk.CTkFrame(cnt,fg_color="white",corner_radius=15);card.pack(pady=20,padx=50)
    ctk.CTkLabel(card,text="➕ Buat Playlist Baru",font=("Segoe UI",24,"bold"),text_color=c["primary"]).pack(pady=(30,10))
    ctk.CTkLabel(card,text="Beri nama playlist koleksi kamu",font=("Segoe UI",13),text_color="gray").pack(pady=(0,30))
    ic=ctk.CTkFrame(card,fg_color="transparent");ic.pack(pady=20,padx=40,fill="x")
    ctk.CTkLabel(ic,text="Nama Playlist:",font=("Segoe UI",12,"bold"),text_color="#333").pack(anchor="w",pady=(0,8))
    nv=ctk.StringVar();ent=ctk.CTkEntry(ic,textvariable=nv,placeholder_text="Contoh: Galau Brutal",height=45,font=("Segoe UI",14),fg_color="#F5F5F5",border_width=2,border_color=c["primary"]);ent.pack(fill="x",pady=(0,20));ent.focus()
    err=ctk.CTkLabel(ic,text="",text_color="red",font=("Segoe UI",11));err.pack(pady=(0,10))
    bc=ctk.CTkFrame(card,fg_color="transparent");bc.pack(pady=20)
    def bikin():
        nm=nv.get().strip()
        if not nm:err.configure(text="⚠️ Isi dulu woy!");return
        if pm.createPlaylist(nm):
            messagebox.showinfo("Mantap",f"Udah jadi nih '{nm}'!")
            cb_suc and cb_suc(nm)
        else:err.configure(text="⚠️ Udah ada nama itu!")
    ent.bind("<Return>",lambda e:bikin())
    ctk.CTkButton(bc,text="Gas Bikin",width=150,height=40,font=("Segoe UI",14,"bold"),fg_color=c["primary"],hover_color=c["hover"],command=bikin).pack(side="left",padx=5)
    ctk.CTkButton(bc,text="Gajadi",width=100,height=40,font=("Segoe UI",14),fg_color="gray",hover_color="#666",command=lambda:cb_suc(None) if cb_suc else None).pack(side="left",padx=5)
    ctk.CTkLabel(card,text="💡 Tips: Jangan pake nama mantan",font=("Segoe UI",10),text_color="#999").pack(side="bottom",pady=15)
