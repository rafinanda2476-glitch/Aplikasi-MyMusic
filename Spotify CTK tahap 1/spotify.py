# spotify_gui_final.py
import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox
import json
from typing import Optional, List

# -------------------------
# Data structures
# -------------------------
class Song:
    def __init__(self, song_id: int, title: str, artist: str, genre: str, year: int):
        self.id = song_id
        self.title = title
        self.artist = artist
        self.genre = genre
        self.year = year

class NodeDLL:
    def __init__(self, song: Song):
        self.song = song
        self.prev = None
        self.next = None

class SongLibrary:
    def __init__(self):
        self.head: Optional[NodeDLL] = None
        self.tail: Optional[NodeDLL] = None
        self.auto_id = 1

    def addSong(self, title: str, artist: str, genre: str, year: int) -> Song:
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

    def findNodeById(self, song_id: int) -> Optional[NodeDLL]:
        cur = self.head
        while cur:
            if cur.song.id == song_id:
                return cur
            cur = cur.next
        return None

    def updateSong(self, song_id: int, title: str, artist: str, genre: str, year: int) -> bool:
        node = self.findNodeById(song_id)
        if not node:
            return False
        node.song.title = title
        node.song.artist = artist
        node.song.genre = genre
        node.song.year = year
        return True

    def deleteSong(self, song_id: int):
        cur = self.head
        while cur:
            if cur.song.id == song_id:
                deleted = cur.song
                if cur.prev is None:
                    self.head = cur.next
                    if self.head:
                        self.head.prev = None
                    else:
                        self.tail = None
                elif cur.next is None:
                    self.tail = cur.prev
                    if self.tail:
                        self.tail.next = None
                    else:
                        self.head = None
                else:
                    cur.prev.next = cur.next
                    cur.next.prev = cur.prev
                self.reindexID()
                return deleted
            cur = cur.next
        return None

    def reindexID(self):
        cur = self.head
        nid = 1
        while cur:
            cur.song.id = nid
            nid += 1
            cur = cur.next
        self.auto_id = nid

    def getAllSongs(self) -> List[Song]:
        res = []
        cur = self.head
        while cur:
            res.append(cur.song)
            cur = cur.next
        return res

    def to_dict_list(self):
        return [
            {"id": s.id, "title": s.title, "artist": s.artist, "genre": s.genre, "year": s.year}
            for s in self.getAllSongs()
        ]

    def load_from_dict_list(self, items):
        # rebuild library sequentially (ignore stored ids)
        self.head = self.tail = None
        self.auto_id = 1
        for it in items:
            self.addSong(it.get("title",""), it.get("artist",""), it.get("genre",""), int(it.get("year",0)))

# -------------------------
# Playlist (unique)
# -------------------------
class PlaylistNode:
    def __init__(self, song: Song):
        self.song = song
        self.prev = None
        self.next = None

class Playlist:
    def __init__(self, name="My Playlist"):
        self.name = name
        self.head: Optional[PlaylistNode] = None
        self.tail: Optional[PlaylistNode] = None
        self.current: Optional[PlaylistNode] = None

    def contains(self, song_id: int) -> bool:
        cur = self.head
        while cur:
            if cur.song.id == song_id:
                return True
            cur = cur.next
        return False

    def addSong(self, song: Song) -> bool:
        if self.contains(song.id):
            return False
        node = PlaylistNode(song)
        if self.head is None:
            self.head = self.tail = node
            return True
        self.tail.next = node
        node.prev = self.tail
        self.tail = node
        return True

    def listSongs(self) -> List[Song]:
        res = []
        cur = self.head
        while cur:
            res.append(cur.song)
            cur = cur.next
        return res

    def removeSong(self, song_id: int) -> bool:
        cur = self.head
        while cur:
            if cur.song.id == song_id:
                if cur.prev:
                    cur.prev.next = cur.next
                else:
                    self.head = cur.next
                if cur.next:
                    cur.next.prev = cur.prev
                else:
                    self.tail = cur.prev
                if self.current == cur:
                    self.current = cur.next or cur.prev
                return True
            cur = cur.next
        return False

    def clear(self):
        self.head = self.tail = self.current = None

    def play(self, song_id: int) -> Optional[Song]:
        cur = self.head
        while cur:
            if cur.song.id == song_id:
                self.current = cur
                return cur.song
            cur = cur.next
        return None

    def play_first(self) -> Optional[Song]:
        if self.head:
            self.current = self.head
            return self.current.song
        return None

    def nextSong(self) -> Optional[Song]:
        if self.current and self.current.next:
            self.current = self.current.next
            return self.current.song
        return None

    def prevSong(self) -> Optional[Song]:
        if self.current and self.current.prev:
            self.current = self.current.prev
            return self.current.song
        return None

    def to_dict(self):
        return {"songs": [s.id for s in self.listSongs()]}

    def reassign_songs_after_reindex(self):
        # match by title+artist+genre+year and update references
        cur = self.head
        while cur:
            old = cur.song
            lib_cur = library.head
            while lib_cur:
                snew = lib_cur.song
                if (snew.title == old.title and snew.artist == old.artist and
                    snew.genre == old.genre and snew.year == old.year):
                    cur.song = snew
                    break
                lib_cur = lib_cur.next
            cur = cur.next

