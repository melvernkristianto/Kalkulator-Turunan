import re
import customtkinter as ctk
import sympy as sp

# --- KONFIGURASI TEMA & WARNA UI/UX ---
WARNA_BG = "#121212"
WARNA_LAYAR = "#1E1E2E"
WARNA_TOMBOL_ANGKA = "#2A2A3C"
WARNA_TOMBOL_FUNGSI = "#3B3B54"
WARNA_TOMBOL_AKSI = "#EF4444"
WARNA_TOMBOL_HITUNG = "#10B981"

ctk.set_appearance_mode("dark")

class KalkulatorTurunanApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Pengaturan Window
        self.title("Kalkulator Turunan + Rumus Trigonometri")
        self.geometry("880x580")
        self.configure(fg_color=WARNA_BG)
        self.resizable(True, True)

        self.ekspresi_layar = ""
        self.x = sp.Symbol('x')

        self.buat_ui()

    def buat_ui(self):
        # Kolom kiri (0) tidak ikut melebar, Kolom kanan (1) mengambil seluruh sisa ruang
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

        # untuk membaca setiap baris dan kolom list tata letak tombol
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

    def terjemahkan_ke_sympy(self, teks):
        teks = teks.replace("^", "**")
        teks = teks.replace("√(", "sqrt(")
        teks = re.sub(r'(\d)([a-zA-Z(])', r'\1*\2', teks)
        teks = re.sub(r'(\))([a-zA-Z0-9(])', r'\1*\2', teks)
        return teks

    def format_math(self, ekspresi):
        hasil = str(ekspresi)
        hasil = hasil.replace("**", "^")
        hasil = hasil.replace("sqrt", "√")
        hasil = hasil.replace("*", "")
        return hasil

    def deteksi_rumus_trigonometri(self, suku):
        """Mendeteksi fungsi trigonometri spesifik dan menyertakan rumus dasar + aturan rantai"""
        penjelasan = []
        
        # Kamus rumus dasar trigonometri
        kamus_trig = [
            (sp.sin, "sin(u)", "d/dx [sin(u)] = cos(u) · u'"),
            (sp.cos, "cos(u)", "d/dx [cos(u)] = -sin(u) · u'"),
            (sp.tan, "tan(u)", "d/dx [tan(u)] = sec^2(u) · u'"),
            (sp.cot, "cot(u)", "d/dx [cot(u)] = -csc^2(u) · u'"),
            (sp.sec, "sec(u)", "d/dx [sec(u)] = sec(u)·tan(u) · u'"),
            (sp.csc, "csc(u)", "d/dx [csc(u)] = -csc(u)·cot(u) · u'")
        ]

        for fungsi_cls, nama, rumus in kamus_trig:
            # Mencari semua kemunculan fungsi trigonometri tersebut di dalam suku
            daftar_atom = list(suku.atoms(fungsi_cls))
            for item in daftar_atom:
                u = item.args[0]  # Sudut di dalam fungsi trigonometri (misal: 3x^2)
                u_aksen = sp.diff(u, self.x)
                
                penjelasan.append(f"   • Rumus Dasar Trigonometri ({nama}):")
                penjelasan.append(f"     {rumus}")
                
                # Jika sudut u bukan hanya 'x' (misal sin(2x) atau cos(x^2)), jabarkan u dan u'
                if u != self.x:
                    penjelasan.append(f"   • Aturan Rantai (Turunan Sudut):")
                    penjelasan.append(f"     Misal u = {self.format_math(u)}  →  u' = {self.format_math(u_aksen)}")

        return penjelasan

    def buat_penjelasan_langkah(self, ekspresi):
        """Membuat rincian langkah penyelesaian berdasarkan bentuk fungsi"""
        langkah = []
        langkah.append(f"Soal:\n  f(x) = {self.format_math(ekspresi)}\n")

        suku_suku = sp.Add.make_args(ekspresi)

        if len(suku_suku) > 1:
            langkah.append("1. Gunakan Aturan Penjumlahan/Pengurangan:")
            langkah.append("   Turunkan setiap suku secara terpisah.\n")
        else:
            langkah.append("1. Identifikasi Bentuk Fungsi & Rumus Dasar:\n")

        for idx, suku in enumerate(suku_suku, start=1):
            turunan_suku = sp.diff(suku, self.x)
            suku_str = self.format_math(suku)
            hasil_suku_str = self.format_math(turunan_suku)

            langkah.append(f"   [Suku {idx}]: {suku_str}")

            # Cek apakah mengandung fungsi trigonometri
            if suku.has(sp.sin, sp.cos, sp.tan, sp.cot, sp.sec, sp.csc):
                # Cek jika ada aturan perkalian antara aljabar dan trigonometri (misal: x^2 * sin(x))
                faktor_bervariabel = [a for a in suku.args if a.has(self.x)] if suku.is_Mul else []
                if len(faktor_bervariabel) >= 2:
                    langkah.append("   • Aturan Perkalian: (u·v)' = u'v + uv'")
                
                # Tampilkan rumus dasar trigonometri yang sesuai
                detail_trig = self.deteksi_rumus_trigonometri(suku)
                langkah.extend(detail_trig)

            elif not suku.has(self.x):
                langkah.append("   • Rumus Dasar Konstanta: d/dx [c] = 0")
            elif suku.is_Pow or (suku.is_Mul and any(arg.is_Pow or arg == self.x for arg in suku.args)):
                langkah.append("   • Rumus Dasar Pangkat: d/dx [a·x^n] = a·n·x^(n-1)")
            elif suku.is_Mul and len([a for a in suku.args if a.has(self.x)]) >= 2:
                langkah.append("   • Aturan Perkalian: (u·v)' = u'v + uv'")
            else:
                langkah.append("   • Turunkan terhadap variabel x.")

            langkah.append(f"   → Hasil turunan suku {idx} = {hasil_suku_str}\n")

        # Langkah penggabungan & penyederhanaan
        turunan_mentah = sp.diff(ekspresi, self.x)
        turunan_akhir = sp.simplify(turunan_mentah)

        langkah.append("2. Gabungkan Semua Hasil Turunan:")
        langkah.append(f"   f'(x) = {self.format_math(turunan_mentah)}\n")

        if str(turunan_mentah) != str(turunan_akhir):
            langkah.append("3. Sederhanakan Bentuk Akhir:")
            langkah.append(f"   f'(x) = {self.format_math(turunan_akhir)}\n")

        langkah.append(f"HASIL AKHIR:\n  f'(x) = {self.format_math(turunan_akhir)}")

        return "\n".join(langkah)

    def proses_turunan(self):
        if not self.ekspresi_layar:
            return
        try:
            siap_hitung = self.terjemahkan_ke_sympy(self.ekspresi_layar)
            ekspresi = sp.sympify(siap_hitung)
            hasil_turunan = sp.simplify(sp.diff(ekspresi, self.x))

            teks_akhir = self.format_math(hasil_turunan)
            self.lbl_hasil.configure(text=f"f'(x) = {teks_akhir}", text_color="#34D399")

            teks_langkah = self.buat_penjelasan_langkah(ekspresi)
            self.tulis_langkah(teks_langkah)

        except Exception:
            self.lbl_hasil.configure(text="Error: Periksa penulisan!", text_color="#F87171")
            self.tulis_langkah("Terjadi kesalahan sintaks.\nPastikan tanda kurung sudah ditutup dengan benar, contoh: sin(2x) atau √(x+1).")

if __name__ == "__main__":
    app = KalkulatorTurunanApp()
    app.mainloop()