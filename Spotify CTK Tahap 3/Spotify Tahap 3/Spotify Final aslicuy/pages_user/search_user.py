# search user page
import customtkinter as ctk
import random

def render_search(p,lib,c,cb_pl,cb_add,q=""):
    scr=ctk.CTkScrollableFrame(p,fg_color="transparent");scr.pack(fill="both",expand=True,padx=15,pady=15)
    def show(cari):
        [x.destroy() for x in scr.winfo_children()]
        if cari.strip():res=lib.searchSongs(cari,fuzzy=True,fields=["title","artist"]);judul=f"Hasil pencarian '{cari}'"
        else:all_s=lib.getAllSongs();res=random.sample(all_s,min(10,len(all_s))) if all_s else [];judul="🔥 Lagu Populer"
        ctk.CTkLabel(scr,text=judul,font=("Segoe UI",18,"bold"),text_color=c["text_head"]).pack(anchor="w",pady=(10,15))
        if not res:ctk.CTkLabel(scr,text="Ga ketemu bro.",text_color="gray",font=("Segoe UI",13)).pack(pady=40);return
        def fmt_waktu(d):return f"{d//60}:{d%60:02d}"
        gf=ctk.CTkFrame(scr,fg_color="transparent");gf.pack(fill="x",pady=10);[gf.grid_columnconfigure(x,weight=1) for x in range(4)]
        for i,s in enumerate(res):
            r=i//4;k=i%4;kartu=ctk.CTkFrame(gf,fg_color="white",corner_radius=10);kartu.grid(row=r,column=k,padx=5,pady=5,sticky="nsew")
            ctk.CTkLabel(kartu,text=s.title,font=("Segoe UI",14,"bold"),text_color="#333",wraplength=120).pack(pady=(15,0))
            ctk.CTkLabel(kartu,text=s.artist,font=("Segoe UI",12),text_color="gray").pack(pady=(0,5))
            ctk.CTkLabel(kartu,text=f"⏱ {fmt_waktu(s.duration)}",font=("Segoe UI",10),text_color="#999").pack(pady=(0,10))
            def gas(x=s,idx=i):cb_pl(res,idx)
            ctk.CTkButton(kartu,text="▶ Play",fg_color=c["primary"],height=30,width=80,command=gas).pack(pady=(0,5))
            ctk.CTkButton(kartu,text="+ Koleksi",fg_color=c["hover"],height=25,width=80,font=("Segoe UI",10),command=lambda sid=s.id:cb_add(sid)).pack(pady=(0,15))
    show(q)
