import asyncio
import os
import uuid
import glob
from flask import Flask, request, jsonify, send_file, render_template
import edge_tts
from pydub import AudioSegment

app = Flask(__name__)
AUDIO_DIR = "static/audio"
os.makedirs(AUDIO_DIR, exist_ok=True)

# Vozes disponíveis em português BR
VOICES = {
    "masculina_grave":  "pt-BR-AntonioNeural",
    "masculina_jovem":  "pt-BR-FabioNeural",
    "feminina_suave":   "pt-BR-FranciscaNeural",
    "feminina_potente": "pt-BR-ThalitaNeural",
}

async def generate_tts(text: str, voice: str, output_path: str, rate: str = "-10%", pitch: str = "-5Hz"):
    communicate = edge_tts.Communicate(text, voice, rate=rate, pitch=pitch)
    await communicate.save(output_path)

def mix_with_beat(voice_path: str, beat_path: str, output_path: str):
    voice = AudioSegment.from_mp3(voice_path)
    beat = AudioSegment.from_mp3(beat_path)

    # Repeat beat to match voice length
    while len(beat) < len(voice):
        beat = beat + beat
    beat = beat[:len(voice)]

    # Beat 8dB quieter than voice
    beat = beat - 8
    mixed = voice.overlay(beat)
    mixed.export(output_path, format="mp3", bitrate="192k")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/generate", methods=["POST"])
def generate():
    data = request.json
    lyrics = data.get("lyrics", "").strip()
    voice_key = data.get("voice", "masculina_grave")
    has_beat = data.get("beat", True)

    if not lyrics:
        return jsonify({"error": "Letra não pode ser vazia"}), 400

    voice = VOICES.get(voice_key, VOICES["masculina_grave"])
    uid = str(uuid.uuid4())[:8]
    voice_path = f"{AUDIO_DIR}/voice_{uid}.mp3"
    output_path = f"{AUDIO_DIR}/music_{uid}.mp3"
    beat_path = "static/beat.mp3"

    try:
        # Generate TTS
        asyncio.run(generate_tts(lyrics, voice, voice_path, rate="-15%", pitch="-8Hz"))

        # Mix with beat if available
        if has_beat and os.path.exists(beat_path):
            mix_with_beat(voice_path, beat_path, output_path)
            os.remove(voice_path)
            final_path = output_path
        else:
            final_path = voice_path

        filename = os.path.basename(final_path)
        return jsonify({"success": True, "file": filename, "url": f"/api/download/{filename}"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/download/<filename>")
def download(filename):
    # Security: only allow our generated files
    if not filename.startswith(("voice_", "music_")) or not filename.endswith(".mp3"):
        return jsonify({"error": "Arquivo inválido"}), 400
    path = os.path.join(AUDIO_DIR, filename)
    if not os.path.exists(path):
        return jsonify({"error": "Arquivo não encontrado"}), 404
    return send_file(path, as_attachment=True, download_name="rimavoz_musica.mp3")

@app.route("/api/voices")
def voices():
    return jsonify(list(VOICES.keys()))

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
