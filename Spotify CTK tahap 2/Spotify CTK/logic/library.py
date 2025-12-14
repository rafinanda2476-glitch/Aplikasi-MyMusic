# logic/library.py
import json
from pathlib import Path

DATAFILE = Path(__file__).resolve().parent.parent / "songs_store.json"

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
        self._load_from_file()

    def _load_from_file(self):
        if not DATAFILE.exists():
            return
        try:
            with open(DATAFILE, "r", encoding="utf-8") as f:
                arr = json.load(f)
            # Saat load dari file, kita masukkan saja langsung (asumsi file aman)
            for item in arr:
                self._insert_node(item.get("title",""), item.get("artist",""), item.get("genre",""), int(item.get("year",0)))
        except Exception:
            pass

    def save_if_supported(self):
        arr = []
        cur = self.head
        while cur:
            s = cur.song
            arr.append({"id": s.id, "title": s.title, "artist": s.artist, "genre": s.genre, "year": s.year})
            cur = cur.next
        with open(DATAFILE, "w", encoding="utf-8") as f:
            json.dump(arr, f, indent=2, ensure_ascii=False)

    # --- FUNGSI CEK DUPLIKAT ---
    def is_duplicate(self, title, artist):
        cur = self.head
        # Bersihkan spasi dan jadikan huruf kecil semua agar akurat
        t_check = title.strip().lower()
        a_check = artist.strip().lower()
        
        while cur:
            current_t = cur.song.title.strip().lower()
            current_a = cur.song.artist.strip().lower()
            
            if current_t == t_check and current_a == a_check:
                return True
            cur = cur.next
        return False

    def _insert_node(self, title, artist, genre, year):
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

    def addSong(self, title, artist, genre, year):
        # 1. Cek Duplikat Sebelum Menambah
        if self.is_duplicate(title, artist):
            return None # Return None tanda gagal/duplikat

        # 2. Jika aman, tambahkan
        return self._insert_node(title, artist, genre, year)

    def findNodeById(self, sid):
        cur = self.head
        while cur:
            if cur.song.id == sid:
                return cur
            cur = cur.next
        return None

    def updateSong(self, sid, t, a, g, y):
        n = self.findNodeById(sid)
        if not n: return False
        n.song.title = t
        n.song.artist = a
        n.song.genre = g
        n.song.year = y
        return True

    def deleteSong(self, sid):
        cur = self.head
        while cur:
            if cur.song.id == sid:
                if cur.prev: cur.prev.next = cur.next
                else: self.head = cur.next
                if cur.next: cur.next.prev = cur.prev
                else: self.tail = cur.prev
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

    def load_sample_if_empty(self):
        if not self.getAllSongs():
            # Data sampel (beberapa dibuat mirip untuk tes)
            self.addSong("Imagine", "John Lennon", "Rock", 1971)
            self.addSong("Billie Jean", "Michael Jackson", "Pop", 1982)
            self.addSong("Take Five", "Dave Brubeck", "Jazz", 1959)