import customtkinter as ctk
from tkinter import messagebox, StringVar

def render_add_song(parent, library, colors, on_saved):
    ctk.CTkLabel(parent, text="Tambah Lagu Baru", font=("Segoe UI", 20, "bold"), text_color=colors["text_head"]).pack(pady=15)
    
    form = ctk.CTkFrame(parent, fg_color="white")
    form.pack(pady=10, padx=40, fill="x")

    vars = {
        "Judul": StringVar(), "Artist": StringVar(), "Genre": StringVar(), "Tahun": StringVar()
    }
    
    fields = ["Judul", "Artist", "Genre", "Tahun"]
    for i, f in enumerate(fields):
        ctk.CTkLabel(form, text=f, text_color="#333").grid(row=i, column=0, padx=20, pady=10, sticky="w")
        ctk.CTkEntry(form, textvariable=vars[f], width=300).grid(row=i, column=1, padx=20, pady=10)

    lbl_stat = ctk.CTkLabel(form, text="", text_color="gray", font=("Arial", 10))
    lbl_stat.grid(row=4, column=1, sticky="w", padx=20)

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
            
            # Panggil addSong
            result = library.addSong(data["Judul"], data["Artist"], data["Genre"], int(data["Tahun"]))
            
            # --- CEK HASILNYA ---
            if result is None:
                messagebox.showerror("Gagal", f"Lagu '{data['Judul']}' sudah ada!")
                lbl_stat.configure(text="Gagal: Duplikat data ditemukan.", text_color="red")
                return

            messagebox.showinfo("Sukses", "Lagu disimpan.")
            on_saved()
            
        except ValueError:
            messagebox.showerror("Error", "Tahun harus angka!")
        except Exception as e:
            print(f"Error: {e}")

    ctk.CTkButton(parent, text="SIMPAN", fg_color=colors["primary"], width=200, height=40, command=save).pack(pady=20)