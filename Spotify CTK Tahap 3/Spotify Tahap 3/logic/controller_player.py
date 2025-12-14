import random

class PlayerController:
    def __init__(self):
        self.queue = []      # Daftar lagu (List biasa)
        self.index = -1      # Posisi sekarang
        self.is_playing = False
        self.history = []    # Track play history
        self.play_mode = 'normal'  # 'normal', 'artist_based', 'genre_based'
        self.countdown_active = False
        self.current_duration = 0
        self.elapsed_time = 0
        self.library_ref = None  # Reference to library for recommendations
        self.shuffle_enabled = False  # Shuffle mode
        self.repeat_mode = 'off'  # 'off', 'one', 'all'
        self.original_queue = []  # Store original queue for shuffle toggle

    @property
    def current_song(self):
        if 0 <= self.index < len(self.queue):
            return self.queue[self.index]
        return None

    def set_queue(self, song_list, start_index=0):
        self.queue = song_list
        self.index = start_index
        self.is_playing = True
        # Reset history when setting new queue
        self.history = []
        if self.current_song:
            self.history.append(self.current_song.id)
            self.current_duration = self.current_song.duration
            self.elapsed_time = 0

    def play(self):
        if self.queue:
            self.is_playing = True
            if self.current_song and self.current_song.id not in self.history:
                self.history.append(self.current_song.id)

    def pause(self):
        self.is_playing = False

    def next(self, force_advance=False):
        """Smart next: normal or artist/genre-based when queue exhausted.
        
        Args:
            force_advance: If True, advance even in repeat_one mode (for manual next)
        """
        if not self.queue:
            return False
        
        # Repeat one: replay current song (only for auto-advance, not manual)
        if self.repeat_mode == 'one' and not force_advance:
            self.is_playing = True
            if self.current_song:
                self.current_duration = self.current_song.duration
                self.elapsed_time = 0
            return True
        
        if self.index < len(self.queue) - 1:
            # Normal next within queue
            self.index += 1
            self.is_playing = True
            if self.current_song:
                if self.current_song.id not in self.history:
                    self.history.append(self.current_song.id)
                self.current_duration = self.current_song.duration
                self.elapsed_time = 0
            return True
        else:
            # Queue exhausted
            if self.repeat_mode == 'all' or (self.repeat_mode == 'one' and force_advance):
                # Loop to start
                self.index = 0
                self.is_playing = True
                if self.current_song:
                    self.current_duration = self.current_song.duration
                    self.elapsed_time = 0
                return True
            elif self.library_ref and self.play_mode == 'artist_based':
                return self.nextByArtist()
            elif self.library_ref and self.play_mode == 'genre_based':
                return self.nextByGenre()
            else:
                # Stop at end if repeat is off
                self.is_playing = False
                return False

    def prev(self):
        """
        Go to previous song using history.
        Pattern: 1 -> 2 -> 3, then prev: 3 -> 2 -> 1 (stops at 1, no loop)
        """
        if not self.queue:
            return False
        
        # Check if we're at the first song and should stop
        if self.index == 0:
            # At first song, don't loop - just stop
            self.is_playing = False
            return False
        else:
            self.index -= 1
            self.is_playing = True
        
        if self.current_song:
            self.current_duration = self.current_song.duration
            self.elapsed_time = 0
        return True

    def nextByArtist(self):
        """Find next song by same artist."""
        if not self.current_song or not self.library_ref:
            return False
        
        artist = self.current_song.artist
        artist_songs = self.library_ref.getSongsByArtist(artist)
        
        # Filter out current song AND songs already in history
        unplayed_artist_songs = [s for s in artist_songs 
                                  if s.id != self.current_song.id and s.id not in self.history]
        
        if unplayed_artist_songs:
            # Add next unplayed artist song to queue
            next_song = unplayed_artist_songs[0]
            self.queue.append(next_song)
            self.index = len(self.queue) - 1
            self.is_playing = True
            self.history.append(next_song.id)
            self.current_duration = next_song.duration
            self.elapsed_time = 0
            return True
        else:
            # No more unplayed songs by this artist, try different artist
            return self.getRecommendations()

    def nextByGenre(self):
        """Find next song by same genre."""
        if not self.current_song or not self.library_ref:
            return False
        
        genre = self.current_song.genre
        genre_songs = self.library_ref.getSongsByGenre(genre)
        
        # Filter out current song and already played
        genre_songs = [s for s in genre_songs if s.id != self.current_song.id and s.id not in self.history]
        
        if genre_songs:
            next_song = random.choice(genre_songs)
            self.queue.append(next_song)
            self.index = len(self.queue) - 1
            self.is_playing = True
            if next_song.id not in self.history:
                self.history.append(next_song.id)
            self.current_duration = next_song.duration
            self.elapsed_time = 0
            return True
        else:
            # No more songs in this genre, try different genre
            return self.getRecommendations()

    def getRecommendations(self):
        """Get smart recommendations when artist/genre exhausted."""
        if not self.library_ref:
            return False
        
        all_songs = self.library_ref.getAllSongs()
        # Filter out played songs
        unplayed = [s for s in all_songs if s.id not in self.history]
        
        if unplayed:
            next_song = random.choice(unplayed)
            self.queue.append(next_song)
            self.index = len(self.queue) - 1
            self.is_playing = True
            if next_song.id not in self.history:
                self.history.append(next_song.id)
            self.current_duration = next_song.duration
            self.elapsed_time = 0
            return True
        else:
            # All songs played, reset history
            self.history = []
            self.index = 0
            return True

    def startCountdown(self, duration):
        """Start countdown timer for current song."""
        self.countdown_active = True
        self.current_duration = duration
        self.elapsed_time = 0

    def updateCountdown(self, delta_seconds=1):
        """Update countdown timer. Returns True if countdown finished."""
        if not self.countdown_active or not self.is_playing:
            return False
        
        self.elapsed_time += delta_seconds
        
        if self.elapsed_time >= self.current_duration:
            # Song finished, auto-advance
            self.countdown_active = False
            return True
        
        return False

    def getRemainingTime(self):
        """Get remaining time in seconds."""
        if self.current_duration > 0:
            remaining = self.current_duration - self.elapsed_time
            return max(0, int(remaining))
        return 0

    def formatTime(self, seconds):
        """Format seconds as MM:SS."""
        mins = seconds // 60
        secs = seconds % 60
        return f"{mins:02d}:{secs:02d}"

    def setLibraryRef(self, library):
        """Set reference to library for recommendations."""
        self.library_ref = library

    def setPlayMode(self, mode):
        """Set play mode: 'normal', 'artist_based', or 'genre_based'."""
        if mode in ['normal', 'artist_based', 'genre_based']:
            self.play_mode = mode
    
    def toggleShuffle(self):
        """Toggle shuffle mode on/off."""
        self.shuffle_enabled = not self.shuffle_enabled
        
        if self.shuffle_enabled and self.queue:
            # Save original queue and current song
            if not self.original_queue:
                self.original_queue = self.queue.copy()
            current = self.current_song
            
            # Shuffle the queue
            shuffled = self.queue.copy()
            random.shuffle(shuffled)
            self.queue = shuffled
            
            # Find current song in shuffled queue
            if current:
                for i, song in enumerate(self.queue):
                    if song.id == current.id:
                        self.index = i
                        break
        elif not self.shuffle_enabled and self.original_queue:
            # Restore original queue
            current = self.current_song
            self.queue = self.original_queue.copy()
            self.original_queue = []
            
            # Find current song in original queue
            if current:
                for i, song in enumerate(self.queue):
                    if song.id == current.id:
                        self.index = i
                        break
        
        return self.shuffle_enabled
    
    def toggleRepeat(self):
        """Toggle repeat mode: off -> all -> one -> off."""
        if self.repeat_mode == 'off':
            self.repeat_mode = 'all'
        elif self.repeat_mode == 'all':
            self.repeat_mode = 'one'
        else:  # 'one'
            self.repeat_mode = 'off'
        
        return self.repeat_mode

