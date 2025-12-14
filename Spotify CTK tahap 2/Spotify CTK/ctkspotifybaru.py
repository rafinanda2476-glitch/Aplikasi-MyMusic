# ctkspotify_final.py
import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, filedialog
import csv
import random

# ============================================================
# Spotify CTk - Electric Blue Theme
# ============================================================
ctk.set_appearance_mode("Light")

# ===========================================
# DATA (Song + DLL Library)
# ===========================================
class Song:
    def __init__(self, sid, title, artist, genre, year):
        self.id = sid
        self.title = title
        self.artist = artist
        self.genre = genre
        self.year = year

class NodeDLL:
    def __init__(self, song):
        self.song = song
        self.prev = None
        self.next = None

class SongLibrary:
    def __init__(self):
        self.head = None
        self.tail = None
        self.auto_id = 1

    def addSong(self, title, artist, genre, year):
        song = Song(self.auto_id, title, artist, genre, year)
        self.auto_id += 1
        node = NodeDLL(song)

        if self.head is None:
            self.head = self.tail = node
        else:
            self.tail.next = node
            node.prev = self.tail
            self.tail = node
        return song

    def findNodeById(self, sid):
        cur = self.head
        while cur:
            if cur.song.id == sid:
                return cur
            cur = cur.next
        return None

    def updateSong(self, sid, t, a, g, y):
        n = self.findNodeById(sid)
        if not n:
            return False
        n.song.title = t
        n.song.artist = a
        n.song.genre = g
        n.song.year = y
        return True

    def deleteSong(self, sid):
        cur = self.head
        while cur:
            if cur.song.id == sid:

                if cur.prev:
                    cur.prev.next = cur.next
                else:
                    self.head = cur.next

                if cur.next:
                    cur.next.prev = cur.prev
                else:
                    self.tail = cur.prev

                self.reindex()
                return True
            cur = cur.next
        return False

    def reindex(self):
        cur = self.head
        idx = 1
        while cur:
            cur.song.id = idx
            idx += 1
            cur = cur.next
        self.auto_id = idx

    def getAllSongs(self):
        arr = []
        cur = self.head
        while cur:
            arr.append(cur.song)
            cur = cur.next
        return arr

library = SongLibrary()

# -------------------------
# Playlist (minimal needed)
# -------------------------
class PlaylistNode:
    def __init__(self, song):
        self.song = song
        self.prev = None
        self.next = None

class Playlist:
    def __init__(self, name="My Playlist"):
        self.name = name
        self.head = None
        self.tail = None
        self.current = None    # pointer to current playing node

    def contains(self, song_id):
        cur = self.head
        while cur:
            if cur.song.id == song_id:
                return True
            cur = cur.next
        return False

    def addSong(self, song):
        if self.contains(song.id):
            return False
        node = PlaylistNode(song)
        if not self.head:
            self.head = self.tail = node
            return True
        self.tail.next = node
        node.prev = self.tail
        self.tail = node
        return True

    def listSongs(self):
        arr = []
        cur = self.head
        while cur:
            arr.append(cur.song)
            cur = cur.next
        return arr

    def removeSong(self, sid):
        cur = self.head
        while cur:
            if cur.song.id == sid:
                # adjust current pointer if needed
                if self.current is cur:
                    # prefer next, else prev, else None
                    if cur.next:
                        self.current = cur.next
                    elif cur.prev:
                        self.current = cur.prev
                    else:
                        self.current = None

                if cur.prev:
                    cur.prev.next = cur.next
                else:
                    self.head = cur.next
                if cur.next:
                    cur.next.prev = cur.prev
                else:
                    self.tail = cur.prev

                return True
            cur = cur.next
        return False

    def clear(self):
        self.head = self.tail = self.current = None

playlist = Playlist()

# -------------------------
# Busy manager for safe_switch
# -------------------------
class BusyManager:
    def __init__(self):
        self.busy = False

    def start(self):
        self.busy = True

    def end(self):
        self.busy = False

