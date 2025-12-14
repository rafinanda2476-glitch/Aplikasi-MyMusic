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

    # Grid container
    grid_container = ctk.CTkFrame(scroll, fg_color="transparent")
    grid_container.pack(fill="both", expand=True, padx=10)
    
    # Get songs (default sort by title)
    all_songs = library.getSortedSongs("title")
    # Take first 8 songs for display
    display_songs = all_songs[:8] if len(all_songs) > 8 else all_songs

    # GRID LAGU
    grid_frame = ctk.CTkFrame(grid_container, fg_color="transparent")
    grid_frame.pack(fill="x")

    # Grid 4 Kolom
    for i in range(4): 
        grid_frame.grid_columnconfigure(i, weight=1)
    
    # Format duration helper
    def format_duration(seconds):
        mins = seconds // 60
        secs = seconds % 60
        return f"{mins}:{secs:02d}"

    for i, s in enumerate(display_songs):
        # Hitung baris dan kolom
        r = i // 4
        c = i % 4
        
        card = ctk.CTkFrame(grid_frame, fg_color="white", corner_radius=10)
        card.grid(row=r, column=c, padx=5, pady=5, sticky="nsew")
        
        # Judul & Artis
        ctk.CTkLabel(card, text=s.title, font=("Segoe UI", 14, "bold"), text_color="#333", wraplength=120).pack(pady=(15,0))
        ctk.CTkLabel(card, text=s.artist, font=("Segoe UI", 12), text_color="gray").pack(pady=(0,5))
        ctk.CTkLabel(card, text=f"⏱ {format_duration(s.duration)}", font=("Segoe UI", 10), text_color="#999").pack(pady=(0,10))
        
        # Click Play Context
        # Pass ALL songs to queue, but find the correct index of this song
        def play_cmd(song=s):
            # Find this song's index in the full all_songs list
            try:
                song_index = all_songs.index(song)
                on_play_context(all_songs, song_index)  # Pass ALL songs, not just display_songs
            except ValueError:
                # Fallback if song not found
                on_play_context(all_songs, 0)
        
        # Button Play di Card
        ctk.CTkButton(card, text="▶ Play", fg_color=colors["primary"], height=30, width=80, command=play_cmd).pack(pady=(0,15))

    ctk.CTkLabel(grid_container, text="Jelajahi lebih banyak di menu Search 🔍", text_color="gray").pack(pady=30)

