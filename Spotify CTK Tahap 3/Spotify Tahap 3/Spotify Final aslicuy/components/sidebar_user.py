# sidebar user
import customtkinter as ctk

def SidebarUser(p,c,cb_h,cb_cp,cb_sp,pm,cur="home"):
    f=ctk.CTkFrame(p,width=240,fg_color=c["bg_sidebar"],corner_radius=0)
    xx=ctk.CTkFrame(f,fg_color="transparent");xx.pack(pady=(25,30),padx=20,anchor="w")
    ctk.CTkLabel(xx,text="🎵",font=("Segoe UI",28)).pack(side="left")
    ctk.CTkLabel(xx,text="MyMusic",font=("Segoe UI",22,"bold"),text_color="white").pack(side="left",padx=10)
    def btn(txt,ic,cmd,id):
        act=(cur==id)
        b=ctk.CTkButton(f,text=f"  {ic}   {txt}",anchor="w",font=("Segoe UI",14,"bold" if act else "normal"),fg_color=c["primary"] if act else "transparent",text_color="white" if act else "#B3B3B3",hover_color=c["hover"],height=40,width=200,command=cmd)
        b.pack(pady=2,padx=10);return b
    btn("Home","🏠",cb_h,"home");btn("Tambah Playlist","➕",cb_cp,"create_playlist")
    ctk.CTkFrame(f,height=2,fg_color="#444").pack(fill="x",padx=20,pady=10)
    ctk.CTkLabel(f,text="YOUR PLAYLIST",text_color="#555",font=("Consolas",15, "bold")).pack(anchor="w",padx=25)
    for pl in pm.getAllPlaylists():
        ic="📚" if pl=="Koleksi Saya" else "🎵"
        btn(pl,ic,lambda n=pl:cb_sp(n),f"playlist_{pl}")
    return f