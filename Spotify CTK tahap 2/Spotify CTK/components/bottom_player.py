import customtkinter as ctk

class BottomPlayer(ctk.CTkFrame):
    def __init__(self, parent, colors, prev_cb, play_cb, next_cb):
        super().__init__(parent, fg_color="#080808", height=80, corner_radius=0)
        self.colors = colors
        self.play_cb = play_cb
        
        # Grid Layout: 3 Kolom
        self.grid_columnconfigure(0, weight=1) # Info Lagu (Kiri)
        self.grid_columnconfigure(1, weight=0) # Kontrol (Tengah - Fixed)
        self.grid_columnconfigure(2, weight=1) # Volume/Kosong (Kanan)
        self.grid_rowconfigure(0, weight=1)

        # 1. Info Area
        info_frame = ctk.CTkFrame(self, fg_color="transparent")
        info_frame.grid(row=0, column=0, sticky="w", padx=20)
        
        self.lbl_title = ctk.CTkLabel(info_frame, text="Ready", font=("Segoe UI", 14, "bold"), text_color="white", anchor="w", width=200)
        self.lbl_title.pack(anchor="w")
        self.lbl_artist = ctk.CTkLabel(info_frame, text="Select song...", font=("Segoe UI", 12), text_color="gray", anchor="w")
        self.lbl_artist.pack(anchor="w")

        # 2. Control Area (Center)
        ctrl_frame = ctk.CTkFrame(self, fg_color="transparent")
        ctrl_frame.grid(row=0, column=1)

        btn_conf = {"fg_color": "transparent", "text_color": "white", "width": 40, "hover_color": "#333", "font": ("Arial", 18)}
        
        ctk.CTkButton(ctrl_frame, text="⏮", command=prev_cb, **btn_conf).pack(side="left", padx=10)
        
        # Tombol Play Besar Bulat
        self.btn_play = ctk.CTkButton(ctrl_frame, text="▶", width=50, height=50, corner_radius=25,
                                      fg_color="white", text_color="black", hover_color="#DDD",
                                      font=("Arial", 20), command=play_cb)
        self.btn_play.pack(side="left", padx=10)

        ctk.CTkButton(ctrl_frame, text="⏭", command=next_cb, **btn_conf).pack(side="left", padx=10)

        # 3. Kanan (Kosong/Spacer)
        ctk.CTkFrame(self, fg_color="transparent").grid(row=0, column=2)

    def update_state(self, song, is_playing):
        if song:
            # Potong judul panjang agar layout tidak rusak (manual ellipsis)
            title = song.title
            if len(title) > 25: title = title[:22] + "..."
            
            self.lbl_title.configure(text=title)
            self.lbl_artist.configure(text=song.artist)
            self.btn_play.configure(text="⏸" if is_playing else "▶")
        else:
            self.lbl_title.configure(text="MyMusic")
            self.lbl_artist.configure(text="Pilih lagu untuk memutar")
            self.btn_play.configure(text="▶")