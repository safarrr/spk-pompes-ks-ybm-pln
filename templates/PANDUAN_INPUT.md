# Template input data calon santri

`template_input.csv` berisi header kosong yang sesuai dengan pembaca data notebook. `contoh_input_dummy.csv` berisi tiga calon santri fiktif untuk contoh pengisian dan pengujian. File contoh tidak memuat data santri asli.

## Cara mengisi

1. Salin `template_input.csv` menjadi file kerja, lalu isi satu calon santri per baris.
2. Pertahankan nama dan urutan semua kolom. Gunakan pemisah titik koma (`;`) dan encoding UTF-8.
3. Simpan sebagai `data/Data_Pendaftar_PSB_Skala_1-5.csv`. Jika file tersebut sudah berisi data asli, simpan cadangannya terlebih dahulu agar tidak tertimpa.
4. Buka `main.ipynb` untuk pekerjaan lokal, atau `notebooks/template_topsis.ipynb` dari GitHub. Sesuaikan `BOBOT` lalu jalankan semua sel dari awal.

Untuk langsung mencoba, salin `contoh_input_dummy.csv` ke lokasi dan nama yang disebut pada langkah 3. Notebook mencari folder `data/` dari direktori kerja dan direktori induknya, sehingga template dalam folder `notebooks/` dapat memakai data di akar proyek.

## Informasi kolom

| Kolom | Isi | Contoh | Aturan |
|---|---|---|---|
| No | Nomor urut calon santri | 1 | Bilangan bulat positif, unik. Sistem membentuk ID A1, A2, dan seterusnya. |
| Nama Lengkap Calon Santri | Nama calon santri | SANTRI CONTOH 001 | Wajib terisi. Gunakan nama fiktif untuk contoh yang dibagikan. |
| Penghasilan Asli | Isian penghasilan sebelum penyeragaman | Rp1.500.000/bulan | Teks wajib terisi untuk penelusuran sumber. |
| Penghasilan (Rp) | Nominal penghasilan bulanan | 1500000 | Angka tanpa Rp atau pemisah ribuan. Dipakai sebagai C1 Cost. |
| Nilai Rata-Rata | Nilai akademik asli | 85.5 | Angka 0–100; gunakan titik untuk desimal. |
| Jumlah Saudara | Jumlah saudara sesuai sumber | 3 | Bilangan bulat tidak negatif. Jangan menganggapnya otomatis sama dengan tanggungan orang tua. |
| Status Orang Tua | Kondisi orang tua | YATIM | Contoh: YATIM PIATU, YATIM, PIATU, CERAI, ORANG TUA LENGKAP. |
| Berkas SKTM | Ketersediaan SKTM | Ada | Isi Ada atau Tidak Ada. |
| C1 (Penghasilan) | Skor konversi penghasilan | 4 | Bilangan bulat 1–5. Tetap diwajibkan format CSV, tetapi tidak dipakai dalam perhitungan karena C1 menggunakan nominal rupiah. |
| C2 (Prestasi) | Skor prestasi akademik | 4 | Bilangan bulat 1–5. Dipakai sebagai C2 Benefit. |
| C3 (Tanggungan) | Skor tanggungan | 3 | Bilangan bulat 1–5. Dipakai sebagai C3 Benefit; verifikasi kesesuaiannya dengan jumlah tanggungan. |
| C4 (Status Ortu) | Skor kondisi orang tua | 4 | Yatim piatu=5; yatim=4; piatu=3; cerai=2; lengkap=1. |
| C5 (SKTM) | Skor kepemilikan SKTM | 5 | Ada=5; tidak ada=1. |
| Keterangan Konversi | Penjelasan penyeragaman data | Sesuai nominal | Wajib terisi; jelaskan asumsi atau perubahan satuan bila ada. |

## Perhatian saat mengisi

- Notebook saat ini memakai **nominal asli untuk C1**, serta **skor yang sudah diisi untuk C2–C5**. Template tidak otomatis mengubah data asli menjadi skor.
- Gunakan rubrik yang disepakati panitia. Rentang batas C1/C2 pada gambar dan kasus jumlah tanggungan 0 perlu ketentuan yang jelas sebelum membuat konversi otomatis; jangan menetapkan ambang sendiri tanpa kesepakatan.
- Jangan mengganti penghasilan yang belum diketahui menjadi 0 tanpa verifikasi. Nol dianggap penghasilan riil terendah dalam C1 Cost.
- Angka `1500000` dan `85.5` valid; hindari `1.500.000` dan `85,5` pada kolom numerik.
- Jangan mengosongkan kolom wajib. Jika memakai titik koma di dalam teks, bungkus teks dengan tanda kutip sesuai format CSV; aplikasi spreadsheet biasanya melakukannya saat ekspor.
- Validasi format tidak menjamin bahwa skor sudah sesuai kondisi nyata. Tinjau kembali data dan rubrik sebelum memakai ranking.

## Berkas untuk GitHub

Template kosong, contoh fiktif, panduan, dan `notebooks/template_topsis.ipynb` boleh dimasukkan ke Git. Folder `data/`, `reports/`, `reports_cli/`, dan notebook lokal `main.ipynb` dikecualikan karena dapat berisi data pribadi.

`.gitignore` hanya berlaku untuk file yang belum dilacak Git. Jika data sudah pernah di-commit, menambahkan `.gitignore` tidak menghapusnya dari riwayat. Periksa `git status` dan daftar file yang akan di-commit sebelum push.
