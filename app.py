import asyncio
import os
import uuid
from flask import Flask, request, jsonify, send_file

app = Flask(__name__)
AUDIO_DIR = "static/audio"
os.makedirs(AUDIO_DIR, exist_ok=True)

VOICES = {
    "masculina_grave":  "pt-BR-AntonioNeural",
    "masculina_jovem":  "pt-BR-FabioNeural",
    "feminina_suave":   "pt-BR-FranciscaNeural",
    "feminina_potente": "pt-BR-ThalitaNeural",
}

async def generate_tts(text, voice, output_path):
    communicate = edge_tts.Communicate(text, voice, rate="-15%", pitch="-8Hz")
    await communicate.save(output_path)

@app.route("/")
def index():
    return open("index.html", encoding="utf-8").read()

@app.route("/api/generate", methods=["POST"])
def generate():
    import edge_tts
    data = request.json
    lyrics = data.get("lyrics", "").strip()
    voice_key = data.get("voice", "masculina_grave")
    if not lyrics:
        return jsonify({"error": "Letra vazia"}), 400
    voice = VOICES.get(voice_key, VOICES["masculina_grave"])
    uid = str(uuid.uuid4())[:8]
    output_path = f"{AUDIO_DIR}/voice_{uid}.mp3"
    try:
        async def run():
            communicate = edge_tts.Communicate(lyrics, voice, rate="-15%", pitch="-8Hz")
            await communicate.save(output_path)
        asyncio.run(run())
        filename = os.path.basename(output_path)
        return jsonify({"success": True, "url": f"/api/download/{filename}"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/download/<filename>")
def download(filename):
    if not filename.endswith(".mp3"):
        return jsonify({"error": "Inválido"}), 400
    path = os.path.join(AUDIO_DIR, filename)
    if not os.path.exists(path):
        return jsonify({"error": "Não encontrado"}), 404
    return send_file(path, as_attachment=True, download_name="rimavoz_musica.mp3")

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
