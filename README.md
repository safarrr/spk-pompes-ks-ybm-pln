# SPK Beasiswa Santri — TOPSIS

Notebook `main.ipynb` memuat perhitungan seleksi beasiswa di Pondok Pesantren Kreatif Sukamakmur YBM PLN. Semua sel sudah dijalankan; tabel hasil dapat langsung dilihat saat notebook dibuka.

1. Buka `main.ipynb` di VS Code atau Jupyter dan pilih kernel Python dari `.venv`.
2. Ubah `BOBOT` di bagian **1. Informasi kriteria, rubrik, dan bobot**. Bobot awal C1=0.30, C2=0.25, C3=0.20, C4=0.15, C5=0.10.
3. Ubah `ALTERNATIF_CONTOH` jika ingin menelusuri substitusi angka santri lain.
4. Jalankan **Restart Kernel & Run All**. Hasil ranking dan ekspor CSV/JSON di `reports/` akan diperbarui.

Notebook mandiri: tidak mengimpor `topsis.py` dan tidak memerlukan pandas/NumPy. Data dibaca dari `data/Data_Pendaftar_PSB_Skala_1-5.csv`, dengan pemisah titik koma.

## Kriteria

| Kode | Kriteria | Sifat | Data perhitungan | Bobot awal |
|---|---|---|---|---|
| C1 | Penghasilan Orang Tua | Cost | Penghasilan (Rp), nominal bulanan | 30% |
| C2 | Prestasi Akademik | Benefit | C2 (Prestasi), skor 1–5 | 25% |
| C3 | Jumlah Tanggungan Ortu | Benefit | C3 (Tanggungan), skor 1–5 | 20% |
| C4 | Status Orang Tua | Benefit | C4 (Status Ortu), skor 1–5 | 15% |
| C5 | Keberadaan SKTM | Benefit | C5 (SKTM), skor 1–5 | 10% |

C1 tidak memakai skor konversi karena skor tinggi pada rubrik sudah mewakili penghasilan rendah. Memakai skor itu sebagai cost akan membalik prioritas. Satuan yang berbeda disetarakan dengan normalisasi vektor.

Notebook menampilkan data sumber lengkap, rubrik pengguna, catatan kualitas data, matriks keputusan, kuadrat dan pembagi normalisasi, matriks R, bobot efektif, matriks Y, ideal A+/A−, kontribusi jarak per kriteria, D+/D−, nilai preferensi V, dan ranking seluruh santri. Nilai antara tidak dibulatkan saat dihitung. Nilai seri mendapat peringkat kompetisi (1,1,3), dengan toleransi absolut 1e-12.

## Meninjau hasil

- `reports/laporan_topsis.html` adalah salinan offline hasil notebook saat penyerahan. Buka di browser untuk membaca penjelasan, rumus teks, dan tabel tanpa Jupyter. HTML ini statis; perubahan bobot dilakukan melalui notebook.
- `reports/10_ranking.csv` memuat hasil ranking terbaru dari notebook.
- `reports/hasil_lengkap.json` memuat data, konfigurasi, dan semua hasil antara tanpa pembulatan tampilan.
- `topsis.py` menyediakan implementasi pembanding yang dapat dijalankan dari terminal. Ubah `config.json`, lalu jalankan `python topsis.py --output reports_cli`; hasil CLI tersimpan terpisah.
- Uji matematis: `python -m unittest discover -s tests -v`.

## Catatan data

Penghasilan 0 dari isian `-` mengikuti konversi CSV dan perlu diverifikasi. Kolom jumlah saudara dipakai sebagai proksi tanggungan melalui skor C3; padanan ini perlu konfirmasi. Kasus 0 saudara belum tercantum dalam rubrik gambar. Semua SKTM memiliki skor yang sama sehingga tidak membedakan ranking. Rentang rubrik dipertahankan sebagai referensi; notebook tidak mengubah skor sumber secara diam-diam.

Hasil adalah rekomendasi prioritas berdasarkan data dan bobot aktif, bukan penetapan penerima. Kuota dan ketentuan kelayakan belum diberikan.


## Persiapan GitHub dan template input

- `.gitignore` mengecualikan `.venv/`, cache Python, data pribadi di `data/`, hasil di `reports/` dan `reports_cli/`, serta notebook lokal `main.ipynb` yang menyimpan output data santri.
- `notebooks/template_topsis.ipynb` adalah salinan notebook tanpa output untuk GitHub. Bobot dan langkah perhitungan tetap dapat dijalankan.
- `templates/template_input.csv` adalah template kosong yang sesuai dengan format pembaca CSV.
- `templates/contoh_input_dummy.csv` berisi tiga calon santri fiktif untuk mencoba notebook.
- `templates/PANDUAN_INPUT.md` menjelaskan isi setiap kolom, format angka, dan langkah pemakaian.

Setelah clone dari GitHub, isi template dan simpan sebagai `data/Data_Pendaftar_PSB_Skala_1-5.csv`. Untuk percobaan, salin contoh data fiktif ke lokasi itu, lalu buka `notebooks/template_topsis.ipynb` dan jalankan semua sel. Jangan menimpa data asli yang sudah ada tanpa menyimpan cadangannya.

Jika ingin menyimpan hasil notebook untuk pekerjaan lokal, gunakan nama `main.ipynb` di akar proyek; nama ini sudah dikecualikan dari Git. Pastikan output di `notebooks/template_topsis.ipynb` tetap kosong sebelum commit. Output notebook tersebut akan terisi bila Anda menjalankannya.

Proyek belum diinisialisasi atau di-push ke GitHub oleh perubahan ini. Periksa `git status` sebelum commit; `.gitignore` tidak menghapus data yang sudah pernah dilacak atau di-commit.
