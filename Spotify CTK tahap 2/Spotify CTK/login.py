import customtkinter as ctk
from tkinter import messagebox, StringVar

class LoginPage(ctk.CTkFrame):
    def __init__(self, parent, on_login, colors):
        super().__init__(parent, fg_color="#FFFFFF")
        self.on_login = on_login
        self.colors = colors
        
        self.pin_var = StringVar()

        # Grid layout 2 kolom
        self.grid_columnconfigure(0, weight=1) # Kiri (Branding)
        self.grid_columnconfigure(1, weight=1) # Kanan (Input PIN)
        self.grid_rowconfigure(0, weight=1)

        self.build_left_panel()
        self.build_right_form()

    def build_left_panel(self):
        # Panel Kiri - Electric Blue
        frame = ctk.CTkFrame(self, fg_color=self.colors["primary"], corner_radius=0)
        frame.grid(row=0, column=0, sticky="nsew")
        
        inner = ctk.CTkFrame(frame, fg_color="transparent")
        inner.pack(expand=True)

        ctk.CTkLabel(inner, text="⚡", font=("Segoe UI", 100)).pack(pady=10)
        ctk.CTkLabel(inner, text="MyMusic", font=("Segoe UI", 36, "bold"), text_color="white").pack()
        ctk.CTkLabel(inner, text="Electric Edition", font=("Segoe UI", 16), text_color="#E0EFFF").pack(pady=5)

    def build_right_form(self):
        # Panel Kanan - Form PIN
        frame = ctk.CTkFrame(self, fg_color="#FFFFFF", corner_radius=0)
        frame.grid(row=0, column=1, sticky="nsew")

        inner = ctk.CTkFrame(frame, fg_color="transparent")
        inner.pack(expand=True, fill="x", padx=50)

        ctk.CTkLabel(inner, text="Akses Cepat", font=("Segoe UI", 28, "bold"), text_color=self.colors["text_head"]).pack(pady=(0, 10))
        ctk.CTkLabel(inner, text="Masukkan PIN Keamanan", font=("Segoe UI", 14), text_color="gray").pack(pady=(0, 30))

        # Input PIN Besar (Ala ATM)
        entry_pin = ctk.CTkEntry(
            inner, 
            placeholder_text="• • • •", 
            height=60, 
            width=200,
            font=("Consolas", 32, "bold"), 
            justify="center", # Teks di tengah
            show="•",         # Masking karakter
            textvariable=self.pin_var,
            border_color=self.colors["primary"]
        )
        entry_pin.pack(pady=(0, 20))

        # Tombol Masuk
        btn_login = ctk.CTkButton(
            inner, 
            text="BUKA KUNCI", 
            height=50, 
            fg_color=self.colors["primary"], 
            hover_color=self.colors["hover"],
            font=("Segoe UI", 14, "bold"),
            command=self.perform_login
        )
        btn_login.pack(fill="x", pady=10)

        # Info PIN (Hint)
        hint_frame = ctk.CTkFrame(inner, fg_color="#F5F9FF", corner_radius=5)
        hint_frame.pack(fill="x", pady=20)
        ctk.CTkLabel(hint_frame, text="🔑 Admin: 0000  |  👤 User: 9999", text_color="#555", font=("Consolas", 12)).pack(pady=10)

        # Bind tombol Enter
        entry_pin.bind("<Return>", lambda e: self.perform_login())
        
        # Fokus otomatis ke input
        entry_pin.focus()

    def perform_login(self):
        pin = self.pin_var.get().strip()

        # LOGIC PIN
        if pin == "0000":
            self.on_login("admin")
            # messagebox.showinfo("Akses Diterima", "Mode Administrator Aktif")
            
        elif pin == "9999":
            self.on_login("user")
            
        else:
            # Efek getar/error visual (Simpel alert dulu)
            messagebox.showerror("Akses Ditolak", "PIN Salah!")
            self.pin_var.set("") # Reset input