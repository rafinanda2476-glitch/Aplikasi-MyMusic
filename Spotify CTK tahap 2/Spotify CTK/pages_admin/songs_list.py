import customtkinter as ctk

def render_songs_list(parent, library, colors, on_edit, on_delete):
    ctk.CTkLabel(parent, text="Database Lagu", font=("Segoe UI", 20, "bold"), text_color=colors["text_head"]).pack(pady=10, padx=20, anchor="w")

    # --- GRID CONFIGURATION ---
    # Bobot kolom harus SAMA PERSIS antara Header dan Isi
    def apply_grid_config(frame):
        frame.grid_columnconfigure(0, weight=1) # ID
        frame.grid_columnconfigure(1, weight=4) # Judul (Paling Lebar)
        frame.grid_columnconfigure(2, weight=3) # Artis
        frame.grid_columnconfigure(3, weight=2) # Genre
        frame.grid_columnconfigure(4, weight=1) # Tahun
        frame.grid_columnconfigure(5, weight=2) # Aksi

    # --- HEADER ---
    header = ctk.CTkFrame(parent, fg_color="#E0E0E0", height=40, corner_radius=5)
    header.pack(fill="x", padx=15)
    apply_grid_config(header) 
    
    h_font = ("Arial", 11, "bold")
    ctk.CTkLabel(header, text="ID", font=h_font).grid(row=0, column=0, pady=10)
    ctk.CTkLabel(header, text="JUDUL", font=h_font, anchor="w").grid(row=0, column=1, pady=10, padx=5, sticky="ew")
    ctk.CTkLabel(header, text="ARTIS", font=h_font, anchor="w").grid(row=0, column=2, pady=10, padx=5, sticky="ew")
    ctk.CTkLabel(header, text="GENRE", font=h_font, anchor="w").grid(row=0, column=3, pady=10, padx=5, sticky="ew")
    ctk.CTkLabel(header, text="THN", font=h_font).grid(row=0, column=4, pady=10)
    ctk.CTkLabel(header, text="AKSI", font=h_font).grid(row=0, column=5, pady=10)

    # --- LIST DATA ---
    scroll = ctk.CTkScrollableFrame(parent, fg_color="transparent")
    scroll.pack(fill="both", expand=True, padx=15, pady=5)

    songs = library.getAllSongs()

    # FUNGSI PEMOTONG TEKS (Agar kolom tidak melar)
    def limit_text(txt, max_len):
        s = str(txt)
        if len(s) > max_len:
            return s[:max_len-3] + "..."
        return s

    if not songs:
        ctk.CTkLabel(scroll, text="Belum ada data lagu.", text_color="gray").pack(pady=20)

    for s in songs:
        row = ctk.CTkFrame(scroll, fg_color="white", corner_radius=5)
        row.pack(fill="x", pady=2)
        apply_grid_config(row) # Terapkan bobot kolom yang sama

        # Render dengan limit text
        ctk.CTkLabel(row, text=str(s.id), text_color="gray").grid(row=0, column=0, pady=8)
        
        # Limit Judul 30 karakter, Artis 20 karakter
        ctk.CTkLabel(row, text=limit_text(s.title, 30), text_color="#333", anchor="w").grid(row=0, column=1, pady=8, padx=5, sticky="ew")
        ctk.CTkLabel(row, text=limit_text(s.artist, 20), text_color="gray", anchor="w").grid(row=0, column=2, pady=8, padx=5, sticky="ew")
        ctk.CTkLabel(row, text=limit_text(s.genre, 12), text_color="gray", anchor="w").grid(row=0, column=3, pady=8, padx=5, sticky="ew")
        
        ctk.CTkLabel(row, text=str(s.year), text_color="gray").grid(row=0, column=4, pady=8)

        # Tombol Aksi
        act_frame = ctk.CTkFrame(row, fg_color="transparent")
        act_frame.grid(row=0, column=5, pady=5)
        
        ctk.CTkButton(act_frame, text="Edit", width=40, height=24, fg_color=colors["primary"], font=("Arial", 10),
                      command=lambda sid=s.id: on_edit(sid)).pack(side="left", padx=2)
        ctk.CTkButton(act_frame, text="Hapus", width=40, height=24, fg_color="#FFEEEE", text_color="red", hover_color="#FFDDDD", font=("Arial", 10),
                      command=lambda sid=s.id: on_delete(sid)).pack(side="left", padx=2)