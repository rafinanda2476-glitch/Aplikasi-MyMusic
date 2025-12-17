# delete song page
import customtkinter as ctk
from tkinter import messagebox

def render_delete_song(p,lib,c,sid,cb_del):
    node=lib.findNodeById(sid)
    if not node:ctk.CTkLabel(p,text="Lagu ga ada.",text_color=c["text_head"]).pack(pady=12);return
    s=node.song;ctk.CTkLabel(p,text=f"Hapus Lagu: {s.title} - {s.artist}",font=("Segoe UI",18,"bold"),text_color=c["text_head"]).pack(pady=12)
    def byebye():messagebox.askyesno("Yakin?","Serius mau dihapus?") and (lib.deleteSong(sid),messagebox.showinfo("Dah ilang","Lagu dihapus."),cb_del and cb_del())
    ctk.CTkButton(p,text="Hapus Sekarang",fg_color=c["danger"],hover_color="#FF4C4C",command=byebye).pack(pady=8)
