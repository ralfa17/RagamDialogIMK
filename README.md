# Playcloud Music Player - Arctic Monkeys Edition
> **Tugas Mata Kuliah:** Interaksi Manusia dan Komputer (IMK)  
> **Topik:** Implementasi 9 Kategori Ragam Dialog Interaktif (*Interactive Dialogue Styles*)  
> **Gaya Desain:** Playcloud Modern UI (Dark Charcoal `#0E0E10`, Soft Terracotta `#E56B45`, Layout 3 Kolom)  
> **Teknologi:** Python (Flask Backend) + HTML5 Web Audio (`<audio>` real preview) + Tailwind CSS + Vanilla JS  

---

## 🎵 Pembaruan Utama (Iterasi & Redesain)

### 1. Desain Visual & Tata Letak Orisinal (Gaya Playcloud UI)
- **Skema Warna Hangat & Adem:**
  - Latar belakang dark charcoal lembut (`#0E0E10`)
  - Kartu & panel abu-abu gelap terstruktur (`#18181C` dan `#1F1F24`) dengan sudut membulat besar (`rounded-2xl` & `rounded-3xl`) serta border tipis transparan (`border-white/5`).
  - Aksen warna **Warm Terracotta / Soft Coral (`#E56B45`)** menggantikan aksen Spotify, memberikan kesan premium, modern, dan orisinal.
- **Tata Letak 3 Kolom Responsif:**
  1. **Sidebar Kiri:** Brand Playcloud, menu navigasi datar (*Home, Albums, Tracks, IMK Lab*), dan daftar *Playlists*.
  2. **Area Utama (Tengah):** Natural Language bar di atas, *Hero Curated Playlist Banner* dengan gradasi terracotta hangat, dan grid kartu album/lagu beranimasi hover.
  3. **Panel Kanan (Right Dock):** Widget *Now Playing* lengkap dengan **Real-time Waveform Audio Visualizer**, tombol aksi cepat, serta tab *Antrean (Queue)* yang mendukung Drag-and-Drop.
- **Bottom Player Bar Bersih:** Memuat thumbnail lagu, judul & album, tombol kontrol ikon universal di tengah, serta slider durasi (*scrubbing*) dan slider volume di kanan.

---

### 2. Pemutaran Audio Nyata & 10 Lagu Arctic Monkeys
Aplikasi memutar audio nyata melalui elemen HTML5 `<audio>` yang terhubung ke state aplikasi (Play/Pause, Next, Previous, Volume, dan Seeking Progress Bar).

