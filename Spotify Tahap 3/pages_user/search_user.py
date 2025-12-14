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

        # Song list
        for i, s in enumerate(results):
            row = ctk.CTkFrame(content_scroll, fg_color="white")
            row.pack(fill="x", pady=4)
            
            # Play button
            def play_this(idx=i):
                on_play_context(results, idx)

            btn_play = ctk.CTkButton(row, text="▶", width=40, fg_color="transparent", 
                                     text_color=colors["primary"], hover_color="#E0EFFF", 
                                     command=play_this)
            btn_play.pack(side="left", padx=5)

            ctk.CTkLabel(row, text=s.title, font=("Segoe UI", 14, "bold"), 
                        text_color="#333", width=250, anchor="w").pack(side="left", padx=5)
            ctk.CTkLabel(row, text=s.artist, text_color="gray").pack(side="left", padx=10)
            ctk.CTkLabel(row, text=f"[{format_duration(s.duration)}]", 
                        text_color="#999", font=("Arial", 10)).pack(side="left", padx=5)
            
            # Add to playlist button
            ctk.CTkButton(row, text="+ Koleksi", width=80, fg_color=colors["hover"], height=30,
                         command=lambda sid=s.id: on_add(sid)).pack(side="right", padx=10, pady=5)
    
    # Show results for initial query
    show_results(query)

