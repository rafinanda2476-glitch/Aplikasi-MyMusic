# logic/playlist.py
import json
from pathlib import Path

PLAYLIST_FILE = Path(__file__).resolve().parent.parent / "playlists.json"

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

    def contains(self, song):
        """Check if playlist contains song by TITLE and ARTIST (not ID)."""
        cur = self.head
        while cur:
            # Compare by title and artist (case-insensitive)
            if (cur.song.title.lower() == song.title.lower() and 
                cur.song.artist.lower() == song.artist.lower()):
                return True
            cur = cur.next
        return False

    def addSong(self, song):
        # UNIK: Cek jika sudah ada (by title + artist)
        if self.contains(song):
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


class PlaylistManager:
    """Manages multiple playlists for a user."""
    
    def __init__(self):
        self.playlists = {}  # {name: Playlist}
        self.current_playlist_name = "My Playlist"
        self.load_playlists()
        
        # Create default playlist if none exist
        if not self.playlists:
            self.createPlaylist("My Playlist")
    
    def createPlaylist(self, name):
        """Create a new playlist."""
        if name in self.playlists:
            return False  # Playlist already exists
        
        self.playlists[name] = Playlist(name)
        self.current_playlist_name = name
        self.save_playlists()
        return True
    
    def deletePlaylist(self, name):
        """Delete a playlist."""
        if name not in self.playlists:
            return False
        
        # Don't delete if it's the only playlist
        if len(self.playlists) == 1:
            return False
        
        del self.playlists[name]
        
        # Switch to another playlist
        if self.current_playlist_name == name:
            self.current_playlist_name = list(self.playlists.keys())[0]
        
        self.save_playlists()
        return True
    
    def getPlaylist(self, name):
        """Get a specific playlist."""
        return self.playlists.get(name)
    
    def getCurrentPlaylist(self):
        """Get the currently active playlist."""
        return self.playlists.get(self.current_playlist_name)
    
    def setCurrentPlaylist(self, name):
        """Set the currently active playlist."""
        if name in self.playlists:
            self.current_playlist_name = name
            return True
        return False
    
    def getAllPlaylists(self):
        """Get list of all playlist names."""
        return list(self.playlists.keys())
    
    def addSongToPlaylist(self, playlist_name, song):
        """Add a song to a specific playlist."""
        playlist = self.playlists.get(playlist_name)
        if playlist:
            result = playlist.addSong(song)
            if result:
                self.save_playlists()
            return result
        return False
    
    def addSongToCurrent(self, song):
        """Add a song to the current playlist."""
        return self.addSongToPlaylist(self.current_playlist_name, song)
    
    def removeSongFromPlaylist(self, playlist_name, song_id):
        """Remove a song from a specific playlist."""
        playlist = self.playlists.get(playlist_name)
        if playlist:
            result = playlist.removeSong(song_id)
            if result:
                self.save_playlists()
            return result
        return False
    
    def addAlbumByArtist(self, playlist_name, artist, library):
        """Add all songs by an artist to a playlist."""
        playlist = self.playlists.get(playlist_name)
        if not playlist:
            return 0
        
        artist_songs = library.getSongsByArtist(artist)
        count = 0
        
        for song in artist_songs:
            if playlist.addSong(song):
                count += 1
        
        if count > 0:
            self.save_playlists()
        
        return count
    
    def save_playlists(self):
        """Save all playlists to file."""
        data = {
            "current": self.current_playlist_name,
            "playlists": {}
        }
        
        for name, playlist in self.playlists.items():
            songs = playlist.listSongs()
            data["playlists"][name] = [s.id for s in songs]
        
        try:
            with open(PLAYLIST_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
        except Exception:
            pass
    
    def load_playlists(self):
        """Load playlists from file."""
        if not PLAYLIST_FILE.exists():
            return
        
        try:
            with open(PLAYLIST_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            self.current_playlist_name = data.get("current", "My Playlist")
            
            # Note: We can't restore songs without library reference
            # This will be populated when songs are re-added
            playlists_data = data.get("playlists", {})
            for name in playlists_data.keys():
                self.playlists[name] = Playlist(name)
                
        except Exception:
            pass
