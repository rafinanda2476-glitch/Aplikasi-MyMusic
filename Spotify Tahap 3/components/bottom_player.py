import customtkinter as ctk
from PIL import Image, ImageDraw
import io

class BottomPlayer(ctk.CTkFrame):
    def __init__(self, parent, colors, prev_cb, play_cb, next_cb, shuffle_cb, repeat_cb):
        super().__init__(parent, fg_color="#000000", height=90, corner_radius=0)
        self.colors = colors
        self.play_cb = play_cb
        self.shuffle_cb = shuffle_cb
        self.repeat_cb = repeat_cb
        
        # Prevent frame from resizing based on content
        self.pack_propagate(False)
        
        # Main container with proper padding
        main_container = ctk.CTkFrame(self, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Grid Layout: 3 columns
        main_container.grid_columnconfigure(0, weight=1)  # Left: Song Info
        main_container.grid_columnconfigure(1, weight=2)  # Center: Controls & Progress
        main_container.grid_columnconfigure(2, weight=1)  # Right: Shuffle/Repeat
        
        # ===== LEFT SECTION: Album Art + Song Info =====
        left_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        left_frame.grid(row=0, column=0, sticky="w", padx=(10, 0))
        
        # Create album artwork placeholder (50x50)
        self.album_art_label = ctk.CTkLabel(left_frame, text="", width=50, height=50, 
                                            fg_color="#333333", corner_radius=4)
        self.album_art_label.grid(row=0, column=0, rowspan=2, padx=(0, 12), pady=0, sticky="w")
        
        # Song title - fixed width to prevent layout shift
        self.lbl_title = ctk.CTkLabel(left_frame, text="", 
                                      font=("Segoe UI", 14, "bold"), 
                                      text_color="white", anchor="w", width=250)
        self.lbl_title.grid(row=0, column=1, sticky="w", pady=(0, 2))
        
        # Artist name - fixed width to prevent layout shift
        self.lbl_artist = ctk.CTkLabel(left_frame, text="", 
                                       font=("Segoe UI", 12), 
                                       text_color="#B3B3B3", anchor="w", width=250)
        self.lbl_artist.grid(row=1, column=1, sticky="w")
        
        # ===== CENTER SECTION: Playback Controls + Progress Bar =====
        center_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        center_frame.grid(row=0, column=1, sticky="ew", padx=(8, 220))  # Shift left for centering
        
        # Controls container (centered)
        controls_container = ctk.CTkFrame(center_frame, fg_color="transparent")
        controls_container.pack(pady=(0, 5))
        
        btn_config = {
            "fg_color": "transparent",
            "text_color": "#B3B3B3",
            "hover_color": "#1A1A1A",
            "width": 32,
            "height": 32,
            "font": ("Segoe UI", 16)
        }
        
        # Shuffle button (leftmost)
        self.btn_shuffle = ctk.CTkButton(controls_container, text="🔀", 
                                         command=shuffle_cb, **btn_config)
        self.btn_shuffle.pack(side="left", padx=8)
        
        # Previous button
        ctk.CTkButton(controls_container, text="⏮", command=prev_cb, **btn_config).pack(side="left", padx=8)
        
        # Play/Pause button (larger, white circle) - fixed size to prevent shifting
        self.btn_play = ctk.CTkButton(controls_container, text="▶", 
                                      width=40, height=40, corner_radius=20,
                                      fg_color="white", text_color="black", 
                                      hover_color="#E0E0E0",
                                      font=("Arial", 15, "bold"), command=play_cb)
        self.btn_play.pack(side="left", padx=8)
        
        # Next button
        ctk.CTkButton(controls_container, text="⏭", command=next_cb, **btn_config).pack(side="left", padx=8)
        
        # Repeat button (rightmost)
        self.btn_repeat = ctk.CTkButton(controls_container, text="🔁", 
                                        command=repeat_cb, **btn_config)
        self.btn_repeat.pack(side="left", padx=8)
        
        # Progress bar container
        progress_container = ctk.CTkFrame(center_frame, fg_color="transparent")
        progress_container.pack(fill="x", pady=0)
        progress_container.grid_columnconfigure(1, weight=1)
        
        # Current time
        self.lbl_current_time = ctk.CTkLabel(progress_container, text="0:00", 
                                             font=("Segoe UI", 10), 
                                             text_color="#B3B3B3", width=40)
        self.lbl_current_time.grid(row=0, column=0, padx=(0, 8))
        
        # Progress bar
        self.progress_bar = ctk.CTkProgressBar(progress_container, 
                                               height=4,
                                               progress_color="white",
                                               fg_color="#4D4D4D")
        self.progress_bar.grid(row=0, column=1, sticky="ew")
        self.progress_bar.set(0)  # Initial progress (empty)
        
        # Total duration
        self.lbl_total_time = ctk.CTkLabel(progress_container, text="0:00", 
                                           font=("Segoe UI", 10), 
                                           text_color="#B3B3B3", width=40)
        self.lbl_total_time.grid(row=0, column=2, padx=(8, 0))
        
        # ===== RIGHT SECTION: Volume Control =====
        right_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        right_frame.grid(row=0, column=2, sticky="e", padx=(0, 10))
        
        # Volume icon
        self.lbl_volume = ctk.CTkLabel(right_frame, text="🔊", 
                                       font=("Segoe UI", 16),
                                       text_color="#B3B3B3")
        self.lbl_volume.pack(side="left", padx=(0, 8))
        
        # Volume slider
        self.volume_slider = ctk.CTkSlider(right_frame, 
                                           width=100,
                                           height=4,
                                           progress_color="white",
                                           fg_color="#4D4D4D",
                                           button_color="white",
                                           button_hover_color="#E0E0E0",
                                           from_=0, to=100)
        self.volume_slider.set(70)  # Default 70%
        self.volume_slider.pack(side="left")

    def update_state(self, song, is_playing):
        """Update player state with current song info."""
        if song:
            # Update title and artist
            title = song.title if len(song.title) <= 30 else song.title[:27] + "..."
            self.lbl_title.configure(text=title)
            self.lbl_artist.configure(text=song.artist)
            
            # Update play/pause button - maintain fixed size
            icon = "⏸" if is_playing else "▶"
            self.btn_play.configure(text=icon, width=40, height=40)
        else:
            # No song - show empty state
            self.lbl_title.configure(text="")
            self.lbl_artist.configure(text="")
            self.btn_play.configure(text="▶")
            # Reset time and progress
            self.lbl_current_time.configure(text="0:00")
            self.lbl_total_time.configure(text="0:00")
            self.progress_bar.set(0)
    
    def update_timer(self, elapsed_seconds, total_duration):
        """Update progress bar and time labels."""
        # Format time as M:SS
        def format_time(seconds):
            mins = seconds // 60
            secs = seconds % 60
            return f"{mins}:{secs:02d}"
        
        self.lbl_current_time.configure(text=format_time(elapsed_seconds))
        self.lbl_total_time.configure(text=format_time(total_duration))
        
        # Update progress bar
        if total_duration > 0:
            progress = elapsed_seconds / total_duration
            self.progress_bar.set(progress)
        else:
            self.progress_bar.set(0)
    
    def update_shuffle_repeat(self, shuffle_enabled, repeat_mode):
        """Update shuffle and repeat button states."""
        # Update shuffle button color
        if shuffle_enabled:
            self.btn_shuffle.configure(text_color="#1DB954")  # Spotify green
        else:
            self.btn_shuffle.configure(text_color="#B3B3B3")
        
        # Update repeat button - show different icons
        if repeat_mode == 'one':
            self.btn_repeat.configure(text="🔂", text_color="#1DB954")  # Repeat one (green)
        elif repeat_mode == 'all':
            self.btn_repeat.configure(text="🔁", text_color="#1DB954")  # Repeat all (green)
        else:
            self.btn_repeat.configure(text="🔁", text_color="#B3B3B3")  # Off (gray)