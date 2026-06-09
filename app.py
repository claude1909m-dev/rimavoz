import os
import uuid
import urllib.request
import urllib.parse
from flask import Flask, request, jsonify, send_file

app = Flask(__name__)
AUDIO_DIR = "static/audio"
os.makedirs(AUDIO_DIR, exist_ok=True)

VOICES = {
    "masculina_grave": "pt-BR",
    "masculina_jovem": "pt-BR",
    "feminina_suave": "pt-BR",
    "feminina_potente": "pt-BR",
}

def generate_tts_google(text, output_path):
    text_encoded = urllib.parse.quote(text[:200])
    url = f"https://translate.google.com/translate_tts?ie=UTF-8&q={text_encoded}&tl=pt-BR&client=tw-ob"
    headers = {"User-Agent": "Mozilla/5.0"}
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=30) as response:
        with open(output_path, "wb") as f:
            f.write(response.read())

@app.route("/")
def index():
    return open("index.html", encoding="utf-8").read()

@app.route("/api/generate", methods=["POST"])
def generate():
    data = request.json
    lyrics = data.get("lyrics", "").strip()
    if not lyrics:
        return jsonify({"error": "Letra vazia"}), 400
    uid = str(uuid.uuid4())[:8]
    output_path = f"{AUDIO_DIR}/voice_{uid}.mp3"
    try:
        # Divide em partes de 200 chars e concatena
        parts = [lyrics[i:i+180] for i in range(0, min(len(lyrics), 1800), 180)]
        part_files = []
        for idx, part in enumerate(parts):
            pfile = f"{AUDIO_DIR}/part_{uid}_{idx}.mp3"
            generate_tts_google(part, pfile)
            part_files.append(pfile)
        # Concatena os arquivos
        with open(output_path, "wb") as out:
            for pf in part_files:
                with open(pf, "rb") as pf_file:
                    out.write(pf_file.read())
                os.remove(pf)
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
