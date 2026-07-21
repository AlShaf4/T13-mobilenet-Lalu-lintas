# Klasifikasi Rambu Lalu Lintas dengan Transfer Learning MobileNetV2

Aplikasi web berbasis Flask yang mengklasifikasikan gambar rambu lalu lintas ke dalam 43 kelas menggunakan model deep learning hasil Transfer Learning dengan arsitektur MobileNetV2. Dibuat sebagai pemenuhan Tugas 13 mata kuliah Praktikum Kecerdasan Buatan.

## Informasi Tugas


|
 Keterangan 
|
 Detail 
|
|
---
|
---
|
|
 Judul Tugas 
|
 Implementasi Transfer Learning MobileNetV2 untuk Klasifikasi Rambu Lalu Lintas Berbasis Website Menggunakan Flask 
|
|
 Nama 
|
 Selsa Shafana Alfiyani 
|
|
 NIM 
|
 301240041 
|
|
 Universitas 
|
 Universitas Bale Bandung (UNIBBA) 
|
|
 Mata Kuliah 
|
 Praktikum Kecerdasan Buatan 
|


## Deskripsi

Website ini memungkinkan pengguna mengunggah foto rambu lalu lintas, lalu sistem akan mengenali jenisnya secara otomatis menggunakan model MobileNetV2 yang telah dilatih pada dataset GTSRB. Selain fitur klasifikasi utama, website juga dilengkapi halaman edukatif berisi penjelasan dataset, teknologi yang dipakai (lengkap dengan grafik hasil training), panduan penggunaan, dan profil pembuat.

## Fitur

- Klasifikasi gambar rambu lalu lintas ke dalam 43 kelas dengan tingkat keyakinan (confidence score)
- Upload gambar lewat drag & drop atau klik pilih file
- Menampilkan 3 kemungkinan hasil teratas (top-3 prediction)
- Pewarnaan otomatis hasil berdasarkan kategori rambu (merah untuk larangan/bahaya, biru untuk wajib/petunjuk)
- Halaman informasi dataset (GTSRB)
- Halaman penjelasan teknologi (Transfer Learning, MobileNetV2) beserta grafik akurasi & loss training
- Halaman panduan penggunaan
- Tampilan modern bertema gelap, responsif untuk mobile dan desktop

## Dataset

Dataset yang digunakan adalah **GTSRB — German Traffic Sign Recognition Benchmark**, sebuah benchmark riset resmi dari IJCNN (International Joint Conference on Neural Networks) 2011.

