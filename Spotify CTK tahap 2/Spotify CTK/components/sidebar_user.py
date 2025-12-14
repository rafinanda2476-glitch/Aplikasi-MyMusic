import customtkinter as ctk

# Tambahkan parameter 'colors'
def SidebarUser(parent, colors, on_home, on_search, on_playlist):
    # Gunakan warna dari colors["bg_sidebar"]
    frame = ctk.CTkFrame(parent, width=240, fg_color=colors["bg_sidebar"], corner_radius=0)
    
    logo_frame = ctk.CTkFrame(frame, fg_color="transparent")
    logo_frame.pack(pady=(25, 30), padx=20, anchor="w")
    ctk.CTkLabel(logo_frame, text="🎵", font=("Segoe UI", 28)).pack(side="left")
    ctk.CTkLabel(logo_frame, text="MyMusic", font=("Segoe UI", 22, "bold"), text_color="white").pack(side="left", padx=10)

    def create_menu_btn(text, icon, command, is_active=False):
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

    create_menu_btn("Home", "🏠", on_home, is_active=True) 
    create_menu_btn("Cari Lagu", "🔍", on_search)
    create_menu_btn("Koleksi Saya", "📚", on_playlist)

    ctk.CTkFrame(frame, fg_color="transparent").pack(expand=True)
    ctk.CTkLabel(frame, text="v1.0.0 Stable", text_color="#555", font=("Arial", 10)).pack(pady=10)

    return frame