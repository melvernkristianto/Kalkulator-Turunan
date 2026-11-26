### Library Python yang Digunakan

| Library | Kegunaan |
| :--- | :--- |
| `re` | (*Regular Expression*) Memvalidasi dan memformat teks input rumus dari pengguna sebelum dihitung (misalnya mengubah penulisan pangkat `^` menjadi `**` atau perkalian implisit seperti `2x` menjadi `2*x`). |
| `sympy` | Melakukan komputasi matematika simbolik, seperti memproses ekspresi aljabar, menghitung turunan (*differentiation*), dan menyederhanakan hasil rumus. |
| `customtkinter` | Membangun antarmuka pengguna grafis (GUI) aplikasi desktop yang lebih modern dan responsif dibandingkan `tkinter` standar. |


### Fungsi-Fungsi sp

| Perintah di Kode | Kegunaan |
| :--- | :--- |
| `sp.Symbol('x')` | Memberi tahu Python bahwa huruf `x` adalah variabel matematika. |
| `sp.sympify(...)` | Mengubah teks biasa (string) menjadi rumus matematika yang bisa dihitung. |
| `sp.diff(ekspresi, x)` | Menghitung turunan (*differentiation*) dari rumus terhadap $x$. |
| `sp.simplify(...)` | Menyederhanakan bentuk hasil aljabar. |
| `sp.sin`, `sp.cos`, `sp.tan` | Representasi fungsi trigonometri simbolik. |
