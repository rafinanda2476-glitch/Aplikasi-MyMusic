class PlayerController:
    def __init__(self):
        self.queue = []      # Daftar lagu (List biasa)
        self.index = -1      # Posisi sekarang
        self.is_playing = False

    @property
    def current_song(self):
        if 0 <= self.index < len(self.queue):
            return self.queue[self.index]
        return None

    def set_queue(self, song_list, start_index=0):
        self.queue = song_list
        self.index = start_index
        self.is_playing = True

    def play(self):
        if self.queue:
            self.is_playing = True

    def pause(self):
        self.is_playing = False

    def next(self):
        if not self.queue: return
        if self.index < len(self.queue) - 1:
            self.index += 1
            self.is_playing = True
        else:
            # Loop ke awal atau stop (disini kita loop)
            self.index = 0 
            self.is_playing = True

    def prev(self):
        if not self.queue: return
        if self.index > 0:
            self.index -= 1
            self.is_playing = True
        else:
            self.index = len(self.queue) - 1
            self.is_playing = True