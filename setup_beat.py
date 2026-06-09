#!/usr/bin/env python3
"""
Script para baixar um beat gratuito de domínio público para usar no RimaVoz.
Execute uma vez antes de subir para o servidor.
"""
import urllib.request
import os

# Beat épico gratuito — Free Music Archive, licença CC0 (domínio público)
# Você pode substituir por qualquer MP3 de domínio público ou CC0
BEAT_URL = "https://files.freemusicarchive.org/storage-freemusicarchive-org/music/no_curator/Tours/Enthusiast/Tours_-_01_-_Enthusiast.mp3"
OUTPUT = "static/beat.mp3"

os.makedirs("static", exist_ok=True)

if os.path.exists(OUTPUT):
    print(f"Beat já existe: {OUTPUT}")
else:
    print("Baixando beat gratuito (CC0)...")
    try:
        urllib.request.urlretrieve(BEAT_URL, OUTPUT)
        print(f"Beat salvo em: {OUTPUT}")
    except Exception as e:
        print(f"Erro ao baixar beat: {e}")
        print("Coloque manualmente um arquivo MP3 em static/beat.mp3")
        print("Use qualquer beat CC0 de: freemusicarchive.org ou ccmixter.org")
