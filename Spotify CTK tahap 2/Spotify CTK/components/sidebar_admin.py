import customtkinter as ctk

# Tambahkan parameter 'colors'
def SidebarAdmin(parent, colors, on_dashboard, on_songs, on_add, on_import):
    # Gunakan colors["bg_sidebar"]
    frame = ctk.CTkFrame(parent, width=240, fg_color=colors["bg_sidebar"], corner_radius=0)
    
    ctk.CTkLabel(frame, text="ADMIN PANEL", font=("Segoe UI", 16, "bold"), text_color=colors["primary"]).pack(pady=(30, 10), padx=20, anchor="w")
    ctk.CTkLabel(frame, text="Manage Music", font=("Segoe UI", 12), text_color="gray").pack(pady=(0, 20), padx=20, anchor="w")

    def create_admin_btn(text, icon, command):
        btn = ctk.CTkButton(
            frame, 
            text=f"{icon}  {text}", 
            anchor="w",
            font=("Segoe UI", 13),
            fg_color="transparent",
            text_color="#E0E0E0",
            hover_color=colors["hover"],
            height=38,
            width=210,
            command=command
        )
        btn.pack(pady=2, padx=10)

    create_admin_btn("Dashboard", "📊", on_dashboard)
    create_admin_btn("Database Lagu", "💿", on_songs)
    create_admin_btn("Tambah Baru", "➕", on_add)
    create_admin_btn("Import CSV", "📥", on_import)

    return frame