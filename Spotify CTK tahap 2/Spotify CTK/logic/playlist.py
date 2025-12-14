# logic/playlist.py
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
        self.current = None

    def contains(self, song_id):
        cur = self.head
        while cur:
            if cur.song.id == song_id:
                return True
            cur = cur.next
        return False

    def addSong(self, song):
        # UNIK: Cek jika sudah ada
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
                if self.current is cur:
                    if cur.next: self.current = cur.next
                    elif cur.prev: self.current = cur.prev
                    else: self.current = None
                
                if cur.prev: cur.prev.next = cur.next
                else: self.head = cur.next
                
                if cur.next: cur.next.prev = cur.prev
                else: self.tail = cur.prev
                return True
            cur = cur.next
        return False