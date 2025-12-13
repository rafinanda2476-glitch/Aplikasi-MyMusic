import customtkinter as ctk
from tkinter import filedialog, messagebox
import csv

def render_import_csv(parent, library, colors, on_finished):
    ctk.CTkLabel(parent, text="Import CSV", font=("Segoe UI", 20, "bold"), text_color=colors["text_head"]).pack(pady=15)
    
    # State untuk menyimpan data preview
    preview_data = []

    info_frame = ctk.CTkFrame(parent, fg_color="white")
    info_frame.pack(fill="x", padx=20, pady=10)
    ctk.CTkLabel(info_frame, text="Pilih file CSV", text_color="gray").pack(pady=10)

    # Area Preview
    preview_scroll = ctk.CTkScrollableFrame(parent, fg_color="#EEE", height=300)
    preview_scroll.pack(fill="both", expand=True, padx=20, pady=10)
    
    # Label placeholder
    lbl_ph = ctk.CTkLabel(preview_scroll, text="Belum ada file dipilih.", text_color="gray")
    lbl_ph.pack(pady=20)

    def load_preview():
        nonlocal preview_data
        path = filedialog.askopenfilename(filetypes=[("CSV", "*.csv")])
        if not path: return

        try:
            data = []
            with open(path, "r", encoding="utf-8") as f:
                reader = csv.reader(f)
                next(reader, None) # Skip header
                for row in reader:
                    if len(row) >= 4:
                        data.append(row)
            
            if not data:
                messagebox.showwarning("Kosong", "File CSV kosong atau format salah.")
                return

            preview_data = data
            
            # Render Preview
            for w in preview_scroll.winfo_children(): w.destroy()
            ctk.CTkLabel(preview_scroll, text=f"Preview: {len(data)} baris ditemukan.", font=("Arial", 12, "bold")).pack(anchor="w", pady=5)

            for row in data[:]: # Tampilkan max 10 baris
                ctk.CTkLabel(preview_scroll, text=f"{row[0]} - {row[1]} ({row[3]})", anchor="w").pack(fill="x", padx=5)
            
            btn_confirm.configure(state="normal", fg_color=colors["primary"]) # Enable button

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def do_import():
        count = 0
        for row in preview_data:
            try:
                t, a, g, y = row[0], row[1], row[2], int(row[3])
                library.addSong(t, a, g, y)
                count += 1
            except: pass
        
        messagebox.showinfo("Sukses", f"Berhasil import {count} lagu!")
        on_finished()

    # Tombol Kontrol
    btn_box = ctk.CTkFrame(parent, fg_color="transparent")
    btn_box.pack(pady=20)

    ctk.CTkButton(btn_box, text="Pilih File CSV", command=load_preview, fg_color="#555").pack(side="left", padx=10)
    
    btn_confirm = ctk.CTkButton(btn_box, text="Konfirmasi Import", command=do_import, state="disabled", fg_color="gray")
    btn_confirm.pack(side="left", padx=10)


    
            # if len(data) > 10:
            #      ctk.CTkLabel(preview_scroll, text="... dan lainnya ...", text_color="gray").pack()