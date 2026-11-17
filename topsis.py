"""Perhitungan TOPSIS transparan. Hanya membutuhkan Python standard library."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA_FILE = ROOT / "data" / "Data_Pendaftar_PSB_Skala_1-5.csv"
TITLE = ("Sistem Penunjang Keputusan Seleksi Penerima Beasiswa Santri "
         "Berprestasi dan Kurang Mampu Menggunakan Metode TOPSIS")
INSTITUTION = "Pondok Pesantren Kreatif Sukamakmur YBM PLN"
CRITERIA = [
    {"code": "C1", "name": "Penghasilan Orang Tua", "column": "Penghasilan (Rp)",
     "type": "cost", "unit": "Rp/bulan", "reason": "Indikator ekonomi riil paling krusial untuk sasaran zakat."},
    {"code": "C2", "name": "Prestasi Akademik", "column": "C2 (Prestasi)",
     "type": "benefit", "unit": "skor 1–5", "reason": "Menjaga standar mutu bahwa penerima beasiswa memang berprestasi."},
    {"code": "C3", "name": "Jumlah Tanggungan Ortu", "column": "C3 (Tanggungan)",
     "type": "benefit", "unit": "skor 1–5", "reason": "Mengukur seberapa berat beban pembagi ekonomi keluarga."},
    {"code": "C4", "name": "Status Orang Tua", "column": "C4 (Status Ortu)",
     "type": "benefit", "unit": "skor 1–5", "reason": "Prioritas perlindungan bagi santri yatim, piatu, atau single parent."},
    {"code": "C5", "name": "Keberadaan SKTM", "column": "C5 (SKTM)",
     "type": "benefit", "unit": "skor 1–5", "reason": "Validasi administratif dari pihak pemerintah/desa."},
]
DEFAULT_WEIGHTS = {"C1": .30, "C2": .25, "C3": .20, "C4": .15, "C5": .10}
NOTES = [
    "C1 menggunakan Penghasilan (Rp) sebagai cost: semakin rendah, semakin diprioritaskan. "
    "Skor C1 (Penghasilan) 1–5 pada CSV tetap ditampilkan sebagai data sumber, tetapi tidak digunakan "
    "dalam matriks karena skor tersebut sudah mengutamakan penghasilan rendah.",
    "C2–C5 menggunakan skor konversi yang sudah ada pada CSV. Rubrik dari gambar pengguna "
    "ditampilkan sebagai referensi; sistem tidak mengubah skor sumber secara diam-diam.",
    "Kolom sumber berisi Jumlah Saudara, bukan jumlah tanggungan orang tua yang terverifikasi. "
    "C3 memakai skor yang tersedia sebagai proksi sementara dan perlu dikonfirmasi panitia.",
    "Penghasilan 0 dari isian '-' mengikuti konversi pada CSV dan perlu diverifikasi. "
    "TOPSIS memperlakukan 0 sebagai penghasilan terendah sehingga berpengaruh pada prioritas.",
    "Semua pendaftar memiliki skor SKTM 5. C5 tetap dihitung dengan bobotnya, tetapi selisih "
    "terhadap ideal positif dan negatif sama-sama 0, sehingga tidak membedakan alternatif.",
    "Hasil adalah urutan rekomendasi, bukan penetapan penerima atau peluang kelulusan. "
    "Kuota dan ketentuan kelayakan belum ditentukan. Nilai seri mendapat peringkat yang sama "
    "(toleransi absolut 10⁻¹²); urutan tampilan seri mengikuti data sumber.",
]


def load_data(path=DATA_FILE):
    """Baca CSV titik koma; tolak data hilang, duplikat, dan skor di luar 1–5."""
    path = Path(path)
    numeric = ["Penghasilan (Rp)", "Nilai Rata-Rata", "Jumlah Saudara",
               "C1 (Penghasilan)", "C2 (Prestasi)", "C3 (Tanggungan)", "C4 (Status Ortu)", "C5 (SKTM)"]
    text_cols = ["No", "Nama Lengkap Calon Santri", "Penghasilan Asli", "Status Orang Tua",
                 "Berkas SKTM", "Keterangan Konversi"]
    with path.open(encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f, delimiter=";")
        missing = set(numeric + text_cols) - set(reader.fieldnames or [])
        if missing:
            raise ValueError(f"Kolom wajib tidak ditemukan: {sorted(missing)}")
        rows, seen = [], set()
        for line, row in enumerate(reader, 2):
            if None in row or any(row.get(c) is None or not row[c].strip() for c in numeric + text_cols):
                raise ValueError(f"Baris {line}: data kosong atau jumlah kolom tidak sesuai.")
            row = {k: v.strip() for k, v in row.items()}
            if not row["No"].isdigit() or int(row["No"]) < 1:
                raise ValueError(f"Baris {line}: No harus bilangan bulat positif.")
            row["id"] = f"A{int(row['No'])}"
            if row["id"] in seen:
                raise ValueError(f"Baris {line}: ID {row['id']} duplikat.")
            seen.add(row["id"])
            for col in numeric:
                try:
                    value = float(row[col])
                except (ValueError, TypeError) as exc:
                    raise ValueError(f"Baris {line}: {col} harus numerik.") from exc
                if not math.isfinite(value) or value < 0:
                    raise ValueError(f"Baris {line}: {col} harus berhingga dan tidak negatif.")
                if col.startswith("C") and (value != int(value) or not 1 <= value <= 5):
                    raise ValueError(f"Baris {line}: {col} harus skor bulat 1–5.")
                if col == "Jumlah Saudara" and value != int(value):
                    raise ValueError(f"Baris {line}: Jumlah Saudara harus bilangan bulat.")
                if col == "Nilai Rata-Rata" and value > 100:
                    raise ValueError(f"Baris {line}: Nilai Rata-Rata harus 0–100.")
                row[col] = int(value) if value.is_integer() else value
            rows.append(row)
    if not rows:
        raise ValueError("CSV tidak berisi pendaftar.")
    return rows


def calculate(matrix, weights, types):
    """TOPSIS normalisasi vektor; seluruh hasil antara dikembalikan tanpa pembulatan."""
    if not matrix or not weights or len(types) != len(weights):
        raise ValueError("Matriks, bobot, dan sifat kriteria harus lengkap.")
    n = len(weights)
    if any(t not in {"benefit", "cost"} for t in types):
        raise ValueError("Sifat kriteria harus benefit atau cost.")
    if any(isinstance(w, bool) or not isinstance(w, (int, float)) or not math.isfinite(w) or w < 0 for w in weights):
        raise ValueError("Bobot harus bilangan berhingga dan tidak negatif.")
    if not math.isfinite(sum(weights)) or sum(weights) <= 0:
        raise ValueError("Total bobot harus berhingga dan lebih besar dari 0.")
    if any(len(row) != n for row in matrix):
        raise ValueError("Jumlah kolom matriks harus sama dengan jumlah bobot.")
    if any(isinstance(x, bool) or not isinstance(x, (int, float)) or not math.isfinite(x) or x < 0
           for row in matrix for x in row):
        raise ValueError("Nilai matriks harus berhingga dan tidak negatif.")
    w = [x / sum(weights) for x in weights]
    squared = [[x * x for x in row] for row in matrix]
    sums = [sum(row[j] for row in squared) for j in range(n)]
    norms = [math.sqrt(x) for x in sums]
    # Kolom nol tidak memiliki variasi; normalisasinya didefinisikan 0.
    normalized = [[x / norms[j] if norms[j] else 0.0 for j, x in enumerate(row)] for row in matrix]
    weighted = [[x * w[j] for j, x in enumerate(row)] for row in normalized]
    positive, negative = [], []
    for j, kind in enumerate(types):
        col = [row[j] for row in weighted]
        positive.append(max(col) if kind == "benefit" else min(col))
        negative.append(min(col) if kind == "benefit" else max(col))
    plus_sq = [[(x - positive[j]) ** 2 for j, x in enumerate(row)] for row in weighted]
    minus_sq = [[(x - negative[j]) ** 2 for j, x in enumerate(row)] for row in weighted]
    d_plus = [math.sqrt(sum(row)) for row in plus_sq]
    d_minus = [math.sqrt(sum(row)) for row in minus_sq]
    # Semua alternatif identik pada kriteria aktif: tidak ada pembeda, skor netral 0.5.
    scores = [b / (a + b) if a + b > 0 else .5 for a, b in zip(d_plus, d_minus)]
    order = sorted(range(len(matrix)), key=lambda i: -scores[i])
    ranks, reference_score, reference_rank = [0] * len(matrix), None, None
    for position, i in enumerate(order, 1):
        if reference_score is None or abs(scores[i] - reference_score) > 1e-12:
            reference_score, reference_rank = scores[i], position
        ranks[i] = reference_rank
    return {"matrix": matrix, "weights": w, "types": types, "squared": squared,
            "sums": sums, "norms": norms, "normalized": normalized, "weighted": weighted,
            "positive": positive, "negative": negative, "plus_sq": plus_sq, "minus_sq": minus_sq,
            "d_plus": d_plus, "d_minus": d_minus, "scores": scores, "order": order, "ranks": ranks}


def analyze(rows, weights=None, types=None):
    weights = DEFAULT_WEIGHTS if weights is None else weights
    types = {c["code"]: c["type"] for c in CRITERIA} if types is None else types
    expected = {c["code"] for c in CRITERIA}
    if set(weights) != expected or set(types) != expected:
        raise ValueError("Konfigurasi harus memuat tepat C1, C2, C3, C4, dan C5.")
    matrix = [[row[c["column"]] for c in CRITERIA] for row in rows]
    return calculate(matrix, [weights[c["code"]] for c in CRITERIA], [types[c["code"]] for c in CRITERIA])


def fmt(value, digits=6):
    if isinstance(value, float):
        return f"{value:,.{digits}f}".translate(str.maketrans({",": ".", ".": ","}))
    if isinstance(value, int):
        return f"{value:,}".replace(",", ".")
    return str(value)


def table(headers, rows, caption=""):
    head = "".join(f"<th scope='col'>{escape(str(h))}</th>" for h in headers)
    body = "".join("<tr>" + "".join(f"<td>{escape(fmt(v))}</td>" for v in row) + "</tr>" for row in rows)
    return ("<div class='table-wrap' role='region' tabindex='0' aria-label='" + escape(caption, quote=True) +
            "'><table><caption>" + escape(caption) + "</caption><thead><tr>" + head +
            "</tr></thead><tbody>" + body + "</tbody></table></div>")


def matrix_table(rows, matrix, caption):
    return table(["Alternatif", "Nama santri"] + [c["code"] for c in CRITERIA],
                 [[row["id"], row["Nama Lengkap Calon Santri"], *values] for row, values in zip(rows, matrix)], caption)


def export_results(rows, result, output_dir):
    """Ekspor seluruh matriks dan hasil tanpa pembulatan dalam CSV dan JSON."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    codes = [c["code"] for c in CRITERIA]

    def write_csv(name, headers, values):
        with (output_dir / name).open("w", encoding="utf-8-sig", newline="") as f:
            writer = csv.writer(f, delimiter=";")
            writer.writerow(headers)
            writer.writerows(values)

    for number, key in enumerate(["matrix", "squared", "normalized", "weighted", "plus_sq", "minus_sq"], 1):
        write_csv(f"{number:02}_{key}.csv", ["Alternatif", "Nama santri", *codes],
                  [[row["id"], row["Nama Lengkap Calon Santri"], *values] for row, values in zip(rows, result[key])])
    write_csv("07_pembagi_dan_ideal.csv", ["Kriteria", "Sifat", "Bobot", "Jumlah kuadrat", "Pembagi", "A+", "A-"],
              [[c["code"], result["types"][j], result["weights"][j], result["sums"][j], result["norms"][j],
                result["positive"][j], result["negative"][j]] for j, c in enumerate(CRITERIA)])
    write_csv("08_peringkat.csv", ["Peringkat", "Alternatif", "Nama santri", "D+", "D-", "V", "Catatan verifikasi"],
              [[result["ranks"][i], rows[i]["id"], rows[i]["Nama Lengkap Calon Santri"], result["d_plus"][i],
                result["d_minus"][i], result["scores"][i], verification(rows[i])] for i in result["order"]])
    payload = {"title": TITLE, "institution": INSTITUTION, "criteria": CRITERIA, "notes": NOTES,
               "rows": rows, "weights": result["weights"], "types": result["types"],
               "source": DATA_FILE.name,
               "source_sha256": hashlib.sha256(DATA_FILE.read_bytes()).hexdigest()}
    (output_dir / "hasil_lengkap.json").write_text(json.dumps({**payload, "result": result}, ensure_ascii=False, indent=2), encoding="utf-8")
    return output_dir


def verification(row):
    return ("Verifikasi penghasilan 0 dari isian '-'" if row["Penghasilan Asli"] == "-"
            else "Tinjau asumsi nominal" if "Asumsi" in row["Keterangan Konversi"] else "Tinjau konversi sumber")


def main():
    parser = argparse.ArgumentParser(description=TITLE)
    parser.add_argument("--config", type=Path, default=ROOT / "config.json")
    parser.add_argument("--output", type=Path, default=ROOT / "reports_cli")
    args = parser.parse_args()
    config = json.loads(args.config.read_text(encoding="utf-8"))
    rows = load_data()
    result = analyze(rows, config["weights"], config["types"])
    output = export_results(rows, result, args.output)
    print(f"Selesai: {len(rows)} alternatif, {len(CRITERIA)} kriteria. Hasil CSV/JSON: {output}")
    print("Peringkat adalah rekomendasi dan perlu verifikasi panitia.")


if __name__ == "__main__":
    main()
