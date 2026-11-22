"""
================================================================================
PLAYCLOUD MUSIC PLAYER - TUGAS BESAR INTERAKSI MANUSIA & KOMPUTER (IMK)
Topik: Implementasi 9 Kategori Ragam Dialog Interaktif (Interactive Dialogue Styles)
Koleksi Spesial: Arctic Monkeys - 10 Essential Tracks
Teknologi: Python (Flask Backend) + HTML5 Web Audio + Tailwind CSS
================================================================================
"""

import os
import re
import shlex
import urllib.parse
import urllib.request
import json
from flask import Flask, jsonify, render_template, request

# Direktori dasar aplikasi
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")
STATIC_DIR = os.path.join(BASE_DIR, "static")
AUDIO_DIR = os.path.join(STATIC_DIR, "audio")

# Pastikan folder static/audio dibuat secara otomatis
os.makedirs(AUDIO_DIR, exist_ok=True)

app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)

# In-memory cache untuk response iTunes API
ITUNES_CACHE = {}

# ==============================================================================
# DATA MASTER: 10 LAGU ARCTIC MONKEYS (ESSENTIAL COLLECTION)
# Dipetakan ke file lokal static/audio/<local_filename> & cover vektor lokal
# ==============================================================================
ARCTIC_MONKEYS_TRACKS = [
    {
        "id": 1,
        "title": "Do I Wanna Know?",
        "artist": "Arctic Monkeys",
        "album": "AM",
        "year": 2013,
        "duration": 272,
        "tempo": 85,
        "mood": "chill",
        "energy": 65,
        "danceability": 55,
        "valence": 42,
        "acousticness": 18,
        "theme": "am_wave",
        "accent": "#E56B45",
        "local_filename": "do_i_wanna_know.mp3",
        "default_preview": "https://audio-ssl.itunes.apple.com/itunes-assets/AudioPreview211/v4/71/cb/ba/71cbbaa1-016b-0e73-dfc2-9f4ede9ddfc0/mzaf_16266777024198047150.plus.aac.p.m4a",
        "lyrics": (
            "Have you got colour in your cheeks?\n"
            "Do you ever get that fear that you can't shift the type\n"
            "That sticks around like summat in your teeth?\n"
            "Are there some aces up your sleeve?\n"
            "Have you no idea that you're in deep?\n"
            "I've dreamt about you nearly every night this week\n"
            "How many secrets can you keep?\n"
            "'Cause there's this tune I found that makes me think of you somehow and I play it on repeat\n"
            "Until I fall asleep, spilling drinks on my settee..."
        )
    },
    {
        "id": 2,
        "title": "R U Mine?",
        "artist": "Arctic Monkeys",
        "album": "AM",
        "year": 2013,
        "duration": 201,
        "tempo": 97,
        "mood": "energetic",
        "energy": 94,
        "danceability": 62,
        "valence": 58,
        "acousticness": 6,
        "theme": "am_wave",
        "accent": "#E56B45",
        "local_filename": "r_u_mine.mp3",
        "default_preview": "https://audio-ssl.itunes.apple.com/itunes-assets/AudioPreview221/v4/6f/80/9f/6f809f2b-b960-90c1-f618-4e1d1fec11fa/mzaf_3957424487272184184.plus.aac.p.m4a",
        "lyrics": (
            "I'm a puppet on a string\n"
            "Tracy Island, time-traveling diamond cutter-shaped heartaches\n"
            "Come to find you four in some velvet morning years too late\n"
            "She's a silver lining, lone ranger riding through an open space\n"
            "In my mind, when she's not right there beside me\n"
            "I go crazy 'cause here isn't where I wanna be\n"
            "And satisfaction feels like a distant memory\n"
            "And I can't help myself, all I wanna hear her say is, 'Are you mine?'..."
        )
    },
    {
        "id": 3,
        "title": "Arabella",
        "artist": "Arctic Monkeys",
        "album": "AM",
        "year": 2013,
        "duration": 207,
        "tempo": 90,
        "mood": "energetic",
        "energy": 86,
        "danceability": 51,
        "valence": 48,
        "acousticness": 12,
        "theme": "am_wave",
        "accent": "#E56B45",
        "local_filename": "arabella.mp3",
        "default_preview": "https://audio-ssl.itunes.apple.com/itunes-assets/AudioPreview221/v4/f4/2c/64/f42c647f-a3b8-424f-e599-9160ac4231f8/mzaf_6009683166111527253.plus.aac.p.m4a",
        "lyrics": (
            "Arabella's got some interstellar-gator skin boots\n"
            "And a Helter Skelter 'round her little finger and I ride it\n"
            "Forever, she's got a Barbarella silver swimsuit\n"
            "And when she needs a shelter from reality she takes a dip in my daydreams\n"
            "My days end best when the sunset gets itself behind\n"
            "That little lady sitting on the passenger side\n"
            "It's sobering to think of her December... and I'm modern day drifting..."
        )
    },
    {
        "id": 4,
        "title": "Knee Socks",
        "artist": "Arctic Monkeys",
        "album": "AM",
        "year": 2013,
        "duration": 257,
        "tempo": 105,
        "mood": "chill",
        "energy": 73,
        "danceability": 68,
        "valence": 62,
        "acousticness": 16,
        "theme": "am_wave",
        "accent": "#E56B45",
        "local_filename": "knee_socks.mp3",
        "default_preview": "https://audio-ssl.itunes.apple.com/itunes-assets/AudioPreview211/v4/e0/85/51/e0855198-d284-738d-98f1-3699ab97c0a7/mzaf_8363209069003571680.plus.aac.p.m4a",
        "lyrics": (
            "You and me could've been a team\n"
            "Each had a half of a four-leaf clover on our team\n"
            "Like you had a phone that was missing on the table\n"
            "When the zeroes lined up on the 24-hour clock\n"
            "When you know who's calling even though the number is blocked\n"
            "When you're walking in your knee socks..."
        )
    },
    {
        "id": 5,
        "title": "Snap Out of It",
        "artist": "Arctic Monkeys",
        "album": "AM",
        "year": 2013,
        "duration": 192,
        "tempo": 133,
        "mood": "happy",
        "energy": 84,
        "danceability": 72,
        "valence": 79,
        "acousticness": 9,
        "theme": "am_wave",
        "accent": "#E56B45",
        "local_filename": "snap_out_of_it.mp3",
        "default_preview": "https://audio-ssl.itunes.apple.com/itunes-assets/AudioPreview221/v4/8b/f7/57/8bf757a5-26c6-a66e-fdfe-7ca271e09646/mzaf_2399808092218944871.plus.aac.p.m4a",
        "lyrics": (
            "What's been going on in your head?\n"
            "There's a new face on you, that's what you said\n"
            "Don't get that look on your face, it's not looking good\n"
            "Snap out of it! Under a spell you are, snap out of it!\n"
            "Forever unchained, I wanna grab your shoulder and shake baby, snap out of it!"
        )
    },
    {
        "id": 6,
        "title": "One for the Road",
        "artist": "Arctic Monkeys",
        "album": "AM",
        "year": 2013,
        "duration": 206,
        "tempo": 112,
        "mood": "chill",
        "energy": 70,
        "danceability": 58,
        "valence": 47,
        "acousticness": 15,
        "theme": "am_wave",
        "accent": "#E56B45",
        "local_filename": "one_for_the_road.mp3",
        "default_preview": "https://audio-ssl.itunes.apple.com/itunes-assets/AudioPreview221/v4/a0/18/f7/a018f738-6882-74ab-d985-65190d39fe7b/mzaf_14184526855571769887.plus.aac.p.m4a",
        "lyrics": (
            "There's no need to show that kind of affection\n"
            "It's just one for the road, ooh-ooh-ooh\n"
            "One for the road, ooh-ooh-ooh\n"
            "From the bottom of your heart, the drinks on the bar\n"
            "And you know we're only going one for the road..."
        )
    },
    {
        "id": 7,
        "title": "No. 1 Party Anthem",
        "artist": "Arctic Monkeys",
        "album": "AM",
        "year": 2013,
        "duration": 243,
        "tempo": 74,
        "mood": "sad",
        "energy": 45,
        "danceability": 42,
        "valence": 29,
        "acousticness": 38,
        "theme": "am_wave",
        "accent": "#E56B45",
        "local_filename": "no_1_party_anthem.mp3",
        "default_preview": "https://audio-ssl.itunes.apple.com/itunes-assets/AudioPreview221/v4/ea/32/b4/ea32b4ce-8211-8e63-024e-cf18c42e2eda/mzaf_15252909301723072031.plus.aac.p.m4a",
        "lyrics": (
            "So you're on the prowl wondering whether\n"
            "She left already or not\n"
            "Leather jacket, collar popped like antenna\n"
            "Never looking back once you've made up your mind\n"
            "The look of love, the rush of blood\n"
            "The 'She's with me' - the Gallic shrug\n"
            "The camera lights, the casual cup of coffee\n"
            "Come on, come on, come on, number one party anthem..."
        )
    },
    {
        "id": 8,
        "title": "Mardy Bum",
        "artist": "Arctic Monkeys",
        "album": "Whatever People Say I Am, That's What I Am Not",
        "year": 2006,
        "duration": 175,
        "tempo": 118,
        "mood": "happy",
        "energy": 78,
        "danceability": 65,
        "valence": 74,
        "acousticness": 22,
        "theme": "retro_grain",
        "accent": "#F59E0B",
        "local_filename": "mardy_bum.mp3",
        "default_preview": "https://audio-ssl.itunes.apple.com/itunes-assets/AudioPreview221/v4/8e/ca/2b/8eca2b46-f92d-0d30-9958-655aa7cc06a1/mzaf_13574770153578890892.plus.aac.p.m4a",
        "lyrics": (
            "Now then Mardy Bum\n"
            "I've seen your frown and it's like looking down the barrel of a gun\n"
            "And it goes off, and out come all these words\n"
            "Oh, there's a very pleasant side to you\n"
            "A side I much prefer, it's one that laughs and jokes around\n"
            "Remember cuddles in the kitchen, yeah, to get the things off the ground\n"
            "And it was up, up and away, oh, but it's right hard for the summit in the day..."
        )
    },
    {
        "id": 9,
        "title": "505",
        "artist": "Arctic Monkeys",
        "album": "Favourite Worst Nightmare",
        "year": 2007,
        "duration": 253,
        "tempo": 70,
        "mood": "sad",
        "energy": 55,
        "danceability": 38,
        "valence": 23,
        "acousticness": 40,
        "theme": "fwn_neon",
        "accent": "#EF4444",
        "local_filename": "505.mp3",
        "default_preview": "https://audio-ssl.itunes.apple.com/itunes-assets/AudioPreview221/v4/d1/0d/ab/d10dabc8-cceb-e718-401f-01516b009460/mzaf_13845311225859403599.plus.aac.p.m4a",
        "lyrics": (
            "I'm going back to 505\n"
            "If it's a seven hour flight or a forty-five minute drive\n"
            "In my imagination, you're waitin' lyin' on your side\n"
            "With your hands between your thighs\n"
            "Stop and wait a sec\n"
            "When you look at me like that, my darlin', what did you expect?\n"
            "I'd probably still adore you with your hands around my neck\n"
            "Or I did last time I checked..."
        )
    },
    {
        "id": 10,
        "title": "Crying Lightning",
        "artist": "Arctic Monkeys",
        "album": "Humbug",
        "year": 2009,
        "duration": 223,
        "tempo": 106,
        "mood": "energetic",
        "energy": 88,
        "danceability": 63,
        "valence": 52,
        "acousticness": 8,
        "theme": "humbug_dark",
        "accent": "#8B5CF6",
        "local_filename": "crying_lightning.mp3",
        "default_preview": "https://audio-ssl.itunes.apple.com/itunes-assets/AudioPreview221/v4/87/80/79/8780790f-fc51-a13e-417d-ce1f449e5542/mzaf_5971917429981500357.plus.aac.p.m4a",
        "lyrics": (
            "Outside the cafe by the cracker factory\n"
            "You were practicing a magic trick\n"
            "And my thoughts got rude as you talked and chewed\n"
            "On the last of your pick and mix\n"
            "Said you're not supposed to do that, you'll break a bone\n"
            "And your past-time consisted of the strange\n"
            "And the twisted and you made me cry... Crying lightning..."
        )
    }
]

