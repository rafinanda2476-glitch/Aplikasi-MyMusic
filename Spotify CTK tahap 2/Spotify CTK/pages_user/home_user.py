import customtkinter as ctk
import random

def render_home(parent, library, colors, on_play_context):
    scroll = ctk.CTkScrollableFrame(parent, fg_color="transparent")
    scroll.pack(fill="both", expand=True)

    # Banner
    banner = ctk.CTkFrame(scroll, fg_color=colors["primary"], corner_radius=10)
    banner.pack(fill="x", padx=15, pady=15)
    ctk.CTkLabel(banner, text="Trending Hits ⚡", font=("Segoe UI", 24, "bold"), text_color="white").pack(padx=20, pady=(20,5), anchor="w")
    ctk.CTkLabel(banner, text="Lagu paling hits minggu ini khusus buat kamu.", text_color="#E0EFFF").pack(padx=20, pady=(0,20), anchor="w")

    all_songs = library.getAllSongs()
    # Kita ambil sampel 8 lagu untuk Home
    display_songs = all_songs[:8] if len(all_songs) > 8 else all_songs

    # GRID LAGU
    grid_frame = ctk.CTkFrame(scroll, fg_color="transparent")
    grid_frame.pack(fill="x", padx=10)

    # Grid 4 Kolom
    for i in range(4): grid_frame.grid_columnconfigure(i, weight=1)

    for i, s in enumerate(display_songs):
        # Hitung baris dan kolom
        r = i // 4
        c = i % 4
        
        card = ctk.CTkFrame(grid_frame, fg_color="white", corner_radius=10)
        card.grid(row=r, column=c, padx=5, pady=5, sticky="nsew")
        
        # Judul & Artis
        ctk.CTkLabel(card, text=s.title, font=("Segoe UI", 14, "bold"), text_color="#333", wraplength=120).pack(pady=(15,0))
        ctk.CTkLabel(card, text=s.artist, font=("Segoe UI", 12), text_color="gray").pack(pady=(0,15))
        
        # Click Play Context
        # Kita kirim seluruh display_songs sebagai antrean, dan index i sebagai start
        def play_cmd(idx=i):
            on_play_context(display_songs, idx)
        
        # Button Play di Card
        ctk.CTkButton(card, text="▶ Play", fg_color=colors["primary"], height=30, width=80, command=play_cmd).pack(pady=(0,15))

    ctk.CTkLabel(scroll, text="Jelajahi lebih banyak di menu Search 🔍", text_color="gray").pack(pady=30)