# Tugas Implementasi Vector Space Model (VSM)
**Mata Kuliah:** Aljabar Linear JTK POLBAN   
**Oleh:** Muhammad Rizqi Sholahuddin   
**Tanggal:** 12 Mei 2026 

## 1. Penjelasan Singkat Algoritma
Program ini mengimplementasikan Vector Space Model (VSM) untuk sistem temu balik informasi (information retrieval). Dokumen teks dan query pencarian direpresentasikan sebagai vektor dalam ruang multidimensi, di mana setiap dimensi mewakili satu kata unik (term) yang telah melalui proses pembersihan.

Proses komputasi dilakukan melalui tahap-tahap berikut:
1. Preprocessing: Teks mentah dari dokumen dan query diubah menjadi huruf kecil (case folding), dipecah menjadi kata individual (tokenization), dibersihkan dari kata umum (stopwords) serta tanda baca, dan direduksi ke bentuk dasarnya menggunakan algoritma Porter Stemmer.
2. Pembobotan TF-IDF: Mengukur bobot kepentingan suatu kata di dalam dokumen.
   * Term Frequency (TF) dihitung secara logaritmik: $TF = 1 + \log_{10}(\text{freq})$ jika kata muncul, dan $0$ jika tidak.
   * Inverse Document Frequency (IDF) dihitung berdasarkan kelangkaan kata di seluruh koleksi dokumen: $IDF = \log_{10}(N/n)$.
   * Bobot Akhir: Nilai $TF \times IDF$.
3. Cosine Similarity: Menghitung sudut kosinus antara vektor dokumen ($v_d$) dan vektor query ($v_q$) untuk menentukan tingkat kemiripan relevansi:
   $$\text{Similarity}(d,q) = \frac{v_d \cdot v_q}{\|v_d\| \cdot \|v_q\|}$$

## 2. Cara Menjalankan Program

### Persyaratan Sistem
* Python 3.13 atau versi terbaru 
* Library NLTK (`nltk`) 

### Langkah-Langkah Eksekusi
1. Pastikan folder proyek memiliki struktur file yang sejajar sebagai berikut:
   ```text
   vsm/
   ├── vsm.py            # Program utama
   ├── requirements.txt  # Dependensi library
   ├── base.txt          # Daftar file dokumen (Minimal 5 dokumen)
   ├── query.txt         # Query pencarian (Minimal 3 variasi file pengujian)
   ├── doc1.txt          # Dokumen teks bahasa Inggris 1
   ├── doc2.txt          # Dokumen teks bahasa Inggris 2
   └── ...
