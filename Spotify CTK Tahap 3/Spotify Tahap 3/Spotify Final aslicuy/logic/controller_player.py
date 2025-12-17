# player controller - audio stuff
import os,warnings
os.environ['PYGAME_HIDE_SUPPORT_PROMPT']="1"
warnings.filterwarnings("ignore")
import pygame,random

class PlayerController:
    def __init__(self):
        try:
            pygame.init()  # Init pygame untuk time.get_ticks()
            pygame.mixer.pre_init(frequency=44100,size=-16,channels=2,buffer=1024)
            pygame.mixer.init()
            pygame.mixer.set_num_channels(32)
        except Exception as e:print(f"Audio Error: {e}")
        self.queue=[];self.index=-1;self.is_playing=False;self.shuf=False;self.rep='off';self.original_queue=[];self.library_ref=None;self._sim_start=0

    def setLibraryRef(self,lib):self.library_ref=lib
    def setPlayMode(self,mode):pass

    @property
    def current_song(self):return self.queue[self.index] if 0<=self.index<len(self.queue) else None

    @property
    def elapsed_time(self):
        # Selalu gunakan simulasi timer untuk konsistensi dengan seek
        if self.is_playing and hasattr(self,'_sim_start'):
            elapsed=(pygame.time.get_ticks()/1000)-self._sim_start
            # Clamp ke durasi lagu
            if self.current_song:
                return min(elapsed, self.current_song.duration)
            return elapsed
        return 0

    @property
    def current_duration(self):return self.current_song.duration if self.current_song else 1

    @property
    def playing(self):return self.is_playing

    def set_queue(self,song_list,start_index=0):
        self.queue=song_list;self.index=start_index
        if not self.shuf:self.original_queue=list(song_list)
        try:pygame.mixer.music.stop()
        except:pass
        self.play_song_at_index()

    def play_song_at_index(self):
        song=self.current_song
        if not song:return
        self._using_real_music=False
        if song.file_path and os.path.exists(song.file_path):
            try:
                pygame.mixer.music.load(song.file_path)
                pygame.mixer.music.play()
                self._using_real_music=True
            except:pass
        self.is_playing=True
        self._sim_start=pygame.time.get_ticks()/1000

    def play(self):
        if self.current_song:
            try:pygame.mixer.music.unpause();pygame.mixer.music.get_busy() or self.play_song_at_index();self.is_playing=True
            except:pass

    def pause(self):
        try:pygame.mixer.music.pause();self.is_playing=False
        except:pass

    def stop(self):
        try:pygame.mixer.music.stop();self.is_playing=False;self.queue=[];self.index=-1
        except:pass

    def seek(self,position):
        if not self.current_song:return
        position=max(0,min(position,self.current_song.duration))
        if getattr(self,'_using_real_music',False):
            try:pygame.mixer.music.set_pos(position)
            except:pass
        self._sim_start=(pygame.time.get_ticks()/1000)-position


    def next(self,force=False):
        if not self.queue:return False
        if self.rep=='one' and not force:self.play_song_at_index();return True
        if self.index<len(self.queue)-1:self.index+=1;self.play_song_at_index();return True
        elif self.rep=='all':self.index=0;self.play_song_at_index();return True
        else:self.is_playing=False;pygame.mixer.music.stop();return False

    def prev(self):
        if self.elapsed_time>3:self.play_song_at_index();return True
        if self.index>0:self.index-=1;self.play_song_at_index();return True
        return False

    def toggleShuffle(self):
        self.shuf=not self.shuf;curr=self.current_song
        if self.shuf:random.shuffle(self.queue);curr in self.queue and setattr(self,'index',self.queue.index(curr))
        else:self.original_queue and setattr(self,'queue',list(self.original_queue));curr in self.queue and setattr(self,'index',self.queue.index(curr))
        return self.shuf

    def toggleRepeat(self):
        if self.rep=='off':self.rep='all'
        elif self.rep=='all':self.rep='one'
        else:self.rep='off'
        return self.rep

    def startCountdown(self,d):pass
    def updateCountdown(self,d=1):
        if not self.is_playing:return False
        if not self.current_song:return False
        
        # Jika pakai real music, cek pygame
        if getattr(self,'_using_real_music',False):
            try:
                if pygame.mixer.music.get_busy():return False
                else:return True  # Real music selesai
            except:pass
        
        # Simulasi: cek elapsed time vs duration
        if hasattr(self,'_sim_start'):
            elapsed=(pygame.time.get_ticks()/1000)-self._sim_start
            if elapsed>=self.current_song.duration:
                return True
        return False