# ============================================================
# MAIN APP — FULL (admin + user with sidebar + bottom player)
# ============================================================
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Aplikasi Musik")
        self.geometry("1000x720")

        # player state
        self.current_song = None   # Song instance
        self.is_playing = False

        # busy/form control
        self.busy = BusyManager()
        self.active_form_reset = None  # callable to reset/cleanup current form

        # UI containers (set later)
        self.content = None
        self.left_sidebar = None
        self.user_right = None
        self.bottom_player = None
        self.now_label = None

        # initial view
        self.show_login()

        # load sample if empty
        self._load_sample_songs_if_empty()

    # ---------------- helpers ----------------
    def safe_switch(self, target_page):
        """
        Use this to navigate between pages. If a form is active (busy),
        ask confirmation, optionally call active_form_reset(), then proceed.
        """
        if self.busy.busy:
            ok = messagebox.askokcancel("Konfirmasi", "Ada form aktif. Batalkan dan pindah halaman?")
            if not ok:
                return
            # try to cleanup active form (if provided)
            if hasattr(self, "active_form_reset") and callable(self.active_form_reset):
                try:
                    self.active_form_reset()
                except Exception:
                    pass
                self.active_form_reset = None
            self.busy.end()

        # execute target
        if callable(target_page):
            target_page()

    def _set_active_form(self, reset_callable=None):
        """
        Mark that a form is active (busy). Provide a reset_callable that will be called
        if user chooses to cancel form via safe_switch.
        """
        self.busy.start()
        self.active_form_reset = reset_callable

    def _clear_active_form(self):
        self.busy.end()
        self.active_form_reset = None

    def _load_sample_songs_if_empty(self):
        if not library.getAllSongs():
            library.addSong("Imagine", "John Lennon", "Rock", 1971)
            library.addSong("Billie Jean", "Michael Jackson", "Pop", 1982)
            library.addSong("Take Five", "Dave Brubeck", "Jazz", 1959)
            library.addSong("Lose Yourself", "Eminem", "Hip Hop", 2002)
            library.addSong("Back in Black", "AC/DC", "Rock", 1980)
            # add couple to playlist
            n1 = library.findNodeById(1)
            n2 = library.findNodeById(2)
            if n1: playlist.addSong(n1.song)
            if n2: playlist.addSong(n2.song)

    # --------------------------
    # UNIVERSAL CLEAR PAGE
    # --------------------------
    def clear(self):
        if self.content:
            self.content.destroy()
        self.content = ctk.CTkFrame(self, fg_color="#E8F1FF")
        self.content.pack(fill="both", expand=True)

    # ============================================================
    # LOGIN PAGE
    # ============================================================
    def show_login(self):
        self.clear()

        ctk.CTkLabel(
            self.content, text="Login Akun",
            font=("Segoe UI", 28, "bold"), text_color="#003B80"
        ).pack(pady=40)

        ctk.CTkLabel(self.content, text="Username", font=("Segoe UI", 12)).pack()
        self.in_user = ctk.CTkEntry(self.content, width=320)
        self.in_user.pack(pady=8)

        ctk.CTkLabel(self.content, text="Password", font=("Segoe UI", 12)).pack()
        self.in_pass = ctk.CTkEntry(self.content, width=320, show="*")
        self.in_pass.pack(pady=8)

        ctk.CTkButton(
            self.content, text="Login", width=220,
            fg_color="#007BFF", hover_color="#005DFF",
            command=self.login_action
        ).pack(pady=20)

        ctk.CTkLabel(self.content, text="(admin: admin@gmail.com / admin123  •  user: user@gmail.com / user123)",
                     text_color="#003B80", font=("Segoe UI", 10)).pack(pady=8)

    def login_action(self):
        u = self.in_user.get().strip()
        p = self.in_pass.get().strip()

        if u == "admin@gmail.com" and p == "admin123":
            # go to admin panel and open list by default (or change to admin_add_page if desired)
            self.safe_switch(self.show_admin)
        elif u == "user@gmail.com" and p == "user123":
            self.safe_switch(self.show_user)
        else:
            messagebox.showerror("Login Gagal", "Username/Password salah!")
        # note: keep admin_add_page call removed from here to avoid accidental navigation

    # ============================================================
    # ADMIN PAGES (unchanged)
    # ============================================================
    def show_admin(self):
        self.clear()

        # Title
        ctk.CTkLabel(self.content, text="Admin Panel", font=("Segoe UI", 26, "bold"),
                     text_color="#003B80").pack(pady=18)

        topbar = ctk.CTkFrame(self.content, fg_color="#DCEBFF")
        topbar.pack(fill="x", padx=20, pady=(0,10))

        def mkbtn(t, cmd, **kw):
            # wrap navigation commands with safe_switch
            return ctk.CTkButton(topbar, text=t, width=140, fg_color="#007BFF", hover_color="#005DFF",
                                 command=lambda: self.safe_switch(cmd), **kw)

        mkbtn("Tambah Lagu", self.admin_add_page).pack(side="left", padx=8, pady=8)
        mkbtn("Edit Lagu", self.admin_edit_page).pack(side="left", padx=8)
        mkbtn("Hapus Lagu", self.admin_delete_page).pack(side="left", padx=8)
        mkbtn("Daftar Lagu", self.admin_list_page).pack(side="left", padx=8)

        ctk.CTkButton(topbar, text="Import CSV", width=140, fg_color="#007BFF",
                      hover_color="#005DFF", command=lambda: self.safe_switch(self.show_admin_import_csv)).pack(side="left", padx=8)

        ctk.CTkButton(topbar, text="Logout", width=120, fg_color="#E8F1FF", text_color="#003B80",
                      hover_color="#BBD7FF", command=lambda: self.safe_switch(self.show_login)).pack(side="right", padx=8)

        self.admin_container = ctk.CTkFrame(self.content, fg_color="#F3F8FF")
        self.admin_container.pack(fill="both", expand=True, padx=20, pady=20)

        # show list by default for admin
        self.admin_list_page()

    # ... admin_add_page, admin_list_page, admin_delete_page, admin_edit_page, admin_edit_form,
    # show_admin_import_csv remain unchanged from earlier version (for brevity they are the same as before)
    # We'll reuse the admin implementations from the prior code block to keep admin features intact.

    def admin_add_page(self):
        for w in self.admin_container.winfo_children():
            w.destroy()

        ctk.CTkLabel(self.admin_container, text="Tambah Lagu Baru",
                     font=("Segoe UI", 20, "bold")).pack(pady=12)

        form = ctk.CTkFrame(self.admin_container, fg_color="#DCEBFF")
        form.pack(pady=10, padx=12, fill="x")

        labels = ["Judul", "Artist", "Genre", "Tahun"]
        entries = {}

        for i, lbl in enumerate(labels):
            ctk.CTkLabel(form, text=lbl).grid(row=i, column=0, pady=8, padx=8, sticky="w")
            if lbl == "Genre":
                entries[lbl] = ctk.CTkComboBox(form, values=["Pop", "Rock", "Jazz", "Hip Hop", "EDM"], width=300)
            else:
                entries[lbl] = ctk.CTkEntry(form, width=300)
            entries[lbl].grid(row=i, column=1, pady=8, padx=8)

        # mark this form active, provide reset function
        def reset_form():
            for e in entries.values():
                try:
                    e.delete(0, "end")
                except:
                    # combo box set to empty
                    try:
                        e.set("")
                    except:
                        pass

        def on_change(event):
            if not self.busy.busy:
                self._set_active_form(reset_form)

        for e in entries.values():
            try:
                e.bind("<KeyRelease>", on_change)
            except:
                pass

        def save():
            t = entries["Judul"].get().strip()
            a = entries["Artist"].get().strip()
            g = entries["Genre"].get().strip()
            y = entries["Tahun"].get().strip()

            if not t or not a or not y:
                messagebox.showerror("Error", "Isi semua kolom!")
                return

            try:
                y = int(y)
            except:
                messagebox.showerror("Error", "Tahun harus angka!")
                return

            library.addSong(t, a, g, y)
            messagebox.showinfo("OK", "Lagu ditambahkan!")

            # clear fields and finish form
            reset_form()
            self._clear_active_form()
            # refresh list view
            self.admin_list_page()

        ctk.CTkButton(self.admin_container, text="Tambah Lagu", fg_color="#007BFF", hover_color="#005DFF",
                      command=save).pack(pady=12)

    def admin_list_page(self):
        for w in self.admin_container.winfo_children():
            w.destroy()

        ctk.CTkLabel(self.admin_container, text="Daftar Semua Lagu",
                     font=("Segoe UI", 20, "bold")).pack(pady=12)

        box = ctk.CTkScrollableFrame(self.admin_container, fg_color="#DCEBFF")
        box.pack(fill="both", expand=True, padx=12, pady=8)

        for s in library.getAllSongs():
            row = ctk.CTkFrame(box, fg_color="#F3F8FF")
            row.pack(fill="x", pady=6, padx=8)

            ctk.CTkLabel(row, text=f"{s.id}. {s.title} - {s.artist} ({s.genre}, {s.year})",
                        text_color="#003B80").pack(side="left", pady=6, padx=8)

    def admin_delete_page(self):
        for w in self.admin_container.winfo_children():
            w.destroy()

        ctk.CTkLabel(self.admin_container, text="Hapus Lagu",
                     font=("Segoe UI", 20, "bold")).pack(pady=12)

        box = ctk.CTkScrollableFrame(self.admin_container, fg_color="#DCEBFF")
        box.pack(fill="both", expand=True, padx=12, pady=8)

        for s in library.getAllSongs():
            row = ctk.CTkFrame(box, fg_color="#F3F8FF")
            row.pack(fill="x", pady=6, padx=8)
            ctk.CTkLabel(row, text=f"{s.id}. {s.title}").pack(side="left", padx=8, pady=8)
            ctk.CTkButton(row, text="Hapus", width=90, fg_color="#007BFF",
                          command=lambda sid=s.id: self._admin_delete_confirm(sid)).pack(side="right", padx=8)

    def _admin_delete_confirm(self, sid):
        if not messagebox.askokcancel("Hapus", "Yakin hapus?"):
            return
        library.deleteSong(sid)
        messagebox.showinfo("OK", "Lagu dihapus.")
        self.admin_delete_page()

    def admin_edit_page(self):
        for w in self.admin_container.winfo_children():
            w.destroy()

        ctk.CTkLabel(self.admin_container, text="Edit Lagu",
                     font=("Segoe UI", 20, "bold")).pack(pady=12)

        box = ctk.CTkScrollableFrame(self.admin_container, fg_color="#DCEBFF")
        box.pack(fill="both", expand=True, padx=12, pady=8)

        for s in library.getAllSongs():
            row = ctk.CTkFrame(box, fg_color="#F3F8FF")
            row.pack(fill="x", pady=6, padx=8)
            ctk.CTkLabel(row, text=f"{s.id}. {s.title}").pack(side="left", padx=8, pady=8)
            ctk.CTkButton(row, text="Edit", width=90, fg_color="#007BFF",
                          command=lambda sid=s.id: self.safe_switch(lambda sid=sid: self.admin_edit_form(sid))).pack(side="right", padx=8)

    def admin_edit_form(self, sid):
        for w in self.admin_container.winfo_children():
            w.destroy()

        node = library.findNodeById(sid)
        if not node:
            messagebox.showerror("Error", "Lagu tidak ditemukan!")
            return

        s = node.song

        ctk.CTkLabel(self.admin_container, text=f"Edit Lagu {sid}",
                     font=("Segoe UI", 20, "bold")).pack(pady=12)

        form = ctk.CTkFrame(self.admin_container, fg_color="#DCEBFF")
        form.pack(pady=10, padx=12, fill="x")

        labels = ["Judul", "Artist", "Genre", "Tahun"]
        entries = {}

        initial = [s.title, s.artist, s.genre, s.year]

        for i, lbl in enumerate(labels):
            ctk.CTkLabel(form, text=lbl).grid(row=i, column=0, pady=8, padx=8, sticky="w")
            if lbl == "Genre":
                cb = ctk.CTkComboBox(form, values=["Pop", "Rock", "Jazz", "Hip Hop", "EDM"], width=300)
                cb.set(s.genre)
                entries[lbl] = cb
            else:
                e = ctk.CTkEntry(form, width=300)
                e.insert(0, str(initial[i]))
                entries[lbl] = e
            entries[lbl].grid(row=i, column=1, pady=8, padx=8)

        # mark as active form
        def reset_edit():
            for i, lbl in enumerate(labels):
                try:
                    if lbl == "Genre":
                        entries[lbl].set(str(initial[i]))
                    else:
                        entries[lbl].delete(0, "end")
                        entries[lbl].insert(0, str(initial[i]))
                except:
                    pass

        self._set_active_form(reset_edit)

        def save():
            t = entries["Judul"].get().strip()
            a = entries["Artist"].get().strip()
            g = entries["Genre"].get().strip()
            y = entries["Tahun"].get().strip()

            try:
                y = int(y)
            except:
                messagebox.showerror("Error", "Tahun salah!")
                return

            library.updateSong(sid, t, a, g, y)
            messagebox.showinfo("OK", "Berhasil diupdate!")
            # done editing
            self._clear_active_form()
            self.admin_edit_page()

        ctk.CTkButton(self.admin_container, text="Simpan Perubahan", fg_color="#007BFF",
                      hover_color="#005DFF", command=save).pack(pady=12)

    def show_admin_import_csv(self):
        for w in self.admin_container.winfo_children():
            w.destroy()

        ctk.CTkLabel(self.admin_container, text="Import Lagu dari CSV",
                     font=("Segoe UI", 20, "bold")).pack(pady=12)

        lbl = ctk.CTkLabel(self.admin_container, text="Belum ada file dipilih")
        lbl.pack(pady=4)

        preview = ctk.CTkScrollableFrame(self.admin_container, height=280, fg_color="#DCEBFF")
        preview.pack(fill="both", expand=True, padx=12, pady=8)

        self.csv_path = None

        # mark this import form active, allow reset that clears preview and path label
        def reset_import():
            self.csv_path = None
            lbl.configure(text="Belum ada file dipilih")
            for w in preview.winfo_children():
                w.destroy()

            if not self.busy.busy:
                self._set_active_form(reset_import)


        def browse():
            path = filedialog.askopenfilename(title="Pilih CSV", filetypes=[("CSV", "*.csv")])
            if not path:
                return
            self.csv_path = path
            lbl.configure(text=f"File: {path}")

            for w in preview.winfo_children():
                w.destroy()

            with open(path, "r", encoding="utf-8") as f:
                rd = csv.DictReader(f)
                for row in rd:
                    ctk.CTkLabel(preview, text=f"{row.get('title')} - {row.get('artist')}").pack(anchor="w", pady=3)

        def import_csv():
            if not self.csv_path:
                messagebox.showerror("Error", "Pilih file CSV!")
                return
            count = 0
            with open(self.csv_path, "r", encoding="utf-8") as f:
                rd = csv.DictReader(f)
                for row in rd:
                    try:
                        library.addSong(row.get("title", ""), row.get("artist", ""), row.get("genre", ""), int(row.get("year", "0")))
                        count += 1
                    except:
                        pass
            messagebox.showinfo("OK", f"Berhasil import {count} lagu!")
            # import finished - clear busy state and move to list
            self._clear_active_form()
            # navigate to list
            self.safe_switch(self.admin_list_page)

        btnf = ctk.CTkFrame(self.admin_container)
        btnf.pack(pady=8)
        ctk.CTkButton(btnf, text="Pilih CSV", command=browse, fg_color="#007BFF").pack(side="left", padx=6)
        ctk.CTkButton(btnf, text="Import", command=import_csv, fg_color="#007BFF").pack(side="left", padx=6)

    # ============================================================
    # USER PAGE (with Sidebar + Right Content + Bottom Player)
    # ============================================================
    def show_user(self):
        # set up main layout: header (with logout), left sidebar, right content, bottom player
        self.clear()

        # HEADER
        header = ctk.CTkFrame(self.content, fg_color="#DCEBFF")
        header.pack(fill="x", padx=12, pady=(12, 6))

        ctk.CTkLabel(header, text="User Panel", font=("Segoe UI", 22, "bold"),
                     text_color="#003B80").pack(side="left", padx=8)

        # Logout kept at top-right
        ctk.CTkButton(header, text="Logout", width=120, fg_color="#E8F1FF",
                      text_color="#003B80", hover_color="#BBD7FF",
                      command=lambda: self.safe_switch(self.show_login)).pack(side="right", padx=8)

        # MAIN WRAPPER (left sidebar + right area)
        main_wrapper = ctk.CTkFrame(self.content, fg_color="#EFF7FF")
        main_wrapper.pack(fill="both", expand=True, padx=12, pady=(6, 0))

        # LEFT SIDEBAR
        self.left_sidebar = ctk.CTkFrame(main_wrapper, width=220, fg_color="#003B80")
        self.left_sidebar.pack(side="left", fill="y", padx=(0,10), pady=8)

        ctk.CTkLabel(self.left_sidebar, text="Spotify", font=("Segoe UI", 20, "bold"),
                     text_color="white").pack(pady=(16,8))

        def menu_btn(title, cb):
            return ctk.CTkButton(self.left_sidebar, text=title, width=180, height=36,
                                 fg_color="#0059B2", hover_color="#0074E8",
                                 command=cb)

        menu_btn("🏠 Home", lambda: self.load_user_page("home")).pack(pady=6)
        menu_btn("🔍 Search", lambda: self.load_user_page("search")).pack(pady=6)
        menu_btn("📁 Playlist Saya", lambda: self.load_user_page("playlist")).pack(pady=6)

        # RIGHT CONTENT area (dynamic)
        self.user_right = ctk.CTkFrame(main_wrapper, fg_color="#F7FBFF")
        self.user_right.pack(side="left", fill="both", expand=True, pady=8)

        # BOTTOM PLAYER (Now Playing above controls) - placed outside main_wrapper so it's fixed at bottom
        self.bottom_player = ctk.CTkFrame(self.content, fg_color="#DCEBFF")
        self.bottom_player.pack(side="bottom", fill="x", padx=12, pady=(8,12))

        # Now Playing (on top of controls)
        self.now_label = ctk.CTkLabel(self.bottom_player, text="Now Playing: (Tidak ada)",
                                      text_color="#003B80", font=("Segoe UI", 12, "italic"))
        self.now_label.pack(anchor="w", padx=12, pady=(8,4))

        # Controls row
        ctrl_frame = ctk.CTkFrame(self.bottom_player, fg_color="#DCEBFF")
        ctrl_frame.pack(fill="x", padx=12, pady=(0,10))

        ctk.CTkButton(ctrl_frame, text="⏮ Prev", width=90, fg_color="#007BFF", hover_color="#005DFF",
                      command=self.prev_song).pack(side="left", padx=6)
        ctk.CTkButton(ctrl_frame, text="▶ Play", width=90, fg_color="#007BFF", hover_color="#005DFF",
                      command=lambda: self.play_song(self.current_song.id if self.current_song else None)).pack(side="left", padx=6)
        ctk.CTkButton(ctrl_frame, text="⏸ Pause", width=90, fg_color="#007BFF", hover_color="#005DFF",
                      command=self.pause_song).pack(side="left", padx=6)
        ctk.CTkButton(ctrl_frame, text="⏭ Next", width=90, fg_color="#007BFF", hover_color="#005DFF",
                      command=self.next_song).pack(side="left", padx=6)
        ctk.CTkButton(ctrl_frame, text="🔁 Repeat", width=90, fg_color="#007BFF", hover_color="#005DFF",
                      command=self.repeat_song).pack(side="left", padx=6)

        # By default, load Home page
        self.load_user_page("home")

    # ----------------------
    # PAGE ROUTER
    # ----------------------
    def load_user_page(self, page):
        """
        Router to render different pages in the right content area.
        pages: home, search, songs, playlist
        """
        # clear right area
        for w in self.user_right.winfo_children():
            w.destroy()

        if page == "home":
            self.render_home()
        elif page == "search":
            self.render_search_page()
        elif page == "playlist":
            self.load_playlist_page()
        else:
            self.render_home()

    # ----------------------
    # RENDER: HOME
    # ----------------------
    def render_home(self):
        # WELCOME BANNER
        banner = ctk.CTkFrame(self.user_right, fg_color="#DCEBFF")
        banner.pack(fill="x", padx=20, pady=16)
        ctk.CTkLabel(banner, text="Selamat Datang di Spotify!", font=("Segoe UI", 24, "bold"),
                     text_color="#003B80").pack(pady=14)
        ctk.CTkLabel(banner, text="Nikmati lagu favoritmu. Gunakan sidebar untuk navigasi.",
                     text_color="#003B80").pack(pady=(0,12))

        all_songs = library.getAllSongs()

        # RECENTLY ADDED
        ctk.CTkLabel(self.user_right, text="Recently Added", font=("Segoe UI", 18, "bold"),
                     text_color="#003B80").pack(anchor="w", padx=24, pady=(8,4))
        recent_frame = ctk.CTkFrame(self.user_right, fg_color="#F5F9FF")
        recent_frame.pack(fill="x", padx=24, pady=(0,8))

        last_five = all_songs[-5:] if len(all_songs) > 5 else all_songs
        if not last_five:
            ctk.CTkLabel(recent_frame, text="(Belum ada lagu)").pack(pady=8)
        else:
            for s in reversed(last_five):
                ctk.CTkLabel(recent_frame, text=f"- {s.title} — {s.artist}", text_color="#003B80",
                             font=("Segoe UI", 14)).pack(anchor="w", padx=10, pady=3)

        # TOP GENRES
        ctk.CTkLabel(self.user_right, text="Top Genres", font=("Segoe UI", 18, "bold"),
                     text_color="#003B80").pack(anchor="w", padx=24, pady=(12,4))
        genre_frame = ctk.CTkFrame(self.user_right, fg_color="#F5F9FF")
        genre_frame.pack(fill="x", padx=24, pady=(0,8))

        genre_count = {}
        for s in all_songs:
            genre_count[s.genre] = genre_count.get(s.genre, 0) + 1

        if not genre_count:
            ctk.CTkLabel(genre_frame, text="(Tidak ada genre)").pack(pady=8)
        else:
            for g, c in genre_count.items():
                ctk.CTkLabel(genre_frame, text=f"{g}: {c} lagu", text_color="#003B80",
                             font=("Segoe UI", 14)).pack(anchor="w", padx=10, pady=3)

        # RECOMMENDATION (random sample)
        ctk.CTkLabel(self.user_right, text="Rekomendasi Hari Ini", font=("Segoe UI", 18, "bold"),
                     text_color="#003B80").pack(anchor="w", padx=24, pady=(12,4))
        rec_frame = ctk.CTkFrame(self.user_right, fg_color="#F5F9FF")
        rec_frame.pack(fill="x", padx=24, pady=(0,8))

        if all_songs:
            sample = random.sample(all_songs, min(3, len(all_songs)))
            for s in sample:
                ctk.CTkLabel(rec_frame, text=f"- {s.title} — {s.artist}", text_color="#003B80",
                             font=("Segoe UI", 14)).pack(anchor="w", padx=10, pady=3)
        else:
            ctk.CTkLabel(rec_frame, text="(Tidak ada lagu)").pack(pady=8)

        # QUICK ACTIONS
        quick = ctk.CTkFrame(self.user_right, fg_color="#DCEBFF")
        quick.pack(fill="x", padx=20, pady=16)
        ctk.CTkLabel(quick, text="Quick Access", font=("Segoe UI", 16, "bold"),
                     text_color="#003B80").pack(pady=8)
        btn_frame = ctk.CTkFrame(quick, fg_color="#DCEBFF")
        btn_frame.pack()
        ctk.CTkButton(btn_frame, text="Daftar Lagu", width=150, fg_color="#007BFF",
                      hover_color="#005DFF", command=lambda: self.load_user_page("songs")).pack(side="left", padx=8, pady=8)
        ctk.CTkButton(btn_frame, text="Playlist", width=150, fg_color="#007BFF",
                      hover_color="#005DFF", command=lambda: self.load_user_page("playlist")).pack(side="left", padx=8, pady=8)
        ctk.CTkButton(btn_frame, text="Search", width=150, fg_color="#007BFF",
                      hover_color="#005DFF", command=lambda: self.load_user_page("search")).pack(side="left", padx=8, pady=8)

    # ----------------------
    # RENDER: SEARCH PAGE
    # ----------------------
    def render_search_page(self):
        # Build a search box and results area inside user_right
        sf = ctk.CTkFrame(self.user_right, fg_color="#F5F9FF")
        sf.pack(fill="x", padx=20, pady=16)

        ctk.CTkLabel(sf, text="Cari Judul:", text_color="#003B80").pack(side="left", padx=(8,6), pady=8)
        self.search_entry_right = ctk.CTkEntry(sf, width=420)
        self.search_entry_right.pack(side="left", padx=6, pady=8)
        ctk.CTkButton(sf, text="Cari", width=120, fg_color="#007BFF", hover_color="#005DFF",
                      command=self._do_search_right).pack(side="left", padx=6)

        # results container
        self.search_results_frame = ctk.CTkScrollableFrame(self.user_right, fg_color="#EAF3FF", height=360)
        self.search_results_frame.pack(fill="both", padx=20, pady=(8,12), expand=True)

        # show all by default
        self._do_search_right()

    def _do_search_right(self):
        q = self.search_entry_right.get().strip().lower()
        if not q:
            items = library.getAllSongs()
        else:
            items = [s for s in library.getAllSongs() if q in s.title.lower()]
        # render
        for w in self.search_results_frame.winfo_children():
            w.destroy()
        if not items:
            ctk.CTkLabel(self.search_results_frame, text="(Tidak ada lagu)", text_color="#003B80").pack(pady=10)
            return
        for s in items:
            row = ctk.CTkFrame(self.search_results_frame, fg_color="#FFFFFF")
            row.pack(fill="x", pady=6, padx=6)
            ctk.CTkLabel(row, text=f"{s.id}. {s.title} - {s.artist} ({s.genre}, {s.year})",
                         text_color="#003B80").pack(side="left", padx=10, pady=8)
            ctk.CTkButton(row, text="Tambah ke Playlist", width=160, fg_color="#007BFF", hover_color="#005DFF",
                          command=lambda sid=s.id: self.user_add_song_to_playlist(sid)).pack(side="right", padx=8)

    # ----------------------
    # RENDER: PLAYLIST PAGE
    # ----------------------
    def load_playlist_page(self):
        for w in self.user_right.winfo_children():
            w.destroy()

        ctk.CTkLabel(self.user_right, text="Playlist Saya", font=("Segoe UI", 20, "bold"),
                     text_color="#003B80").pack(pady=8)

        self.playlist_frame = ctk.CTkScrollableFrame(self.user_right, fg_color="#EAF3FF", height=420)
        self.playlist_frame.pack(fill="both", padx=12, pady=8, expand=True)

        # refresh view
        self._refresh_playlist_view()

    # -----------------------------------------------------------------
    # Render playlist area (separate function for easy refresh)
    # -----------------------------------------------------------------
    def _refresh_playlist_view(self):
        # ensure playlist_frame exists (called from several places)
        try:
            for w in self.playlist_frame.winfo_children():
                w.destroy()
        except Exception:
            # fallback: create playlist_frame if missing
            self.playlist_frame = ctk.CTkScrollableFrame(self.user_right, fg_color="#EAF3FF", height=420)
            self.playlist_frame.pack(fill="both", padx=12, pady=8, expand=True)

        songs = playlist.listSongs()
        if not songs:
            ctk.CTkLabel(self.playlist_frame, text="(Playlist Kosong)", text_color="#003B80").pack(pady=12)
            return

        for i, s in enumerate(songs, start=1):
            row = ctk.CTkFrame(self.playlist_frame, fg_color="#FFFFFF")
            row.pack(fill="x", pady=6, padx=6)

            ctk.CTkLabel(row, text=f"{i}. {s.title} - {s.artist} ({s.genre}, {s.year})",
                         text_color="#003B80").pack(side="left", padx=10, pady=8)

            ctk.CTkButton(row, text="Play", width=80, fg_color="#007BFF", hover_color="#005DFF",
                          command=lambda sid=s.id: self.play_song(sid)).pack(side="right", padx=6)
            ctk.CTkButton(row, text="Hapus", width=90, fg_color="#007BFF", hover_color="#005DFF",
                          command=lambda sid=s.id: self.user_remove_playlist(sid)).pack(side="right", padx=6)

    # =================================================================
    # Tambahkan Lagu ke Playlist (keputusan logika tetap)
    # =================================================================
    def user_add_song_to_playlist(self, sid):
        node = library.findNodeById(sid)
        if not node:
            messagebox.showerror("Error", "Lagu tidak ditemukan!")
            return

        ok = playlist.addSong(node.song)
        if ok:
            messagebox.showinfo("OK", "Lagu ditambahkan ke playlist!")
        else:
            messagebox.showwarning("Perhatian", "Lagu sudah ada di playlist!")

        # refresh playlist view (in same page if open)
        try:
            self._refresh_playlist_view()
        except:
            pass

    # =================================================================
    # Hapus Lagu dari Playlist
    # =================================================================
    def user_remove_playlist(self, sid):
        ok = playlist.removeSong(sid)
        if ok:
            messagebox.showinfo("OK", "Lagu dihapus dari playlist.")
        else:
            messagebox.showerror("Error", "Lagu tidak ditemukan!")

        self._refresh_playlist_view()

        if self.current_song and self.current_song.id == sid:
            # stop or set pointer
            if playlist.current:
                self.current_song = playlist.current.song
                self.is_playing = False
            else:
                self.current_song = None
                self.is_playing = False
            self.update_now_playing()

    # =================================================================
    # PLAYER CONTROLS (logic preserved)
    # =================================================================
    def play_song(self, sid):
        if sid is None:
            messagebox.showerror("Error", "Tidak ada lagu dipilih!")
            return

        # find node in playlist
        cur = playlist.head
        while cur:
            if cur.song.id == sid:
                playlist.current = cur
                self.current_song = cur.song
                self.is_playing = True
                # update label and UI
                self.update_now_playing()
                messagebox.showinfo("Play Lagu", f"Memutar lagu:\n{cur.song.title} - {cur.song.artist}")
                return
            cur = cur.next

        messagebox.showerror("Error", "Lagu tidak ditemukan di playlist!")

    def pause_song(self):
        if not self.current_song:
            return
        self.is_playing = False
        self.update_now_playing()
        messagebox.showinfo("Pause", f"Lagu dijeda: {self.current_song.title}")

    def next_song(self):
        if not playlist.current:
            messagebox.showinfo("Info", "Tidak ada lagu sedang diputar.")
            return
        if not playlist.current.next:
            messagebox.showinfo("Info", "Tidak ada lagu berikutnya.")
            return
        playlist.current = playlist.current.next
        self.current_song = playlist.current.song
        self.is_playing = True
        self.update_now_playing()
        messagebox.showinfo("Next", f"Memutar: {self.current_song.title}")

    def prev_song(self):
        if not playlist.current:
            messagebox.showinfo("Info", "Tidak ada lagu sedang diputar.")
            return
        if not playlist.current.prev:
            messagebox.showinfo("Info", "Tidak ada lagu sebelumnya.")
            return
        playlist.current = playlist.current.prev
        self.current_song = playlist.current.song
        self.is_playing = True
        self.update_now_playing()
        messagebox.showinfo("Prev", f"Memutar: {self.current_song.title}")

    def repeat_song(self):
        if not self.current_song:
            messagebox.showinfo("Info", "Tidak ada lagu untuk diulang.")
            return
        # simple repeat behavior: replay same song
        self.is_playing = True
        self.update_now_playing()
        messagebox.showinfo("Repeat", f"Mengulang: {self.current_song.title}")

    def update_now_playing(self):
        # ensure now_label exists (created in show_user)
        try:
            if self.current_song and self.is_playing:
                s = self.current_song
                self.now_label.configure(text=f"Now Playing: {s.title} - {s.artist}")
            elif self.current_song and not self.is_playing:
                s = self.current_song
                self.now_label.configure(text=f"Paused: {s.title}")
            else:
                self.now_label.configure(text="Now Playing: (Tidak ada)")
        except Exception:
            pass

    def _clear_playlist_confirm(self):
        if messagebox.askyesno("Konfirmasi", "Kosongkan playlist?"):
            playlist.clear()
            self._refresh_playlist_view()
            self.current_song = None
            self.is_playing = False
            self.update_now_playing()

# ============================================================
# RUN PROGRAM
# ============================================================
if __name__ == "__main__":
    App().mainloop()
