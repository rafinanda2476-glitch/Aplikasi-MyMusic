import customtkinter as ctk

def render_playlist(parent, playlist, colors, on_play_context, on_remove):
    ctk.CTkLabel(parent, text="Koleksi Saya", font=("Segoe UI", 22, "bold"), text_color=colors["text_head"]).pack(pady=15, padx=20, anchor="w")

    scroll = ctk.CTkScrollableFrame(parent, fg_color="transparent")
    scroll.pack(fill="both", expand=True, padx=15, pady=(0,15))

    songs = playlist.listSongs()
    if not songs:
        ctk.CTkLabel(scroll, text="Playlist kosong.", text_color="gray").pack(pady=20)
        return

    for i, s in enumerate(songs, start=1):
        row = ctk.CTkFrame(scroll, fg_color="white", corner_radius=8)
        row.pack(fill="x", pady=4)

        ctk.CTkLabel(row, text=str(i), width=30, text_color="gray").pack(side="left", padx=10)
        
        # Info
        ctk.CTkLabel(row, text=s.title, font=("Segoe UI", 14, "bold"), text_color="#333", width=200, anchor="w").pack(side="left", padx=5)
        ctk.CTkLabel(row, text=s.artist, text_color="gray").pack(side="left", padx=5)

        # Tombol Hapus (Merah Teks)
        ctk.CTkButton(row, text="Hapus", width=70, height=28, fg_color="#FFEEEE", text_color="red", 
                      hover_color="#FFDDDD", command=lambda sid=s.id: on_remove(sid)).pack(side="right", padx=10, pady=8)

        # Play Button (Blue)
        ctk.CTkButton(row, text="Putar", width=70, height=28, fg_color=colors["primary"], 
                      command=lambda sid=s.id: on_play_context(sid)).pack(side="right", padx=5)