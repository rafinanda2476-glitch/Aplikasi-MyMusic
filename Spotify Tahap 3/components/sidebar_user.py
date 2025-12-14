import customtkinter as ctk

def SidebarUser(parent, colors, on_home, on_create_playlist, on_select_playlist, playlist_manager, active_page="home"):
    # Gunakan warna dari colors["bg_sidebar"]
    frame = ctk.CTkFrame(parent, width=240, fg_color=colors["bg_sidebar"], corner_radius=0)
    
    logo_frame = ctk.CTkFrame(frame, fg_color="transparent")
    logo_frame.pack(pady=(25, 30), padx=20, anchor="w")
    ctk.CTkLabel(logo_frame, text="🎵", font=("Segoe UI", 28)).pack(side="left")
    ctk.CTkLabel(logo_frame, text="MyMusic", font=("Segoe UI", 22, "bold"), text_color="white").pack(side="left", padx=10)

    def create_menu_btn(text, icon, command, page_id):
        is_active = (active_page == page_id)
        btn = ctk.CTkButton(
            frame, 
            text=f"  {icon}   {text}", 
            anchor="w",
            font=("Segoe UI", 14, "bold" if is_active else "normal"),
            # Gunakan colors["primary"] jika aktif
            fg_color=colors["primary"] if is_active else "transparent",
            text_color="white" if is_active else "#B3B3B3",
            hover_color=colors["hover"],
            height=40,
            width=200,
            command=command
        )
        btn.pack(pady=2, padx=10)
        return btn

    # Static menu items
    create_menu_btn("Home", "🏠", on_home, "home")
    create_menu_btn("Tambah Playlist", "➕", on_create_playlist, "create_playlist")
    
    # Separator
    separator = ctk.CTkFrame(frame, height=2, fg_color="#444")
    separator.pack(fill="x", padx=20, pady=10)
    
    # Dynamic playlist items
    playlists = playlist_manager.getAllPlaylists()
    for pl_name in playlists:
        icon = "📚" if pl_name == "Koleksi Saya" else "🎵"
        page_id = f"playlist_{pl_name}"
        create_menu_btn(pl_name, icon, 
                       lambda name=pl_name: on_select_playlist(name), 
                       page_id)

    return frame