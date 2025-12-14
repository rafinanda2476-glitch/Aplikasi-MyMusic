import customtkinter as ctk
from tkinter import messagebox
import os
from pathlib import Path

# logic
from logic.library import SongLibrary
from logic.playlist import PlaylistManager
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
from pages_user.create_playlist import render_create_playlist
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
        self.title("MyMusic")
        self.geometry("1280x850")
        
        # logic layers
        self.library = SongLibrary()
        self.playlist_manager = PlaylistManager() # Multi-playlist support
        
        # Player Controller (Queue Based)
        self.player = PlayerController()
        self.player.setLibraryRef(self.library)  # Set library reference for recommendations
        self.player.setPlayMode("artist_based")  # Enable artist-based navigation

        # Attach app as observer to library
        self.library.attach_observer(self)

        # containers
        self.header = None
        self.main_container = None
        self.sidebar_frame = None
        self.content_frame = None
        self.bottom_player = None
        self.current_page = "home"  # Track current page for sidebar highlighting

        self.role = "login"
        
        # File watcher for cross-instance sync
        self.songs_file_path = Path("songs_store.json")
        self.last_file_mtime = None
        self.file_watcher_id = None
        
        # Countdown timer ID
        self.countdown_timer_id = None

        # load sample songs
        self.library.load_sample_if_empty()

        self.show_login()

    # Observer pattern callback for library changes
    def on_library_changed(self, action, data):
        """Called when library changes (add/update/delete song)."""
        # Save library
        self.library.save_if_supported()
        
        # Refresh current page if needed
        if self.role != "login" and hasattr(self, 'content_frame'):
            # Reload current page to reflect changes
            self.reload_current_page()

    def reload_current_page(self):
        """Reload the current page to reflect library changes."""
        if self.current_page:
            self.load_page(self.current_page)

    def clear_root(self):
        for w in self.winfo_children():
            w.destroy()

    def show_login(self):
        self.clear_root()
        # Stop file watcher
        if self.file_watcher_id:
            self.after_cancel(self.file_watcher_id)
            self.file_watcher_id = None
        # Stop countdown timer if running
        if self.countdown_timer_id:
            self.after_cancel(self.countdown_timer_id)
            self.countdown_timer_id = None
        self.role = "login"
        LoginPage(self, on_login=self._on_login, colors=COLORS).pack(fill="both", expand=True)

    def _on_login(self, role):
        if role not in ("user", "admin"): return
        self.role = role
        self.build_main_ui()

    def build_main_ui(self):
        self.clear_root()

        # 1. TOPBAR
        self.header = TopBar(self, logout_callback=self.on_logout, colors=COLORS,
                             on_search=self.on_topbar_search if self.role == "user" else None)
        self.header.pack(side="top", fill="x")

        # 2. MAIN CONTAINER
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.pack(side="top", fill="both", expand=True)

        # Set default page
        if self.role == "user":
            self.current_page = "home"
            self.current_playlist = None  # Track selected playlist
        else:
            self.current_page = "dashboard"

        # 3. SIDEBAR with active page highlighting
        if self.role == "user":
            self.sidebar_frame = SidebarUser(
                self.main_container,
                colors=COLORS,
                on_home=lambda: self.load_page("home"),
                on_create_playlist=lambda: self.load_page("create_playlist"),
                on_select_playlist=self.select_playlist,
                playlist_manager=self.playlist_manager,
                active_page=self.current_page
            )
        else: # admin
            self.sidebar_frame = SidebarAdmin(
                self.main_container,
                colors=COLORS,
                on_dashboard=lambda: self.load_page("dashboard"),
                on_songs=lambda: self.load_page("songs"),
                on_add=lambda: self.load_page("add"),
                on_import=lambda: self.load_page("import"),
                active_page=self.current_page
            )
        
        self.sidebar_frame.pack(side="left", fill="y")

        # 4. CONTENT FRAME
        self.content_frame = ctk.CTkFrame(self.main_container, fg_color=COLORS["bg_content"], corner_radius=15)
        self.content_frame.pack(side="right", fill="both", expand=True, padx=15, pady=15)

        # 5. BOTTOM PLAYER (User Only)
        if self.role == "user":
            self.bottom_player = BottomPlayer(
                self.content_frame, 
                colors=COLORS,
                prev_cb=self.on_prev,
                play_cb=self.on_play_pause,
                next_cb=self.on_next,
                shuffle_cb=self.on_shuffle,
                repeat_cb=self.on_repeat,
                playlist_manager=self.playlist_manager
            )
            self.bottom_player.pack(side="bottom", fill="x")
            
            # Start countdown timer
            self.start_countdown_timer()

        # Load default page
        self.load_page(self.current_page)
        
        # Start file watcher for cross-instance sync
        self.start_file_watcher()

    def load_page(self, page, **kwargs):
        # Update current page for sidebar highlighting
        self.current_page = page
        
        # Rebuild sidebar with updated active page
        if self.sidebar_frame:
            self.sidebar_frame.destroy()
            
            if self.role == "user":
                self.sidebar_frame = SidebarUser(
                    self.main_container,
                    colors=COLORS,
                    on_home=lambda: self.load_page("home"),
                    on_create_playlist=lambda: self.load_page("create_playlist"),
                    on_select_playlist=self.select_playlist,
                    playlist_manager=self.playlist_manager,
                    active_page=self.current_page
                )
            else:  # admin
                self.sidebar_frame = SidebarAdmin(
                    self.main_container,
                    colors=COLORS,
                    on_dashboard=lambda: self.load_page("dashboard"),
                    on_songs=lambda: self.load_page("songs"),
                    on_add=lambda: self.load_page("add"),
                    on_import=lambda: self.load_page("import"),
                    active_page=self.current_page
                )
            
            self.sidebar_frame.pack(side="left", fill="y")
            self.sidebar_frame.lift()
        
        # Clear content area (except player)
        for w in self.content_frame.winfo_children():
            if w != self.bottom_player:
                w.destroy()
        
        # Wrapper halaman
        page_area = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        page_area.pack(fill="both", expand=True, side="top")

        # USER PAGES
        if page == "home":
            render_home(page_area, self.library, colors=COLORS,
                        on_play_context=self.play_from_context)
        
        elif page == "search":
            # Get query from topbar search or use empty string
            search_query = getattr(self, 'search_query', '')
            render_search(page_area, self.library, colors=COLORS,
                          on_play_context=self.play_from_context,
                          on_add=self.add_to_playlist,
                          query=search_query)

        elif page == "playlist":
            render_playlist(page_area, self.library, self.playlist_manager, colors=COLORS,
                            on_play_context=self.play_from_context,
                            on_remove=self.remove_from_playlist,
                            on_rename=self.on_playlist_renamed,
                            on_delete=self.on_playlist_deleted)
        
        elif page == "create_playlist":
            def on_playlist_created(playlist_name):
                if playlist_name:  # If not cancelled
                    self.playlist_manager.setCurrentPlaylist(playlist_name)
                    # Select the new playlist - will refresh sidebar and show playlist page
                    self.select_playlist(playlist_name)
                else:
                    # User cancelled, go back to home
                    self.load_page("home")
            
            render_create_playlist(page_area, self.playlist_manager, colors=COLORS,
                                  on_success=on_playlist_created)

        # ADMIN PAGES
        elif page == "dashboard":
            render_dashboard(page_area, self.library, colors=COLORS)

        elif page == "songs":
            render_songs_list(page_area, self.library, colors=COLORS,
                on_edit=lambda sid: self.load_page("edit", song_id=sid),
                on_delete=lambda sid: self.load_page("delete", song_id=sid))
        
        elif page == "add":
             render_add_song(page_area, self.library, colors=COLORS, on_saved=lambda: self.load_page("songs"))
        
        elif page == "edit":
             render_edit_song(page_area, self.library, colors=COLORS, song_id=kwargs.get("song_id"), on_saved=lambda: self.load_page("songs"))
        
        elif page == "delete":
             render_delete_song(page_area, self.library, colors=COLORS, song_id=kwargs.get("song_id"), on_deleted=lambda: self.load_page("songs"))
        
        elif page == "import":
            render_import_csv(page_area, self.library, colors=COLORS, on_finished=lambda: self.load_page("songs"))

        self.refresh_bottom_player()

    def select_playlist(self, playlist_name):
        """Handle playlist selection from sidebar"""
        self.playlist_manager.setCurrentPlaylist(playlist_name)
        self.current_page = f"playlist_{playlist_name}"
        self.load_page("playlist")

    def on_topbar_search(self, query):
        """Handle search from topbar search bar"""
        self.search_query = query  # Store query to pass to search page
        self.load_page("search")

    # --- LOGIC PLAYER & PLAYLIST ---
    
    def play_from_context(self, song_list, start_index):
        self.player.set_queue(song_list, start_index)
        if self.player.current_song:
            self.player.startCountdown(self.player.current_song.duration)
        self.refresh_bottom_player()
        # Ensure timer shows 0:00 at start
        if self.role == "user" and self.bottom_player and self.player.current_song:
            self.bottom_player.update_timer(0, self.player.current_song.duration)

    def add_to_playlist(self, song_id):
        node = self.library.findNodeById(song_id)
        if not node: return
        
        # Get all playlists
        all_playlist_names = self.playlist_manager.getAllPlaylists()
        
        # Filter playlists that DON'T already have this song
        available_playlists = []
        for pl_name in all_playlist_names:
            playlist = self.playlist_manager.getPlaylist(pl_name)
            if playlist and not playlist.contains(node.song):
                available_playlists.append(pl_name)
        
        # Check if song already exists in ALL playlists
        if not available_playlists:
            messagebox.showwarning("Sudah Ada", "Lagu ini sudah ada di semua playlist!")
            return
        
        if len(available_playlists) == 1:
            # Only one available playlist, add directly
            if self.playlist_manager.addSongToPlaylist(available_playlists[0], node.song):
                messagebox.showinfo("Sukses", f"Lagu ditambahkan ke '{available_playlists[0]}'!")
            else:
                messagebox.showwarning("Info", "Gagal menambahkan lagu.")
        else:
            # Multiple available playlists, show selection dialog
            self.show_playlist_selection_dialog(node.song, available_playlists)

    def show_playlist_selection_dialog(self, song, playlists):
        """Show dialog to select which playlist to add song to."""
        from tkinter import Toplevel
        
        dialog = Toplevel(self)
        dialog.title("Pilih Playlist")
        dialog.geometry("400x500")
        dialog.transient(self)
        dialog.grab_set()
        
        # Configure for CTk style
        dialog.configure(bg=COLORS["bg_content"])
        
        # Header
        header_frame = ctk.CTkFrame(dialog, fg_color=COLORS["primary"])
        header_frame.pack(fill="x", padx=0, pady=0)
        
        ctk.CTkLabel(header_frame, text="Tambah ke Playlist", 
                    font=("Segoe UI", 18, "bold"), text_color="white").pack(pady=15)
        
        # Song info
        info_frame = ctk.CTkFrame(dialog, fg_color="white")
        info_frame.pack(fill="x", padx=20, pady=15)
        
        ctk.CTkLabel(info_frame, text=song.title, font=("Segoe UI", 14, "bold"), 
                    text_color="#333", wraplength=350).pack(pady=(10, 0), padx=10)
        ctk.CTkLabel(info_frame, text=song.artist, font=("Segoe UI", 12), 
                    text_color="gray").pack(pady=(0, 10), padx=10)
        
        # Playlist list
        ctk.CTkLabel(dialog, text="Pilih playlist:", font=("Segoe UI", 12, "bold"),
                    text_color=COLORS["text_head"]).pack(anchor="w", padx=20, pady=(10, 5))
        
        scroll_frame = ctk.CTkScrollableFrame(dialog, fg_color="transparent")
        scroll_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        def add_to_selected_playlist(playlist_name):
            if self.playlist_manager.addSongToPlaylist(playlist_name, song):
                messagebox.showinfo("Sukses", f"Lagu ditambahkan ke '{playlist_name}'!")
                dialog.destroy()
            else:
                messagebox.showwarning("Info", "Lagu sudah ada di playlist ini.")
        
        for pl_name in playlists:
            btn = ctk.CTkButton(
                scroll_frame,
                text=f"📚 {pl_name}",
                font=("Segoe UI", 13),
                fg_color="white",
                text_color=COLORS["text_head"],
                border_width=2,
                border_color=COLORS["primary"],
                hover_color=COLORS["bg_content"],
                height=45,
                anchor="w",
                command=lambda name=pl_name: add_to_selected_playlist(name)
            )
            btn.pack(fill="x", pady=3, padx=5)
        
        # Cancel button
        ctk.CTkButton(dialog, text="Batal", fg_color="gray", hover_color="#666",
                     command=dialog.destroy).pack(pady=15)
    
    def remove_from_playlist(self, song_id):
        if self.playlist_manager.removeSongFromPlaylist(self.playlist_manager.current_playlist_name, song_id):
            messagebox.showinfo("Dihapus", "Lagu dihapus dari playlist.")
            # Reload playlist page
            self.load_page("playlist")
    
    def on_playlist_renamed(self, new_name):
        """Handle playlist rename event."""
        # Update current playlist name
        self.playlist_manager.setCurrentPlaylist(new_name)
        # Update current_page to reflect new name
        self.current_page = f"playlist_{new_name}"
        # Reload playlist page with new name
        self.load_page("playlist")
    
    def on_playlist_deleted(self):
        """Handle playlist delete event."""
        # Navigate to the current playlist (which has been switched by deletePlaylist)
        current_pl_name = self.playlist_manager.current_playlist_name
        self.select_playlist(current_pl_name)

    def on_play_pause(self):
        if self.player.is_playing:
            self.player.pause()
        else:
            self.player.play()
        self.refresh_bottom_player()

    def on_next(self):
        result = self.player.next(force_advance=True)  # Manual next always advances
        if result and self.player.current_song:
            self.player.startCountdown(self.player.current_song.duration)
        self.refresh_bottom_player()

    def on_prev(self):
        result = self.player.prev()
        if result and self.player.current_song:
            self.player.startCountdown(self.player.current_song.duration)
        self.refresh_bottom_player()
    
    def auto_advance(self):
        """Auto-advance to next song (respects repeat one mode)."""
        result = self.player.next(force_advance=False)  # Respect repeat mode
        if result and self.player.current_song:
            self.player.startCountdown(self.player.current_song.duration)
        self.refresh_bottom_player()

    def refresh_bottom_player(self):
        if self.role != "user" or not self.bottom_player: return
        self.bottom_player.update_state(self.player.current_song, self.player.is_playing)
        self.bottom_player.update_shuffle_repeat(self.player.shuffle_enabled, self.player.repeat_mode)

    def start_countdown_timer(self):
        """Start the countdown timer loop."""
        self.update_countdown()

    def update_countdown(self):
        """Update countdown timer every second."""
        if self.role == "user" and self.bottom_player:
            if self.player.current_song:
                # Update elapsed time if playing
                if self.player.is_playing:
                    finished = self.player.updateCountdown(1)
                    
                    if finished:
                        # Song finished, pause briefly then auto-advance
                        self.player.pause()  # Pause first
                        self.bottom_player.update_state(self.player.current_song, False)
                        # Delay 2 seconds before next song for smooth transition
                        self.after(2000, self.auto_advance)  # Use auto_advance, not on_next
                
                # ALWAYS update display when song exists (playing or paused)
                elapsed = self.player.elapsed_time
                total = self.player.current_duration
                self.bottom_player.update_timer(elapsed, total)
            
            # Schedule next update
            self.countdown_timer_id = self.after(1000, self.update_countdown)

    def on_logout(self):
        if messagebox.askyesno("Logout", "Keluar aplikasi?"):
            self.show_login()
    
    def on_shuffle(self):
        """Toggle shuffle mode."""
        self.player.toggleShuffle()
        self.refresh_bottom_player()
    
    def on_repeat(self):
        """Toggle repeat mode."""
        self.player.toggleRepeat()
        self.refresh_bottom_player()
    
    def start_file_watcher(self):
        """Start watching songs_store.json for changes from other instances."""
        try:
            if self.songs_file_path.exists():
                self.last_file_mtime = self.songs_file_path.stat().st_mtime
        except:
            pass
        
        # Start periodic check
        self.check_file_changes()
    
    def check_file_changes(self):
        """Check if songs_store.json has been modified by another instance."""
        try:
            if self.songs_file_path.exists():
                current_mtime = self.songs_file_path.stat().st_mtime
                
                if self.last_file_mtime and current_mtime != self.last_file_mtime:
                    # File has been modified! Reload library
                    print("[File Watcher] Detected changes in songs_store.json - reloading...")
                    self.library._load_from_file()
                    
                    # Reload current page to show new data
                    if self.role != "login" and hasattr(self, 'current_page'):
                        self.reload_current_page()
                
                self.last_file_mtime = current_mtime
        except Exception as e:
            print(f"[File Watcher] Error: {e}")
        
        # Schedule next check (every 2 seconds)
        if self.role != "login":
            self.file_watcher_id = self.after(2000, self.check_file_changes)

if __name__ == "__main__":
    app = App()
    app.mainloop()