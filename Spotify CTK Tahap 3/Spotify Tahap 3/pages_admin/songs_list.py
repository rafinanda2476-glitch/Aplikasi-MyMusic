import customtkinter as ctk

def render_songs_list(parent, library, colors, on_edit, on_delete):
    # --- HEADER SECTION ---
    header_frame = ctk.CTkFrame(parent, fg_color="transparent")
    header_frame.pack(fill="x", padx=20, pady=10)
    
    # Title
    ctk.CTkLabel(header_frame, text="Database Lagu", font=("Segoe UI", 20, "bold"), 
                 text_color=colors["text_head"]).pack(side="left")
    
    # Sort Container
    sort_container = ctk.CTkFrame(header_frame, fg_color="transparent")
    sort_container.pack(side="right")
    
    ctk.CTkLabel(sort_container, text="Urutkan:", font=("Segoe UI", 12), 
                 text_color="#666").pack(side="left", padx=(0,8))
    
    # --- KONFIGURASI SORTING (UBAH DI SINI) ---
    sort_var = ctk.StringVar(value="")
    
    # 1. List Label Menggunakan HURUF KAPITAL (Tampilan)
    all_labels = ["Judul", "Artis", "Tahun", "Genre"]
    
    # 2. Mapping Tampilan Kapital -> Nilai Internal Database
    label_to_value = {
        "Judul": "title", 
        "Artis": "artist", 
        "Tahun": "year", 
        "Genre": "genre"
    }

    # Variabel bantu untuk menyimpan status sorting internal saat ini (default: title)
    # Kita butuh ini agar fitur Search tahu kita sedang sorting berdasarkan apa
    current_sort_internal = ["title"] 

    # Dropdown Menu
    sort_menu = ctk.CTkOptionMenu(sort_container, variable=sort_var, 
                                   values=all_labels,
                                   width=120, height=32,
                                   fg_color=colors["primary"],
                                   button_color=colors["primary"],
                                   button_hover_color=colors["hover"],
                                   dropdown_fg_color="white",
                                   dropdown_hover_color="#F0F0F0",
                                   font=("Segoe UI", 12))
    sort_menu.pack(side="left")
    
    # Set tampilan awal tombol menjadi "URUTKAN" (bukan title/judul)
    sort_menu.set("Urutkan") 

    # --- SEARCH SECTION ---
    search_center_frame = ctk.CTkFrame(parent, fg_color="transparent")
    search_center_frame.pack(fill="x", padx=20, pady=(0,10))
    
    search_var = ctk.StringVar()
    
    search_container = ctk.CTkFrame(search_center_frame, fg_color="transparent")
    search_container.pack(expand=True)
    
    ctk.CTkLabel(search_container, text="🔍", font=("Segoe UI", 16)).pack(side="left", padx=(0,8))
    
    search_entry = ctk.CTkEntry(search_container, textvariable=search_var, 
                                placeholder_text="Cari berdasarkan judul atau artis...", 
                                width=500, height=38,
                                font=("Segoe UI", 12),
                                fg_color="#F5F5F5",
                                border_width=2,
                                border_color=colors["primary"])
    search_entry.pack(side="left")

    # --- CONTENT CONTAINER ---
    content_container = ctk.CTkFrame(parent, fg_color="transparent")
    content_container.pack(fill="both", expand=True, padx=15, pady=5)
    
    # Pagination state
    current_page = [1]
    items_per_page = 50
    
    # Forward references
    render_table_ref = None

    # --- FUNGSI RENDER TABEL ---
    def render_table(sort_by="title", search_query="", page=1):
        # Bersihkan konten lama
        for w in content_container.winfo_children():
            w.destroy()
        
        # Grid Config
        def apply_grid_config(frame):
            frame.grid_columnconfigure(0, weight=1, uniform="col")   # NO
            frame.grid_columnconfigure(1, weight=5, uniform="col")   # JUDUL
            frame.grid_columnconfigure(2, weight=4, uniform="col")   # ARTIS
            frame.grid_columnconfigure(3, weight=3, uniform="col")   # GENRE
            frame.grid_columnconfigure(4, weight=2, uniform="col")   # TAHUN
            frame.grid_columnconfigure(5, weight=2, uniform="col")   # DURASI
            frame.grid_columnconfigure(6, weight=3, uniform="col")   # AKSI

        # Header Row
        header = ctk.CTkFrame(content_container, fg_color="#E0E0E0", height=40, corner_radius=5)
        header.pack(fill="x", pady=(0, 5))
        apply_grid_config(header)

        h_font = ("Segoe UI", 11, "bold")
        ctk.CTkLabel(header, text="NO", font=h_font).grid(row=0, column=0, pady=10, sticky="ew")
        ctk.CTkLabel(header, text="JUDUL", font=h_font, anchor="w").grid(row=0, column=1, pady=10, padx=10, sticky="ew")
        ctk.CTkLabel(header, text="ARTIS", font=h_font, anchor="w").grid(row=0, column=2, pady=10, padx=10, sticky="ew")
        ctk.CTkLabel(header, text="GENRE", font=h_font, anchor="w").grid(row=0, column=3, pady=10, padx=10, sticky="ew")
        ctk.CTkLabel(header, text="TAHUN", font=h_font).grid(row=0, column=4, pady=10, sticky="ew")
        ctk.CTkLabel(header, text="DURASI", font=h_font).grid(row=0, column=5, pady=10, sticky="ew")
        ctk.CTkLabel(header, text="AKSI", font=h_font).grid(row=0, column=6, pady=10, sticky="ew")

        # Scrollable Area
        scroll = ctk.CTkScrollableFrame(content_container, fg_color="transparent")
        scroll.pack(fill="both", expand=True)

        # 1. Ambil data (Logika sorting menggunakan nilai internal 'sort_by' misal: "title")
        songs = library.getSortedSongs(sort_by)
        
        # 2. Filter Search
        if search_query.strip():
            q = search_query.lower()
            songs = [s for s in songs if q in s.title.lower() or q in s.artist.lower()]

        # 3. Pagination
        total_songs = len(songs)
        total_pages = max(1, (total_songs + items_per_page - 1) // items_per_page)
        current_page[0] = min(page, total_pages)
        
        start_idx = (current_page[0] - 1) * items_per_page
        end_idx = min(start_idx + items_per_page, total_songs)
        page_songs = songs[start_idx:end_idx]

        # Helper Functions
        def limit_text(txt, max_len):
            s = str(txt)
            return s[:max_len-3] + "..." if len(s) > max_len else s
        
        def format_duration(seconds):
            return f"{seconds // 60}:{seconds % 60:02d}"

        # Render Rows
        if not page_songs:
            ctk.CTkLabel(scroll, text="Tidak ada data yang cocok.", text_color="gray").pack(pady=20)
        else:
            for idx, s in enumerate(page_songs, start=start_idx + 1):
                row = ctk.CTkFrame(scroll, fg_color="white", corner_radius=5)
                row.pack(fill="x", pady=2)
                apply_grid_config(row)

                ctk.CTkLabel(row, text=str(idx), text_color="gray").grid(row=0, column=0, pady=8, sticky="ew")
                ctk.CTkLabel(row, text=limit_text(s.title, 40), text_color="#333", anchor="w").grid(row=0, column=1, pady=8, padx=10, sticky="ew")
                ctk.CTkLabel(row, text=limit_text(s.artist, 30), text_color="gray", anchor="w").grid(row=0, column=2, pady=8, padx=10, sticky="ew")
                ctk.CTkLabel(row, text=limit_text(s.genre, 20), text_color="gray", anchor="w").grid(row=0, column=3, pady=8, padx=10, sticky="ew")
                ctk.CTkLabel(row, text=str(s.year), text_color="gray").grid(row=0, column=4, pady=8, sticky="ew")
                ctk.CTkLabel(row, text=format_duration(s.duration), text_color="gray").grid(row=0, column=5, pady=8, sticky="ew")

                # Buttons
                act_frame = ctk.CTkFrame(row, fg_color="transparent")
                act_frame.grid(row=0, column=6, pady=5)
                
                ctk.CTkButton(act_frame, text="Edit", width=40, height=24, fg_color=colors["primary"], 
                             font=("Arial", 10), command=lambda sid=s.id: on_edit(sid)).pack(side="left", padx=2)
                ctk.CTkButton(act_frame, text="Hapus", width=40, height=24, fg_color="#FFEEEE", 
                             text_color="red", hover_color="#FFDDDD", font=("Arial", 10),
                             command=lambda sid=s.id: on_delete(sid)).pack(side="left", padx=2)
        
        # Pagination UI
        if total_pages > 1:
            pagination_frame = ctk.CTkFrame(content_container, fg_color="transparent")
            pagination_frame.pack(fill="x", pady=10)
            
            info_text = f"Halaman {current_page[0]} dari {total_pages} | Menampilkan {start_idx + 1}-{end_idx} dari {total_songs} lagu"
            ctk.CTkLabel(pagination_frame, text=info_text, text_color="gray").pack(side="left", padx=20)
            
            # Gunakan current_sort_internal[0] agar saat ganti halaman sorting tidak reset
            btn_next = ctk.CTkButton(pagination_frame, text="Next ▶", width=80, height=30,
                                    fg_color=colors["primary"] if current_page[0] < total_pages else "gray",
                                    command=lambda: change_page(current_page[0] + 1) if current_page[0] < total_pages else None)
            btn_next.pack(side="right", padx=5)
            
            btn_prev = ctk.CTkButton(pagination_frame, text="◀ Prev", width=80, height=30,
                                    fg_color=colors["primary"] if current_page[0] > 1 else "gray",
                                    command=lambda: change_page(current_page[0] - 1) if current_page[0] > 1 else None)
            btn_prev.pack(side="right", padx=5)

    # --- LOGIKA SORTING BARU (FIX) ---
    def on_dropdown_sort(label):
        """Callback saat user memilih opsi di dropdown"""
        # 1. Translate Label ("JUDUL") -> Internal ("title")
        internal_value = label_to_value.get(label, "title")
        
        # 2. Simpan state internal (agar Search tahu kita sedang sort apa)
        current_sort_internal[0] = internal_value
        
        # 3. Update pilihan dropdown (sembunyikan yang dipilih)
        other_options = [l for l in all_labels if l != label]
        sort_menu.configure(values=other_options)
        
        # 4. Render tabel pakai nilai INTERNAL ("title")
        current_page[0] = 1
        render_table(internal_value, search_var.get(), 1)
        
        # 5. Set Tampilan Dropdown tetap KAPITAL ("JUDUL")
        sort_var.set(label) 

    # Pasang command ke dropdown
    sort_menu.configure(command=on_dropdown_sort)

    # --- SEARCH LOGIC ---
    search_timer = None
    def on_search_change(*args):
        nonlocal search_timer
        if search_timer:
            parent.after_cancel(search_timer)
        
        # Debounce 300ms
        # PENTING: Gunakan current_sort_internal[0] agar hasil search tetap terurut sesuai pilihan user
        search_timer = parent.after(300, lambda: render_table(current_sort_internal[0], search_var.get(), 1)) # Reset ke page 1

    search_var.trace_add("write", on_search_change)

    # --- HELPER PAGINATION ---
    def change_page(new_page):
        # Gunakan internal sort yang tersimpan
        render_table(current_sort_internal[0], search_var.get(), new_page)
    
    # Simpan referensi
    render_table_ref = render_table

    # Render Awal (Default sorting by title, page 1)
    render_table("title", "", 1)