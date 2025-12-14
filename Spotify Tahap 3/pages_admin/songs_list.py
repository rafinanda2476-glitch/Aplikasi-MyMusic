import customtkinter as ctk

def render_songs_list(parent, library, colors, on_edit, on_delete):
    # Header with search and sort
    header_frame = ctk.CTkFrame(parent, fg_color="transparent")
    header_frame.pack(fill="x", padx=20, pady=10)
    
    ctk.CTkLabel(header_frame, text="Database Lagu", font=("Segoe UI", 20, "bold"), 
                text_color=colors["text_head"]).pack(side="left")
    
    # Search box
    search_var = ctk.StringVar()
    search_entry = ctk.CTkEntry(header_frame, textvariable=search_var, 
                                placeholder_text="Cari judul atau artis...", width=250, height=35)
    search_entry.pack(side="right", padx=5)
    
    # Sort dropdown
    sort_var = ctk.StringVar(value="title")
    sort_options = ["title", "artist", "year", "genre"]
    
    ctk.CTkLabel(header_frame, text="Search:", font=("Segoe UI", 12)).pack(side="right", padx=5)
    sort_menu = ctk.CTkOptionMenu(header_frame, variable=sort_var, values=sort_options,
                                   width=120, fg_color=colors["primary"])
    sort_menu.pack(side="right", padx=5)

    # Container for dynamic content
    content_container = ctk.CTkFrame(parent, fg_color="transparent")
    content_container.pack(fill="both", expand=True, padx=15, pady=5)
    
    # Pagination state
    current_page = [1]  # Using list to allow modification in nested functions
    items_per_page = 50

    def render_table(sort_by="title", search_query="", page=1):
        # Clear existing content
        for w in content_container.winfo_children():
            w.destroy()
        
        # Grid configuration function
        def apply_grid_config(frame):
            frame.grid_columnconfigure(0, weight=1)  # No (sequential)
            frame.grid_columnconfigure(1, weight=4)  # Judul
            frame.grid_columnconfigure(2, weight=3)  # Artis
            frame.grid_columnconfigure(3, weight=2)  # Genre
            frame.grid_columnconfigure(4, weight=1)  # Tahun
            frame.grid_columnconfigure(5, weight=2)  # Durasi
            frame.grid_columnconfigure(6, weight=2)  # Aksi

        # Header row
        header = ctk.CTkFrame(content_container, fg_color="#E0E0E0", height=40, corner_radius=5)
        header.pack(fill="x", pady=(0, 5))
        apply_grid_config(header)

        h_font = ("Arial", 11, "bold")
        ctk.CTkLabel(header, text="NO", font=h_font).grid(row=0, column=0, pady=10)
        ctk.CTkLabel(header, text="JUDUL", font=h_font, anchor="w").grid(row=0, column=1, pady=10, padx=5, sticky="ew")
        ctk.CTkLabel(header, text="ARTIS", font=h_font, anchor="w").grid(row=0, column=2, pady=10, padx=5, sticky="ew")
        ctk.CTkLabel(header, text="GENRE", font=h_font, anchor="w").grid(row=0, column=3, pady=10, padx=5, sticky="ew")
        ctk.CTkLabel(header, text="TAHUN", font=h_font).grid(row=0, column=4, pady=10)
        ctk.CTkLabel(header, text="DURASI", font=h_font).grid(row=0, column=5, pady=10)
        ctk.CTkLabel(header, text="AKSI", font=h_font).grid(row=0, column=6, pady=10)

        # Scrollable list
        scroll = ctk.CTkScrollableFrame(content_container, fg_color="transparent")
        scroll.pack(fill="both", expand=True)

        # Get sorted songs
        songs = library.getSortedSongs(sort_by)
        
        # Apply search filter
        if search_query.strip():
            q = search_query.lower()
            songs = [s for s in songs if q in s.title.lower() or q in s.artist.lower()]

        # Pagination calculation
        total_songs = len(songs)
        total_pages = max(1, (total_songs + items_per_page - 1) // items_per_page)
        current_page[0] = min(page, total_pages)  # Ensure page is valid
        
        start_idx = (current_page[0] - 1) * items_per_page
        end_idx = min(start_idx + items_per_page, total_songs)
        page_songs = songs[start_idx:end_idx]

        # Text limiter function
        def limit_text(txt, max_len):
            s = str(txt)
            if len(s) > max_len:
                return s[:max_len-3] + "..."
            return s
        
        # Format duration as MM:SS
        def format_duration(seconds):
            mins = seconds // 60
            secs = seconds % 60
            return f"{mins}:{secs:02d}"

        if not page_songs:
            ctk.CTkLabel(scroll, text="Tidak ada data yang cocok.", text_color="gray").pack(pady=20)
        else:
            for idx, s in enumerate(page_songs, start=start_idx + 1):  # Sequential numbering
                row = ctk.CTkFrame(scroll, fg_color="white", corner_radius=5)
                row.pack(fill="x", pady=2)
                apply_grid_config(row)

                # Render columns with sequential number
                ctk.CTkLabel(row, text=str(idx), text_color="gray").grid(row=0, column=0, pady=8)
                ctk.CTkLabel(row, text=limit_text(s.title, 30), text_color="#333", anchor="w").grid(row=0, column=1, pady=8, padx=5, sticky="ew")
                ctk.CTkLabel(row, text=limit_text(s.artist, 20), text_color="gray", anchor="w").grid(row=0, column=2, pady=8, padx=5, sticky="ew")
                ctk.CTkLabel(row, text=limit_text(s.genre, 12), text_color="gray", anchor="w").grid(row=0, column=3, pady=8, padx=5, sticky="ew")
                ctk.CTkLabel(row, text=str(s.year), text_color="gray").grid(row=0, column=4, pady=8)
                ctk.CTkLabel(row, text=format_duration(s.duration), text_color="gray").grid(row=0, column=5, pady=8)

                # Action buttons
                act_frame = ctk.CTkFrame(row, fg_color="transparent")
                act_frame.grid(row=0, column=6, pady=5)
                
                ctk.CTkButton(act_frame, text="Edit", width=40, height=24, fg_color=colors["primary"], 
                             font=("Arial", 10), command=lambda sid=s.id: on_edit(sid)).pack(side="left", padx=2)
                ctk.CTkButton(act_frame, text="Hapus", width=40, height=24, fg_color="#FFEEEE", 
                             text_color="red", hover_color="#FFDDDD", font=("Arial", 10),
                             command=lambda sid=s.id: on_delete(sid)).pack(side="left", padx=2)
        
        # Pagination controls
        if total_pages > 1:
            pagination_frame = ctk.CTkFrame(content_container, fg_color="transparent")
            pagination_frame.pack(fill="x", pady=10)
            
            # Info text
            info_text = f"Halaman {current_page[0]} dari {total_pages} | Menampilkan {start_idx + 1}-{end_idx} dari {total_songs} lagu"
            ctk.CTkLabel(pagination_frame, text=info_text, text_color="gray").pack(side="left", padx=20)
            
            # Previous button
            btn_prev = ctk.CTkButton(pagination_frame, text="◀ Prev", width=80, height=30,
                                    fg_color=colors["primary"] if current_page[0] > 1 else "gray",
                                    command=lambda: change_page(current_page[0] - 1) if current_page[0] > 1 else None)
            btn_prev.pack(side="right", padx=5)
            
            # Next button  
            btn_next = ctk.CTkButton(pagination_frame, text="Next ▶", width=80, height=30,
                                    fg_color=colors["primary"] if current_page[0] < total_pages else "gray",
                                    command=lambda: change_page(current_page[0] + 1) if current_page[0] < total_pages else None)
            btn_next.pack(side="right", padx=5)

    def change_page(new_page):
        render_table(sort_var.get(), search_var.get(), new_page)

    # Initial render
    render_table("title", "", 1)
    
    # Bind sort change
    def on_sort_change(*args):
        current_page[0] = 1  # Reset to page 1 on sort change
        render_table(sort_var.get(), search_var.get(), 1)
    
    sort_var.trace_add("write", on_sort_change)
    
    # Bind search with debounce (300ms delay)
    search_timer = None
    def on_search_change(*args):
        nonlocal search_timer
        if search_timer:
            parent.after_cancel(search_timer)
        current_page[0] = 1  # Reset to page 1 on search
        search_timer = parent.after(300, lambda: render_table(sort_var.get(), search_var.get(), 1))
    
    search_var.trace_add("write", on_search_change)
