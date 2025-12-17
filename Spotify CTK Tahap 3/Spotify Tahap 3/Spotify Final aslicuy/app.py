# app utama - ini penting bgt
import customtkinter as ctk
from tkinter import messagebox
import os
from pathlib import Path

from logic.library import SongLibrary as Lib
from logic.playlist import PlaylistManager as PM
from logic.controller_player import PlayerController as PC

from components.topbar import TopBar
from components.sidebar_user import SidebarUser
from components.sidebar_admin import SidebarAdmin
from components.bottom_player import BottomPlayer

from pages_user.home_user import render_home
from pages_user.search_user import render_search
from pages_user.playlist_user import render_playlist
from pages_user.create_playlist import render_create_playlist

from pages_admin.dashboard import render_dashboard
from pages_admin.songs_list import render_songs_list
from pages_admin.add_song import render_add_song
from pages_admin.edit_song import render_edit_song
from pages_admin.delete_song import render_delete_song

try:from pages_admin.import_folder import render_import_folder
except ImportError:
    def render_import_folder(p,*a,**k):ctk.CTkLabel(p,text="ERROR: import_folder.py hilang!",text_color="red").pack(pady=20)

from login import PageLogin

ctk.set_appearance_mode("Light")
THEME={"primary":"#0047FF","hover":"#0033CC","bg_sidebar":"#001040","bg_content":"#F0F5FF","text_head":"#001A5E","danger":"#FF3333"}

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("MyMusic");self.geometry("1280x850")
        self.lib=Lib();self.pm=PM();self.player=PC()
        self.pm.setLibRef(self.lib)  # Koneksikan playlist ke library untuk reload lagu
        self.player.setLibraryRef(self.lib);self.player.setPlayMode("artist_based");self.lib.attach_observer(self)
        self.header=None;self.main_cont=None;self.side_frame=None;self.content=None;self.bot_player=None
        self.curr_page="home";self.role="login";self.fpath=Path("songs_store.json");self.last_mtime=None;self.watcher_id=None;self.timer_id=None
        self.lib.load_sample_if_empty();self.show_login()

    def on_library_changed(self,action,d):
        self.lib.save_if_supported()
        if self.role!="login" and hasattr(self,'content'):self.reload_page()

    def reload_page(self):
        if self.curr_page:self.go_to(self.curr_page)

    def bersih(self):
        for x in self.winfo_children():x.destroy()

    def show_login(self):
        self.bersih()
        if self.watcher_id:self.after_cancel(self.watcher_id);self.watcher_id=None
        if self.timer_id:self.after_cancel(self.timer_id);self.timer_id=None
        try:self.player.stop()
        except:pass
        self.role="login";PageLogin(self,cb_login=self.handle_login,c=THEME).pack(fill="both",expand=True)

    def handle_login(self,r):
        if r not in("user","admin"):return
        self.role=r;self.bikin_ui_utama()

    def bikin_ui_utama(self):
        self.bersih()
        self.header=TopBar(self,self.tombol_logout,THEME,on_search=self.handle_search if self.role=="user" else None)
        self.header.pack(side="top",fill="x")
        self.main_cont=ctk.CTkFrame(self,fg_color="transparent");self.main_cont.pack(side="top",fill="both",expand=True)
        if self.role=="user":self.curr_page="home";self.curr_pl=None
        else:self.curr_page="dashboard"
        self.update_sidebar()
        self.content=ctk.CTkFrame(self.main_cont,fg_color=THEME["bg_content"],corner_radius=15)
        self.content.pack(side="right",fill="both",expand=True,padx=15,pady=15)
        if self.role=="user":
            self.bot_player=BottomPlayer(self.content,THEME,self.prev_song,self.play_pause,self.next_song,self.shuffle_mode,self.repeat_mode,pm=self.pm,cb_seek=self.seek_song)
            self.bot_player.pack(side="bottom",fill="x");self.cek_timer()
        self.go_to(self.curr_page);self.mulai_watcher()

    def update_sidebar(self):
        if self.side_frame:self.side_frame.destroy()
        if self.role=="user":self.side_frame=SidebarUser(self.main_cont,THEME,lambda:self.go_to("home"),lambda:self.go_to("create_playlist"),self.pilih_playlist,self.pm,cur=self.curr_page)
        else:self.side_frame=SidebarAdmin(self.main_cont,THEME,lambda:self.go_to("dashboard"),lambda:self.go_to("songs"),lambda:self.go_to("add"),lambda:self.go_to("import"),cur=self.curr_page)
        self.side_frame.pack(side="left",fill="y");self.side_frame.lift()

    def go_to(self,page,**kw):
        self.curr_page=page;self.update_sidebar()
        for w in self.content.winfo_children():
            if w!=self.bot_player:w.destroy()
        area=ctk.CTkFrame(self.content,fg_color="transparent");area.pack(fill="both",expand=True,side="top")
        if page=="home":render_home(area,self.lib,THEME,self.main_sembarang)
        elif page=="search":q=getattr(self,'pencarian','');render_search(area,self.lib,THEME,self.main_sembarang,self.tambah_ke_playlist,q=q)
        elif page=="playlist":render_playlist(area,self.lib,self.pm,THEME,self.main_sembarang,self.hapus_dari_playlist,self.rename_pl,self.delete_pl)
        elif page=="create_playlist":render_create_playlist(area,self.pm,THEME,self.on_playlist_created)
        elif page=="dashboard":render_dashboard(area,self.lib,THEME)
        elif page=="songs":render_songs_list(area,self.lib,THEME,lambda id:self.go_to("edit",song_id=id),lambda id:self.go_to("delete",song_id=id))
        elif page=="add":render_add_song(area,self.lib,THEME,lambda:self.go_to("songs"))
        elif page=="edit":render_edit_song(area,self.lib,THEME,kw.get("song_id"),lambda:self.go_to("songs"))
        elif page=="delete":render_delete_song(area,self.lib,THEME,kw.get("song_id"),lambda:self.go_to("songs"))
        elif page=="import":render_import_folder(area,self.lib,THEME,lambda:self.go_to("songs"))
        self.refresh_player()

    def pilih_playlist(self,nama):self.pm.setCurrentPlaylist(nama);self.curr_page=f"playlist_{nama}";self.go_to("playlist")
    def handle_search(self,q):self.pencarian=q;self.go_to("search")

    def main_sembarang(self,songs,start_idx):
        self.player.set_queue(songs,start_idx);self.refresh_player()
        if self.role=="user" and self.bot_player and self.player.current_song:self.bot_player.update_timer(0,self.player.current_song.duration)

    def tambah_ke_playlist(self,s_id):
        node=self.lib.findNodeById(s_id)
        if not node:return
        list_pl=self.pm.getAllPlaylists();avail=[x for x in list_pl if not self.pm.getPlaylist(x).contains(node.song)]
        if not avail:messagebox.showwarning("Wetsss","Bikin playlist dulu gih.");return
        if len(avail)==1:self.pm.addSongToPlaylist(avail[0],node.song);messagebox.showinfo("Joss",f"Masuk ke '{avail[0]}'!")
        else:self.munculin_dialog_pilih(node.song,avail)

    def munculin_dialog_pilih(self,song,playlists):
        from tkinter import Toplevel
        d=Toplevel(self);d.title("Pilih Dong");d.geometry("300x400")
        for name in playlists:ctk.CTkButton(d,text=f"📂 {name}",command=lambda n=name:(self.pm.addSongToPlaylist(n,song),d.destroy())).pack(pady=5)

    def hapus_dari_playlist(self,s_id):pass
    def rename_pl(self,new_name):self.pm.setCurrentPlaylist(new_name);self.update_sidebar();self.go_to("playlist")
    def delete_pl(self):
        all_pl=self.pm.getAllPlaylists()
        if all_pl:self.pilih_playlist(all_pl[0])
        else:self.go_to("home")

    def on_playlist_created(self,nm):
        if nm:
            self.pm.setCurrentPlaylist(nm)
            self.update_sidebar()
            self.pilih_playlist(nm)
        else:
            self.go_to("home")

    def play_pause(self):
        if self.player.playing:self.player.pause()
        else:self.player.play()
        self.refresh_player()

    def next_song(self):
        if self.player.next(force=True):self.refresh_player()
    def prev_song(self):
        if self.player.prev():self.refresh_player()
    def shuffle_mode(self):self.player.toggleShuffle();self.refresh_player()
    def repeat_mode(self):self.player.toggleRepeat();self.refresh_player()
    def seek_song(self,pos):self.player.seek(pos)

    def refresh_player(self):
        if self.role!="user" or not self.bot_player:return
        self.bot_player.update_state(self.player.current_song,self.player.playing)
        self.bot_player.update_shuffle_repeat(self.player.shuf,self.player.rep)

    def cek_timer(self):
        if self.role=="user" and self.bot_player:
            if self.player.current_song:
                if self.player.updateCountdown():
                    self.player.next(force=False)
                    self.refresh_player()
                    if self.player.current_song:self.bot_player.update_timer(0,self.player.current_song.duration)
                elif self.player.playing:
                    try:self.bot_player.update_timer(self.player.elapsed_time,self.player.current_duration)
                    except:pass
            self.timer_id=self.after(100,self.cek_timer)

    def tombol_logout(self):
        if messagebox.askyesno("Keluar","Yakin kah kids?"):self.show_login()

    def mulai_watcher(self):
        try:
            if self.fpath.exists():self.last_mtime=self.fpath.stat().st_mtime
        except:pass
        self.cek_file()

    def cek_file(self):
        try:
            if self.fpath.exists():
                curr=self.fpath.stat().st_mtime
                if self.last_mtime and curr!=self.last_mtime:self.lib.load_memori();self.reload_page() if self.role!="login" else None
                self.last_mtime=curr
        except:pass
        if self.role!="login":self.watcher_id=self.after(2000,self.cek_file)

if __name__=="__main__":app_instance=App();app_instance.mainloop()