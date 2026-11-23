import re
import sympy as sp
from gui import KalkulatorTurunanUI

# Variabel simbol matematika utama
x = sp.Symbol('x')

# ================= FUNGSI PENERJEMAH & FORMATTING =================

def terjemahkan_ke_sympy(teks):
    """Menerjemahkan teks input pengguna agar bisa dipahami oleh SymPy"""
    teks = teks.replace("^", "**")
    teks = teks.replace("√(", "sqrt(")
    teks = re.sub(r'(\d)([a-zA-Z(])', r'\1*\2', teks)
    teks = re.sub(r'(\))([a-zA-Z0-9(])', r'\1*\2', teks)
    return teks

def format_math(ekspresi):
    """Mengubah format SymPy kembali ke format teks yang ramah dibaca manusia"""
    hasil = str(ekspresi)
    hasil = hasil.replace("**", "^")
    hasil = hasil.replace("sqrt", "√")
    hasil = hasil.replace("*", "")
    return hasil

# ================= DETEKSI ATURAN & LANGKAH PENYELESAIAN =================

def deteksi_rumus_trigonometri(suku):
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
        daftar_atom = list(suku.atoms(fungsi_cls))
        for item in daftar_atom:
            u = item.args[0]  # Sudut di dalam fungsi trigonometri (misal: 3x^2)
            u_aksen = sp.diff(u, x)
            
            penjelasan.append(f"   • Rumus Dasar Trigonometri ({nama}):")
            penjelasan.append(f"     {rumus}")
            
            # Jika sudut u bukan hanya 'x' (misal sin(2x) atau cos(x^2)), jabarkan aturan rantai
            if u != x:
                penjelasan.append(f"   • Aturan Rantai (Turunan Sudut):")
                penjelasan.append(f"     Misal u = {format_math(u)}  →  u' = {format_math(u_aksen)}")

    return penjelasan

def buat_penjelasan_langkah(ekspresi):
    """Membuat rincian langkah penyelesaian berdasarkan bentuk fungsi matematika"""
    langkah = []
    langkah.append(f"Soal:\n  f(x) = {format_math(ekspresi)}\n")

    suku_suku = sp.Add.make_args(ekspresi)

    if len(suku_suku) > 1:
        langkah.append("1. Gunakan Aturan Penjumlahan/Pengurangan:")
        langkah.append("   Turunkan setiap suku secara terpisah.\n")
    else:
        langkah.append("1. Identifikasi Bentuk Fungsi & Rumus Dasar:\n")

    # program memproses setiap suku satu per satu
    for idx, suku in enumerate(suku_suku, start=1):
        turunan_suku = sp.diff(suku, x)
        suku_str = format_math(suku)
        hasil_suku_str = format_math(turunan_suku)

        langkah.append(f"   [Suku {idx}]: {suku_str}")

        # Cek apakah mengandung fungsi trigonometri
        if suku.has(sp.sin, sp.cos, sp.tan, sp.cot, sp.sec, sp.csc):
            # Cek jika ada aturan perkalian (misal: x^2 * sin(x))
            faktor_bervariabel = [a for a in suku.args if a.has(x)] if suku.is_Mul else []
            if len(faktor_bervariabel) >= 2:
                langkah.append("   • Aturan Perkalian: (u·v)' = u'v + uv'")
            
            detail_trig = deteksi_rumus_trigonometri(suku)
            langkah.extend(detail_trig)

        elif not suku.has(x):
            langkah.append("   • Rumus Dasar Konstanta: d/dx [c] = 0")
        elif suku.is_Pow or (suku.is_Mul and any(arg.is_Pow or arg == x for arg in suku.args)):
            langkah.append("   • Rumus Dasar Pangkat: d/dx [a·x^n] = a·n·x^(n-1)")
        elif suku.is_Mul and len([a for a in suku.args if a.has(x)]) >= 2:
            langkah.append("   • Aturan Perkalian: (u·v)' = u'v + uv'")
        else:
            langkah.append("   • Turunkan terhadap variabel x.")

        langkah.append(f"   → Hasil turunan suku {idx} = {hasil_suku_str}\n")

    # Langkah penggabungan & penyederhanaan
    turunan_mentah = sp.diff(ekspresi, x)
    turunan_akhir = sp.simplify(turunan_mentah)

    langkah.append("2. Gabungkan Semua Hasil Turunan:")
    langkah.append(f"   f'(x) = {format_math(turunan_mentah)}\n")

    if str(turunan_mentah) != str(turunan_akhir):
        langkah.append("3. Sederhanakan Bentuk Akhir:")
        langkah.append(f"   f'(x) = {format_math(turunan_akhir)}\n")

    langkah.append(f"HASIL AKHIR:\n  f'(x) = {format_math(turunan_akhir)}")

    return "\n".join(langkah)

# ================= 3. FUNGSI EKSEKUSI UTAMA (DIHUBUNGKAN KE UI) =================

def proses_hitung(ekspresi_str):
    """
    Menerima teks rumus dari layar UI, lalu mengembalikan:
    (status_sukses: bool, teks_hasil: str, teks_langkah: str)
    """
    try:
        siap_hitung = terjemahkan_ke_sympy(ekspresi_str)
        ekspresi = sp.sympify(siap_hitung)
        hasil_turunan = sp.simplify(sp.diff(ekspresi, x))

        teks_akhir = format_math(hasil_turunan)
        teks_langkah = buat_penjelasan_langkah(ekspresi)

        return True, f"f'(x) = {teks_akhir}", teks_langkah
    except Exception:
        pesan_error = "Terjadi kesalahan sintaks.\nPastikan tanda kurung sudah ditutup dengan benar, contoh: sin(2x) atau √(x+1)."
        return False, "Error: Periksa penulisan!", pesan_error

# ================= 4. TITIK MASUK PROGRAM (ENTRY POINT) =================

if __name__ == "__main__":
    app = KalkulatorTurunanUI(fungsi_hitung=proses_hitung)
    app.mainloop()