# -------------------------
# Globals & helpers
# -------------------------
ALLOWED_GENRES = [
    "Jazz","Blues","Gospel","RnB","Funk","Rock","Metal",
    "Electronic","Reggae","Hip Hop","Techno","Pop","Dangdut"
]
library = SongLibrary()
default_playlist = Playlist()

# -------------------------
# Theme manager
# -------------------------
class ThemeManager:
    def __init__(self):
        self.dark = False
        self.bg = "#ffffff"
        self.fg = "#000000"
    def toggle(self):
        self.dark = not self.dark
    def apply(self, root):
        self.bg = "#1e1e1e" if self.dark else "#ffffff"
        self.fg = "#f0f0f0" if self.dark else "#000000"
        try:
            root.configure(bg=self.bg)
        except:
            pass
        def apply_rec(w):
            try:
                if isinstance(w, Frame):
                    w.configure(bg=self.bg)
                elif isinstance(w, Label):
                    w.configure(bg=self.bg, fg=self.fg)
                elif isinstance(w, Button):
                    w.configure(bg=("#333333" if self.dark else "#e0e0e0"), fg=self.fg,
                                activebackground=("#444444" if self.dark else "#d0d0d0"))
                elif isinstance(w, Listbox):
                    w.configure(bg=("#2b2b2b" if self.dark else "#ffffff"), fg=self.fg,
                                selectbackground=("#444444" if self.dark else "#c0c0ff"))
                elif isinstance(w, Entry):
                    w.configure(bg=("#2d2d2d" if self.dark else "white"), fg=self.fg,
                                insertbackground=self.fg)
                elif isinstance(w, Canvas):
                    w.configure(bg=self.bg)
                elif isinstance(w, ttk.Combobox):
                    try:
                        style = ttk.Style()
                        style.theme_use('default')
                        if self.dark:
                            style.configure('TCombobox', fieldbackground='#2d2d2d', foreground=self.fg)
                        else:
                            style.configure('TCombobox', fieldbackground='white', foreground=self.fg)
                    except:
                        pass
            except:
                pass
            for ch in w.winfo_children():
                apply_rec(ch)
        apply_rec(root)

# -------------------------
# Busy manager
# -------------------------
class BusyManager:
    def __init__(self):
        self.busy = False
        self.armed = False   # form terbuka, tapi belum dianggap busy

    def arm(self):
        """Dipanggil saat form dibuka."""
        self.armed = True
        self.busy = False

    def engage(self):
        """Dipanggil saat user mulai mengetik → busy = True."""
        if self.armed:
            self.busy = True

    def end(self):
        """Reset."""
        self.busy = False
        self.armed = False

