import customtkinter as ctk

def SidebarAdmin(parent, colors, on_dashboard, on_songs, on_add, on_import, active_page="dashboard"):
    # Gunakan colors["bg_sidebar"]
    frame = ctk.CTkFrame(parent, width=240, fg_color=colors["bg_sidebar"], corner_radius=0)
    
    ctk.CTkLabel(frame, text="ADMIN PANEL", font=("Segoe UI", 16, "bold"), text_color=colors["primary"]).pack(pady=(30, 10), padx=20, anchor="w")
    ctk.CTkLabel(frame, text="Manage Music", font=("Segoe UI", 12), text_color="gray").pack(pady=(0, 20), padx=20, anchor="w")

    def create_admin_btn(text, icon, command, page_id):
        is_active = (active_page == page_id)
        btn = ctk.CTkButton(
            frame, 
            text=f"{icon}  {text}", 
            anchor="w",
            font=("Segoe UI", 13, "bold" if is_active else "normal"),
            fg_color=colors["primary"] if is_active else "transparent",
            text_color="white" if is_active else "#E0E0E0",
            hover_color=colors["hover"],
            height=38,
            width=210,
            command=command
        )
        btn.pack(pady=2, padx=10)

    create_admin_btn("Dashboard", "📊", on_dashboard, "dashboard")
    create_admin_btn("Database Lagu", "💿", on_songs, "songs")
    create_admin_btn("Tambah Baru", "➕", on_add, "add")
    create_admin_btn("Import CSV", "📥", on_import, "import")

    return frame
