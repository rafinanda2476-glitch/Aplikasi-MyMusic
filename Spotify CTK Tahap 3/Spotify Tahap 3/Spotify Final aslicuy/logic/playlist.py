# playlist manager
import json
from pathlib import Path

FILE_P=Path(__file__).resolve().parent.parent/"playlists.json"

class Node:
    def __init__(self,d):self.song=d;self.prev=None;self.next=None

class Playlist:
    def __init__(self,n="My Playlist"):self.name=n;self.head=None;self.tail=None;self.now=None

    def contains(self,s):
        c=self.head
        while c:
            if c.song.title.lower()==s.title.lower() and c.song.artist.lower()==s.artist.lower():return True
            c=c.next
        return False

    def addSong(self,s):
        if self.contains(s):return False
        n=Node(s)
        if not self.head:self.head=n;self.tail=n;return True
        self.tail.next=n;n.prev=self.tail;self.tail=n;return True

    def listSongs(self):
        res=[];c=self.head
        while c:res.append(c.song);c=c.next
        return res

    def removeSong(self,id):
        c=self.head
        while c:
            if c.song.id==id:
                if self.now==c:
                    if c.next:self.now=c.next
                    elif c.prev:self.now=c.prev
                    else:self.now=None
                if c.prev:c.prev.next=c.next
                else:self.head=c.next
                if c.next:c.next.prev=c.prev
                else:self.tail=c.prev
                return True
            c=c.next
        return False

class PlaylistManager:
    def __init__(self,lib_ref=None):self.all_p={};self.active_p="My Playlist";self.lib_ref=lib_ref;self.baca_file();self.all_p or self.createPlaylist("My Playlist")

    def setLibRef(self,lib):
        self.lib_ref=lib
        # Reload playlist dengan lagu setelah library tersedia
        self.reload_songs()

    def reload_songs(self):
        if not self.lib_ref:return
        if not FILE_P.exists():return
        try:
            f=open(FILE_P,"r",encoding="utf-8");d=json.load(f);f.close()
            raw=d.get("playlists",{})
            for k,ids in raw.items():
                if k not in self.all_p:self.all_p[k]=Playlist(k)
                pl=self.all_p[k]
                for sid in ids:
                    node=self.lib_ref.findNodeById(sid)
                    if node and not pl.contains(node.song):pl.addSong(node.song)
        except:pass

    def createPlaylist(self,n):
        if n in self.all_p:return False
        self.all_p[n]=Playlist(n);self.active_p=n;self.simpan_file();return True

    def deletePlaylist(self,n):
        if n not in self.all_p:return False
        del self.all_p[n]
        if self.active_p==n:self.active_p=list(self.all_p.keys())[0] if self.all_p else None
        self.simpan_file();return True

    def renamePlaylist(self,old,new):
        if not new or not new.strip():return False,"Kosong"
        new=new.strip()
        if old not in self.all_p:return False,"Ga ketemu"
        if new in self.all_p and new!=old:return False,"Udah ada"
        if old==new:return True,"Sama aja"
        p=self.all_p[old];p.name=new;self.all_p[new]=p;del self.all_p[old]
        if self.active_p==old:self.active_p=new
        self.simpan_file();return True,"Sukses"

    def getPlaylist(self,n):return self.all_p.get(n)
    def getCurrentPlaylist(self):return self.all_p.get(self.active_p)
    def setCurrentPlaylist(self,n):
        if n in self.all_p:self.active_p=n;return True
        return False
    def getAllPlaylists(self):return list(self.all_p.keys())

    @property
    def current_playlist_name(self):return self.active_p

    def addSongToPlaylist(self,n,s):
        p=self.all_p.get(n)
        if p:r=p.addSong(s);r and self.simpan_file();return r
        return False

    def removeSongFromPlaylist(self,n,id):
        p=self.all_p.get(n)
        if p:r=p.removeSong(id);r and self.simpan_file();return r
        return False

    def simpan_file(self):
        d={"current":self.active_p,"playlists":{}}
        for k,v in self.all_p.items():l=v.listSongs();d["playlists"][k]=[x.id for x in l]
        try:f=open(FILE_P,"w",encoding="utf-8");json.dump(d,f,indent=2);f.close()
        except:pass

    def baca_file(self):
        if not FILE_P.exists():return
        try:f=open(FILE_P,"r",encoding="utf-8");d=json.load(f);f.close();self.active_p=d.get("current","My Playlist");raw=d.get("playlists",{});[self.all_p.update({k:Playlist(k)}) for k in raw.keys()]
        except:pass

