# add song page
import customtkinter as ctk
from tkinter import messagebox,StringVar,filedialog
import os
from tinytag import TinyTag

GENRES = ["Pop", "Rock", "Hip Hop", "Jazz", "R&B", "Electronic"]

def render_add_song(parent,library,colors,on_saved):
    ctk.CTkLabel(parent,text="Tambah Lagu (Single File)",font=("Segoe UI",20,"bold"),text_color=colors["text_head"]).pack(pady=20)
    f_form=ctk.CTkFrame(parent,fg_color="white",corner_radius=15);f_form.pack(fill="x",padx=40,pady=10)
    vs={"File Path":StringVar(),"Judul":StringVar(),"Artist":StringVar(),"Genre":StringVar(value="Pop"),"Tahun":StringVar(),"Durasi":StringVar()}
    def pilih_file():
        path=filedialog.askopenfilename(filetypes=[("Audio Files","*.mp3 *.wav *.flac")])
        if path:
            vs["File Path"].set(path)
            try:
                tag=TinyTag.get(path);vs["Judul"].set(tag.title if tag.title else os.path.basename(path).replace('.mp3',''))
                vs["Artist"].set(tag.artist if tag.artist else "Unknown Artist")
                # Cek genre dari metadata, jika tidak ada di list, default ke Pop
                detected_genre = tag.genre if tag.genre else "Pop"
                vs["Genre"].set(detected_genre if detected_genre in GENRES else "Pop")
                vs["Tahun"].set(str(tag.year) if tag.year else "2025");vs["Durasi"].set(str(int(tag.duration)) if tag.duration else "180")
            except Exception as e:print(f"Gagal baca: {e}");vs["Judul"].set(os.path.basename(path))
    row_idx=0
    ctk.CTkLabel(f_form,text="Pilih File MP3:",font=("Segoe UI",12,"bold"),text_color="#333").grid(row=row_idx,column=0,padx=20,pady=15,sticky="w")
    f_browse=ctk.CTkFrame(f_form,fg_color="transparent");f_browse.grid(row=row_idx,column=1,padx=20,pady=15,sticky="ew")
    ent_path=ctk.CTkEntry(f_browse,textvariable=vs["File Path"],placeholder_text="Belum ada file dipilih...",state="readonly",width=250);ent_path.pack(side="left",fill="x",expand=True,padx=(0,10))
    ctk.CTkButton(f_browse,text="📂 Browse",width=80,command=pilih_file,fg_color=colors["primary"],hover_color=colors["hover"]).pack(side="right");row_idx+=1
    ctk.CTkFrame(f_form,height=2,fg_color="#F0F0F0").grid(row=row_idx,column=0,columnspan=2,sticky="ew",padx=10,pady=5);row_idx+=1
    
    # Input fields
    for l in ["Judul","Artist"]:
        ctk.CTkLabel(f_form,text=l,text_color="#555").grid(row=row_idx,column=0,padx=20,pady=8,sticky="w")
        ctk.CTkEntry(f_form,textvariable=vs[l],width=350).grid(row=row_idx,column=1,padx=20,pady=8,sticky="w");row_idx+=1
    
    # Genre dropdown
    ctk.CTkLabel(f_form,text="Genre",text_color="#555").grid(row=row_idx,column=0,padx=20,pady=8,sticky="w")
    genre_menu=ctk.CTkOptionMenu(f_form,variable=vs["Genre"],values=GENRES,width=350,fg_color=colors["primary"],button_color=colors["primary"])
    genre_menu.grid(row=row_idx,column=1,padx=20,pady=8,sticky="w");row_idx+=1
    
    # Tahun dan Durasi
    for l in ["Tahun","Durasi"]:
        ctk.CTkLabel(f_form,text=l,text_color="#555").grid(row=row_idx,column=0,padx=20,pady=8,sticky="w")
        ctk.CTkEntry(f_form,textvariable=vs[l],width=350).grid(row=row_idx,column=1,padx=20,pady=8,sticky="w")
        l=="Durasi" and ctk.CTkLabel(f_form,text="detik",text_color="gray",font=("Arial",10)).grid(row=row_idx,column=1,padx=(370,0),sticky="w");row_idx+=1
    
    def simpan_lagu():
        try:
            path=vs["File Path"].get();judul=vs["Judul"].get().strip();artis=vs["Artist"].get().strip();genre=vs["Genre"].get()
            if not path:messagebox.showwarning("Kosong","Pilih file lagunya dulu bos!");return
            if not judul or not artis:messagebox.showwarning("Kosong","Judul dan Artis wajib diisi.");return
            try:thn=int(vs["Tahun"].get().strip())
            except:thn=2025
            try:dur=int(float(vs["Durasi"].get().strip()))
            except:dur=180
            if library.addSong(judul,artis,genre,thn,dur,file_path=path):library.save_if_supported();messagebox.showinfo("Berhasil","Lagu berhasil ditambahkan!");on_saved()
            else:messagebox.showerror("Gagal","Lagu ini sudah ada di database!")
        except Exception as e:messagebox.showerror("Error",str(e))
    btn_frame=ctk.CTkFrame(parent,fg_color="transparent");btn_frame.pack(pady=20)
    ctk.CTkButton(btn_frame,text="Simpan Lagu",fg_color=colors["primary"],width=150,height=45,font=("Segoe UI",14,"bold"),command=simpan_lagu).pack(side="left",padx=5)
    ctk.CTkButton(btn_frame,text="Batal",fg_color="gray",hover_color="#555555",width=100,height=45,font=("Segoe UI",14),command=on_saved).pack(side="left",padx=5)