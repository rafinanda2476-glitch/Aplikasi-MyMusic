# home user page
import customtkinter as ctk

def render_home(p,lib,c,cb_play):
    scr=ctk.CTkScrollableFrame(p,fg_color="transparent");scr.pack(fill="both",expand=True)
    b=ctk.CTkFrame(scr,fg_color=c["primary"],corner_radius=10);b.pack(fill="x",padx=15,pady=15)
    ctk.CTkLabel(b,text="Trending Hits ⚡",font=("Segoe UI",24,"bold"),text_color="white").pack(padx=20,pady=(20,5),anchor="w")
    ctk.CTkLabel(b,text="Lagu paling hits minggu ini khusus buat kamu.",text_color="#E0EFFF").pack(padx=20,pady=(0,20),anchor="w")
    gc=ctk.CTkFrame(scr,fg_color="transparent");gc.pack(fill="both",expand=True,padx=10)
    lagu2=lib.getSortedSongs("title");tampil=lagu2[:8] if len(lagu2)>8 else lagu2
    gf=ctk.CTkFrame(gc,fg_color="transparent");gf.pack(fill="x");[gf.grid_columnconfigure(x,weight=1) for x in range(4)]
    def fmt_waktu(d):return f"{d//60}:{d%60:02d}"
    for i,s in enumerate(tampil):
        r=i//4;k=i%4;kartu=ctk.CTkFrame(gf,fg_color="white",corner_radius=10);kartu.grid(row=r,column=k,padx=5,pady=5,sticky="nsew")
        ctk.CTkLabel(kartu,text=s.title,font=("Segoe UI",14,"bold"),text_color="#333",wraplength=120).pack(pady=(15,0))
        ctk.CTkLabel(kartu,text=s.artist,font=("Segoe UI",12),text_color="gray").pack(pady=(0,5))
        ctk.CTkLabel(kartu,text=f"⏱ {fmt_waktu(s.duration)}",font=("Segoe UI",10),text_color="#999").pack(pady=(0,10))
        def gas(x=s):
            try:idx=lagu2.index(x);cb_play(lagu2,idx)
            except:cb_play(lagu2,0)
        ctk.CTkButton(kartu,text="▶ Play",fg_color=c["primary"],height=30,width=80,command=gas).pack(pady=(0,15))
    ctk.CTkLabel(gc,text="Jelajahi lebih banyak di menu Search 🔍",text_color="gray").pack(pady=30)
