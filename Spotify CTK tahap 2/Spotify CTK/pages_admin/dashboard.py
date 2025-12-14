import customtkinter as ctk

def render_dashboard(parent, library, colors):
    # Header
    ctk.CTkLabel(parent, text="Dashboard Admin", font=("Segoe UI", 24, "bold"), text_color=colors["text_head"]).pack(pady=20, padx=20, anchor="w")

    all_songs = library.getAllSongs()
    total_songs = len(all_songs)
    genres = set(s.genre for s in all_songs)
    artists = set(s.artist for s in all_songs)

    # Container Kartu
    cards_frame = ctk.CTkFrame(parent, fg_color="transparent")
    cards_frame.pack(fill="x", padx=15)
    
    # Helper membuat kartu
    def make_card(parent, title, value, color, icon):
        card = ctk.CTkFrame(parent, fg_color=color, corner_radius=10)
        card.pack(side="left", fill="both", expand=True, padx=5)
        
        ctk.CTkLabel(card, text=icon, font=("Segoe UI", 30)).pack(pady=(15,0))
        ctk.CTkLabel(card, text=str(value), font=("Segoe UI", 32, "bold"), text_color="white").pack()
        ctk.CTkLabel(card, text=title, font=("Segoe UI", 14), text_color="#EFEFEF").pack(pady=(0,15))

    # Baris 1: Statistik
    # Menggunakan warna dari palette atau hardcoded yang sesuai tema
    make_card(cards_frame, "Total Lagu", total_songs, colors["primary"], "🎵") 
    make_card(cards_frame, "Total Genre", len(genres), "#28A745", "🎷") 
    make_card(cards_frame, "Total Artis", len(artists), "#6F42C1", "🎤") 

    # Baris 2: Quick Actions
    ctk.CTkLabel(parent, text="Aksi Cepat", font=("Segoe UI", 16, "bold"), text_color="#555").pack(pady=(30,10), padx=20, anchor="w")
    
    action_frame = ctk.CTkFrame(parent, fg_color="white", corner_radius=10)
    action_frame.pack(fill="x", padx=20)

    ctk.CTkButton(action_frame, text="Backup Data JSON", fg_color="#6C757D", command=lambda: print("Backup...")).pack(side="left", padx=10, pady=20)
    ctk.CTkButton(action_frame, text="Reset Player Cache", fg_color=colors["danger"], command=lambda: print("Reset...")).pack(side="left", padx=10, pady=20)