# -------------------------
# Application
# -------------------------
class App:
    def __init__(self, root):
        self.root = root
        self.theme = ThemeManager()
        self.busy = BusyManager()
        self.is_playing = False
        self.current_playing_song: Optional[Song] = None

        self.root.title("Spotify GUI with Playlist UNIK")
        self.root.geometry("960x700")

        # Header: title left, controls right
        self.header = Frame(self.root, bd=0, relief=FLAT)
        self.header.pack(fill=X, side=TOP)

        self.title_label = Label(self.header, text="Spotify GUI", font=("Arial", 20, "bold"))
        self.title_label.pack(side=LEFT, padx=12, pady=8)

        # right controls container inside header
        self.header_right = Frame(self.header)
        self.header_right.pack(side=RIGHT, padx=8, pady=6)

        # back button (will be enabled when in sub-pages)
        self.back_button = Button(self.header_right, text="Kembali", command=lambda: self.safe_switch(self.show_role_selection))
        # theme toggle area - we'll draw a small canvas + fallback button
        self.theme_canvas = Canvas(self.header_right, width=40, height=20, highlightthickness=0)
        self.theme_canvas.pack(side=RIGHT, padx=(0,4))

        # main container under header
        self.container = Frame(self.root)
        self.container.pack(fill=BOTH, expand=True, padx=8, pady=(0,8))

        # place for dynamic content
        self.content = None
        self.active_form_reset = None

        # attach theme draw
        self.draw_theme_switch()

        # menu
        menubar = Menu(self.root)
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Save Library", command=self.save_library)
        filemenu.add_command(label="Load Library", command=self.load_library)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="File", menu=filemenu)
        self.root.config(menu=menubar)

        # initial page
        self.show_role_selection()
        self.theme.apply(self.root)

    # safe_switch (handles busy)
    def safe_switch(self, target_page):
        if self.busy.busy:
            ok = messagebox.askokcancel("Konfirmasi", "Ada form aktif. Batalkan dan pindah?")
            if not ok:
                return
            if hasattr(self, "active_form_reset") and callable(self.active_form_reset):
                try:
                    self.active_form_reset()
                except:
                    pass
                self.active_form_reset = None
            self.busy.end()
        if callable(target_page):
            target_page()
        self.theme.apply(self.root)

    def clear_container(self):
        for w in self.container.winfo_children():
            w.destroy()

    # Role selection
    def show_role_selection(self):
        self.clear_container()
        frame = Frame(self.container)
        frame.pack(expand=True, fill=BOTH)

        Label(frame, text="Pilih Peran", font=("Arial", 20, "bold")).pack(pady=20)
        Button(frame, text="Admin", width=20, height=2, command=self.enter_admin).pack(pady=8)
        Button(frame, text="User", width=20, height=2, command=self.enter_user).pack(pady=8)

    def enter_admin(self):
        self.safe_switch(self.show_admin_main)

    def enter_user(self):
        self.safe_switch(self.show_user_main)

    # ---------------- Admin ----------------
    def show_admin_main(self):
        self.clear_container()
        # show back button only in subpages (enable)
        self.back_button.config(state=NORMAL)

        topbar = Frame(self.container)
        topbar.pack(fill=X, pady=6)
        Button(topbar, text="Tambah Lagu", command=lambda: self.safe_switch(self.show_admin_add)).pack(side=LEFT, padx=6)
        Button(topbar, text="Hapus Lagu", command=lambda: self.safe_switch(self.show_admin_delete)).pack(side=LEFT, padx=6)
        Button(topbar, text="Lihat Semua Lagu", command=lambda: self.safe_switch(self.show_admin_list)).pack(side=LEFT, padx=6)
        Button(topbar, text="Edit Lagu", command=lambda: self.safe_switch(self.show_admin_edit_tab)).pack(side=LEFT, padx=6)
        Button(topbar, text="Kembali", command=lambda: self.safe_switch(self.show_role_selection)).pack(side=RIGHT, padx=6)

        self.content = Frame(self.container, bd=1, relief=SOLID, padx=12, pady=12)
        self.content.pack(fill=BOTH, expand=True, padx=10, pady=(0,10))
        self.show_admin_add()

    def show_admin_add(self):
        for w in self.content.winfo_children(): w.destroy()
        Label(self.content, text="Form Tambah Lagu", font=("Arial", 14, "bold")).pack(anchor=W, pady=6)
        form = Frame(self.content); form.pack(anchor=W, pady=6)
        Label(form, text="Judul:").grid(row=0, column=0, sticky=W, pady=3)
        title_entry = Entry(form, width=60); title_entry.grid(row=0, column=1, pady=3)
        Label(form, text="Penyanyi:").grid(row=1, column=0, sticky=W, pady=3)
        artist_entry = Entry(form, width=60); artist_entry.grid(row=1, column=1, pady=3)
        Label(form, text="Genre:").grid(row=2, column=0, sticky=W, pady=3)
        genre_combo = ttk.Combobox(form, values=ALLOWED_GENRES, state="readonly", width=30); genre_combo.grid(row=2, column=1, sticky=W, pady=3)
        genre_combo.set(ALLOWED_GENRES[0])
        Label(form, text="Tahun:").grid(row=3, column=0, sticky=W, pady=3)
        year_entry = Entry(form, width=20); year_entry.grid(row=3, column=1, sticky=W, pady=3)

        self.busy.arm()

        title_entry.bind("<Key>", lambda e: self.busy.engage())
        artist_entry.bind("<Key>", lambda e: self.busy.engage())
        year_entry.bind("<Key>", lambda e: self.busy.engage())
        genre_combo.bind("<<ComboboxSelected>>", lambda e: self.busy.engage())

        def reset_add():
            try:
                title_entry.delete(0, END); artist_entry.delete(0, END); year_entry.delete(0, END); genre_combo.set(ALLOWED_GENRES[0])
            except:
                pass
        self.active_form_reset = reset_add

        def submit_add():
            title = title_entry.get().strip(); artist = artist_entry.get().strip(); genre = genre_combo.get().strip(); year_text = year_entry.get().strip()
            if not title or not artist or not genre or not year_text:
                messagebox.showerror("Error", "Semua field harus diisi!", parent=self.root); return
            try:
                year = int(year_text)
            except:
                messagebox.showerror("Error", "Tahun harus angka!", parent=self.root); return
            library.addSong(title, artist, genre, year)
            reset_add()
            self.active_form_reset = None
            self.busy.end()
            messagebox.showinfo("Berhasil", "Lagu berhasil ditambahkan!", parent=self.root)

        Button(self.content, text="Tambah Lagu", command=submit_add).pack(anchor=W, pady=8)
        self.theme.apply(self.root)

    def show_admin_delete(self):
        for w in self.content.winfo_children(): w.destroy()
        Label(self.content, text="Form Hapus Lagu (berdasarkan ID)", font=("Arial", 14, "bold")).pack(anchor=W, pady=6)
        frame = Frame(self.content); frame.pack(anchor=W, pady=6)
        Label(frame, text="ID Lagu:").grid(row=0, column=0, sticky=W)
        id_entry = Entry(frame, width=20); id_entry.grid(row=0, column=1, sticky=W, padx=6)

        self.busy.arm()

        id_entry.bind("<Key>", lambda e: self.busy.engage())

        def reset_del():
            try:
                id_entry.delete(0, END)
            except:
                pass
        self.active_form_reset = reset_del

        def submit_delete():
            val = id_entry.get().strip()
            try:
                song_id = int(val)
            except:
                messagebox.showerror("Error", "ID harus angka!", parent=self.root); id_entry.delete(0, END); id_entry.focus_set(); return
            deleted_song = library.deleteSong(song_id)
            id_entry.delete(0, END)
            id_entry.focus_set()
            if deleted_song:
                # remove from playlist by comparing metadata if needed, but remove by id first
                default_playlist.removeSong(deleted_song.id)
                default_playlist.reassign_songs_after_reindex()
            self.active_form_reset = None
            self.busy.end()
            if deleted_song:
                messagebox.showinfo("Berhasil", "Lagu berhasil dihapus!", parent=self.root)
            else:
                messagebox.showerror("Gagal", "ID tidak ditemukan!", parent=self.root)

        Button(self.content, text="Hapus Lagu", command=submit_delete).pack(anchor=W, pady=8)
        self.theme.apply(self.root)

    def show_admin_list(self):
        for w in self.content.winfo_children(): w.destroy()
        Label(self.content, text="Daftar Lagu", font=("Arial", 14, "bold")).pack(anchor=W, pady=6)
        list_frame = Frame(self.content); list_frame.pack(fill=BOTH, expand=True)
        scrollbar = Scrollbar(list_frame); scrollbar.pack(side=RIGHT, fill=Y)
        listbox = Listbox(list_frame, width=110, height=20, yscrollcommand=scrollbar.set)
        listbox.pack(side=LEFT, fill=BOTH, expand=True); scrollbar.config(command=listbox.yview)
        def refresh_list():
            listbox.delete(0, END)
            songs = library.getAllSongs()
            if not songs:
                messagebox.showwarning("Kosong", "Belum ada lagu dalam database.", parent=self.root); return
            for s in songs:
                listbox.insert(END, f"{s.id}. {s.title} - {s.artist} ({s.genre}, {s.year})")
        def on_double_click(event):
            sel = listbox.curselection()
            if not sel: return
            idx = sel[0]; item_text = listbox.get(idx)
            try:
                song_id = int(item_text.split('.')[0])
            except:
                return
            self.safe_switch(lambda: self.show_edit_form(song_id))
        listbox.bind("<Double-Button-1>", on_double_click)
        refresh_list()
        btn_frame = Frame(self.content); btn_frame.pack(anchor=W, pady=6)
        Button(btn_frame, text="Refresh", command=refresh_list).pack(side=LEFT, padx=4)
        Button(btn_frame, text="Back", command=lambda: self.safe_switch(self.show_admin_main)).pack(side=LEFT, padx=4)
        self.theme.apply(self.root)

    def show_admin_edit_tab(self):
        for w in self.content.winfo_children(): w.destroy()
        Label(self.content, text="Edit Lagu", font=("Arial", 14, "bold")).pack(anchor=W, pady=6)
        Label(self.content, text="Untuk mengedit lagu, buka 'Lihat Semua Lagu' lalu double-click lagu, atau masukkan ID di bawah.", fg="gray").pack(anchor=W, pady=6)
        frame = Frame(self.content); frame.pack(anchor=W, pady=6)
        Label(frame, text="Masukkan ID untuk edit:").grid(row=0, column=0, sticky=W)
        id_entry = Entry(frame, width=20); id_entry.grid(row=0, column=1, padx=6)
        def open_by_id():
            val = id_entry.get().strip()
            try:
                sid = int(val)
            except:
                messagebox.showerror("Error", "ID harus angka!", parent=self.root); return
            node = library.findNodeById(sid)
            if not node:
                messagebox.showerror("Gagal", "ID tidak ditemukan!", parent=self.root); return
            self.safe_switch(lambda: self.show_edit_form(sid))
        Button(self.content, text="Buka Edit", command=open_by_id).pack(anchor=W, pady=8)
        self.theme.apply(self.root)

    def show_edit_form(self, song_id):
        node = library.findNodeById(song_id)
        if not node:
            messagebox.showerror("Gagal", "ID tidak ditemukan!", parent=self.root); return
        for w in self.content.winfo_children(): w.destroy()
        Label(self.content, text=f"Edit Lagu ID {song_id}", font=("Arial", 14, "bold")).pack(anchor=W, pady=6)
        form = Frame(self.content); form.pack(anchor=W, pady=6)
        Label(form, text="Judul:").grid(row=0, column=0, sticky=W, pady=3)
        title_entry = Entry(form, width=60); title_entry.grid(row=0, column=1, pady=3); title_entry.insert(0, node.song.title)
        Label(form, text="Penyanyi:").grid(row=1, column=0, sticky=W, pady=3)
        artist_entry = Entry(form, width=60); artist_entry.grid(row=1, column=1, pady=3); artist_entry.insert(0, node.song.artist)
        Label(form, text="Genre:").grid(row=2, column=0, sticky=W, pady=3)
        genre_combo = ttk.Combobox(form, values=ALLOWED_GENRES, state="readonly", width=30); genre_combo.grid(row=2, column=1, sticky=W, pady=3)
        genre_combo.set(node.song.genre if node.song.genre in ALLOWED_GENRES else ALLOWED_GENRES[0])
        Label(form, text="Tahun:").grid(row=3, column=0, sticky=W, pady=3)
        year_entry = Entry(form, width=20); year_entry.grid(row=3, column=1, sticky=W, pady=3); year_entry.insert(0, str(node.song.year))
        self.busy.arm()

        title_entry.bind("<Key>", lambda e: self.busy.engage())
        artist_entry.bind("<Key>", lambda e: self.busy.engage())
        year_entry.bind("<Key>", lambda e: self.busy.engage())
        genre_combo.bind("<<ComboboxSelected>>", lambda e: self.busy.engage())

        def reset_edit():
            try:
                title_entry.delete(0, END); artist_entry.delete(0, END); year_entry.delete(0, END); genre_combo.set(ALLOWED_GENRES[0])
            except:
                pass
        self.active_form_reset = reset_edit
        def submit_edit():
            title = title_entry.get().strip(); artist = artist_entry.get().strip(); genre = genre_combo.get().strip(); year_text = year_entry.get().strip()
            if not title or not artist or not genre or not year_text:
                messagebox.showerror("Error", "Semua field harus diisi!", parent=self.root); return
            try:
                year = int(year_text)
            except:
                messagebox.showerror("Tahun Salah", "Tahun harus angka!", parent=self.root); return
            ok = library.updateSong(song_id, title, artist, genre, year)
            if ok:
                messagebox.showinfo("Berhasil", "Perubahan lagu disimpan.", parent=self.root)
                self.active_form_reset = None
                self.busy.end()
                # ensure playlist references (title/artist/year) still valid - playlist stores object reference so no update needed unless reindex
                self.show_admin_list()
            else:
                messagebox.showerror("Gagal", "Gagal menyimpan perubahan.", parent=self.root)
        Button(self.content, text="Simpan Perubahan", command=submit_edit).pack(anchor=W, pady=8)
        def cancel_edit():
            if hasattr(self, "active_form_reset") and callable(self.active_form_reset):
                try: self.active_form_reset()
                except: pass
            self.active_form_reset = None
            self.busy.end()
            self.show_admin_list()
        Button(self.content, text="Batal", command=cancel_edit).pack(anchor=W, pady=4)
        self.theme.apply(self.root)

    # ---------------- User ----------------
    def show_user_main(self):
        self.clear_container()
        # show back button
        self.back_button.config(state=NORMAL)
        topbar = Frame(self.container); topbar.pack(fill=X, pady=6)
        Label(topbar, text="User Panel", font=("Arial", 12, "bold")).pack(side=LEFT, padx=6)
        Button(topbar, text="Kembali", command=lambda: self.safe_switch(self.show_role_selection)).pack(side=RIGHT, padx=6)
        self.content = Frame(self.container, bd=1, relief=SOLID, padx=12, pady=12)
        self.content.pack(fill=BOTH, expand=True, padx=10, pady=(0,10))

        # Search panel
        Label(self.content, text="Cari Lagu (berdasarkan Judul)", font=("Arial", 12)).pack(anchor=W, pady=6)
        search_frame = Frame(self.content); search_frame.pack(fill=X, anchor=W, pady=4)
        Label(search_frame, text="Judul:").grid(row=0, column=0, sticky=W)
        q_entry = Entry(search_frame, width=40); q_entry.grid(row=0, column=1, padx=6)
        res_frame = Frame(self.content); res_frame.pack(fill=X, pady=6)
        res_scroll = Scrollbar(res_frame); res_scroll.pack(side=RIGHT, fill=Y)
        result_box = Listbox(res_frame, width=110, height=8, yscrollcommand=res_scroll.set)
        result_box.pack(side=LEFT, fill=X, expand=True); res_scroll.config(command=result_box.yview)

        def do_search():
            q = q_entry.get().strip().lower()
            result_box.delete(0, END)
            if not q:
                messagebox.showerror("Error", "Masukkan judul untuk mencari.", parent=self.root); return
            found = False
            for s in library.getAllSongs():
                if q in s.title.lower():
                    result_box.insert(END, f"{s.id}. {s.title} - {s.artist} ({s.genre}, {s.year})")
                    found = True
            # reset entry after search
            q_entry.delete(0, END)
            if not found:
                messagebox.showinfo("Tidak ditemukan", "Tidak ada lagu yang cocok.", parent=self.root)

        def add_selected_to_playlist():
            sel = result_box.curselection()
            if not sel:
                messagebox.showerror("Error", "Pilih hasil pencarian untuk ditambahkan.", parent=self.root); return
            sid = int(result_box.get(sel[0]).split('.')[0])
            node = library.findNodeById(sid)
            if not node:
                messagebox.showerror("Error", "Lagu tidak ditemukan di library.", parent=self.root); return
            added = default_playlist.addSong(node.song)
            if not added:
                messagebox.showwarning("Duplikat", "Lagu sudah ada di playlist (unik).", parent=self.root)
            else:
                messagebox.showinfo("Berhasil", "Lagu ditambahkan ke playlist.", parent=self.root)
            # reset entry + results after add
            q_entry.delete(0, END)
            result_box.delete(0, END)
            refresh_playlist_box()

        Button(search_frame, text="Cari", command=do_search).grid(row=0, column=2, padx=6)
        Button(search_frame, text="Tambah ke Playlist", command=add_selected_to_playlist).grid(row=0, column=3, padx=6)
        Button(search_frame, text="Clear Hasil", command=lambda: result_box.delete(0, END)).grid(row=0, column=4, padx=6)

        # Playlist panel (below search)
        Label(self.content, text="Playlist Saya (UNIK)", font=("Arial", 12)).pack(anchor=W, pady=(12,6))
        pl_frame = Frame(self.content); pl_frame.pack(fill=BOTH, expand=True)
        pl_scroll = Scrollbar(pl_frame); pl_scroll.pack(side=RIGHT, fill=Y)
        playlist_box = Listbox(pl_frame, width=110, height=10, yscrollcommand=pl_scroll.set)
        playlist_box.pack(side=LEFT, fill=BOTH, expand=True); pl_scroll.config(command=playlist_box.yview)

        def refresh_playlist_box():
            playlist_box.delete(0, END)
            songs = default_playlist.listSongs()
            if not songs:
                playlist_box.insert(END, "(Playlist kosong)")
                return
            # display sequence number in playlist (1., 2., 3.) per your request
            for idx, s in enumerate(songs, start=1):
                playlist_box.insert(END, f"{idx}. {s.title} - {s.artist} ({s.genre}, {s.year})")

        def play_selected_from_playlist():
            sel = playlist_box.curselection()
            if not sel:
                messagebox.showerror("Error", "Pilih lagu di playlist untuk diputar.", parent=self.root); return
            text = playlist_box.get(sel[0])
            if text.startswith("("):
                messagebox.showerror("Error", "Playlist kosong.", parent=self.root); return
            # Need to map playlist index back to song object
            idx = int(text.split('.')[0])  # 1-based index in playlist display
            songs = default_playlist.listSongs()
            if idx <= 0 or idx > len(songs):
                messagebox.showerror("Error", "Index playlist tidak valid.", parent=self.root); return
            song = songs[idx-1]
            # set playlist current pointer properly
            # find node in playlist whose song object matches
            cur = default_playlist.head
            while cur:
                if cur.song is song:
                    default_playlist.current = cur
                    break
                cur = cur.next
            self.current_playing_song = song
            self.is_playing = True
            messagebox.showinfo("Play", f"Memutar: {song.title} - {song.artist}", parent=self.root)

        def pause_selected():
            if not self.current_playing_song:
                messagebox.showerror("Error", "Tidak ada lagu yang sedang diputar.", parent=self.root); return
            if not self.is_playing:
                messagebox.showinfo("Info", "Lagu sudah di-pause.", parent=self.root); return
            self.is_playing = False
            messagebox.showinfo("Pause", f"Pause: {self.current_playing_song.title}", parent=self.root)

        def remove_selected_from_playlist():
            sel = playlist_box.curselection()
            if not sel:
                messagebox.showerror("Error", "Pilih lagu di playlist untuk dihapus.", parent=self.root); return
            text = playlist_box.get(sel[0])
            if text.startswith("("):
                messagebox.showerror("Error", "Playlist kosong.", parent=self.root); return
            idx = int(text.split('.')[0])
            songs = default_playlist.listSongs()
            if idx <= 0 or idx > len(songs):
                messagebox.showerror("Error", "Index tidak valid.", parent=self.root); return
            target_song = songs[idx-1]
            # remove by matching title+artist+genre+year or by object identity if possible
            removed = default_playlist.removeSong(target_song.id)
            if removed:
                messagebox.showinfo("Berhasil", "Lagu dihapus dari playlist.", parent=self.root)
                refresh_playlist_box()
            else:
                # fallback: try matching by metadata (if id changed)
                # iterate nodes to find matching metadata
                cur = default_playlist.head
                found = False
                while cur:
                    if (cur.song.title == target_song.title and cur.song.artist == target_song.artist and
                        cur.song.genre == target_song.genre and cur.song.year == target_song.year):
                        # remove this song using id
                        default_playlist.removeSong(cur.song.id)
                        found = True
                        break
                    cur = cur.next
                if found:
                    messagebox.showinfo("Berhasil", "Lagu dihapus dari playlist.", parent=self.root)
                    refresh_playlist_box()
                else:
                    messagebox.showerror("Gagal", "Gagal menghapus lagu dari playlist.", parent=self.root)

        def clear_playlist():
            if messagebox.askyesno("Konfirmasi", "Kosongkan playlist?"):
                default_playlist.clear()
                refresh_playlist_box()

        def prev_in_playlist():
            prv = default_playlist.prevSong()
            if prv:
                self.current_playing_song = prv
                self.is_playing = True
                messagebox.showinfo("Prev", f"Memutar: {prv.title} - {prv.artist}", parent=self.root)
                refresh_playlist_box()
            else:
                messagebox.showinfo("Info", "Tidak ada lagu sebelumnya.", parent=self.root)

        def next_in_playlist():
            nxt = default_playlist.nextSong()
            if nxt:
                self.current_playing_song = nxt
                self.is_playing = True
                messagebox.showinfo("Next", f"Memutar: {nxt.title} - {nxt.artist}", parent=self.root)
                refresh_playlist_box()
            else:
                messagebox.showinfo("Info", "Tidak ada lagu berikutnya.", parent=self.root)

        # control buttons
        btn_frame = Frame(self.content); btn_frame.pack(anchor=W, pady=6)
        Button(btn_frame, text="Play", command=play_selected_from_playlist).pack(side=LEFT, padx=6)
        Button(btn_frame, text="Pause", command=pause_selected).pack(side=LEFT, padx=6)
        Button(btn_frame, text="Next", command=next_in_playlist).pack(side=LEFT, padx=6)
        Button(btn_frame, text="Prev", command=prev_in_playlist).pack(side=LEFT, padx=6)
        Button(btn_frame, text="Hapus dari Playlist", command=remove_selected_from_playlist).pack(side=LEFT, padx=6)
        Button(btn_frame, text="Clear Playlist", command=clear_playlist).pack(side=LEFT, padx=6)

        refresh_playlist_box()
        self.theme.apply(self.root)

        # Now playing status
        status_frame = tk.Frame(self.content, bd=1, relief=tk.SUNKEN)
        status_frame.pack(fill=tk.X, pady=(10,0))
        self.now_playing_label = tk.Label(status_frame, text="Now Playing: (Tidak ada)", font=("Arial",10,"italic"))
        self.now_playing_label.pack(pady=6)
        

        def update_now_playing():
            if self.current_playing_song and self.is_playing:
                s = self.current_playing_song
                self.now_playing_label.config(text=f"Now Playing: {s.title} - {s.artist} ({s.genre})")
            elif self.current_playing_song and not self.is_playing:
                s = self.current_playing_song
                self.now_playing_label.config(text=f"Paused: {s.title} - {s.artist}")
            else:
                self.now_playing_label.config(text="Now Playing: (Tidak ada)")

        refresh_playlist_box()
        refresh_playlist_box()

        def schedule_update():
            update_now_playing()
            self.root.after(100, schedule_update)

        schedule_update()
        self.update_now_playing = update_now_playing

    # ---------------- Theme drawing ----------------
    def draw_theme_switch(self):
        # draw the little slider on header's canvas
        canvas = self.theme_canvas
        canvas.delete("all")
        if self.theme.dark:
            track_color = "#2a2a2a"; knob_color = "#ffd700"; icon = "☀"; icon_color = "#333"; knob_x = 22
        else:
            track_color = "#d0d0d0"; knob_color = "#4a5568"; icon = "🌙"; icon_color = "#fff"; knob_x = 2
        # track
        canvas.create_oval(0,0,20,20, fill=track_color, outline=track_color)
        canvas.create_oval(20,0,40,20, fill=track_color, outline=track_color)
        canvas.create_rectangle(10,0,30,20, fill=track_color, outline=track_color)
        # knob
        canvas.create_oval(knob_x,2,knob_x+16,18, fill=knob_color, outline=knob_color)
        canvas.create_text(knob_x+8,10, text=icon, fill=icon_color, font=("Arial", 9))
        # bind click
        canvas.bind("<Button-1>", lambda e: (self.toggle_theme(), self.draw_theme_switch()))

    def toggle_theme(self):
        self.theme.toggle()
        self.theme.apply(self.root)
        # redraw theme indicator
        try:
            self.draw_theme_switch()
        except:
            pass

    # ---------------- Save / Load ----------------
    def save_library(self):
        try:
            data = {"songs": library.to_dict_list(), "playlist": default_playlist.to_dict()}
            with open("music_data.json", "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            messagebox.showinfo("Saved", "Library & playlist disimpan ke music_data.json", parent=self.root)
        except Exception as e:
            messagebox.showerror("Error", f"Gagal menyimpan: {e}", parent=self.root)

    def load_library(self):
        try:
            with open("music_data.json", "r", encoding="utf-8") as f:
                data = json.load(f)
            songs = data.get("songs", [])
            library.load_from_dict_list(songs)
            # rebuild playlist by ids stored (if any)
            default_playlist.clear()
            pd = data.get("playlist", {})
            for sid in pd.get("songs", []):
                node = library.findNodeById(sid)
                if node:
                    default_playlist.addSong(node.song)
            # after loading, playlist references are correct because we used library objects
            messagebox.showinfo("Loaded", "Library & playlist berhasil dimuat.", parent=self.root)
        except FileNotFoundError:
            messagebox.showwarning("Not found", "music_data.json tidak ditemukan.", parent=self.root)
        except Exception as e:
            messagebox.showerror("Error", f"Gagal memuat: {e}", parent=self.root)

# -------------------------
# Run
# -------------------------
if __name__ == "__main__":
    # sample seeds
    library.addSong("Imagine", "John Lennon", "Rock", 1971)
    library.addSong("Billie Jean", "Michael Jackson", "Pop", 1982)
    library.addSong("Take Five", "Dave Brubeck", "Jazz", 1959)
    library.addSong("Back in Black", "AC/DC", "Rock", 1980)
    library.addSong("Lose Yourself", "Eminem", "Hip Hop", 2002)

    # add some to playlist
    n1 = library.findNodeById(1)
    n2 = library.findNodeById(2)
    if n1: default_playlist.addSong(n1.song)
    if n2: default_playlist.addSong(n2.song)

    root = tk.Tk()
    app = App(root)
    root.mainloop()
