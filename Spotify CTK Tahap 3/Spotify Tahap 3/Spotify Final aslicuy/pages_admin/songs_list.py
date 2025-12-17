# songs list admin
import customtkinter as ctk

def render_songs_list(p,lib,c,cb_edit,cb_del):
    h=ctk.CTkFrame(p,fg_color="transparent");h.pack(fill="x",padx=20,pady=10)
    ctk.CTkLabel(h,text="Database Lagu",font=("Segoe UI",20,"bold"),text_color=c["text_head"]).pack(side="left")
    sc=ctk.CTkFrame(h,fg_color="transparent");sc.pack(side="right")
    ctk.CTkLabel(sc,text="Urutkan:",font=("Segoe UI",12),text_color="#666").pack(side="left",padx=(0,8))
    sv=ctk.StringVar(value="");lbls=["Judul","Artis","Tahun","Genre"];maps={"Judul":"title","Artis":"artist","Tahun":"year","Genre":"genre"};cur_srt=["title"]
    sm=ctk.CTkOptionMenu(sc,variable=sv,values=lbls,width=120,height=32,fg_color=c["primary"],button_color=c["primary"],button_hover_color=c["hover"],dropdown_fg_color="white",dropdown_hover_color="#F0F0F0",font=("Segoe UI",12));sm.pack(side="left");sm.set("Urutkan")
    scf=ctk.CTkFrame(p,fg_color="transparent");scf.pack(fill="x",padx=20,pady=(0,10))
    s_var=ctk.StringVar();s_con=ctk.CTkFrame(scf,fg_color="transparent");s_con.pack(expand=True)
    ctk.CTkLabel(s_con,text="🔍",font=("Segoe UI",16)).pack(side="left",padx=(0,8))
    se=ctk.CTkEntry(s_con,textvariable=s_var,placeholder_text="Cari...",width=500,height=38,font=("Segoe UI",12),fg_color="#F5F5F5",border_width=2,border_color=c["primary"]);se.pack(side="left")
    cont=ctk.CTkFrame(p,fg_color="transparent");cont.pack(fill="both",expand=True,padx=15,pady=5)
    cur_pg=[1];per_pg=50
    def render(sby="title",q="",pg=1):
        for x in cont.winfo_children():x.destroy()
        def atur_grid(f):[f.grid_columnconfigure(i,weight=w,uniform="c") for i,w in enumerate([1,5,4,3,2,2,3])]
        hd=ctk.CTkFrame(cont,fg_color="#E0E0E0",height=40,corner_radius=5);hd.pack(fill="x",pady=(0,5));atur_grid(hd)
        font_h=("Segoe UI",11,"bold")
        hdrs=["NO","JUDUL","ARTIS","GENRE","TAHUN","DURASI","AKSI"]
        for i,t in enumerate(hdrs):
            anc="w" if i in [1,2,3] else "center"
            if i in [1,2,3]:px=(10,10)
            elif i==4:px=(0,25)
            else:px=(0,0)
            ctk.CTkLabel(hd,text=t,font=font_h,anchor=anc).grid(row=0,column=i,pady=10,padx=px,sticky="ew")
        scr=ctk.CTkScrollableFrame(cont,fg_color="transparent");scr.pack(fill="both",expand=True)
        lgs=lib.getSortedSongs(sby)
        if q.strip():qq=q.lower();lgs=[x for x in lgs if qq in x.title.lower() or qq in x.artist.lower()]
        tot_s=len(lgs);tot_p=max(1,(tot_s+per_pg-1)//per_pg);cur_pg[0]=min(pg,tot_p);st=(cur_pg[0]-1)*per_pg;en=min(st+per_pg,tot_s);pg_s=lgs[st:en]
        def fmt(x):return f"{x//60}:{x%60:02d}"
        if not pg_s:ctk.CTkLabel(scr,text="Kosong bos.",text_color="gray").pack(pady=20)
        else:
            for idx,s in enumerate(pg_s,start=st+1):
                row=ctk.CTkFrame(scr,fg_color="white",corner_radius=5);row.pack(fill="x",pady=2);atur_grid(row)
                ctk.CTkLabel(row,text=str(idx),text_color="gray").grid(row=0,column=0,pady=8,sticky="ew")
                ctk.CTkLabel(row,text=s.title[:37]+"..." if len(s.title)>40 else s.title,text_color="#333",anchor="w").grid(row=0,column=1,pady=8,padx=10,sticky="ew")
                ctk.CTkLabel(row,text=s.artist[:27]+"..." if len(s.artist)>30 else s.artist,text_color="gray",anchor="w").grid(row=0,column=2,pady=8,padx=10,sticky="ew")
                ctk.CTkLabel(row,text=s.genre,text_color="gray",anchor="w").grid(row=0,column=3,pady=8,padx=10,sticky="ew")
                ctk.CTkLabel(row,text=str(s.year),text_color="gray").grid(row=0,column=4,pady=8,padx=(0,25),sticky="ew")
                ctk.CTkLabel(row,text=fmt(s.duration),text_color="gray").grid(row=0,column=5,pady=8,sticky="ew")
                act=ctk.CTkFrame(row,fg_color="transparent");act.grid(row=0,column=6,pady=5)
                ctk.CTkButton(act,text="Edit",width=40,height=24,fg_color=c["primary"],command=lambda id=s.id:cb_edit(id)).pack(side="left",padx=2)
                ctk.CTkButton(act,text="Hapus",width=40,height=24,fg_color="#FFEEEE",text_color="red",hover_color="#FFDDDD",command=lambda id=s.id:cb_del(id)).pack(side="left",padx=2)
        if tot_p>1:
            pf=ctk.CTkFrame(cont,fg_color="transparent");pf.pack(fill="x",pady=10)
            ctk.CTkLabel(pf,text=f"Hal {cur_pg[0]}/{tot_p} | {st+1}-{en} dari {tot_s}",text_color="gray").pack(side="left",padx=20)
            ctk.CTkButton(pf,text="Next ▶",width=80,height=30,fg_color=c["primary"] if cur_pg[0]<tot_p else "gray",command=lambda:ganti(cur_pg[0]+1) if cur_pg[0]<tot_p else None).pack(side="right",padx=5)
            ctk.CTkButton(pf,text="◀ Prev",width=80,height=30,fg_color=c["primary"] if cur_pg[0]>1 else "gray",command=lambda:ganti(cur_pg[0]-1) if cur_pg[0]>1 else None).pack(side="right",padx=5)
    def pilih_sort(l):iv=maps.get(l,"title");cur_srt[0]=iv;sm.configure(values=[x for x in lbls if x!=l]);cur_pg[0]=1;render(iv,s_var.get(),1);sv.set(l)
    sm.configure(command=pilih_sort)
    tmr=None
    def cari(*a):
        nonlocal tmr
        if tmr:p.after_cancel(tmr)
        tmr=p.after(300,lambda:render(cur_srt[0],s_var.get(),1))
    s_var.trace_add("write",cari)
    def ganti(n):render(cur_srt[0],s_var.get(),n)
    render("title","",1)