10 Lagu Arctic Monkeys yang terdaftar:
1. *Do I Wanna Know?* (Album: AM, 2013)
2. *R U Mine?* (Album: AM, 2013)
3. *Arabella* (Album: AM, 2013)
4. *Knee Socks* (Album: AM, 2013)
5. *Snap Out of It* (Album: AM, 2013)
6. *One for the Road* (Album: AM, 2013)
7. *No. 1 Party Anthem* (Album: AM, 2013)
8. *Mardy Bum* (Album: Whatever People Say I Am, That's What I Am Not, 2006)
9. *505* (Album: Favourite Worst Nightmare, 2007)
10. *Crying Lightning* (Album: Humbug, 2009)

**Mekanisme Audio:**
- Secara otomatis mengambil stream audio preview 30 detik resmi dan cover album 600x600 dari **iTunes Search API** (`https://itunes.apple.com/search?term=Arctic+Monkeys+[judul]&entity=song&limit=1`).
- Didukung sistem *caching in-memory* di Python backend `app.py`.
- Mendukung file lokal `.mp3` jika diletakkan di folder `static/audio/<slug>.mp3`.

---

## 📌 Pemetaan 9 Kategori Ragam Dialog Interaktif

| No | Kategori Ragam Dialog | Komponen Antarmuka Web | Logika Pemrosesan di Python (`app.py`) |
|:--:|---|---|---|
| **1** | **Dialog Berbasis Perintah Tunggal** *(Command Line Dialogue)* | Panel **CLI Terminal** di tab *IMK Lab* (dapat dibuka cepat via tombol *Terminal* atau pintasan `Ctrl+K`). Perintah: `PLAY "505"`, `PAUSE`, `NEXT`, `VOLUME 80`, dll. | Endpoint `POST /api/cli` mem-parsing token teks perintah dan argumennya, lalu mengembalikan aksi pemutar audio. |
| **2** | **Dialog Berbasis Bahasa Pemrograman** *(Batch Script Dialogue)* | Editor teks **Playlist Batch Script Runner** di tab *IMK Lab* untuk mengeksekusi kumpulan baris instruksi sekaligus. | Endpoint `POST /api/batch` menginterpretasikan baris demi baris perintah secara sekuensial dan menghasilkan log status eksekusi. |
| **3** | **Antarmuka Berbasis Bahasa Alami** *(Natural Language Interface)* | Bilah **Smart Music Assistant** di bilah atas (*Header*) dengan pemahaman kalimat santai (contoh: *"Putar lagu galau Arctic Monkeys"* $\rightarrow$ memutar *505*, *"Kecilin suaranya"* $\rightarrow$ volume -20%). | Endpoint `POST /api/nlp` menganalisis maksud (*intent*) dan kata kunci Bahasa Indonesia sehari-hari. |
| **4a** | **Sistem Menu Datar** *(Flat Menu)* | Navigasi vertikal di sidebar kiri (*Home, Albums, Tracks, IMK Lab*) dengan **Highlight Marker** oranye terracotta pada menu aktif. | Menampilkan opsi pada satu tingkatan datar yang mudah dijangkau tanpa percabangan rumit. |
| **4b** | **Sistem Menu Tarik** *(Pulldown Menu)* | Menu dropdown pada ikon `...` di tiap baris lagu & tombol avatar profil di pojok kanan atas. | Menyembunyikan opsi lanjutan (*Play Now, Add to Queue, Audio Analysis, Remove*) agar ruang visual tetap bersih. |
| **5** | **Dialog Berbasis Pengisian Formulir** *(Form Filling Dialogue)* | Modal formulir **Create New Playlist** (Nama, Deskripsi, Dropdown Genre, Dropdown Mood, & Radio Button Public/Private). | Endpoint `POST /api/playlist` melakukan validasi *server-side* dan mengembalikan pesan kesalahan jika data tidak sesuai. |
| **6** | **Antarmuka Berbasis Ikon** *(Icon-Based Interface)* | **Bottom Player Bar** dan kontrol di panel kanan yang menggunakan simbol piktogram universal (Play/Pause, Skip, Shuffle, Repeat, Like, Volume). | Pengguna langsung memahami fungsi tombol melintasi batasan bahasa (*language-independent*). |
| **7** | **Sistem Penjendelaan** *(Windowing System)* | Panel samping kanan (*Right Dock*) yang dapat dibuka/tutup, serta **Floating Draggable Lyrics Window** yang dapat digeser di layar. | Memungkinkan *multi-tasking* mandiri tanpa mengganggu alur tampilan utama. |
| **8** | **Manipulasi Langsung** *(Direct Manipulation)* | Fitur **Drag-and-Drop** pada daftar antrean lagu di Right Dock, serta **Interactive Sliders** untuk scrubbing durasi lagu dan volume suara secara real-time. | Manipulasi objek secara fisik menggunakan kursor mouse dengan umpan balik visual instan. |
| **9** | **Antarmuka Berbasis Interaksi Grafis** *(Graphical Interaction Interface)* | **Real-time Waveform Audio Visualizer** yang beranimasi dinamis di panel kanan, Grid Kartu Album beranimasi hover, Diagram Batang **Tempo (BPM)**, dan **Radar/Spider Chart** atribut audio. | Representasi visual grafis non-tekstual dari data numerik dan audio real-time. |

---

## 🔍 Tombol "IMK Inspector Mode"
- Klik tombol **"IMK Inspector"** di header kanan atas.
- Seluruh komponen antarmuka akan diberi garis batas oranye putus-putus dan badge penanda **`[IMK-1]` hingga `[IMK-9]`**.
- Klik sembarang badge untuk membuka **Jendela Modal Teori IMK** yang memuat:
  1. *Konsep Teori IMK*
  2. *Kelebihan & Karakteristik*
  3. *Implementasi Spesifik pada Aplikasi Ini*
- Sangat praktis untuk kebutuhan presentasi dan tangkapan layar (*screenshot*) laporan Word.

---

## 🚀 Cara Menjalankan Aplikasi

1. **Instal Dependensi:**
   ```bash
   pip install -r requirements.txt
   ```
2. **Jalankan Server Flask:**
   ```bash
   python app.py
   ```
3. **Buka di Browser:**
   Akses salah satu alamat berikut di peramban (Chrome, Edge, Firefox):
   - **`http://127.0.0.1:5000`** atau **`http://localhost:5000`**

---

## 🛡️ Keandalan & Penanganan Error (Zero Failed to Fetch)
- **CORS Otomatis (`@app.after_request` & `@app.before_request`):** Seluruh response API dilengkapi header `Access-Control-Allow-Origin: *`, `Access-Control-Allow-Headers: Content-Type, Authorization`, dan preflight HTTP `OPTIONS` 200 OK.
- **Path Relatif:** Seluruh pemanggilan `fetch()` menggunakan path relatif (`/api/songs`, `/api/cli`, `/api/batch`, `/api/nlp`, `/api/playlist`, `/api/queue/reorder`) sehingga tidak bergantung pada hardcoded IP/port.
- **Host Binding `0.0.0.0:5000`:** Memungkinkan server diakses secara fleksibel dari `localhost`, `127.0.0.1`, maupun jaringan lokal LAN.
- **Client-Side Fallback Engine:** Jika jaringan browser sempat terputus atau server sedang restart, antarmuka web secara otomatis mengalihkan parsing CLI, NLP, Batch Script, dan Playlist ke engine parser lokal tanpa memunculkan error atau memutus respons tombol.
