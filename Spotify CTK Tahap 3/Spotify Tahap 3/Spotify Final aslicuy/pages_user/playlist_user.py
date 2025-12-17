# playlist user page
import customtkinter as ctk
from tkinter import messagebox,simpledialog

def render_playlist(p,lib,pm,c,cb_pl,cb_del_song,cb_ren=None,cb_del_pl=None):
    cont=ctk.CTkFrame(p,fg_color="transparent");cont.pack(fill="both",expand=True,padx=15,pady=(5,5))
    cont.grid_rowconfigure(0,weight=0);cont.grid_rowconfigure(1,weight=1);cont.grid_columnconfigure(0,weight=1)
    def show():
        [x.destroy() for x in cont.winfo_children()]
        cur=pm.getCurrentPlaylist()
        if not cur:ctk.CTkLabel(cont,text="Mana playlistnya?",text_color="gray").grid(row=0,column=0,pady=20);return
        lagu2=cur.listSongs()
        def opsis(ev):
            import tkinter as tk
            m=tk.Menu(p,tearoff=0,bg="#FFFFFF",fg="#333333",relief="flat",bd=0)
            def ganti_nama():
                from tkinter import Toplevel
                if cur.name=="Koleksi Saya":messagebox.showwarning("Eitss","Gaboleh ganti nama yg ini bos.");return
                d=Toplevel(p);d.title("Ganti Nama");d.geometry("500x300");d.transient(p);d.grab_set();d.configure(bg="#282828")
                cf=ctk.CTkFrame(d,fg_color="#282828");cf.pack(fill="both",expand=True,padx=30,pady=15)
                ctk.CTkLabel(cf,text="Ganti Nama Playlist",font=("Segoe UI",20,"bold"),text_color="white").pack(anchor="w",pady=(0,10))
                nv=ctk.StringVar(value=cur.name);e=ctk.CTkEntry(cf,textvariable=nv,height=38,fg_color="#3E3E3E",text_color="white");e.pack(fill="x",pady=(0,15));e.focus()
                def gas():
                    nn=nv.get().strip()
                    if nn:ok,msg=pm.renamePlaylist(cur.name,nn);d.destroy();ok and cb_ren and cb_ren(nn) or (not ok and messagebox.showerror("Yah gagal",msg))
                    else:messagebox.showwarning("Kosong","Isi dong namanya!")
                bf=ctk.CTkFrame(cf,fg_color="transparent");bf.pack(fill="x")
                ctk.CTkButton(bf,text="Batal",command=d.destroy,fg_color="transparent",border_width=1,border_color="white",width=100).pack(side="left")
                ctk.CTkButton(bf,text="Simpan",command=gas,fg_color="#1DB954",text_color="black",width=100).pack(side="right");e.bind("<Return>",lambda e:gas())
            def apus_pl():
                from tkinter import Toplevel
                if cur.name=="Koleksi Saya":messagebox.showwarning("Waduh","Jangan dihapus dong yang ini.");return
                d=Toplevel(p);d.title("Hapus?");d.geometry("400x200");d.transient(p)
                cf=ctk.CTkFrame(d,fg_color="#282828");cf.pack(fill="both",expand=True,padx=20,pady=20)
                ctk.CTkLabel(cf,text=f"Yakin hapus '{cur.name}'?",text_color="white",font=("Segoe UI",16)).pack(pady=20)
                def yes():pm.deletePlaylist(cur.name) and d.destroy();cb_del_pl and cb_del_pl() or d.destroy()
                ctk.CTkButton(cf,text="Hapus Aja",command=yes,fg_color="red").pack()
            m.add_command(label="Ganti Nama",command=ganti_nama);m.add_separator();m.add_command(label="Hapus Playlist",command=apus_pl)
            try:m.tk_popup(ev.x_root,ev.y_root)
            finally:m.grab_release()
        h=ctk.CTkFrame(cont,fg_color="white",corner_radius=10);h.grid(row=0,column=0,sticky="ew",pady=(0,15))
        info=ctk.CTkFrame(h,fg_color="transparent");info.pack(fill="x",padx=20,pady=15)
        row1=ctk.CTkFrame(info,fg_color="transparent");row1.pack(fill="x",anchor="w")
        ctk.CTkLabel(row1,text=f"🎵 {cur.name}",font=("Segoe UI",18,"bold"),text_color=c["text_head"]).pack(side="left")
        btn_titik=ctk.CTkButton(row1,text="⋮",width=30,fg_color="transparent",text_color="#999",font=("Segoe UI",18));btn_titik.pack(side="left",padx=(8,0));btn_titik.bind("<Button-1>",opsis)
        ctk.CTkLabel(info,text=f"{len(lagu2)} lagu",font=("Segoe UI",12),text_color="#777").pack(anchor="w",pady=(5,0))
        scr=ctk.CTkScrollableFrame(cont,fg_color="transparent");scr.grid(row=1,column=0,sticky="nsew")
        if not lagu2:ctk.CTkLabel(scr,text="Masih sepi nih.",text_color="gray").pack(pady=40);return
        def fmt(d):return f"{d//60}:{d%60:02d}"
        for i,s in enumerate(lagu2):
            brs=ctk.CTkFrame(scr,fg_color="#F8F9FA",corner_radius=8);brs.pack(fill="x",pady=3,padx=5)
            def mainkan(ix=i):cb_pl(lagu2,ix)
            ctk.CTkButton(brs,text="▶",width=38,height=38,fg_color=c["primary"],command=mainkan).pack(side="left",padx=10,pady=8)
            inf=ctk.CTkFrame(brs,fg_color="transparent");inf.pack(side="left",fill="x",expand=True,padx=5)
            ctk.CTkLabel(inf,text=s.title,font=("Segoe UI",13,"bold"),text_color=c["text_head"],anchor="w").pack(anchor="w")
            ctk.CTkLabel(inf,text=f"{s.artist} • {s.genre} • {fmt(s.duration)}",font=("Segoe UI",11),text_color="#888",anchor="w").pack(anchor="w")
            ctk.CTkButton(brs,text="✕",width=35,height=35,fg_color="#FFE5E5",text_color=c["danger"],command=lambda id=s.id:hapus(id)).pack(side="right",padx=10)
    def hapus(id):nm=pm.current_playlist_name;pm.removeSongFromPlaylist(nm,id) and show();cb_del_song and cb_del_song(id)
    show()
