import customtkinter as ctk
import random

def render_search(parent, library, colors, on_play_context, on_add):
    # Header Input
    head = ctk.CTkFrame(parent, fg_color="white", corner_radius=0)
    head.pack(fill="x", pady=(0,10))
    
    entry_var = ctk.StringVar()
    entry = ctk.CTkEntry(head, textvariable=entry_var, placeholder_text="Cari judul lagu...", width=300, height=40)
    entry.pack(side="left", padx=20, pady=15)

    btn_search = ctk.CTkButton(head, text="Cari", width=100, height=40, fg_color=colors["primary"], hover_color=colors["hover"])
    btn_search.pack(side="left", pady=15)

    # Content
    content_scroll = ctk.CTkScrollableFrame(parent, fg_color="transparent")
    content_scroll.pack(fill="both", expand=True, padx=15, pady=(0,15))

    def show_list(songs_list, title="Hasil Pencarian"):
        for w in content_scroll.winfo_children(): w.destroy()
        
        ctk.CTkLabel(content_scroll, text=title, font=("Segoe UI", 16, "bold"), text_color=colors["text_head"]).pack(anchor="w", pady=(10,10))

        if not songs_list:
            ctk.CTkLabel(content_scroll, text="Tidak ditemukan.", text_color="gray").pack()
            return

        for i, s in enumerate(songs_list):
            row = ctk.CTkFrame(content_scroll, fg_color="white")
            row.pack(fill="x", pady=4)
            
            # Play saat klik row (Kirim konteks list ini)
            def play_this(idx=i):
                on_play_context(songs_list, idx)

            btn_play = ctk.CTkButton(row, text="▶", width=40, fg_color="transparent", text_color=colors["primary"], 
                                     hover_color="#E0EFFF", command=play_this)
            btn_play.pack(side="left", padx=5)

            ctk.CTkLabel(row, text=s.title, font=("Segoe UI", 14, "bold"), text_color="#333", width=250, anchor="w").pack(side="left", padx=5)
            ctk.CTkLabel(row, text=s.artist, text_color="gray").pack(side="left", padx=10)
            
            # Tombol Tambah ke Playlist
            ctk.CTkButton(row, text="+ Koleksi", width=80, fg_color=colors["hover"], height=30,
                          command=lambda sid=s.id: on_add(sid)).pack(side="right", padx=10, pady=5)

    # Default View (Trending)
    all_songs = library.getAllSongs()
    trending = random.sample(all_songs, min(5, len(all_songs))) if all_songs else []
    show_list(trending, "🔥 Sedang Banyak Dicari")

    def perform_search():
        q = entry_var.get().lower().strip()
        if not q:
            show_list(trending, "🔥 Sedang Banyak Dicari")
            return
        
        # Search title only
        res = [s for s in all_songs if q in s.title.lower()]
        show_list(res, f"Hasil pencarian: '{q}'")

    btn_search.configure(command=perform_search)
    entry.bind("<Return>", lambda e: perform_search())