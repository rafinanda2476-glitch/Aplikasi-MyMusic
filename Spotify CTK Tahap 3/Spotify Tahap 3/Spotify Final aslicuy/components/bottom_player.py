# bottom player - music control with seek
import customtkinter as ctk

class BottomPlayer(ctk.CTkFrame):
    def __init__(self,p,c,cb_pr,cb_pl,cb_nx,cb_sh,cb_rp,pm=None,cb_seek=None):
        super().__init__(p,fg_color="#000000",height=90,corner_radius=0)
        self.c=c;self.playing=False;self.pm=pm;self.cur_s=None;self.cb_seek=cb_seek;self.pack_propagate(False)
        self._tot_dur=1;self._user_seeking=False
        mc=ctk.CTkFrame(self,fg_color="transparent");mc.pack(fill="both",expand=True,padx=10,pady=10)
        mc.grid_columnconfigure(0,weight=1,uniform="fixed");mc.grid_columnconfigure(1,weight=2,uniform="fixed");mc.grid_columnconfigure(2,weight=1,uniform="fixed")
        
        # KIRI
        f_kiri=ctk.CTkFrame(mc,fg_color="transparent");f_kiri.grid(row=0,column=0,sticky="w",padx=(10,0))
        self.art=ctk.CTkLabel(f_kiri,text="",width=50,height=50,fg_color="#333333",corner_radius=4);self.art.grid(row=0,column=0,rowspan=2,padx=(0,12),pady=0,sticky="w")
        inf=ctk.CTkFrame(f_kiri,fg_color="transparent");inf.grid(row=0,column=1,sticky="w",pady=(0,2))
        self.lbl_t=ctk.CTkLabel(inf,text="",font=("Segoe UI",14,"bold"),text_color="white",anchor="w");self.lbl_t.pack(side="left")
        self.btn_add=ctk.CTkButton(inf,text="➕",width=20,height=20,fg_color="transparent",hover_color="#2A2A2A",border_width=1.8,border_color="#808080",text_color="#FFFFFF",font=("Segoe UI",10,"bold"),corner_radius=10,command=self.pilih_pl)
        self.lbl_a=ctk.CTkLabel(f_kiri,text="",font=("Segoe UI",12),text_color="#B3B3B3",anchor="w");self.lbl_a.grid(row=1,column=1,sticky="w")
        
        # TENGAH
        f_tengah=ctk.CTkFrame(mc,fg_color="transparent");f_tengah.grid(row=0,column=1,sticky="ew")
        ctrl_box=ctk.CTkFrame(f_tengah,fg_color="transparent");ctrl_box.pack(pady=(0,5),anchor="center")
        def b_kpcl(txt,cmd):return ctk.CTkButton(ctrl_box,text=txt,command=cmd,fg_color="transparent",text_color="#B3B3B3",hover_color="#1A1A1A",width=32,height=32,font=("Segoe UI",16))
        self.b_shuf=b_kpcl("🔀",cb_sh);self.b_shuf.pack(side="left",padx=8)
        b_kpcl("⏮",cb_pr).pack(side="left",padx=8)
        self.b_play=ctk.CTkButton(ctrl_box,text="▶",width=40,height=40,corner_radius=20,fg_color="white",text_color="black",hover_color="#E0E0E0",font=("Arial",15,"bold"),command=cb_pl);self.b_play.pack(side="left",padx=8)
        b_kpcl("⏭",cb_nx).pack(side="left",padx=8)
        self.b_rep=b_kpcl("🔁",cb_rp);self.b_rep.pack(side="left",padx=8)
        p_box=ctk.CTkFrame(f_tengah,fg_color="transparent");p_box.pack(fill="x",pady=0);p_box.grid_columnconfigure(1,weight=1)
        self.l_cur=ctk.CTkLabel(p_box,text="0:00",font=("Segoe UI",10),text_color="#B3B3B3",width=40);self.l_cur.grid(row=0,column=0,padx=(0,8))
        
        # SEEKABLE SLIDER dengan event binding
        self.prog=ctk.CTkSlider(p_box,height=6,progress_color="white",fg_color="#4D4D4D",button_color="white",button_hover_color="#1DB954",from_=0,to=100,number_of_steps=100)
        self.prog.grid(row=0,column=1,sticky="ew");self.prog.set(0)
        
        # Bind mouse events untuk detect user drag
        self.prog.bind("<Button-1>",self._start_seek)
        self.prog.bind("<ButtonRelease-1>",self._end_seek)
        
        self.l_tot=ctk.CTkLabel(p_box,text="0:00",font=("Segoe UI",10),text_color="#B3B3B3",width=40);self.l_tot.grid(row=0,column=2,padx=(8,0))
        
        # KANAN - VOLUME
        f_kanan=ctk.CTkFrame(mc,fg_color="transparent");f_kanan.grid(row=0,column=2,sticky="e",padx=(0,10))
        ctk.CTkLabel(f_kanan,text="🔊",font=("Segoe UI",16),text_color="#B3B3B3").pack(side="left",padx=(0,8))
        self.vol=ctk.CTkSlider(f_kanan,width=100,height=4,progress_color="white",fg_color="#4D4D4D",button_color="white",button_hover_color="#E0E0E0",from_=0,to=100,command=self._on_volume)
        self.vol.set(70);self.vol.pack(side="left")
        self._on_volume(70)

    def _start_seek(self,e):
        self._user_seeking=True

    def _end_seek(self,e):
        if self.cb_seek and self.cur_s and self._tot_dur>0:
            val=self.prog.get()
            new_time=(val/100)*self._tot_dur
            self.cb_seek(new_time)
            # Update tampilan langsung
            self.l_cur.configure(text=self._fmt(new_time))
        self._user_seeking=False

    def _fmt(self,x):
        m=int(x//60);s=int(x%60);return f"{m}:{s:02d}"

    def _on_volume(self,val):
        try:
            import pygame
            pygame.mixer.music.set_volume(val/100)
        except:pass

    def pilih_pl(self):
        if not self.cur_s or not self.pm:return
        from tkinter import Toplevel,messagebox
        lst=self.pm.getAllPlaylists()
        if not lst:messagebox.showinfo("Wetsss","Bikin playlist dulu gih.");return
        d=Toplevel(self);d.title("Masukin ke...");d.geometry("350x400");d.transient(self);d.grab_set();d.configure(bg="#282828");d.resizable(False,False)
        c=ctk.CTkFrame(d,fg_color="#282828");c.pack(fill="both",expand=True,padx=20,pady=20)
        ctk.CTkLabel(c,text="Pilih Playlist",font=("Segoe UI",18,"bold"),text_color="white").pack(pady=(0,15))
        ctk.CTkLabel(c,text=f'Masukin "{self.cur_s.title}"',font=("Segoe UI",11),text_color="#B3B3B3").pack(pady=(0,20))
        scr=ctk.CTkScrollableFrame(c,fg_color="#1A1A1A",height=250);scr.pack(fill="both",expand=True)
        def gas(nm):self.pm.addSongToPlaylist(nm,self.cur_s);d.destroy()
        for p in lst:
            fr=ctk.CTkFrame(scr,fg_color="transparent");fr.pack(fill="x",pady=3,padx=5)
            ctk.CTkButton(fr,text=p,fg_color="transparent",hover_color="#333333",text_color="white",anchor="w",font=("Segoe UI",12),command=lambda n=p:gas(n)).pack(fill="x",ipady=8)
        ctk.CTkButton(c,text="Gajadi",fg_color="transparent",border_width=1,border_color="#666666",hover_color="#333333",command=d.destroy).pack(pady=(15,0))

    def update_state(self,s,playing):
        if s:
            self.cur_s=s
            t=s.title if len(s.title)<=25 else s.title[:22]+"...";a=s.artist if len(s.artist)<=25 else s.artist[:22]+"..."
            self.lbl_t.configure(text=t);self.lbl_a.configure(text=a);self.btn_add.pack(side="left",padx=(6,0),pady=(2,0))
            ic="⏸" if playing else "▶";self.b_play.configure(text=ic,width=40,height=40)
        else:
            self.cur_s=None;self.lbl_t.configure(text="");self.lbl_a.configure(text="");self.btn_add.pack_forget()
            self.b_play.configure(text="▶");self.l_cur.configure(text="0:00");self.l_tot.configure(text="0:00");self.prog.set(0)

    def update_timer(self,el,tot):
        self._tot_dur=tot
        # Jangan update slider jika user sedang drag
        if self._user_seeking:return
        self.l_cur.configure(text=self._fmt(el));self.l_tot.configure(text=self._fmt(tot))
        if tot>0:self.prog.set((el/tot)*100)
        else:self.prog.set(0)

    def update_shuffle_repeat(self,shuf,rep):
        if shuf:self.b_shuf.configure(text_color="#1DB954")
        else:self.b_shuf.configure(text_color="#B3B3B3")
        if rep=='one':self.b_rep.configure(text="🔂",text_color="#1DB954")
        elif rep=='all':self.b_rep.configure(text="🔁",text_color="#1DB954")
        else:self.b_rep.configure(text="🔁",text_color="#B3B3B3")