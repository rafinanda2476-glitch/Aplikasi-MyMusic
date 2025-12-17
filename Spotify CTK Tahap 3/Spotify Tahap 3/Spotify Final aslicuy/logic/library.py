# library class - database lagu
import json
from pathlib import Path

FILE_DB=Path("songs_store.json")

class Item:
    def __init__(self,id,t,a,g,y,d=180,file_path=""):
        self.id=id;self.title=t;self.artist=a;self.genre=g;self.year=y;self.duration=d;self.file_path=file_path

class Node:
    def __init__(self,data):self.song=data;self.prev=None;self.next=None

class SongLibrary:
    def __init__(self):self.head=None;self.tail=None;self.auto_id=1;self.obs=[];self.load_memori()

    def load_memori(self):
        if not FILE_DB.exists():return
        try:
            with open(FILE_DB,"r",encoding="utf-8") as f:data=json.load(f)
            self.head=None;self.tail=None;max_id=0
            for x in data:
                cid=x.get("id",0)
                if cid>max_id:max_id=cid
                item=Item(cid,x.get("title",""),x.get("artist",""),x.get("genre",""),int(x.get("year",0)),x.get("duration",180),x.get("file_path",""))
                self._ins(item)
            self.auto_id=max_id+1
        except:pass

    def _ins(self,item):
        n=Node(item)
        if not self.head:self.head=n;self.tail=n
        else:self.tail.next=n;n.prev=self.tail;self.tail=n

    def save_if_supported(self):
        arr=[];c=self.head
        while c:s=c.song;arr.append({"id":s.id,"title":s.title,"artist":s.artist,"genre":s.genre,"year":s.year,"duration":s.duration,"file_path":s.file_path});c=c.next
        try:
            with open(FILE_DB,"w",encoding="utf-8") as f:json.dump(arr,f,indent=2)
        except:pass

    def is_duplicate(self,t,a):
        c=self.head
        while c:
            if c.song.title.lower()==t.lower() and c.song.artist.lower()==a.lower():return True
            c=c.next
        return False

    def cek_kembar(self,t,a):return self.is_duplicate(t,a)

    def addSong(self,t,a,g,y,d=180,file_path=""):
        if self.is_duplicate(t,a):return None
        item=Item(self.auto_id,t,a,g,y,d,file_path);self.auto_id+=1;self._ins(item);self.kabari_obs("add",item);return item

    def findNodeById(self,id):
        c=self.head
        while c:
            if c.song.id==id:return c
            c=c.next
        return None

    def updateSong(self,id,t,a,g,y,d=None):
        n=self.findNodeById(id)
        if not n:return False
        n.song.title=t;n.song.artist=a;n.song.genre=g;n.song.year=y
        if d:n.song.duration=d
        self.kabari_obs("update",n.song);return True

    def deleteSong(self,id):
        c=self.head
        while c:
            if c.song.id==id:
                if c.prev:c.prev.next=c.next
                else:self.head=c.next
                if c.next:c.next.prev=c.prev
                else:self.tail=c.prev
                self.kabari_obs("delete",id);return True
            c=c.next
        return False

    def getAllSongs(self):
        arr=[];c=self.head
        while c:arr.append(c.song);c=c.next
        return arr
    def load_sample_if_empty(self):pass
    def attach_observer(self,o):self.obs.append(o)
    def kabari_obs(self,act,dat):
        for o in self.obs:
            if hasattr(o,'on_library_changed'):o.on_library_changed(act,dat)

    def getSortedSongs(self,sort_by="title"):
        res=self.getAllSongs()
        if sort_by=="title":return sorted(res,key=lambda x:x.title.lower())
        elif sort_by=="artist":return sorted(res,key=lambda x:x.artist.lower())
        elif sort_by=="genre":return sorted(res,key=lambda x:x.genre.lower())
        elif sort_by=="year":return sorted(res,key=lambda x:x.year)
        return res

    def searchSongs(self,q,fuzzy=True,fields=None):
        if not q:return self.getAllSongs()
        return [s for s in self.getAllSongs() if q.lower() in s.title.lower() or q.lower() in s.artist.lower()]