# Database in-memory playlist pengguna
USER_PLAYLISTS = [
    {
        "id": 1,
        "name": "Midnight Indie Vibes",
        "description": "Koleksi track atmosferik malam hari untuk fokus dan nugas.",
        "genre": "Indie Rock",
        "mood": "Chill",
        "visibility": "Public",
        "song_count": 10
    },
    {
        "id": 2,
        "name": "High Energy Workout",
        "description": "Lagu dengan ketukan drum dan riff gitar membakar semangat.",
        "genre": "Alternative Rock",
        "mood": "Energetic",
        "visibility": "Private",
        "song_count": 6
    }
]


# ==============================================================================
# RESOLVER AUDIO REAL (CEK LOCAL static/audio/ -> ITUNES API -> CLOUD FALLBACK)
# ==============================================================================
def resolve_song_audio(song):
    """
    Menyelesaikan URL audio secara otomatis:
    1. Cek file audio lokal di static/audio/<local_filename>
    2. Cek cache in-memory iTunes API
    3. Panggil iTunes Search API (timeout 3 detik)
    4. Fallback ke preview URL resmi terverifikasi
    """
    song_id = song["id"]
    local_name = song.get("local_filename", "")
    local_file_path = os.path.join(AUDIO_DIR, local_name) if local_name else ""

    # 1. Jika file lokal ada di static/audio/, utamakan file lokal
    if local_file_path and os.path.exists(local_file_path):
        return {
            "audio_url": f"/static/audio/{local_name}",
            "source": "local_storage"
        }

    # 2. Cek in-memory cache
    if song_id in ITUNES_CACHE:
        return ITUNES_CACHE[song_id]

    # 3. Coba query iTunes Search API secara dinamis
    query_term = f"Arctic Monkeys {song['title']}"
    encoded_query = urllib.parse.quote(query_term)
    itunes_url = f"https://itunes.apple.com/search?term={encoded_query}&entity=song&limit=3"

    try:
        req = urllib.request.Request(itunes_url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
        with urllib.request.urlopen(req, timeout=3) as response:
            payload = json.loads(response.read().decode("utf-8"))
            results = payload.get("results", [])
            for item in results:
                if "arctic monkeys" in item.get("artistName", "").lower():
                    preview = item.get("previewUrl")
                    if preview:
                        resolved = {
                            "audio_url": preview,
                            "source": "itunes_api"
                        }
                        ITUNES_CACHE[song_id] = resolved
                        return resolved
    except Exception:
        pass  # Jaringan offline atau timeout -> fallback

    # 4. Fallback ke URL preview cloud resmi
    fallback = {
        "audio_url": song["default_preview"],
        "source": "verified_cloud"
    }
    ITUNES_CACHE[song_id] = fallback
    return fallback


def get_enriched_songs():
    """Mengembalikan daftar 10 lagu Arctic Monkeys lengkap dengan URL audio real & metadata vektor."""
    enriched = []
    for s in ARCTIC_MONKEYS_TRACKS:
        item = dict(s)
        resolved = resolve_song_audio(s)
        item["audio_url"] = resolved["audio_url"]
        item["source"] = resolved["source"]
        enriched.append(item)
    return enriched


def find_song_by_query(query_str):
    """Pencarian lagu fleksibel berdasarkan judul, id, atau potongan kata."""
    if not query_str:
        return None
    q = query_str.lower().strip()
    # Cek ID numerik langsung
    if q.isdigit():
        target_id = int(q)
        for s in ARCTIC_MONKEYS_TRACKS:
            if s["id"] == target_id:
                return s
    # Cek kecocokan judul persis atau parsial
    for s in ARCTIC_MONKEYS_TRACKS:
        if q in s["title"].lower():
            return s
    return None


def create_player_action(action_type, **payload):
    """Membentuk instruksi pemutar audio terstandar untuk dieksekusi frontend JavaScript."""
    action = {"type": action_type}
    action.update(payload)
    return action


# ==============================================================================
# RAGAM DIALOG 1: DIALOG BERBASIS PERINTAH TUNGGAL (Command Line Dialogue)
# & RAGAM DIALOG 2: DIALOG BERBASIS BAHASA PEMROGRAMAN (Batch Script Dialogue)
# ==============================================================================
def parse_and_execute_command(command_line):
    """Core Command Parser untuk CLI dan Batch Script."""
    trimmed = command_line.strip()
    if not trimmed or trimmed.startswith("#"):
        return ("Baris komentar/kosong dilewati", [])

    try:
        tokens = shlex.split(trimmed)
    except ValueError:
        return ("SYNTAX ERROR: Tanda kutip tidak tertutup dengan benar", [])

    if not tokens:
        return ("", [])

    verb = tokens[0].upper()
    arguments = " ".join(tokens[1:]).strip()

    # 1. PLAY
    if verb == "PLAY":
        if not arguments:
            return ("Melanjutkan pemutaran audio (Resume)", [create_player_action("resume")])
        song = find_song_by_query(arguments)
        if not song:
            return (f'ERROR: Lagu "{arguments}" tidak ditemukan di daftar Arctic Monkeys.', [])
        return (
            f'Memutar: "{song["title"]}" ({song["album"]})',
            [create_player_action("play", id=song["id"])]
        )

    # 2. PAUSE / STOP
    elif verb in ("PAUSE", "STOP"):
        return ("Pemutaran audio dijeda (Paused)", [create_player_action("pause")])

    # 3. NEXT / SKIP
    elif verb in ("NEXT", "SKIP"):
        return ("Beralih ke lagu berikutnya di antrean", [create_player_action("next")])

    # 4. PREV / BACK
    elif verb in ("PREV", "BACK"):
        return ("Kembali ke lagu sebelumnya", [create_player_action("prev")])

    # 5. QUEUE
    elif verb in ("QUEUE", "ENQUEUE"):
        if not arguments:
            return ("ERROR: Sintaks QUEUE memerlukan judul lagu. Contoh: QUEUE \"505\"", [])
        song = find_song_by_query(arguments)
        if not song:
            return (f'ERROR: Lagu "{arguments}" tidak ditemukan.', [])
        return (
            f'Ditambahkan ke antrean: "{song["title"]}"',
            [create_player_action("queue", id=song["id"])]
        )

    # 6. VOLUME / SET_VOLUME
    elif verb in ("VOLUME", "SET_VOLUME"):
        if not arguments:
            return ("ERROR: Masukkan nilai volume 0 - 100. Contoh: VOLUME 80", [])
        try:
            val = int(arguments)
            if not 0 <= val <= 100:
                return ("ERROR: Nilai volume harus antara 0 dan 100", [])
            return (f"Tingkat volume diatur ke {val}%", [create_player_action("volume", value=val)])
        except ValueError:
            return (f'ERROR: "{arguments}" bukan angka integer valid', [])

    # 7. SHUFFLE
    elif verb == "SHUFFLE":
        arg = arguments.lower()
        if arg in ("on", "1", "true"):
            return ("Mode Acak (Shuffle) diaktifkan [ON]", [create_player_action("shuffle", value=True)])
        elif arg in ("off", "0", "false"):
            return ("Mode Acak (Shuffle) dinonaktifkan [OFF]", [create_player_action("shuffle", value=False)])
        return ("ERROR: Gunakan format SHUFFLE ON atau SHUFFLE OFF", [])

    # 8. REPEAT
    elif verb == "REPEAT":
        arg = arguments.lower()
        if arg in ("on", "1", "true"):
            return ("Mode Putar Ulang (Repeat) diaktifkan [ON]", [create_player_action("repeat", value=True)])
        elif arg in ("off", "0", "false"):
            return ("Mode Putar Ulang (Repeat) dinonaktifkan [OFF]", [create_player_action("repeat", value=False)])
        return ("ERROR: Gunakan format REPEAT ON atau REPEAT OFF", [])

    # 9. HELP
    elif verb == "HELP":
        help_text = (
            "DAFTAR PERINTAH RESMI CLI PLAYCLOUD:\n"
            "  PLAY [judul]     - Putar lagu (cth: PLAY \"Arabella\" atau PLAY \"505\")\n"
            "  PLAY             - Melanjutkan pemutaran (Resume)\n"
            "  PAUSE            - Menjeda pemutaran lagu saat ini\n"
            "  NEXT / PREV      - Lagu berikutnya / sebelumnya\n"
            "  QUEUE [judul]    - Masukkan lagu ke daftar antrean\n"
            "  VOLUME [0-100]   - Atur volume (cth: VOLUME 75)\n"
            "  SHUFFLE ON|OFF   - Aktifkan / matikan acak lagu\n"
            "  REPEAT ON|OFF    - Aktifkan / matikan putar ulang"
        )
        return (help_text, [])

    return (f'ERROR: Perintah "{tokens[0]}" tidak dikenal. Ketik "HELP".', [])


# --- Endpoint CLI: Selalu kembalikan JSON valid dengan status 200 ---
@app.route("/api/cli", methods=["GET", "POST"])
def api_cli():
    """Endpoint Ragam Dialog 1: Menerima perintah teks tunggal dari CLI Terminal."""
    try:
        if request.method == "GET":
            return jsonify({
                "status": "ok",
                "message": "CLI Terminal endpoint aktif. Kirim POST dengan JSON {'cmd': '...'}",
                "output": "Ketik HELP untuk panduan.",
                "actions": []
            }), 200

        payload = request.get_json(silent=True) or {}
        raw_command = (payload.get("cmd") or payload.get("command", "")).strip()

        if not raw_command:
            return jsonify({
                "status": "ok",
                "command": "",
                "output": "Masukkan perintah (contoh: PLAY \"Arabella\" atau HELP)",
                "actions": [],
                "action": "none",
                "payload": {}
            }), 200

        message, actions = parse_and_execute_command(raw_command)
        first_action = actions[0] if actions else {"type": "none"}

        return jsonify({
            "status": "ok",
            "command": raw_command,
            "output": message,
            "actions": actions,
            "action": first_action.get("type", "none"),
            "payload": first_action
        }), 200
    except Exception as e:
        return jsonify({
            "status": "ok",
            "command": "",
            "output": f"Terjadi kesalahan pemrosesan perintah: {str(e)}",
            "actions": [],
            "action": "error",
            "payload": {}
        }), 200


# --- Endpoint Batch: Selalu kembalikan JSON valid dengan status 200 ---
@app.route("/api/batch", methods=["GET", "POST"])
def api_batch():
    """Endpoint Ragam Dialog 2: Mengeksekusi blok kode batch script secara sekuensial."""
    try:
        if request.method == "GET":
            return jsonify({
                "status": "ok",
                "summary": "Batch Script endpoint aktif.",
                "logs": ["Kirim POST dengan JSON {'script': '...'}"],
                "actions": []
            }), 200

        payload = request.get_json(silent=True) or {}
        script_content = payload.get("script", "")

        execution_logs = []
        accumulated_actions = []
        lines = script_content.splitlines()

        for line_number, raw_line in enumerate(lines, start=1):
            clean_line = raw_line.strip()
            if not clean_line or clean_line.startswith("#"):
                if clean_line.startswith("#"):
                    execution_logs.append(f"[Line {line_number:02d}] KOMENTAR: {clean_line}")
                continue

            message, actions = parse_and_execute_command(clean_line)
            status_tag = "OK" if "ERROR" not in message else "FAIL"
            execution_logs.append(f"[Line {line_number:02d} | {status_tag}] {clean_line} => {message}")
            accumulated_actions.extend(actions)

        summary = f"Selesai: {len(accumulated_actions)} aksi diproses dari skrip batch."
        return jsonify({
            "status": "ok",
            "summary": summary,
            "logs": execution_logs,
            "actions": accumulated_actions
        }), 200
    except Exception as e:
        return jsonify({
            "status": "ok",
            "summary": "Gagal memproses skrip batch.",
            "logs": [f"Error: {str(e)}"],
            "actions": []
        }), 200


# ==============================================================================
# RAGAM DIALOG 3: ANTARMUKA BERBASIS BAHASA ALAMI (Natural Language Interface)
# ==============================================================================
NLP_KEYWORDS = {
    "galau": [9, 7],      # 505 atau No. 1 Party Anthem
    "sedih": [9, 7],
    "santai": [1, 4, 6],   # Do I Wanna Know?, Knee Socks, One for the Road
    "malam": [9, 1],       # 505, Do I Wanna Know?
    "nugas": [1, 4, 6],
    "semangat": [2, 3, 10],# R U Mine?, Arabella, Crying Lightning
    "rock": [2, 3, 10],
    "ngebeat": [2, 3, 10],
    "olahraga": [2, 3, 10],
    "ceria": [5, 8],       # Snap Out of It, Mardy Bum
    "senang": [5, 8],
    "populer": [1, 2, 9]   # Do I Wanna Know?, R U Mine?, 505
}

@app.route("/api/nlp", methods=["GET", "POST"])
def api_nlp():
    """Endpoint Ragam Dialog 3: Natural Language Processing untuk Bahasa Indonesia."""
    try:
        if request.method == "GET":
            return jsonify({
                "status": "ok",
                "output": "Smart Assistant siap menerima instruksi via POST {'text': '...'}",
                "actions": []
            }), 200

        payload = request.get_json(silent=True) or {}
        text = (payload.get("text") or payload.get("query") or payload.get("prompt", "")).lower().strip()

        if not text:
            return jsonify({
                "status": "ok",
                "output": "Ketik kalimat instruksi, contoh: 'Putar lagu galau Arctic Monkeys' atau 'Kecilin volumenya'",
                "actions": []
            }), 200

        has = lambda *words: any(w in text for w in words)

        # 1. Deteksi angka spesifik volume (cth: "volume 60", "atur volume ke 40")
        m_vol = re.search(r'volume.*?(\d+)', text)
        if m_vol:
            vol_target = max(0, min(100, int(m_vol.group(1))))
            return jsonify({
                "status": "ok",
                "output": f"Asisten AI: Tingkat volume diatur ke {vol_target}%.",
                "actions": [create_player_action("volume", value=vol_target)]
            }), 200

        # 2. Kontrol Volume relatif (naik / turun)
        if has("volume", "suara", "bunyi"):
            if has("kecil", "pelan", "turun", "rendah", "kurang", "kecilkan", "turunkan"):
                return jsonify({
                    "status": "ok",
                    "output": "Asisten AI: Baik, tingkat volume dikecilkan 20%.",
                    "actions": [create_player_action("volume_delta", value=-20)]
                }), 200
            if has("besar", "keras", "naik", "tambah", "kencang", "besarkan", "keraskan", "naikkan"):
                return jsonify({
                    "status": "ok",
                    "output": "Asisten AI: Siap! Volume dinaikkan 20%.",
                    "actions": [create_player_action("volume_delta", value=20)]
                }), 200

        # 3. Kontrol Playback (Pause, Resume, Next, Prev)
        if has("pause", "jeda", "berhenti", "stop", "diam"):
            return jsonify({
                "status": "ok",
                "output": "Asisten AI: Pemutaran lagu dijeda sementara.",
                "actions": [create_player_action("pause")]
            }), 200
        if has("lanjut", "teruskan", "putar lagi", "play") and not has("lagu", "track", "putar", "arctic"):
            return jsonify({
                "status": "ok",
                "output": "Asisten AI: Melanjutkan pemutaran musik.",
                "actions": [create_player_action("resume")]
            }), 200
        if has("next", "skip", "ganti", "berikut", "lanjut lagu", "lagu berikutnya"):
            return jsonify({
                "status": "ok",
                "output": "Asisten AI: Beralih ke track berikutnya.",
                "actions": [create_player_action("next")]
            }), 200
        if has("kembali", "mundur", "sebelum", "prev", "balik", "lagu sebelumnya"):
            return jsonify({
                "status": "ok",
                "output": "Asisten AI: Mengulang kembali lagu sebelumnya.",
                "actions": [create_player_action("prev")]
            }), 200

        # 4. Pencocokan Judul Lagu Langsung (cth: "putar arabella", "mainkan 505")
        for s in ARCTIC_MONKEYS_TRACKS:
            if s["title"].lower() in text or (s["title"].lower().replace("?", "") in text):
                return jsonify({
                    "status": "ok",
                    "output": f'Asisten AI: Memutar "{s["title"]}" dari album {s["album"]}.',
                    "actions": [create_player_action("play", id=s["id"])]
                }), 200

        # 5. Pencocokan Mood / Suasana Hati
        for key, song_ids in NLP_KEYWORDS.items():
            if key in text:
                target_song = next((s for s in ARCTIC_MONKEYS_TRACKS if s["id"] == song_ids[0]), None)
                if target_song:
                    return jsonify({
                        "status": "ok",
                        "output": f'Asisten AI: Menemukan lagu bernuansa {key}: "{target_song["title"]}" ({target_song["album"]}).',
                        "actions": [create_player_action("play", id=target_song["id"])]
                    }), 200

        return jsonify({
            "status": "ok",
            "output": (
                "Asisten AI: Maaf, saya belum memahami kalimat tersebut. "
                "Coba instruksi seperti: 'Putar lagu galau Arctic Monkeys', "
                "'Tolong kecilkan volumenya', atau 'Putar lagu Arabella'."
            ),
            "actions": []
        }), 200
    except Exception as e:
        return jsonify({
            "status": "ok",
            "output": f"Asisten AI error: {str(e)}",
            "actions": []
        }), 200


# ==============================================================================
# RAGAM DIALOG 4: SISTEM MENU (Flat Navigation & Pulldown Menus)
# ==============================================================================
@app.get("/api/menus")
def api_menus():
    """Menyediakan metadata konfigurasi menu datar & menu tarik."""
    return jsonify({
        "status": "ok",
        "flat_menus": [
            {"id": "home", "label": "Home", "icon": "home"},
            {"id": "albums", "label": "Albums", "icon": "disc-3"},
            {"id": "tracks", "label": "Tracks", "icon": "music-2"},
            {"id": "lab", "label": "IMK Lab", "icon": "terminal"}
        ],
        "pulldown_options": [
            {"id": "play", "label": "Play Now", "icon": "play"},
            {"id": "queue", "label": "Add to Queue", "icon": "list-plus"},
            {"id": "lyrics", "label": "View Lyrics", "icon": "file-text"},
            {"id": "remove", "label": "Remove from Queue", "icon": "trash-2"}
        ]
    }), 200


# ==============================================================================
# RAGAM DIALOG 5: DIALOG PENGISIAN FORMULIR (Form Filling Dialogue)
# ==============================================================================
@app.route("/api/playlist", methods=["GET", "POST"])
def api_playlist():
    """Endpoint manajemen playlist pengguna."""
    try:
        if request.method == "GET":
            return jsonify({"status": "ok", "playlists": USER_PLAYLISTS}), 200

        form_data = request.get_json(silent=True) or {}
        name = form_data.get("name", "").strip()
        description = form_data.get("description", "").strip()
        genre = form_data.get("genre", "").strip()
        mood = form_data.get("mood", "Chill").strip()
        visibility = form_data.get("visibility", "Public").strip()

        # Validasi Server-Side
        errors = {}
        if not name:
            errors["name"] = "Nama playlist wajib diisi!"
        elif len(name) < 3:
            errors["name"] = "Nama playlist minimal 3 karakter!"
        elif len(name) > 40:
            errors["name"] = "Nama playlist maksimal 40 karakter!"

        if not genre:
            errors["genre"] = "Pilih salah satu genre musik!"

        if errors:
            return jsonify({"status": "error", "errors": errors}), 200

        new_pl = {
            "id": len(USER_PLAYLISTS) + 1,
            "name": name,
            "description": description or "Tanpa deskripsi.",
            "genre": genre,
            "mood": mood,
            "visibility": visibility,
            "song_count": 0
        }
        USER_PLAYLISTS.append(new_pl)
        return jsonify({
            "status": "ok",
            "message": f'Playlist "{name}" berhasil dibuat!',
            "playlist": new_pl,
            "all_playlists": USER_PLAYLISTS
        }), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "errors": {"server": str(e)}
        }), 200


