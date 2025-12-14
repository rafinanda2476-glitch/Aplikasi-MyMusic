import customtkinter as ctk
from tkinter import messagebox, simpledialog

def render_create_playlist(parent, playlist_manager, colors, on_success):
    """Page for creating a new playlist"""
    
    # Scrollable container for the page
    scroll_container = ctk.CTkScrollableFrame(parent, fg_color="transparent")
    scroll_container.pack(expand=True, fill="both", padx=20, pady=20)
    
    # Center wrapper
    center_wrapper = ctk.CTkFrame(scroll_container, fg_color="transparent")
    center_wrapper.pack(expand=True, fill="both", pady=50)
    
    # Card in center
    card = ctk.CTkFrame(center_wrapper, fg_color="white", corner_radius=15)
    card.pack(pady=20, padx=50)
    
    # Header
    ctk.CTkLabel(card, text="➕ Buat Playlist Baru", 
                font=("Segoe UI", 24, "bold"), 
                text_color=colors["primary"]).pack(pady=(30, 10))
    
    ctk.CTkLabel(card, text="Beri nama playlist koleksi kamu", 
                font=("Segoe UI", 13), 
                text_color="gray").pack(pady=(0, 30))
    
    # Input container
    input_container = ctk.CTkFrame(card, fg_color="transparent")
    input_container.pack(pady=20, padx=40, fill="x")
    
    ctk.CTkLabel(input_container, text="Nama Playlist:", 
                font=("Segoe UI", 12, "bold"),
                text_color="#333").pack(anchor="w", pady=(0, 8))
    
    # Name entry
    name_var = ctk.StringVar()
    name_entry = ctk.CTkEntry(input_container, 
                             textvariable=name_var,
                             placeholder_text="Contoh: Lagu Santai, Workout, etc.",
                             height=45,
                             font=("Segoe UI", 14),
                             fg_color="#F5F5F5",
                             border_width=2,
                             border_color=colors["primary"])
    name_entry.pack(fill="x", pady=(0, 20))
    name_entry.focus()
    
    # Error label (hidden by default)
    error_label = ctk.CTkLabel(input_container, text="", 
                               text_color="red", 
                               font=("Segoe UI", 11))
    error_label.pack(pady=(0, 10))
    
    # Buttons
    button_container = ctk.CTkFrame(card, fg_color="transparent")
    button_container.pack(pady=20)
    
    def create_playlist():
        name = name_var.get().strip()
        
        if not name:
            error_label.configure(text="⚠️ Nama playlist tidak boleh kosong!")
            return
        
        if playlist_manager.createPlaylist(name):
            messagebox.showinfo("Sukses", f"Playlist '{name}' berhasil dibuat!")
            if on_success:
                on_success(name)  # Callback to switch to playlist page
        else:
            error_label.configure(text="⚠️ Playlist dengan nama ini sudah ada!")
    
    # Bind Enter key
    name_entry.bind("<Return>", lambda e: create_playlist())
    
    # Buat button
    ctk.CTkButton(button_container, text="Buat Playlist", 
                 width=150, height=40,
                 font=("Segoe UI", 14, "bold"),
                 fg_color=colors["primary"],
                 hover_color=colors["hover"],
                 command=create_playlist).pack(side="left", padx=5)
    
    # Batal button
    ctk.CTkButton(button_container, text="Batal", 
                 width=100, height=40,
                 font=("Segoe UI", 14),
                 fg_color="gray",
                 hover_color="#666",
                 command=lambda: on_success(None) if on_success else None).pack(side="left", padx=5)
    
    # Info text at bottom
    ctk.CTkLabel(card, text="💡 Kamu bisa menambahkan lagu dari halaman Search", 
                font=("Segoe UI", 10),
                text_color="#999").pack(side="bottom", pady=15)
