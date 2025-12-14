import customtkinter as ctk
from tkinter import messagebox, StringVar

def render_add_song(parent, library, colors, on_saved):
    ctk.CTkLabel(parent, text="Tambah Lagu Baru", font=("Segoe UI", 20, "bold"), text_color=colors["text_head"]).pack(pady=15)
    
    form = ctk.CTkFrame(parent, fg_color="white")
    form.pack(pady=10, padx=40, fill="x")

    vars = {
        "Judul": StringVar(), "Artist": StringVar(), "Genre": StringVar(), "Tahun": StringVar(), "Durasi": StringVar()
    }
    
    fields = ["Judul", "Artist", "Genre", "Tahun", "Durasi"]
    for i, f in enumerate(fields):
        ctk.CTkLabel(form, text=f, text_color="#333").grid(row=i, column=0, padx=20, pady=10, sticky="w")
        entry = ctk.CTkEntry(form, textvariable=vars[f], width=300)
        entry.grid(row=i, column=1, padx=20, pady=10)
        
        # Placeholder untuk durasi
        if f == "Durasi":
            entry.delete(0, "end")
            entry.insert(0, "3:00")
            ctk.CTkLabel(form, text="(Format: MM:SS atau detik)", text_color="gray", font=("Arial", 9)).grid(row=i, column=2, padx=5, sticky="w")

    lbl_stat = ctk.CTkLabel(form, text="", text_color="gray", font=("Arial", 10))
    lbl_stat.grid(row=5, column=1, sticky="w", padx=20)

    def on_type(*args):
        try: lbl_stat.configure(text="Mengetik...", text_color="gray")
        except: pass

    for v in vars.values(): v.trace_add("write", on_type)

    def save():
        try:
            data = {k: v.get().strip() for k, v in vars.items()}
            if any(not x for x in data.values()):
                messagebox.showerror("Error", "Semua kolom harus diisi!")
                return
            
            try:
                genre = str(data["Genre"])
            except ValueError:
                messagebox.showerror("Error", "Genre Tidak Valid!")
                return
            if genre not in ["Pop", "Rock", "Jazz", "Classical", "Hip-Hop", "Reggee"]:
                messagebox.showerror("Error", "Genre Tidak Valid!")
                return
            
            try:
                tahun = int(data["Tahun"])
            except ValueError:
                messagebox.showerror("Error", "Tahun Harus Angka!")
                return
            if tahun < 1 or tahun >2025:
                messagebox.showerror("Error", "Tahun Tidak Valid!")
                return
            # Parse duration (MM:SS or seconds)
            duration_str = data["Durasi"].strip()
            try:
                if ":" in duration_str:
                    # MM:SS format
                    parts = duration_str.split(":")
                    if len(parts) == 2:
                        mins = int(parts[0])
                        secs = int(parts[1])
                        duration = mins * 60 + secs
                    else:
                        raise ValueError("Format durasi salah")
                else:
                    # Just seconds
                    duration = int(duration_str)
                
                if duration < 1 or duration > 3600:  # Max 1 hour
                    messagebox.showerror("Error", "Durasi harus antara 1 detik - 1 jam!")
                    return
            except ValueError:
                messagebox.showerror("Error", "Format durasi salah! Gunakan MM:SS atau detik.")
                return
            
            # Panggil addSong dengan duration
            result = library.addSong(data["Judul"], data["Artist"], data["Genre"], int(data["Tahun"]), duration)
            
            # --- CEK HASILNYA ---
            if result is None:
                messagebox.showerror("Gagal", f"Lagu '{data['Judul']}' sudah ada!")
                lbl_stat.configure(text="Gagal: Duplikat data ditemukan.", text_color="red")
                return

            library.save_if_supported()  # Save changes
            messagebox.showinfo("Sukses", "Lagu disimpan.")
            on_saved()
            
        except ValueError:
            messagebox.showerror("Error", "Tahun harus angka!")
        except Exception as e:
            print(f"Error: {e}")

    ctk.CTkButton(parent, text="SIMPAN", fg_color=colors["primary"], width=200, height=40, command=save).pack(pady=20)