import re
import customtkinter as ctk
import sympy as sp

# --- KONFIGURASI TEMA & WARNA UI/UX ---
# Kamu bisa mengubah kode warna Hex di bawah ini untuk kustomisasi tampilan
WARNA_BG = "#121212"          # Latar belakang utama
WARNA_LAYAR = "#1E1E2E"       # Kotak layar input/output
WARNA_TOMBOL_ANGKA = "#2A2A3C"# Tombol angka & variabel
WARNA_TOMBOL_FUNGSI = "#3B3B54"# Tombol sin, cos, akar, pangkat
WARNA_TOMBOL_AKSI = "#EF4444" # Tombol C dan DEL (Merah)
WARNA_TOMBOL_HITUNG = "#10B981"# Tombol Hitung Turunan (Hijau)

ctk.set_appearance_mode("dark")

class KalkulatorTurunanApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Pengaturan Window
        self.title("Kalkulator Turunan")
        self.geometry("380x580")
        self.configure(fg_color=WARNA_BG)
        self.resizable(False, False)

        # Variabel ekspresi matematika
        self.ekspresi_layar = ""
        self.x = sp.Symbol('x')

        self.ui()

    def ui(self):
        # AREA LAYAR (DISPLAY)
        frame_layar = ctk.CTkFrame(self, fg_color=WARNA_LAYAR, corner_radius=15)
        frame_layar.pack(padx=20, pady=(20, 15), fill="x")

        # Layar Input (Read-only agar user fokus memakai tombol, tapi tetap bisa diseleksi)
        self.entry_input = ctk.CTkEntry(
            frame_layar,
            font=("Consolas", 22, "bold"),
            fg_color="transparent",
            border_width=0,
            text_color="#FFFFFF",
            justify="right"
        )
        self.entry_input.pack(padx=15, pady=(10, 5), fill="x")
        self.entry_input.insert(0, "0")

        # Garis pemisah tipis di dalam layar
        garis = ctk.CTkFrame(frame_layar, height=1, fg_color="#374151")
        garis.pack(padx=15, pady=5, fill="x")

        # Layar Output Hasil Turunan
        self.lbl_hasil = ctk.CTkLabel(
            frame_layar,
            text="f'(x) = ",
            font=("Consolas", 18, "bold"),
            text_color="#34D399",
            anchor="e",
            wraplength=310
        )
        self.lbl_hasil.pack(padx=15, pady=(5, 15), fill="x")

        # AREA TOMBOL (KEYPAD GRID)
        frame_tombol = ctk.CTkFrame(self, fg_color="transparent")
        frame_tombol.pack(padx=20, pady=5, fill="both", expand=True)

        # Susunan tombol kalkulator (Baris x Kolom)
        tata_letak_tombol = [
            ["sin(", "cos(", "tan(", "C", "DEL"],
            ["√(",   "^",    "(",    ")",   "/"],
            ["7",    "8",    "9",    "x",   "*"],
            ["4",    "5",    "6",    "+",   "-"],
            ["1",    "2",    "3",    "0",   "."]
        ]

        # Mengatur proporsi kolom agar merata
        for col in range(5):
            frame_tombol.grid_columnconfigure(col, weight=1)

        # Membuat tombol secara otomatis berdasarkan daftar di atas
        for y, baris in enumerate(tata_letak_tombol):
            frame_tombol.grid_rowconfigure(y, weight=1)
            for x, teks in enumerate(baris):
                # Penentuan warna tombol berdasarkan jenisnya
                if teks in ["C", "DEL"]:
                    warna = WARNA_TOMBOL_AKSI
                elif teks in ["sin(", "cos(", "tan(", "√(", "^", "(", ")", "/", "*", "+", "-"]:
                    warna = WARNA_TOMBOL_FUNGSI
                else:
                    warna = WARNA_TOMBOL_ANGKA

                btn = ctk.CTkButton(
                    frame_tombol,
                    text=teks,
                    font=("Roboto", 16, "bold"),
                    fg_color=warna,
                    hover_color="#4B5563",
                    corner_radius=10,
                    height=52,
                    command=lambda t=teks: self.klik_tombol(t)
                )
                btn.grid(row=y, column=x, padx=4, pady=4, sticky="nsew")

        # TOMBOL EKSEKUSI UTAMA (HITUNG TURUNAN)
        btn_hitung = ctk.CTkButton(
            self,
            text="HITUNG TURUNAN  d/dx",
            font=("Roboto", 16, "bold"),
            fg_color=WARNA_TOMBOL_HITUNG,
            hover_color="#059669",
            text_color="#FFFFFF",
            corner_radius=12,
            height=50,
            command=self.proses_turunan
        )
        btn_hitung.pack(padx=20, pady=(10, 20), fill="x")

    def klik_tombol(self, nilai):
        if nilai == "C":
            self.ekspresi_layar = ""
            self.perbarui_layar("0")
            self.lbl_hasil.configure(text="f'(x) = ", text_color="#34D399")
        elif nilai == "DEL":
            self.ekspresi_layar = self.ekspresi_layar[:-1]
            self.perbarui_layar(self.ekspresi_layar if self.ekspresi_layar else "0")
        else:
            self.ekspresi_layar += nilai
            self.perbarui_layar(self.ekspresi_layar)

    def perbarui_layar(self, teks):
        self.entry_input.delete(0, "end")
        self.entry_input.insert(0, teks)

    def terjemahkan_ke_sympy(self, teks):
        teks = teks.replace("^", "**")
        teks = teks.replace("√(", "sqrt(")
        # Menyisipkan tanda kali '*' otomatis (misal: 3x -> 3*x, 2sin(x) -> 2*sin(x))
        teks = re.sub(r'(\d)([a-zA-Z(])', r'\1*\2', teks)
        teks = re.sub(r'(\))([a-zA-Z0-9(])', r'\1*\2', teks)
        return teks

    def format_hasil(self, ekspresi):
        hasil = str(ekspresi)
        hasil = hasil.replace("**", "^")
        hasil = hasil.replace("sqrt", "√")
        hasil = hasil.replace("*", "")
        return hasil

    def proses_turunan(self):
        if not self.ekspresi_layar:
            return
        try:
            siap_hitung = self.terjemahkan_ke_sympy(self.ekspresi_layar)
            ekspresi = sp.sympify(siap_hitung)
            hasil_turunan = sp.simplify(sp.diff(ekspresi, self.x))
            
            teks_akhir = self.format_hasil(hasil_turunan)
            self.lbl_hasil.configure(text=f"f'(x) = {teks_akhir}", text_color="#34D399")
        except Exception:
            self.lbl_hasil.configure(text="Error: Periksa tanda kurung!", text_color="#F87171")

if __name__ == "__main__":
    app = KalkulatorTurunanApp()
    app.mainloop()