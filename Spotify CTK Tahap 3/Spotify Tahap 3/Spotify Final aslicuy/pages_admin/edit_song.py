# edit song page
import customtkinter as ctk
from tkinter import messagebox

GENRES = ["Pop", "Rock", "Hip Hop", "Jazz", "R&B", "Electronic"]

def render_edit_song(p,lib,c,sid,cb_save):
    node=lib.findNodeById(sid)
    if not node:ctk.CTkLabel(p,text="Lagu ga ketemu.",text_color=c["text_head"]).pack(pady=12);return
    s=node.song;ctk.CTkLabel(p,text=f"Edit Lagu ID {sid}",font=("Segoe UI",20,"bold"),text_color=c["text_head"]).pack(pady=8)
    f=ctk.CTkFrame(p,fg_color="white");f.pack(pady=10,padx=12,fill="x")
    def fmt(d):return f"{d//60}:{d%60:02d}"
    
    ents={}
    row=0
    
    # Judul
    ctk.CTkLabel(f,text="Judul").grid(row=row,column=0,pady=8,padx=8,sticky="w")
    ents["Judul"]=ctk.CTkEntry(f,width=360);ents["Judul"].insert(0,s.title);ents["Judul"].grid(row=row,column=1,pady=8,padx=8);row+=1
    
    # Artist
    ctk.CTkLabel(f,text="Artist").grid(row=row,column=0,pady=8,padx=8,sticky="w")
    ents["Artist"]=ctk.CTkEntry(f,width=360);ents["Artist"].insert(0,s.artist);ents["Artist"].grid(row=row,column=1,pady=8,padx=8);row+=1
    
    # Genre dropdown
    ctk.CTkLabel(f,text="Genre").grid(row=row,column=0,pady=8,padx=8,sticky="w")
    genre_var=ctk.StringVar(value=s.genre if s.genre in GENRES else "Pop")
    genre_menu=ctk.CTkOptionMenu(f,variable=genre_var,values=GENRES,width=360,fg_color=c["primary"],button_color=c["primary"])
    genre_menu.grid(row=row,column=1,pady=8,padx=8);row+=1
    ents["Genre"]=genre_var
    
    # Tahun
    ctk.CTkLabel(f,text="Tahun").grid(row=row,column=0,pady=8,padx=8,sticky="w")
    ents["Tahun"]=ctk.CTkEntry(f,width=360);ents["Tahun"].insert(0,str(s.year));ents["Tahun"].grid(row=row,column=1,pady=8,padx=8);row+=1
    
    # Durasi
    ctk.CTkLabel(f,text="Durasi").grid(row=row,column=0,pady=8,padx=8,sticky="w")
    ents["Durasi"]=ctk.CTkEntry(f,width=360);ents["Durasi"].insert(0,fmt(s.duration));ents["Durasi"].grid(row=row,column=1,pady=8,padx=8)
    ctk.CTkLabel(f,text="(Format: MM:SS)",text_color="gray",font=("Arial",9)).grid(row=row,column=2,padx=5,sticky="w")
    
    def cek_duplikat_lain(new_title,new_artist,current_id):
        # Cek apakah ada lagu LAIN dengan judul+artis yang sama
        cur=lib.head
        while cur:
            if cur.song.id!=current_id:
                if cur.song.title.lower()==new_title.lower() and cur.song.artist.lower()==new_artist.lower():
                    return True
            cur=cur.next
        return False
    
    def save():
        t=ents["Judul"].get().strip();a=ents["Artist"].get().strip()
        g=ents["Genre"].get() if isinstance(ents["Genre"],ctk.StringVar) else ents["Genre"].get().strip()
        y=ents["Tahun"].get().strip();d=ents["Durasi"].get().strip()
        
        if not t or not a:
            messagebox.showerror("Error","Judul dan Artis wajib diisi!");return
        
        # Cek duplikat dengan lagu lain
        if cek_duplikat_lain(t,a,sid):
            messagebox.showerror("Duplikat",f"Lagu '{t}' oleh '{a}' sudah ada di database!");return
        
        try:y=int(y)
        except:messagebox.showerror("Error","Tahun harus angka!");return
        try:dur=int(d.split(":")[0])*60+int(d.split(":")[1]) if ":" in d else int(d);(dur<1 or dur>3600) and (_ for _ in ()).throw(ValueError("ngaco"))
        except:messagebox.showerror("Error","Durasi salah format!");return
        lib.updateSong(sid,t,a,g,y,dur);lib.save_if_supported();messagebox.showinfo("Sip","Udah update.");cb_save and cb_save()
    
    def cancel():
        cb_save and cb_save()
    
    # Tombol
    btn_frame=ctk.CTkFrame(p,fg_color="transparent");btn_frame.pack(pady=10)
    ctk.CTkButton(btn_frame,text="Simpan Perubahan",fg_color=c["primary"],hover_color=c["hover"],command=save).pack(side="left",padx=5)
    ctk.CTkButton(btn_frame,text="Batal",fg_color="gray",hover_color="#555555",command=cancel).pack(side="left",padx=5)
