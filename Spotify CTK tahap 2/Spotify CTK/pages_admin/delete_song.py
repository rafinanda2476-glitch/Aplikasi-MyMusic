import customtkinter as ctk
from tkinter import messagebox

# Tambah parameter colors
def render_delete_song(parent, library, colors, song_id, on_deleted):
    node = library.findNodeById(song_id)
    if not node:
        ctk.CTkLabel(parent, text="Lagu tidak ditemukan", text_color=colors["text_head"]).pack(pady=12)
        return
    s = node.song
    ctk.CTkLabel(parent, text=f"Hapus Lagu: {s.title} - {s.artist}", font=("Segoe UI", 18, "bold"), text_color=colors["text_head"]).pack(pady=12)
    
    def do_delete():
        if messagebox.askyesno("Konfirmasi", "Yakin hapus lagu ini?"):
            library.deleteSong(song_id)
            messagebox.showinfo("OK", "Lagu dihapus.")
            if on_deleted:
                on_deleted()

    # Gunakan colors["danger"] (merah) yang ada di app.py
    ctk.CTkButton(parent, text="Hapus Sekarang", fg_color=colors["danger"], hover_color="#FF4C4C", command=do_delete).pack(pady=8)