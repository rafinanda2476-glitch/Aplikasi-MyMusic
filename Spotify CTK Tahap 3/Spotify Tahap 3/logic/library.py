# logic/library.py
import json
from pathlib import Path
from logic.fuzzy_search import fuzzy_search_songs

DATAFILE = Path(__file__).resolve().parent.parent / "songs_store.json"

class Song:
    def __init__(self, sid, title, artist, genre, year, duration=180):
        self.id = sid
        self.title = title
        self.artist = artist
        self.genre = genre
        self.year = year
        self.duration = duration  # Duration in seconds, default 3 minutes

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
        self.observers = []  # Observer pattern for real-time sync
        self._load_from_file()

    def _load_from_file(self):
        if not DATAFILE.exists():
            return
        try:
            with open(DATAFILE, "r", encoding="utf-8") as f:
                arr = json.load(f)
            
            # CLEAR existing data first to prevent duplicates during reload
            self.head = None
            self.tail = None
            self._id_counter = 0
            
            # Load with duration support (default to 180 if not present)
            for item in arr:
                duration = item.get("duration", 180)
                self._insert_node(
                    item.get("title",""), 
                    item.get("artist",""), 
                    item.get("genre",""), 
                    int(item.get("year",0)),
                    duration
                )
        except Exception:
            pass

    def save_if_supported(self):
        arr = []
        cur = self.head
        while cur:
            s = cur.song
            arr.append({
                "id": s.id, 
                "title": s.title, 
                "artist": s.artist, 
                "genre": s.genre, 
                "year": s.year,
                "duration": s.duration
            })
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

    def _insert_node(self, title, artist, genre, year, duration=180):
        song = Song(self.auto_id, title, artist, genre, year, duration)
        self.auto_id += 1
        node = NodeDLL(song)
        if self.head is None:
            self.head = self.tail = node
        else:
            self.tail.next = node
            node.prev = self.tail
            self.tail = node
        return song

    def addSong(self, title, artist, genre, year, duration=180):
        # 1. Cek Duplikat Sebelum Menambah
        if self.is_duplicate(title, artist):
            return None # Return None tanda gagal/duplikat

        # 2. Jika aman, tambahkan
        song = self._insert_node(title, artist, genre, year, duration)
        if song:
            self.notify_observers("add", song)
        return song

    def findNodeById(self, sid):
        cur = self.head
        while cur:
            if cur.song.id == sid:
                return cur
            cur = cur.next
        return None

    def updateSong(self, sid, t, a, g, y, duration=None):
        n = self.findNodeById(sid)
        if not n: return False
        n.song.title = t
        n.song.artist = a
        n.song.genre = g
        n.song.year = y
        if duration is not None:
            n.song.duration = duration
        self.notify_observers("update", n.song)
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
                self.notify_observers("delete", sid)
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
            self.addSong("Imagine", "John Lennon", "Rock", 1971, 183)
            self.addSong("Billie Jean", "Michael Jackson", "Pop", 1982, 294)
            self.addSong("Take Five", "Dave Brubeck", "Jazz", 1959, 324)
    
    # --- OBSERVER PATTERN FOR REAL-TIME SYNC ---
    def attach_observer(self, observer):
        """Attach an observer to be notified of library changes."""
        if observer not in self.observers:
            self.observers.append(observer)
    
    def detach_observer(self, observer):
        """Detach an observer."""
        if observer in self.observers:
            self.observers.remove(observer)
    
    def notify_observers(self, action, data):
        """Notify all observers of a change."""
        for observer in self.observers:
            observer.on_library_changed(action, data)
    
    # --- SORTING AND FILTERING ---
    def getSortedSongs(self, sort_by="title"):
        """Get all songs sorted by specified field."""
        songs = self.getAllSongs()
        
        # Empty string means no sorting, return original order
        if not sort_by or sort_by == "":
            return songs
        
        if sort_by == "title":
            return sorted(songs, key=lambda s: s.title.lower())
        elif sort_by == "artist":
            return sorted(songs, key=lambda s: s.artist.lower())
        elif sort_by == "genre":
            return sorted(songs, key=lambda s: s.genre.lower())
        elif sort_by == "year":
            return sorted(songs, key=lambda s: s.year)
        else:
            return songs
    
    def getSongsByArtist(self, artist):
        """Get all songs by a specific artist."""
        import random
        artist_lower = artist.lower()
        songs = [s for s in self.getAllSongs() if artist_lower in s.artist.lower()]
        random.shuffle(songs)  # Shuffle to avoid alphabetical order
        return songs
    
    def getSongsByGenre(self, genre):
        """Get all songs of a specific genre."""
        import random
        genre_lower = genre.lower()
        songs = [s for s in self.getAllSongs() if genre_lower in s.genre.lower()]
        random.shuffle(songs)  # Shuffle to avoid alphabetical order
        return songs
    
    def getAllArtists(self):
        """Get unique list of all artists."""
        artists = set()
        cur = self.head
        while cur:
            artists.add(cur.song.artist)
            cur = cur.next
        return sorted(list(artists))
    
    def getAllGenres(self):
        """Get unique list of all genres."""
        genres = set()
        cur = self.head
        while cur:
            genres.add(cur.song.genre)
            cur = cur.next
        return sorted(list(genres))
    
    # --- SEARCH METHODS ---
    def searchSongs(self, query, fuzzy=True, search_fields=None):
        """Search songs with optional fuzzy matching."""
        if not query:
            return self.getAllSongs()
        
        songs = self.getAllSongs()
        
        if search_fields is None:
            search_fields = ['title', 'artist']
        
        if fuzzy:
            return fuzzy_search_songs(query, songs, threshold=2, search_fields=search_fields)
        else:
            # Exact substring search
            query_lower = query.lower()
            results = []
            for song in songs:
                for field in search_fields:
                    field_value = getattr(song, field, "").lower()
                    if query_lower in field_value:
                        results.append(song)
                        break
            return results