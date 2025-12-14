import customtkinter as ctk
import random

def render_search(parent, library, colors, on_play_context, on_add, query=""):
    # Content area - no header, search comes from topbar
    content_scroll = ctk.CTkScrollableFrame(parent, fg_color="transparent")
    content_scroll.pack(fill="both", expand=True, padx=15, pady=15)

    def show_results(search_query):
        # Clear content
        for w in content_scroll.winfo_children():
            w.destroy()
        
        # Perform search
        if search_query.strip():
            results = library.searchSongs(search_query, fuzzy=True, search_fields=["title", "artist"])
            title = f"Hasil pencarian '{search_query}'"
        else:
            # Show trending if no query
            all_songs = library.getAllSongs()
            results = random.sample(all_songs, min(10, len(all_songs))) if all_songs else []
            title = "🔥 Lagu Populer"
        
        # Header
        ctk.CTkLabel(content_scroll, text=title, font=("Segoe UI", 18, "bold"), 
                    text_color=colors["text_head"]).pack(anchor="w", pady=(10,15))

        if not results:
            ctk.CTkLabel(content_scroll, text="Tidak ada hasil ditemukan.", 
                        text_color="gray", font=("Segoe UI", 13)).pack(pady=40)
            return

        # Format duration helper
        def format_duration(seconds):
            mins = seconds // 60
            secs = seconds % 60
            return f"{mins}:{secs:02d}"

        # Grid container (same as home page)
        grid_frame = ctk.CTkFrame(content_scroll, fg_color="transparent")
        grid_frame.pack(fill="x", pady=10)

        # Grid 4 Kolom
        for i in range(4): 
            grid_frame.grid_columnconfigure(i, weight=1)

        # Display results in grid (same as home page)
        for i, s in enumerate(results):
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
            def play_cmd(song=s, idx=i):
                on_play_context(results, idx)
            
            # Button Play di Card
            ctk.CTkButton(card, text="▶ Play", fg_color=colors["primary"], height=30, width=80, command=play_cmd).pack(pady=(0,5))
            
            # Add to collection button
            ctk.CTkButton(card, text="+ Koleksi", fg_color=colors["hover"], height=25, width=80, 
                         font=("Segoe UI", 10), command=lambda sid=s.id: on_add(sid)).pack(pady=(0,15))
    
    # Show results for initial query
    show_results(query)


