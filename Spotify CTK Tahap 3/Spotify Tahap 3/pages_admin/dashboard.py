import customtkinter as ctk

def render_dashboard(parent, library, colors):
    scroll = ctk.CTkScrollableFrame(parent, fg_color="transparent")
    scroll.pack(fill="both", expand=True)
    
    # Header
    ctk.CTkLabel(scroll, text="Dashboard Admin", font=("Segoe UI", 24, "bold"), text_color=colors["text_head"]).pack(pady=20, padx=20, anchor="w")

    all_songs = library.getAllSongs()
    total_songs = len(all_songs)
    genres = set(s.genre for s in all_songs)
    artists = set(s.artist for s in all_songs)
    
    # Calculate total duration
    total_duration_sec = sum(s.duration for s in all_songs)
    total_hours = total_duration_sec // 3600
    total_mins = (total_duration_sec % 3600) // 60

    # Container Kartu
    cards_frame = ctk.CTkFrame(scroll, fg_color="transparent")
    cards_frame.pack(fill="x", padx=15)
    
    # Helper membuat kartu
    def make_card(parent, title, value, color, icon):
        card = ctk.CTkFrame(parent, fg_color=color, corner_radius=10)
        card.pack(side="left", fill="both", expand=True, padx=5)
        
        ctk.CTkLabel(card, text=icon, font=("Segoe UI", 30)).pack(pady=(15,0))
        ctk.CTkLabel(card, text=str(value), font=("Segoe UI", 32, "bold"), text_color="white").pack()
        ctk.CTkLabel(card, text=title, font=("Segoe UI", 14), text_color="#EFEFEF").pack(pady=(0,15))

    # Baris 1: Statistik Utama
    make_card(cards_frame, "Total Lagu", total_songs, colors["primary"], "🎵") 
    make_card(cards_frame, "Total Genre", len(genres), "#28A745", "🎷") 
    make_card(cards_frame, "Total Artis", len(artists), "#6F42C1", "🎤")
    make_card(cards_frame, "Total Durasi", f"{total_hours}h {total_mins}m", "#FD7E14", "⏱")

    # Top Artists Section
    ctk.CTkLabel(scroll, text="🌟 Top 5 Artis (Berdasarkan Jumlah Lagu)", 
                font=("Segoe UI", 16, "bold"), 
                text_color="#555").pack(pady=(30,10), padx=20, anchor="w")
    
    top_artists_frame = ctk.CTkFrame(scroll, fg_color="white", corner_radius=10)
    top_artists_frame.pack(fill="x", padx=20, pady=(0,10))
    
    # Count songs per artist
    artist_counts = {}
    for song in all_songs:
        artist_counts[song.artist] = artist_counts.get(song.artist, 0) + 1
    
    # Sort and get top 5
    top_artists = sorted(artist_counts.items(), key=lambda x: x[1], reverse=True)[:5]
    
    if top_artists:
        for i, (artist, count) in enumerate(top_artists, 1):
            artist_row = ctk.CTkFrame(top_artists_frame, fg_color="transparent")
            artist_row.pack(fill="x", padx=15, pady=8)
            
            # Rank
            ctk.CTkLabel(artist_row, text=f"#{i}", 
                        font=("Segoe UI", 14, "bold"),
                        text_color=colors["primary"],
                        width=40).pack(side="left")
            
            # Artist name
            ctk.CTkLabel(artist_row, text=artist, 
                        font=("Segoe UI", 14),
                        text_color="#333",
                        anchor="w").pack(side="left", fill="x", expand=True, padx=10)
            
            # Song count
            ctk.CTkLabel(artist_row, text=f"{count} lagu", 
                        font=("Segoe UI", 12),
                        text_color="#666").pack(side="right")
    
    # Genre Distribution Section
    ctk.CTkLabel(scroll, text="📊 Distribusi Genre", 
                font=("Segoe UI", 16, "bold"), 
                text_color="#555").pack(pady=(20,10), padx=20, anchor="w")
    
    genre_frame = ctk.CTkFrame(scroll, fg_color="white", corner_radius=10)
    genre_frame.pack(fill="x", padx=20, pady=(0,10))
    
    # Count songs per genre
    genre_counts = {}
    for song in all_songs:
        genre_counts[song.genre] = genre_counts.get(song.genre, 0) + 1
    
    # Sort by count
    sorted_genres = sorted(genre_counts.items(), key=lambda x: x[1], reverse=True)
    
    # Color palette for genres
    genre_colors = ["#007BFF", "#28A745", "#FD7E14", "#6F42C1", "#DC3545", "#17A2B8"]
    
    if sorted_genres:
        for i, (genre, count) in enumerate(sorted_genres[:6]):  # Show max 6 genres
            genre_row = ctk.CTkFrame(genre_frame, fg_color="transparent")
            genre_row.pack(fill="x", padx=15, pady=6)
            
            # Genre color indicator
            color_box = ctk.CTkFrame(genre_row, 
                                    fg_color=genre_colors[i % len(genre_colors)],
                                    width=20, height=20,
                                    corner_radius=3)
            color_box.pack(side="left", padx=(0, 10))
            
            # Genre name
            ctk.CTkLabel(genre_row, text=genre, 
                        font=("Segoe UI", 13),
                        text_color="#333",
                        anchor="w",
                        width=150).pack(side="left")
            
            # Progress bar background
            progress_bg = ctk.CTkFrame(genre_row, fg_color="#E9ECEF", 
                                      height=20, corner_radius=10)
            progress_bg.pack(side="left", fill="x", expand=True, padx=5)
            
            # Progress fill
            percentage = (count / total_songs) * 100
            progress_fill = ctk.CTkFrame(progress_bg, 
                                        fg_color=genre_colors[i % len(genre_colors)],
                                        height=20, 
                                        corner_radius=10)
            progress_fill.place(relx=0, rely=0, relwidth=percentage/100, relheight=1)
            
            # Count label
            ctk.CTkLabel(genre_row, text=f"{count} ({percentage:.1f}%)", 
                        font=("Segoe UI", 11),
                        text_color="#666",
                        width=100).pack(side="right")
    
    # Recent Uploads
    ctk.CTkLabel(scroll, text="🆕 Lagu Terbaru Ditambahkan", 
                font=("Segoe UI", 16, "bold"), 
                text_color="#555").pack(pady=(20,10), padx=20, anchor="w")
    
    recent_frame = ctk.CTkFrame(scroll, fg_color="white", corner_radius=10)
    recent_frame.pack(fill="x", padx=20, pady=(0,20))
    
    # Get last 5 songs (assuming higher IDs are newer)
    recent_songs = sorted(all_songs, key=lambda s: s.id, reverse=True)[:5]
    
    for song in recent_songs:
        song_row = ctk.CTkFrame(recent_frame, fg_color="transparent")
        song_row.pack(fill="x", padx=15, pady=6)
        
        # Music note icon
        ctk.CTkLabel(song_row, text="🎵", 
                    font=("Segoe UI", 16)).pack(side="left", padx=(0, 10))
        
        # Song info
        info_frame = ctk.CTkFrame(song_row, fg_color="transparent")
        info_frame.pack(side="left", fill="x", expand=True)
        
        ctk.CTkLabel(info_frame, text=song.title, 
                    font=("Segoe UI", 13, "bold"),
                    text_color="#333",
                    anchor="w").pack(fill="x")
        
        ctk.CTkLabel(info_frame, text=f"{song.artist} • {song.genre} • {song.year}", 
                    font=("Segoe UI", 11),
                    text_color="#666",
                    anchor="w").pack(fill="x")
