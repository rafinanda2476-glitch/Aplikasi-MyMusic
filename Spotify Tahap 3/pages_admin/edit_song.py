import customtkinter as ctk
from tkinter import messagebox

# Tambah parameter colors
def render_edit_song(parent, library, colors, song_id, on_saved):
    node = library.findNodeById(song_id)
    if not node:
        ctk.CTkLabel(parent, text="Lagu tidak ditemukan", text_color=colors["text_head"]).pack(pady=12)
        return
    s = node.song
    ctk.CTkLabel(parent, text=f"Edit Lagu ID {song_id}", font=("Segoe UI", 20, "bold"), text_color=colors["text_head"]).pack(pady=8)
    
    form = ctk.CTkFrame(parent, fg_color="white")
    form.pack(pady=10, padx=12, fill="x")
    
    # Format duration as MM:SS
    def format_duration(seconds):
        mins = seconds // 60
        secs = seconds % 60
        return f"{mins}:{secs:02d}"
    
    labels = ["Judul", "Artist", "Genre", "Tahun", "Durasi"]
    entries = {}
    initial = [s.title, s.artist, s.genre, s.year, format_duration(s.duration)]
    
    for i, lbl in enumerate(labels):
        ctk.CTkLabel(form, text=lbl).grid(row=i, column=0, pady=8, padx=8, sticky="w")
        entries[lbl] = ctk.CTkEntry(form, width=360)
        entries[lbl].insert(0, str(initial[i]))
        entries[lbl].grid(row=i, column=1, pady=8, padx=8)
        
        # Helper text for duration
        if lbl == "Durasi":
            ctk.CTkLabel(form, text="(Format: MM:SS)", text_color="gray", font=("Arial", 9)).grid(row=i, column=2, padx=5, sticky="w")
        
    def save():
        t = entries["Judul"].get().strip()
        a = entries["Artist"].get().strip()
        g = entries["Genre"].get().strip()
        y = entries["Tahun"].get().strip()
        d = entries["Durasi"].get().strip()
        
        try:
            y = int(y)
        except:
            messagebox.showerror("Error", "Tahun salah!")
            return
        
        # Parse duration
        try:
            if ":" in d:
                parts = d.split(":")
                if len(parts) == 2:
                    mins = int(parts[0])
                    secs = int(parts[1])
                    duration = mins * 60 + secs
                else:
                    raise ValueError("Format salah")
            else:
                duration = int(d)
            
            if duration < 1 or duration > 3600:
                raise ValueError("Durasi tidak valid")
        except ValueError:
            messagebox.showerror("Error", "Format durasi salah! Gunakan MM:SS atau detik.")
            return
        
        library.updateSong(song_id, t, a, g, y, duration)
        library.save_if_supported()  # Save changes
        messagebox.showinfo("OK", "Berhasil diupdate!")
        if on_saved:
            on_saved()

    # Gunakan warna primary
    ctk.CTkButton(parent, text="Simpan Perubahan", fg_color=colors["primary"], hover_color=colors["hover"], command=save).pack(pady=10)