# ==============================================================================
# RAGAM DIALOG 8 & 9: MANIPULASI LANGSUNG & INTERAKSI GRAFIS
# ==============================================================================
@app.route("/api/queue/reorder", methods=["GET", "POST"])
def api_reorder_queue():
    """Menerima susunan baru antrean hasil Drag-and-Drop (Manipulasi Langsung)."""
    try:
        payload = request.get_json(silent=True) or {}
        new_order = payload.get("queue_ids", [])
        return jsonify({"status": "ok", "queue_ids": new_order}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 200


@app.get("/api/songs")
def api_songs():
    """Mengembalikan 10 lagu Arctic Monkeys lengkap dengan URL audio real dan cover."""
    try:
        songs = get_enriched_songs()
        return jsonify({
            "status": "ok",
            "total": len(songs),
            "artist": "Arctic Monkeys",
            "songs": songs
        }), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e),
            "songs": ARCTIC_MONKEYS_TRACKS
        }), 200


@app.get("/")
def index():
    """Merender antarmuka pengguna Playcloud UI modern."""
    return render_template("index.html")


if __name__ == "__main__":
    print("=" * 70)
    print(" PLAYCLOUD MUSIC PLAYER - ARCTIC MONKEYS EDITION BERJALAN")
    print(" Buka di browser: http://127.0.0.1:5000")
    print("=" * 70)
    app.run(debug=True, host="127.0.0.1", port=5000)
