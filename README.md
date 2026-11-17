# SPK Beasiswa Santri — TOPSIS

Sistem pendukung keputusan untuk seleksi beasiswa di Pondok Pesantren Kreatif Sukamakmur YBM PLN menggunakan metode TOPSIS. Proyek dapat dijalankan melalui notebook untuk melihat perhitungan bertahap, atau terminal untuk langsung menghasilkan laporan.

## 1. Persiapan

Siapkan Python 3 (disarankan 3.10 atau lebih baru). Untuk notebook, gunakan VS Code dengan ekstensi **Python** dan **Jupyter**, atau JupyterLab di browser.

Unduh dan ekstrak proyek, atau clone repository melalui Git. Buka terminal di folder `spk`, yaitu folder yang berisi `topsis.py` dan `config.json`. Semua perintah berikut dijalankan dari folder tersebut.

Buat dan aktifkan virtual environment agar paket Python terpisah dari proyek lain.

**Windows (PowerShell):**

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python --version
```

**macOS / Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
python --version
```

Aktifkan kembali `.venv` setiap membuka terminal baru. Jika `.venv` sudah tersedia di komputer sendiri, cukup jalankan perintah aktivasi.

## 2. Siapkan data

Data santri asli tidak disertakan dalam repository. Untuk mencoba dengan tiga calon santri fiktif, salin file contoh dengan perintah berikut. **Jalankan hanya jika file tujuan belum berisi data yang ingin disimpan; cadangkan data yang sudah ada sebelum menggantinya.**

**Windows (PowerShell):**

```powershell
Copy-Item templates/contoh_input_dummy.csv data/Data_Pendaftar_PSB_Skala_1-5.csv
```

**macOS / Linux:**

```bash
cp -i templates/contoh_input_dummy.csv data/Data_Pendaftar_PSB_Skala_1-5.csv
```

Untuk memakai data sendiri, isi [template_input.csv](templates/template_input.csv), lalu simpan sebagai `data/Data_Pendaftar_PSB_Skala_1-5.csv`. Pertahankan header, gunakan pemisah titik koma (`;`) dan encoding UTF-8. Panduan tiap kolom tersedia di [PANDUAN_INPUT.md](templates/PANDUAN_INPUT.md).

## 3. Jalankan perhitungan

Pilih salah satu cara berikut. Notebook dan CLI membaca file data yang sama, tetapi pengaturan bobot dan folder hasilnya terpisah.

### Cara A — Notebook di VS Code

1. Dengan `.venv` aktif, pasang kernel notebook:

   ```bash
   python -m pip install ipykernel
   ```

2. Buka folder proyek di VS Code, lalu buka `notebooks/template_topsis.ipynb`. Notebook ini tersedia setelah clone dan belum berisi output. Jika ada `main.ipynb` untuk pekerjaan lokal, file itu juga dapat digunakan.
3. Klik **Select Kernel** di kanan atas notebook, lalu pilih lingkungan Python `.venv` proyek.
4. Di bagian **1. Informasi kriteria, rubrik, dan bobot**, sesuaikan `BOBOT` bila diperlukan. Bobot awal C1=0.30, C2=0.25, C3=0.20, C4=0.15, C5=0.10.
5. Biarkan `ALTERNATIF_CONTOH = "A1"` untuk data dummy, atau ganti dengan ID yang ada di CSV untuk melihat contoh substitusi santri lain.
6. Klik **Run All**. Setelah mengubah data atau bobot, restart kernel lalu jalankan semua sel kembali dari awal.

Jika berhasil, notebook menampilkan tabel ranking dan pesan **Pemeriksaan konsistensi lulus.** Hasil CSV/JSON tersimpan di folder `reports/`.

Notebook memakai `IPython` untuk menampilkan hasil, tidak mengimpor `topsis.py`, dan tidak membutuhkan pandas/NumPy. Perubahan `config.json` tidak mengubah bobot notebook; ubah `BOBOT` langsung di dalam notebook.

### Cara B — Notebook di browser dengan JupyterLab

Dengan `.venv` aktif, jalankan:

```bash
python -m pip install jupyterlab ipykernel
python -m jupyterlab
```

Buka alamat lokal yang ditampilkan terminal jika browser tidak terbuka otomatis. Pilih `notebooks/template_topsis.ipynb`, lalu jalankan seluruh sel melalui menu **Run → Run All Cells**. Pengaturan bobot dan hasilnya sama seperti Cara A. Untuk menghentikan JupyterLab, tekan `Ctrl+C` di terminal dan ikuti konfirmasi yang muncul.

### Cara C — Langsung dari terminal

Cara ini hanya menggunakan pustaka standar Python, sehingga tidak perlu memasang paket tambahan. Setelah menyiapkan data, jalankan:

```bash
python topsis.py --config config.json --output reports_cli
```

Hasil CSV/JSON disimpan di `reports_cli/`. Buka `reports_cli/08_peringkat.csv` dengan aplikasi spreadsheet atau editor teks untuk melihat ranking.