- Sumber: [Kaggle - GTSRB](https://www.kaggle.com/datasets/meowmeowmeowmeowmeow/gtsrb-german-traffic-sign)
- Jumlah kelas: 43 jenis rambu lalu lintas
- Jumlah gambar: 39.209 data training, 12.630 data uji
- Struktur folder `Train/` berisi 43 subfolder bernama angka `0` sampai `42` (bukan zero-padded)
- Folder `Test/` tidak dilengkapi label valid pada dataset yang digunakan, sehingga hanya dipakai untuk uji coba manual, bukan pengukuran akurasi resmi

## Arsitektur Model

MobileNetV2 (pretrained ImageNet, include_top=False, frozen)
↓
GlobalAveragePooling2D
↓
Dense(128, activation='relu')
↓
Dropout(0.5)
↓
Dense(43, activation='softmax')


| Keterangan | Jumlah |
|---|---|
| Total parameter | 2.427.499 (~9,26 MB) |
| Parameter dilatih (trainable) | 169.515 |
| Parameter beku dari base model | 2.257.984 |
| Akurasi validasi akhir | ± 65% (lihat catatan di bagian Hasil Training) |

## Struktur Folder

PROJECT_MOBILENET_TRAFFICSIGN/
│
├── templates/
│ ├── index.html → Beranda
│ ├── klasifikasi.html → Upload & hasil prediksi
│ ├── tentang_dataset.html → Info dataset GTSRB
│ ├── tentang_teknologi.html → Penjelasan materi + grafik training
│ ├── tentang_kami.html → Profil pembuat
│ └── cara_penggunaan.html → Panduan pemakaian
│
├── static/
│ ├── css/
│ │ └── styles.css
│ ├── js/
│ │ └── scripts.js
│ └── img/
│ ├── stop.png
│ ├── speed20.png
│ ├── no_entry.png
│ ├── turn_right.png
│ └── grafik_training.png → dihasilkan otomatis oleh train_model.py
│
├── dataset/
│ ├── Train/ → 43 folder kelas (0 sampai 42)
│ └── Test/ → gambar tanpa label valid, uji manual saja
│
├── venv/ → (masuk .gitignore)
│
├── app.py → Aplikasi utama Flask
├── train_model.py → Script training model
├── class_mapping.py → Dictionary 43 nama kelas rambu
├── labels.json → dihasilkan otomatis oleh train_model.py
├── mobilenet_traffic_sign.h5 → model hasil training
│
├── Procfile → perintah start untuk Railway
├── requirements.txt
├── .gitignore
└── README.md


## Teknologi yang Digunakan

- Python 3
- TensorFlow / Keras — training & inference model
- Flask — web framework backend
- Gunicorn — WSGI server untuk production
- HTML, CSS, JavaScript (vanilla) — frontend
- Matplotlib — visualisasi grafik hasil training
- Font Awesome — ikon
- Google Fonts (Poppins) — tipografi

## Cara Menjalankan di Lokal

### 1. Clone repository

```bash
git clone https://github.com/AlShaf4/T133-mobilenet-Lalu-lintas.git
cd PROJECT_MOBILENET_TRAFFICSIGN
```

### 2. Buat dan aktifkan virtual environment

```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # macOS / Linux
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Siapkan dataset

Download dataset GTSRB dari Kaggle, lalu ekstrak sehingga strukturnya menjadi:

dataset/
├── Train/ (berisi 43 folder kelas: 0 sampai 42)
└── Test/


### 5. Latih model

```bash
python train_model.py
```

Setelah selesai, script ini otomatis menghasilkan:
- `mobilenet_traffic_sign.h5` — model terlatih
- `labels.json` — mapping index kelas hasil generator ke nomor kelas asli
- `static/img/grafik_training.png` — grafik akurasi & loss training

> **Catatan:** proses training dengan CPU membutuhkan waktu cukup lama (bisa 3–5 jam untuk 15 epoch tergantung spesifikasi komputer), karena dataset berisi lebih dari 39.000 gambar training.

### 6. Jalankan aplikasi

```bash
python app.py
```

Buka `http://127.0.0.1:5000/` di browser.

## Hasil Training

| Epoch | Akurasi Training | Loss Training | Akurasi Validasi | Loss Validasi |
|---|---|---|---|---|
| 1 | 43,78% | 1,9290 | 56,29% | 1,3674 |
| 5 | 67,17% | 0,9859 | 64,06% | 1,1502 |
| 10 | 71,81% | 0,8388 | 65,57% | 1,1252 |
| 12 | 72,75% | 0,8044 | 66,75% (tertinggi) | 1,0652 (terendah) |
| 15 | 73,90% | 0,7684 | 65,25% | 1,1804 |

Akurasi evaluasi akhir pada data validasi: **65,34%**

Terdapat indikasi overfitting ringan pada epoch-epoch akhir, ditandai akurasi training yang terus naik namun akurasi validasi yang justru sedikit menurun. Grafik lengkap tersedia di halaman **Tentang Teknologi** pada aplikasi setelah model dilatih.

## Deployment

Aplikasi ini dikonfigurasi untuk deploy ke [Railway](https://railway.app) menggunakan `Procfile` dan `gunicorn`.

**Isi `Procfile`:**

web: gunicorn app:app --bind 0.0.0.0:$PORT --timeout 120


**Langkah deploy:**
1. Push seluruh project (termasuk `mobilenet_traffic_sign.h5` dan `labels.json`) ke GitHub
2. Buka Railway → New Project → Deploy from GitHub repo
3. Railway otomatis mendeteksi `requirements.txt` dan `Procfile`
4. Setelah build selesai, generate domain publik lewat Settings → Networking

## Catatan & Keterbatasan

- Rambu dalam dataset merupakan standar Jerman, sehingga mungkin ada sedikit perbedaan desain dengan rambu di Indonesia
- Folder `Test/` pada dataset tidak memiliki label resmi, sehingga tidak digunakan untuk mengukur akurasi akhir model
- `flow_from_directory` mengurutkan folder kelas secara alfabetis sebagai string, bukan numerik — karena itu mapping index ke nama kelas dilakukan lewat `labels.json`, bukan asumsi langsung index = nomor kelas
- Model menggunakan TensorFlow penuh (bukan TFLite), sehingga proses build dan cold start saat deployment membutuhkan RAM yang cukup besar

## Lisensi

Proyek ini dibuat untuk keperluan tugas akademik (Praktikum Kecerdasan Buatan, UNIBBA) dan tidak untuk penggunaan komersial. Dataset GTSRB digunakan sesuai lisensi yang berlaku di Kaggle.
