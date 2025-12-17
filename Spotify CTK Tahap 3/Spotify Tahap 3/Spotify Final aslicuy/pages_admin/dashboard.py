# dashboard admin
import customtkinter as ctk

def render_dashboard(p,lib,c):
    scr=ctk.CTkScrollableFrame(p,fg_color="transparent");scr.pack(fill="both",expand=True)
    ctk.CTkLabel(scr,text="Dashboard Admin",font=("Segoe UI",24,"bold"),text_color=c["text_head"]).pack(pady=20,padx=20,anchor="w")
    all_s=lib.getAllSongs();tot=len(all_s);gens=set(x.genre for x in all_s);arts=set(x.artist for x in all_s)
    dur=sum(x.duration for x in all_s);h=dur//3600;m=(dur%3600)//60
    cf=ctk.CTkFrame(scr,fg_color="transparent");cf.pack(fill="x",padx=15)
    def bikin(par,t,v,col,ic):
        card=ctk.CTkFrame(par,fg_color=col,corner_radius=10);card.pack(side="left",fill="both",expand=True,padx=5)
        ctk.CTkLabel(card,text=ic,font=("Segoe UI",30)).pack(pady=(15,0))
        ctk.CTkLabel(card,text=str(v),font=("Segoe UI",32,"bold"),text_color="white").pack()
        ctk.CTkLabel(card,text=t,font=("Segoe UI",14),text_color="#EFEFEF").pack(pady=(0,15))
    bikin(cf,"Total Lagu",tot,c["primary"],"🎵");bikin(cf,"Total Genre",len(gens),"#28A745","🎷");bikin(cf,"Total Artis",len(arts),"#6F42C1","🎤");bikin(cf,"Total Durasi",f"{h}h {m}m","#FD7E14","⏱")
    ctk.CTkLabel(scr,text="🌟 Top 5 Artis (Berdasarkan Jumlah Lagu)",font=("Segoe UI",16,"bold"),text_color="#555").pack(pady=(30,10),padx=20,anchor="w")
    taf=ctk.CTkFrame(scr,fg_color="white",corner_radius=10);taf.pack(fill="x",padx=20,pady=(0,10))
    cnt={};[cnt.update({s.artist:cnt.get(s.artist,0)+1}) for s in all_s];srtd=sorted(cnt.items(),key=lambda x:x[1],reverse=True)[:5]
    if srtd:
        for i,(a,num) in enumerate(srtd,1):
            ar=ctk.CTkFrame(taf,fg_color="transparent");ar.pack(fill="x",padx=15,pady=8)
            ctk.CTkLabel(ar,text=f"#{i}",font=("Segoe UI",14,"bold"),text_color=c["primary"],width=40).pack(side="left")
            ctk.CTkLabel(ar,text=a,font=("Segoe UI",14),text_color="#333",anchor="w").pack(side="left",fill="x",expand=True,padx=10)
            ctk.CTkLabel(ar,text=f"{num} lagu",font=("Segoe UI",12),text_color="#666").pack(side="right")
    ctk.CTkLabel(scr,text="📊 Distribusi Genre",font=("Segoe UI",16,"bold"),text_color="#555").pack(pady=(20,10),padx=20,anchor="w")
    gf=ctk.CTkFrame(scr,fg_color="white",corner_radius=10);gf.pack(fill="x",padx=20,pady=(0,10))
    g_cnt={};[g_cnt.update({s.genre:g_cnt.get(s.genre,0)+1}) for s in all_s];s_gen=sorted(g_cnt.items(),key=lambda x:x[1],reverse=True)
    g_cols=["#007BFF","#28A745","#FD7E14","#6F42C1","#DC3545","#17A2B8"]
    if s_gen:
        for i,(g,num) in enumerate(s_gen[:6]):
            gr=ctk.CTkFrame(gf,fg_color="transparent");gr.pack(fill="x",padx=15,pady=6)
            ctk.CTkFrame(gr,fg_color=g_cols[i%len(g_cols)],width=20,height=20,corner_radius=3).pack(side="left",padx=(0,10))
            ctk.CTkLabel(gr,text=g,font=("Segoe UI",13),text_color="#333",anchor="w",width=150).pack(side="left")
            bg=ctk.CTkFrame(gr,fg_color="#E9ECEF",height=20,corner_radius=10);bg.pack(side="left",fill="x",expand=True,padx=5)
            pct=(num/tot)*100;fill=ctk.CTkFrame(bg,fg_color=g_cols[i%len(g_cols)],height=20,corner_radius=10);fill.place(relx=0,rely=0,relwidth=pct/100,relheight=1)
            ctk.CTkLabel(gr,text=f"{num} ({pct:.1f}%)",font=("Segoe UI",11),text_color="#666",width=100).pack(side="right")
    ctk.CTkLabel(scr,text="🆕 Lagu Terbaru Ditambahkan",font=("Segoe UI",16,"bold"),text_color="#555").pack(pady=(20,10),padx=20,anchor="w")
    rf=ctk.CTkFrame(scr,fg_color="white",corner_radius=10);rf.pack(fill="x",padx=20,pady=(0,20))
    last=sorted(all_s,key=lambda s:s.id,reverse=True)[:5]
    for s in last:
        sr=ctk.CTkFrame(rf,fg_color="transparent");sr.pack(fill="x",padx=15,pady=6)
        ctk.CTkLabel(sr,text="🎵",font=("Segoe UI",16)).pack(side="left",padx=(0,10))
        inf=ctk.CTkFrame(sr,fg_color="transparent");inf.pack(side="left",fill="x",expand=True)
        ctk.CTkLabel(inf,text=s.title,font=("Segoe UI",13,"bold"),text_color="#333",anchor="w").pack(fill="x")
        ctk.CTkLabel(inf,text=f"{s.artist} • {s.genre} • {s.year}",font=("Segoe UI",11),text_color="#666",anchor="w").pack(fill="x")
