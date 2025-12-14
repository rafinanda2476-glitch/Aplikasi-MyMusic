import customtkinter as ctk

def TopBar(parent, logout_callback, colors):
    frame = ctk.CTkFrame(parent, fg_color="white", height=60, corner_radius=0)
    
    # Logo text kiri
    ctk.CTkLabel(frame, text="MyMusic", font=("Segoe UI", 18, "bold"), text_color=colors["primary"]).pack(side="left", padx=20)

    # Tombol Logout Kanan (Tanpa icon akun)
    ctk.CTkButton(frame, text="Keluar", width=80, fg_color="#FFEEED", text_color="red", 
                  hover_color="#FFDDD9", command=logout_callback).pack(side="right", padx=20, pady=10)

    return frame