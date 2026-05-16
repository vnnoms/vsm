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
2. Buka terminal atau Command Prompt, lalu arahkan posisi ke folder proyek ini menggunakan perintah cd. Contoh:
   cd Documents/Aljabar_Linear/vsm

3. Install library NLTK yang dibutuhkan dengan mengetik perintah:
   pip install -r requirements.txt

4. Jalankan program utama dengan memberikan argumen file daftar dokumen dan file query yang ingin diuji coba. Perintah eksekusinya:
   python vsm.py base.txt query1.txt

   *Catatan: Pengguna bisa mengganti "query1.txt" menjadi "query2.txt" atau "query3.txt" di terminal untuk mencoba variasi kata kunci pengujian lainnya.

---

## 3. Contoh Hasil Keluaran Program

Setiap kali dijalankan, program akan otomatis membuat atau memperbarui tiga file hasil (output) di dalam folder:

A. File index.txt (Inverted Index)
Menampilkan daftar kata bersih yang ditemukan di seluruh dokumen, diikuti informasi nomor dokumen dan nilai bobot skornya (dibulatkan 1 angka desimal).
Contoh isi:
algebra: 1,0.2 2,0.2 5,0.2
matrix: 1,0.7
scienc: 1,0.7

B. File weights.txt (Daftar Bobot Dokumen)
Menampilkan daftar kata-kata yang ada di setiap dokumen lengkap beserta nilai bobot detail hasil hitungan dengan presisi 4 angka desimal.
Contoh isi:
doc1.txt: python, 0.6990 scienc, 0.6990 linear, 0.0969 model, 0.0969
doc2.txt: retriev, 0.2218 phyton, 0.3979 linear, 0.0969 algebra, 0.2218

C. File response.txt (Hasil Perangkingan)
Baris pertama adalah jumlah total dokumen yang cocok dengan query (skor lebih dari 0.001). Baris berikutnya menampilkan nama file dokumen dan nilai kemiripannya, diurutkan secara otomatis dari peringkat tertinggi ke terendah.
Contoh isi:
3
doc1.txt 0.5843
doc5.txt 0.1224
doc2.txt 0.0912
