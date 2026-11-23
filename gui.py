import customtkinter as ctk

# --- KONFIGURASI TEMA & WARNA UI/UX ---
WARNA_BG = "#121212"
WARNA_LAYAR = "#1E1E2E"
WARNA_TOMBOL_ANGKA = "#2A2A3C"
WARNA_TOMBOL_FUNGSI = "#3B3B54"
WARNA_TOMBOL_AKSI = "#EF4444"
WARNA_TOMBOL_HITUNG = "#10B981"

ctk.set_appearance_mode("dark")

class KalkulatorTurunanUI(ctk.CTk):
    def __init__(self, fungsi_hitung=None):
        super().__init__()

        # Menghubungkan fungsi logika matematika dari luar
        self.fungsi_hitung = fungsi_hitung

        # Pengaturan Jendela Utama
        self.title("Kalkulator Turunan + Rumus Trigonometri")
        self.geometry("880x580")
        self.configure(fg_color=WARNA_BG)
        self.resizable(True, True)

        self.ekspresi_layar = ""
        self.buat_ui()

    def buat_ui(self):
        # Kolom kiri (0) tetap, Kolom kanan (1) melebar mengikuti ukuran jendela
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # ================= PANEL KIRI (KALKULATOR) =================
        frame_kiri = ctk.CTkFrame(self, fg_color="transparent", width=310)
        frame_kiri.grid(row=0, column=0, padx=(20, 10), pady=20, sticky="nsew")
        frame_kiri.pack_propagate(False)

        # Area Layar Input & Output
        frame_layar = ctk.CTkFrame(frame_kiri, fg_color=WARNA_LAYAR, corner_radius=15)
        frame_layar.pack(pady=(0, 15), fill="x")

        lbl_info = ctk.CTkLabel(
            frame_layar, text="f(x) =", font=("Roboto", 13), text_color="#9CA3AF", anchor="w"
        )
        lbl_info.pack(padx=15, pady=(10, 0), fill="x")

        self.entry_input = ctk.CTkEntry(
            frame_layar,
            font=("Consolas", 19, "bold"),
            fg_color="transparent",
            border_width=0,
            text_color="#FFFFFF",
            justify="right"
        )
        self.entry_input.pack(padx=15, pady=(0, 5), fill="x")
        self.entry_input.insert(0, "0")

        garis = ctk.CTkFrame(frame_layar, height=1, fg_color="#374151")
        garis.pack(padx=15, pady=5, fill="x")

        self.lbl_hasil = ctk.CTkLabel(
            frame_layar,
            text="f'(x) = ",
            font=("Consolas", 16, "bold"),
            text_color="#34D399",
            anchor="e",
            wraplength=280
        )
        self.lbl_hasil.pack(padx=15, pady=(5, 15), fill="x")

        # Area Tombol
        frame_tombol = ctk.CTkFrame(frame_kiri, fg_color="transparent")
        frame_tombol.pack(pady=5, fill="both", expand=True)

        tata_letak_tombol = [
            ["sin(", "cos(", "tan(", "C", "DEL"],
            ["√(",   "^",    "(",    ")",   "/"],
            ["7",    "8",    "9",    "x",   "*"],
            ["4",    "5",    "6",    "+",   "-"],
            ["1",    "2",    "3",    "0",   "."]
        ]

        for col in range(5):
            frame_tombol.grid_columnconfigure(col, weight=1)

        for x, baris in enumerate(tata_letak_tombol):
            frame_tombol.grid_rowconfigure(x, weight=1)
            for y, teks in enumerate(baris):
                if teks in ["C", "DEL"]:
                    warna = WARNA_TOMBOL_AKSI
                elif teks in ["sin(", "cos(", "tan(", "√(", "^", "(", ")", "/", "*", "+", "-"]:
                    warna = WARNA_TOMBOL_FUNGSI
                else:
                    warna = WARNA_TOMBOL_ANGKA

                btn = ctk.CTkButton(
                    frame_tombol,
                    text=teks,
                    font=("Roboto", 13, "bold"),
                    fg_color=warna,
                    hover_color="#4B5563",
                    corner_radius=10,
                    height=46,
                    command=lambda t=teks: self.klik_tombol(t)
                )
                btn.grid(row=x, column=y, padx=3, pady=3, sticky="nsew")

        # Tombol Eksekusi Utama
        btn_hitung = ctk.CTkButton(
            frame_kiri,
            text="HITUNG & TAMPILKAN LANGKAH",
            font=("Roboto", 13, "bold"),
            fg_color=WARNA_TOMBOL_HITUNG,
            hover_color="#059669",
            text_color="#FFFFFF",
            corner_radius=12,
            height=46,
            command=self.proses_turunan
        )
        btn_hitung.pack(pady=(10, 0), fill="x")

        # ================= PANEL KANAN (LANGKAH PENYELESAIAN) =================
        frame_kanan = ctk.CTkFrame(self, fg_color=WARNA_LAYAR, corner_radius=15)
        frame_kanan.grid(row=0, column=1, padx=(10, 20), pady=20, sticky="nsew")

        lbl_judul_langkah = ctk.CTkLabel(
            frame_kanan,
            text="Langkah-Langkah",
            font=("Roboto", 16, "bold"),
            text_color="#60A5FA",
            anchor="center"
        )
        lbl_judul_langkah.pack(padx=15, pady=(15, 10), fill="x")

        self.box_langkah = ctk.CTkTextbox(
            frame_kanan,
            font=("Consolas", 13),
            fg_color="#161622",
            text_color="#E5E7EB",
            corner_radius=10,
            wrap="word"
        )
        self.box_langkah.pack(padx=15, pady=(0, 15), fill="both", expand=True)
        self.tulis_langkah("Masukkan fungsi f(x) di sebelah kiri, lalu klik Hitung untuk melihat rumus dasar dan langkah penyelesaiannya.")

    def tulis_langkah(self, teks):
        self.box_langkah.configure(state="normal")
        self.box_langkah.delete("1.0", "end")
        self.box_langkah.insert("1.0", teks)
        self.box_langkah.configure(state="disabled")

    def klik_tombol(self, nilai):
        if nilai == "C":
            self.ekspresi_layar = ""
            self.perbarui_layar("0")
            self.lbl_hasil.configure(text="f'(x) = ", text_color="#34D399")
            self.tulis_langkah("Layar dibersihkan. Silakan masukkan fungsi baru.")
        elif nilai == "DEL":
            self.ekspresi_layar = self.ekspresi_layar[:-1]
            self.perbarui_layar(self.ekspresi_layar if self.ekspresi_layar else "0")
        else:
            self.ekspresi_layar += nilai
            self.perbarui_layar(self.ekspresi_layar)

    def perbarui_layar(self, teks):
        self.entry_input.delete(0, "end")
        self.entry_input.insert(0, teks)

    def proses_turunan(self):
        if not self.ekspresi_layar:
            return

        # Panggil fungsi logika yang dihubungkan dari luar
        if self.fungsi_hitung:
            sukses, hasil, langkah = self.fungsi_hitung(self.ekspresi_layar)
            if sukses:
                self.lbl_hasil.configure(text=hasil, text_color="#34D399")
                self.tulis_langkah(langkah)
            else:
                self.lbl_hasil.configure(text="Error: Periksa penulisan!", text_color="#F87171")
                self.tulis_langkah(langkah)