Untuk mengubah bobot CLI, edit bagian `weights` di `config.json`, lalu jalankan perintah yang sama lagi. Setiap bobot harus tidak negatif dan totalnya lebih dari nol; program menormalisasi total bobot secara otomatis. Hasil pada folder tujuan akan diperbarui setiap kali perintah dijalankan.

## 4. Lihat hasil

| Cara menjalankan | Lokasi hasil | Isi |
|---|---|---|
| Notebook | `reports/10_ranking.csv` | Ranking seluruh santri |
| Notebook | `reports/hasil_lengkap.json` | Data, bobot, dan seluruh hasil antara |
| Terminal | `reports_cli/08_peringkat.csv` | Ranking seluruh santri |
| Terminal | `reports_cli/hasil_lengkap.json` | Data, konfigurasi, dan seluruh hasil antara |

Eksekusi notebook mengekspor CSV/JSON. Jika tersedia, `reports/laporan_topsis.html` adalah salinan statis hasil notebook saat penyerahan dan tidak otomatis diperbarui saat notebook dijalankan.

## Kendala umum

- **`python`, `python3`, atau `py` tidak ditemukan:** pastikan Python sudah terpasang dan tersedia di PATH, lalu buka ulang terminal. Pada Windows, gunakan `py` untuk membuat `.venv`; setelah aktif, gunakan `python`.
- **Aktivasi PowerShell diblokir:** gunakan Command Prompt dan jalankan `.venv\Scripts\activate.bat`. Jalankan perintah Python berikutnya dari terminal yang sama.
- **`No module named IPython` atau kernel tidak tersedia:** aktifkan `.venv`, jalankan `python -m pip install ipykernel`, lalu pilih kembali kernel `.venv` di VS Code.
- **`FileNotFoundError` atau “Folder data tidak ditemukan”:** pastikan CSV sudah disimpan dengan nama persis `data/Data_Pendaftar_PSB_Skala_1-5.csv` dan buka notebook dari folder proyek.
- **Kolom wajib tidak ditemukan atau data tidak valid:** gunakan header template dan pemisah `;`. Isi seluruh kolom wajib; gunakan `1500000` untuk penghasilan, `85.5` untuk nilai desimal, dan skor bulat 1–5 untuk C1–C5.
- **`ALTERNATIF_CONTOH` tidak valid:** pilih ID yang ada di data. ID dibentuk dari kolom `No`, misalnya `No` bernilai `1` menjadi `A1`.

## Menjalankan pengujian

Dengan `.venv` aktif, jalankan dari akar proyek:

```bash
python -m unittest discover -s tests -v
```

Pengujian `test_nominal_income_is_used_as_cost` membaca CSV di `data/` dan mengasumsikan seluruh skor SKTM sama. Dengan data dummy yang skor SKTM-nya bervariasi, pengujian tersebut akan gagal pada pemeriksaan kontribusi jarak C5; perhitungan notebook dan CLI tetap dapat dijalankan.

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

## Catatan data

Penghasilan 0 dari isian `-` mengikuti konversi CSV dan perlu diverifikasi. Kolom jumlah saudara dipakai sebagai proksi tanggungan melalui skor C3; padanan ini perlu konfirmasi. Kasus 0 saudara belum tercantum dalam rubrik gambar. Semua SKTM memiliki skor yang sama sehingga tidak membedakan ranking. Rentang rubrik dipertahankan sebagai referensi; notebook tidak mengubah skor sumber secara diam-diam.

Hasil adalah rekomendasi prioritas berdasarkan data dan bobot aktif, bukan penetapan penerima. Kuota dan ketentuan kelayakan belum diberikan.


## Persiapan GitHub dan template input

- `.gitignore` mengecualikan `.venv/`, cache Python, data pribadi di `data/`, hasil di `reports/` dan `reports_cli/`, serta notebook lokal `main.ipynb` yang menyimpan output data santri.
- `notebooks/template_topsis.ipynb` adalah salinan notebook tanpa output untuk GitHub. Bobot dan langkah perhitungan tetap dapat dijalankan.
- `templates/template_input.csv` adalah template kosong yang sesuai dengan format pembaca CSV.
- `templates/contoh_input_dummy.csv` berisi tiga calon santri fiktif untuk mencoba notebook.
- `templates/PANDUAN_INPUT.md` menjelaskan isi setiap kolom, format angka, dan langkah pemakaian.

Jika ingin menyimpan hasil notebook untuk pekerjaan lokal, gunakan nama `main.ipynb` di akar proyek; nama ini sudah dikecualikan dari Git. Pastikan output di `notebooks/template_topsis.ipynb` tetap kosong sebelum commit. Output notebook tersebut akan terisi bila Anda menjalankannya.

Periksa `git status` sebelum commit; `.gitignore` tidak menghapus data yang sudah pernah dilacak atau di-commit.
