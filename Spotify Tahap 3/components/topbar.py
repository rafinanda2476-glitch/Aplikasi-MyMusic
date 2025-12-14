import customtkinter as ctk

def TopBar(parent, logout_callback, colors, on_search=None):
    frame = ctk.CTkFrame(parent, fg_color="white", height=60, corner_radius=0)
    
    # Logo text kiri
    ctk.CTkLabel(frame, text="MyMusic", font=("Segoe UI", 18, "bold"), text_color=colors["primary"]).pack(side="left", padx=20)

    # Search bar tengah (only for user role if on_search provided)
    if on_search:
        search_container = ctk.CTkFrame(frame, fg_color="transparent")
        search_container.pack(side="left", expand=True, padx=20)
        
        # Search icon
        ctk.CTkLabel(search_container, text="🔍", font=("Segoe UI", 16)).pack(side="left", padx=(0, 8))
        
        # Search entry
        search_var = ctk.StringVar()
        search_entry = ctk.CTkEntry(search_container, 
                                     textvariable=search_var,
                                     placeholder_text="Cari lagu atau artis...",
                                     width=400,
                                     height=35,
                                     fg_color="#F5F5F5",
                                     border_width=0)
        search_entry.pack(side="left")
        
        # Bind Enter key to search
        def perform_search(event=None):
            query = search_var.get().strip()
            if query or event is None:  # Allow empty search to show all
                on_search(query)
        
        search_entry.bind("<Return>", perform_search)

    # Tombol Logout Kanan (Tanpa icon akun)
    ctk.CTkButton(frame, text="Keluar", width=80, fg_color="#FFEEED", text_color="red", 
                  hover_color="#FFDDD9", command=logout_callback).pack(side="right", padx=20, pady=10)

    return frame