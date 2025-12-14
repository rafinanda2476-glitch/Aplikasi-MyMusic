import customtkinter as ctk
from tkinter import messagebox

# logic
from logic.library import SongLibrary
from logic.playlist import Playlist
from logic.controller_player import PlayerController

# components
from components.topbar import TopBar
from components.sidebar_user import SidebarUser
from components.sidebar_admin import SidebarAdmin
from components.bottom_player import BottomPlayer

# pages
from pages_user.home_user import render_home
from pages_user.search_user import render_search
from pages_user.playlist_user import render_playlist
from pages_admin.dashboard import render_dashboard
from pages_admin.songs_list import render_songs_list
from pages_admin.add_song import render_add_song
from pages_admin.edit_song import render_edit_song
from pages_admin.delete_song import render_delete_song
from pages_admin.import_csv import render_import_csv

# login
from login import LoginPage

# --- CONFIG TEMA ---
ctk.set_appearance_mode("Light")
COLORS = {
    "primary": "#0047FF",       # Electric Blue
    "hover": "#0033CC",         # Darker Electric
    "bg_sidebar": "#001040",    # Deep Navy
    "bg_content": "#F0F5FF",    # Ice Blue
    "text_head": "#001A5E",     # Navy Text
    "danger": "#FF3333"         # Red for delete
}

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("MyMusic - Electric Blue Edition")
        self.geometry("1280x850")
        
        # logic layers
        self.library = SongLibrary()
        self.playlist = Playlist() # Saved User Playlist
        
        # Player Controller baru (Queue Based)
        self.player = PlayerController() 

        # containers
        self.header = None
        self.main_container = None
        self.sidebar_frame = None
        self.content_frame = None
        self.bottom_player = None

        self.role = "login"

        # load sample songs
        self.library.load_sample_if_empty()

        self.show_login()

    def clear_root(self):
        for w in self.winfo_children():
            w.destroy()

    def show_login(self):
        self.clear_root()
        self.role = "login"
        LoginPage(self, on_login=self._on_login, colors=COLORS).pack(fill="both", expand=True)

    def _on_login(self, role):
        if role not in ("user", "admin"): return
        self.role = role
        self.build_main_ui()

    def build_main_ui(self):
        self.clear_root()

        # 1. TOPBAR
        self.header = TopBar(self, logout_callback=self.on_logout, colors=COLORS)
        self.header.pack(side="top", fill="x")

        # 2. MAIN CONTAINER
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.pack(side="top", fill="both", expand=True)

        # 3. SIDEBAR
        if self.role == "user":
            self.sidebar_frame = SidebarUser(
                self.main_container,
                colors=COLORS,
                on_home=lambda: self.load_page("home"),
                on_search=lambda: self.load_page("search"),
                on_playlist=lambda: self.load_page("playlist"),
            )
        else: # admin
            self.sidebar_frame = SidebarAdmin(
                self.main_container,
                colors=COLORS,
                on_dashboard=lambda: self.load_page("admin_dashboard"),
                on_songs=lambda: self.load_page("admin_songs"),
                on_add=lambda: self.load_page("admin_add"),
                on_import=lambda: self.load_page("admin_import")
            )
        
        self.sidebar_frame.pack(side="left", fill="y")

        # 4. CONTENT FRAME
        self.content_frame = ctk.CTkFrame(self.main_container, fg_color=COLORS["bg_content"], corner_radius=15)
        self.content_frame.pack(side="left", fill="both", expand=True, padx=15, pady=15)

        # 5. BOTTOM PLAYER (User Only)
        if self.role == "user":
            self.bottom_player = BottomPlayer(
                self.content_frame, 
                colors=COLORS,
                prev_cb=self.on_prev,
                play_cb=self.on_play_pause, # Satu fungsi toggle
                next_cb=self.on_next
            )
            self.bottom_player.pack(side="bottom", fill="x")

        # Default page
        if self.role == "user":
            self.load_page("home")
        else:
            self.load_page("admin_dashboard")

    def load_page(self, page, **kwargs):
        # Clear content area (kecuali player)
        for w in self.content_frame.winfo_children():
            if w != self.bottom_player:
                w.destroy()
        
        # Wrapper halaman
        page_area = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        page_area.pack(fill="both", expand=True, side="top")

        if page == "home":
            render_home(page_area, self.library, colors=COLORS,
                        on_play_context=self.play_from_context) # Pass fungsi play context
        
        elif page == "search":
            render_search(page_area, self.library, colors=COLORS,
                          on_play_context=self.play_from_context,
                          on_add=self.add_to_playlist)

        elif page == "playlist":
            render_playlist(page_area, self.playlist, colors=COLORS,
                            on_play_context=self.play_from_playlist,
                            on_remove=self.remove_from_playlist)

        elif page == "admin_dashboard":
            render_dashboard(page_area, self.library, colors=COLORS)

        elif page == "admin_songs":
            render_songs_list(page_area, self.library, colors=COLORS,
                on_edit=lambda sid: self.load_page("admin_edit", song_id=sid),
                on_delete=lambda sid: self.load_page("admin_delete", song_id=sid))
        
        elif page == "admin_add":
             render_add_song(page_area, self.library, colors=COLORS, on_saved=lambda: self.load_page("admin_songs"))
        
        elif page == "admin_edit":
             render_edit_song(page_area, self.library, colors=COLORS, song_id=kwargs.get("song_id"), on_saved=lambda: self.load_page("admin_songs"))
        
        elif page == "admin_delete":
             render_delete_song(page_area, self.library, colors=COLORS, song_id=kwargs.get("song_id"), on_deleted=lambda: self.load_page("admin_songs"))
        
        elif page == "admin_import":
            from pages_admin.import_csv import render_import_csv
            render_import_csv(page_area, self.library, colors=COLORS, on_finished=lambda: self.load_page("admin_songs"))

        self.refresh_bottom_player()

    # --- LOGIC PLAYER & PLAYLIST ---
    
    # Fungsi ini dipanggil dari Home/Search. 
    # Menerima: list_lagu_context (semua lagu di halaman itu) dan index lagu yang diklik
    def play_from_context(self, song_list, start_index):
        self.player.set_queue(song_list, start_index)
        self.refresh_bottom_player()

    def play_from_playlist(self, song_id):
        # Konversi LinkedList Playlist ke List biasa untuk PlayerController
        songs = self.playlist.listSongs()
        # Cari index
        idx = 0
        for i, s in enumerate(songs):
            if s.id == song_id:
                idx = i
                break
        self.player.set_queue(songs, idx)
        self.refresh_bottom_player()

    def add_to_playlist(self, song_id):
        node = self.library.findNodeById(song_id)
        if not node: return
        if self.playlist.addSong(node.song):
            messagebox.showinfo("Sukses", "Lagu ditambahkan ke Koleksi.")
        else:
            messagebox.showwarning("Info", "Lagu sudah ada di playlist.")

    def remove_from_playlist(self, song_id):
        if self.playlist.removeSong(song_id):
            messagebox.showinfo("Dihapus", "Lagu dihapus.")
            # Refresh halaman playlist
            self.load_page("playlist")

    def on_play_pause(self):
        if self.player.is_playing:
            self.player.pause()
        else:
            self.player.play()
        self.refresh_bottom_player()

    def on_next(self):
        self.player.next()
        self.refresh_bottom_player()

    def on_prev(self):
        self.player.prev()
        self.refresh_bottom_player()

    def refresh_bottom_player(self):
        if self.role != "user" or not self.bottom_player: return
        self.bottom_player.update_state(self.player.current_song, self.player.is_playing)

    def on_logout(self):
        if messagebox.askyesno("Logout", "Keluar aplikasi?"):
            self.show_login()