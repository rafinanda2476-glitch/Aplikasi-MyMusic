import customtkinter as ctk
from tkinter import messagebox, simpledialog

def render_playlist(parent, library, playlist_manager, colors, on_play_context, on_remove):
    # Top bar - removed playlist selector, now controlled via sidebar
    top_bar = ctk.CTkFrame(parent, fg_color="transparent")
    top_bar.pack(fill="x", padx=20, pady=10)
    
    # Content container
    content_container = ctk.CTkFrame(parent, fg_color="transparent")
    content_container.pack(fill="both", expand=True, padx=15, pady=5)
    
    def render_playlist_content():
        # Clear content
        for w in content_container.winfo_children():
            w.destroy()
        
        current_pl = playlist_manager.getCurrentPlaylist()
        if not current_pl:
            ctk.CTkLabel(content_container, text="Playlist tidak ditemukan", text_color="gray").pack(pady=20)
            return
        
        songs = current_pl.listSongs()
        
        # Header
        header_frame = ctk.CTkFrame(content_container, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0,10))
        
        ctk.CTkLabel(header_frame, text=f"📚 {current_pl.name}", 
                    font=("Segoe UI", 18, "bold"), text_color=colors["primary"]).pack(side="left")
        
        ctk.CTkLabel(header_frame, text=f"{len(songs)} lagu", 
                    font=("Segoe UI", 12), text_color="gray").pack(side="left", padx=10)
        
        # Scrollable list
        scroll = ctk.CTkScrollableFrame(content_container, fg_color="transparent")
        scroll.pack(fill="both", expand=True)
        
        if not songs:
            ctk.CTkLabel(scroll, text="Playlist masih kosong.\nTambahkan lagu dari halaman Cari Lagu.", 
                        text_color="gray", font=("Segoe UI", 13)).pack(pady=40)
            return
        
        # Format duration helper
        def format_duration(seconds):
            mins = seconds // 60
            secs = seconds % 60
            return f"{mins}:{secs:02d}"
        
        for i, s in enumerate(songs):
            row = ctk.CTkFrame(scroll, fg_color="#F5F9FF", corner_radius=8)
            row.pack(fill="x", pady=3, padx=5)
            
            # Play button
            def play_this(idx=i):
                on_play_context(songs, idx)
            
            btn_play = ctk.CTkButton(row, text="▶", width=35, height=35, fg_color=colors["primary"],
                                    hover_color=colors["hover"], command=play_this,
                                    font=("Segoe UI", 16))
            btn_play.pack(side="left", padx=8, pady=6)
            
            # Info container
            info_frame = ctk.CTkFrame(row, fg_color="transparent")
            info_frame.pack(side="left", fill="x", expand=True, padx=5)
            
            ctk.CTkLabel(info_frame, text=s.title, font=("Segoe UI", 13, "bold"), 
                        text_color="#0033CC", anchor="w").pack(anchor="w")
            ctk.CTkLabel(info_frame, text=f"{s.artist} • {s.genre} • {format_duration(s.duration)}", 
                        font=("Segoe UI", 11), text_color="#666", anchor="w").pack(anchor="w")
            
            # Remove button
            ctk.CTkButton(row, text="✕", width=35, height=35, fg_color="#FFE0E0",
                         text_color="#CC0000", hover_color="#FFCCCC",
                         font=("Segoe UI", 14, "bold"),
                         command=lambda sid=s.id: remove_from_playlist(sid)).pack(side="right", padx=8, pady=6)
    
    def remove_from_playlist(song_id):
        current_pl_name = playlist_manager.current_playlist_name
        if playlist_manager.removeSongFromPlaylist(current_pl_name, song_id):
            render_playlist_content()
            if on_remove:
                on_remove(song_id)
    
    # Initial render
    render_playlist_content()
