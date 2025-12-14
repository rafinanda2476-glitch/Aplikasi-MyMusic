import customtkinter as ctk
from tkinter import messagebox, simpledialog

def render_playlist(parent, library, playlist_manager, colors, on_play_context, on_remove, on_rename=None, on_delete=None):
    # Content container - no top bar, starts from top
    content_container = ctk.CTkFrame(parent, fg_color="transparent")
    content_container.pack(fill="both", expand=True, padx=15, pady=(5, 5))
    
    # Configure main grid - 2 rows
    content_container.grid_rowconfigure(0, weight=0)  # Header row
    content_container.grid_rowconfigure(1, weight=1)  # Song list row
    content_container.grid_columnconfigure(0, weight=1)
    
    def render_playlist_content():
        # Clear content
        for w in content_container.winfo_children():
            w.destroy()
        
        current_pl = playlist_manager.getCurrentPlaylist()
        if not current_pl:
            ctk.CTkLabel(content_container, text="Playlist tidak ditemukan", text_color="gray").grid(row=0, column=0, pady=20)
            return
        
        songs = current_pl.listSongs()
        
        # Menu functions
        def show_options_menu(event):
            """Show options menu when three-dots button is clicked."""
            import tkinter as tk
            
            # Create styled menu
            menu = tk.Menu(
                parent, 
                tearoff=0, 
                bg="#FFFFFF",
                fg="#333333",
                activebackground=colors["primary"],
                activeforeground="white",
                font=("Segoe UI", 12),
                relief="flat",
                bd=0,
                borderwidth=1,
                activeborderwidth=0
            )
            
            # Configure menu appearance
            menu.configure(
                relief="solid",
                borderwidth=1,
                background="white",
                foreground="#333"
            )
            
            def handle_rename():
                """Handle rename option with Spotify-style dialog."""
                from tkinter import Toplevel
                
                # Protect default playlist
                if current_pl.name == "Koleksi Saya":
                    messagebox.showwarning("Tidak Diizinkan", 
                                          "Playlist 'Koleksi Saya' tidak dapat diubah namanya.")
                    return
                
                # Create Spotify-style rename dialog
                dialog = Toplevel(parent)
                dialog.title("Edit details")
                dialog.geometry("500x300")
                dialog.transient(parent)
                dialog.grab_set()
                dialog.configure(bg="#282828")
                dialog.resizable(False, False)
                
                # Content with dark theme
                content = ctk.CTkFrame(dialog, fg_color="#282828")
                content.pack(fill="both", expand=True, padx=30, pady=15)
                
                # Title
                ctk.CTkLabel(content, text="Edit details", 
                            font=("Segoe UI", 20, "bold"), 
                            text_color="white").pack(anchor="w", pady=(0, 10))
                
                # Label
                ctk.CTkLabel(content, text="Name", 
                            font=("Segoe UI", 11, "bold"), 
                            text_color="white").pack(anchor="w", pady=(0, 5))
                
                # Input field - Spotify style
                name_var = ctk.StringVar(value=current_pl.name)
                entry = ctk.CTkEntry(content, textvariable=name_var, 
                                    height=38, font=("Segoe UI", 13),
                                    fg_color="#3E3E3E", 
                                    border_width=1,
                                    border_color="#535353",
                                    text_color="white")
                entry.pack(fill="x", pady=(0, 15))
                entry.focus()
                entry.select_range(0, 'end')
                
                # Buttons frame
                btn_frame = ctk.CTkFrame(content, fg_color="transparent")
                btn_frame.pack(fill="x")
                
                def do_rename():
                    new_name = name_var.get().strip()
                    if new_name:
                        success, message = playlist_manager.renamePlaylist(current_pl.name, new_name)
                        dialog.destroy()
                        if success:
                            if on_rename:
                                on_rename(new_name)
                        else:
                            messagebox.showerror("Error", message)
                    else:
                        messagebox.showwarning("Peringatan", "Nama playlist tidak boleh kosong!")
                
                # Done button (close without saving)
                ctk.CTkButton(btn_frame, text="Done", width=95, height=40,
                             fg_color="transparent",
                             border_width=1,
                             border_color="#727272",
                             text_color="white",
                             hover_color="#3E3E3E",
                             font=("Segoe UI", 13, "bold"),
                             corner_radius=50,
                             command=dialog.destroy).pack(side="left")
                
                # Spacer
                ctk.CTkFrame(btn_frame, fg_color="transparent").pack(side="left", expand=True)
                
                # Save button - Spotify green
                ctk.CTkButton(btn_frame, text="Save", width=115, height=40,
                             fg_color="#1DB954", 
                             hover_color="#1ed760",
                             text_color="black",
                             font=("Segoe UI", 14, "bold"),
                             corner_radius=50,
                             command=do_rename).pack(side="right")
                
                # Bind Enter key
                entry.bind("<Return>", lambda e: do_rename())
            
            def handle_delete():
                """Handle delete option with Spotify-style dialog."""
                from tkinter import Toplevel
                
                # Protect default playlist
                if current_pl.name == "Koleksi Saya":
                    messagebox.showwarning("Tidak Diizinkan", 
                                          "Playlist 'Koleksi Saya' tidak dapat dihapus.")
                    return
                
                # Create Spotify-style delete confirmation dialog
                dialog = Toplevel(parent)
                dialog.title("Delete playlist")
                dialog.geometry("450x220")
                dialog.transient(parent)
                dialog.grab_set()
                dialog.configure(bg="#282828")
                dialog.resizable(False, False)
                
                # Content centered
                content = ctk.CTkFrame(dialog, fg_color="#282828")
                content.pack(fill="both", expand=True, padx=30, pady=18)
                
                # Title centered
                ctk.CTkLabel(content, 
                            text="Delete from Your Library?",
                            font=("Segoe UI", 16, "bold"),
                            text_color="white").pack(pady=(0, 5))
                
                # Subtitle
                ctk.CTkLabel(content, 
                            text=f'This will delete "{current_pl.name}" from Your Library.',
                            font=("Segoe UI", 11),
                            text_color="#B3B3B3").pack(pady=(0, 12))
                
                # Buttons side by side - Spotify style
                btn_frame = ctk.CTkFrame(content, fg_color="transparent")
                btn_frame.pack()
                
                def do_delete():
                    playlist_name = current_pl.name
                    if playlist_manager.deletePlaylist(playlist_name):
                        dialog.destroy()
                        if on_delete:
                            on_delete()
                    else:
                        dialog.destroy()
                        messagebox.showerror("Error", "Gagal menghapus playlist.")
                
                ctk.CTkButton(btn_frame, text="Cancel", width=125, height=40,
                             fg_color="transparent",
                             border_width=1,
                             border_color="#727272",
                             text_color="white",
                             hover_color="#3E3E3E",
                             font=("Segoe UI", 13, "bold"),
                             corner_radius=50,
                             command=dialog.destroy).pack(side="left", padx=(0, 10))
                
                ctk.CTkButton(btn_frame, text="Delete", width=125, height=40,
                             fg_color="white",
                             text_color="black",
                             hover_color="#E0E0E0",
                             font=("Segoe UI", 13, "bold"),
                             corner_radius=50,
                             command=do_delete).pack(side="left")
            
            # Add menu items with icons and better spacing
            menu.add_command(
                label="Rename Playlist",
                command=handle_rename,
                compound="left",
                font=("Segoe UI", 11),
                foreground="#333"
            )
            
            # Add separator for visual distinction
            menu.add_separator()
            
            menu.add_command(
                label="Delete Playlist",
                command=handle_delete,
                compound="left",
                font=("Segoe UI", 11),
                foreground="#D32F2F"
            )
            
            try:
                menu.tk_popup(event.x_root, event.y_root)
            finally:
                menu.grab_release()
        
        # ROW 0: Simple clean header
        header_box = ctk.CTkFrame(
            content_container, 
            fg_color="white",
            corner_radius=10
        )
        header_box.grid(row=0, column=0, sticky="ew", pady=(0, 15))
        
        # Inner frame for playlist info
        info_frame = ctk.CTkFrame(header_box, fg_color="transparent")
        info_frame.pack(fill="x", padx=20, pady=15)
        
        # Playlist name row
        name_row = ctk.CTkFrame(info_frame, fg_color="transparent")
        name_row.pack(fill="x", anchor="w")
        
        # Simple playlist name
        ctk.CTkLabel(
            name_row,
            text=f"🎵 {current_pl.name}",
            font=("Segoe UI", 18, "bold"),
            text_color=colors["text_head"]
        ).pack(side="left")
        
        # Three-dots menu button
        menu_btn = ctk.CTkButton(
            name_row,
            text="⋮",
            width=30,
            height=30,
            font=("Segoe UI", 18),
            fg_color="transparent",
            text_color="#999",
            hover_color="#F5F5F5",
            cursor="hand2"
        )
        menu_btn.pack(side="left", padx=(8, 0))
        menu_btn.bind("<Button-1>", show_options_menu)
        
        # Simple song count
        ctk.CTkLabel(
            info_frame,
            text=f"{len(songs)} lagu",
            font=("Segoe UI", 12),
            text_color="#777"
        ).pack(anchor="w", pady=(5, 0))
        
        # ROW 1: Scrollable song list
        scroll = ctk.CTkScrollableFrame(content_container, fg_color="transparent")
        scroll.grid(row=1, column=0, sticky="nsew")
        
        if not songs:
            ctk.CTkLabel(scroll, text="Playlist masih kosong.\nTambahkan lagu dari halaman Cari Lagu.", 
                        text_color="gray", font=("Segoe UI", 13)).pack(pady=40)
            return
        
        # Format duration helper
        def format_duration(seconds):
            mins = seconds // 60
            secs = seconds % 60
            return f"{mins}:{secs:02d}"
        
        for i, s in enumerate(songs):
            # Simple clean row design
            row = ctk.CTkFrame(
                scroll, 
                fg_color="#F8F9FA",
                corner_radius=8
            )
            row.pack(fill="x", pady=3, padx=5)
            
            # Play button
            def play_this(idx=i):
                on_play_context(songs, idx)
            
            btn_play = ctk.CTkButton(
                row, 
                text="▶", 
                width=38, 
                height=38, 
                fg_color=colors["primary"],
                hover_color=colors["hover"],
                command=play_this,
                font=("Segoe UI", 14),
                corner_radius=8
            )
            btn_play.pack(side="left", padx=10, pady=8)
            
            # Info container
            info_frame = ctk.CTkFrame(row, fg_color="transparent")
            info_frame.pack(side="left", fill="x", expand=True, padx=5, pady=8)
            
            # Song title
            ctk.CTkLabel(
                info_frame, 
                text=s.title, 
                font=("Segoe UI", 13, "bold"), 
                text_color=colors["text_head"], 
                anchor="w"
            ).pack(anchor="w")
            
            # Metadata (simple, no icons)
            ctk.CTkLabel(
                info_frame, 
                text=f"{s.artist} • {s.genre} • {format_duration(s.duration)}", 
                font=("Segoe UI", 11), 
                text_color="#888",
                anchor="w"
            ).pack(anchor="w", pady=(2, 0))
            
            # Remove button
            ctk.CTkButton(
                row, 
                text="✕", 
                width=35, 
                height=35, 
                fg_color="#FFE5E5",
                text_color=colors["danger"], 
                hover_color="#FFCCCC",
                font=("Segoe UI", 14, "bold"),
                corner_radius=8,
                command=lambda sid=s.id: remove_from_playlist(sid)
            ).pack(side="right", padx=10, pady=8)
    
    def remove_from_playlist(song_id):
        current_pl_name = playlist_manager.current_playlist_name
        if playlist_manager.removeSongFromPlaylist(current_pl_name, song_id):
            render_playlist_content()
            if on_remove:
                on_remove(song_id)
    
    # Initial render
    render_playlist_content()
