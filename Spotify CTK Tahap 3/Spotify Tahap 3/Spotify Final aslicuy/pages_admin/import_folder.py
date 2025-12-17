# import folder - scan mp3
import customtkinter as ctk
from tkinter import filedialog,messagebox
import os
from tinytag import TinyTag

GENRES = ["Pop", "Rock", "Hip Hop", "Jazz", "R&B", "Electronic"]

def render_import_folder(parent,library,colors,on_finished):
    ctk.CTkLabel(parent,text="Scan Folder Musik (MP3)",font=("Segoe UI",24,"bold"),text_color=colors["text_head"]).pack(pady=20)
    frame=ctk.CTkFrame(parent,fg_color="white");frame.pack(fill="both",expand=True,padx=20,pady=10)
    lbl_info=ctk.CTkLabel(frame,text="Pilih folder di komputer yang berisi file MP3.",font=("Segoe UI",14),text_color="gray");lbl_info.pack(pady=20)
    log_box=ctk.CTkTextbox(frame,height=200,width=600);log_box.pack(pady=10,fill="x",padx=20);log_box.insert("0.0","Siap melakukan scan...\n")
    def log(text):
        print(text)
        try:log_box.insert("end",text+"\n");log_box.see("end");log_box.update()
        except:pass
    def mulai_scan():
        folder=filedialog.askdirectory()
        if not folder:return
        try:lbl_info.configure(text=f"Sedang Scan: {folder}")
        except:pass
        count=0;skipped=0;log(f"Memulai Scan di: {folder}")
        for root,dirs,files in os.walk(folder):
            for file in files:
                if file.lower().endswith('.mp3'):
                    full_path=os.path.join(root,file)
                    try:
                        tag=TinyTag.get(full_path);title=tag.title if tag.title else file.replace('.mp3','');artist=tag.artist if tag.artist else "Unknown Artist"
                        detected_genre=tag.genre if tag.genre else "Pop"
                        genre=detected_genre if detected_genre in GENRES else "Pop"
                        year=int(tag.year) if tag.year and str(tag.year).isdigit() else 2024;duration=int(tag.duration) if tag.duration else 180
                        if not library.is_duplicate(title,artist):library.addSong(title,artist,genre,year,duration,file_path=full_path);log(f"[Berhasil] {title}");count+=1
                        else:log(f"[Duplikat] {title} - Lewati.");skipped+=1
                    except Exception as e:log(f"[Error] {file}: {e}")
        library.save_if_supported();log("Selesai")
        try:messagebox.showinfo("Selesai",f"Berhasil scan {count} lagu baru!\n({skipped} lagu sudah ada sebelumnya)");on_finished()
        except:pass
    ctk.CTkButton(frame,text="Pilih Folder & Scan",command=mulai_scan,fg_color=colors["primary"],hover_color=colors["hover"],height=45,font=("Segoe UI",14,"bold")).pack(pady=20)