# 🎙️ RimaVoz — Gerador de Música com IA

**100% gratuito • Sem mensalidade • Direitos seus para monetizar**

---

## O que faz

- Transforma qualquer letra em música narrada/cantada por IA
- Voz gerada pela IA da Microsoft (Edge TTS) em português brasileiro
- Mixa automaticamente com um beat épico gratuito
- Download em MP3 — arquivo 100% seu para postar e monetizar

---

## Como funciona

```
Sua letra → Edge TTS (voz IA grátis) → Mistura com beat CC0 → MP3 para download
```

---

## Deploy gratuito no Railway (recomendado — mais fácil)

### Passo 1 — Criar conta gratuita
1. Acesse **railway.app**
2. Clique em "Start a New Project"
3. Entre com sua conta GitHub (crie uma em github.com se não tiver)

### Passo 2 — Subir o projeto
1. No Railway, clique em **"Deploy from GitHub repo"**
2. Crie um repositório no GitHub com estes arquivos
3. Conecte o repositório ao Railway
4. O Railway detecta automaticamente o Procfile e faz o deploy

### Passo 3 — Configurar variáveis (opcional)
Não precisa de nenhuma variável de ambiente — já funciona direto.

### Passo 4 — Acessar o app
O Railway gera uma URL como: `https://rimavoz-production.up.railway.app`
Abra no celular e comece a usar!

---

## Deploy alternativo no Render (também gratuito)

1. Acesse **render.com** e crie conta
2. Clique em "New Web Service"
3. Conecte seu repositório GitHub
4. Em "Build Command": `pip install -r requirements.txt && python setup_beat.py`
5. Em "Start Command": `gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120`
6. Plano: **Free**
7. Clique em Deploy

---

## Rodar localmente (para testar no computador)

```bash
# Instalar dependências
pip install -r requirements.txt

# Instalar ffmpeg (necessário para mixagem)
# Windows: baixe em ffmpeg.org
# Mac: brew install ffmpeg
# Linux: sudo apt install ffmpeg

# Baixar beat gratuito
python setup_beat.py

# Iniciar servidor
python app.py

# Abrir no navegador
# http://localhost:5000
```

---

## Substituir o beat

Coloque qualquer arquivo MP3 em `static/beat.mp3`.

Fontes de beats gratuitos para uso comercial:
- **freemusicarchive.org** — filtrar por licença CC0
- **ccmixter.org** — beats CC0
- **pixabay.com/music** — buscar "rap beat" ou "hip hop"
- YouTube Audio Library — alguns permitem monetização

---

## Direitos e monetização

| Componente | Origem | Direitos |
|---|---|---|
| Voz gerada | Microsoft Edge TTS | Uso pessoal e comercial permitido |
| Beat | CC0 / Domínio público | Livre para uso comercial |
| Letra | Você | 100% seus |
| Música final | Você | 100% seus direitos |

✅ Pode postar no YouTube com monetização
✅ Pode postar no Instagram e TikTok
✅ Pode distribuir no Spotify via DistroKid/TuneCore
✅ Não precisa creditar ninguém

---

## Estrutura do projeto

```
rimavoz-app/
├── app.py              ← Servidor principal
├── requirements.txt    ← Dependências Python
├── Procfile            ← Configuração de deploy
├── setup_beat.py       ← Baixa o beat gratuito
├── static/
│   ├── beat.mp3        ← Beat (gerado pelo setup_beat.py)
│   └── audio/          ← Músicas geradas (criado automaticamente)
└── templates/
    └── index.html      ← Interface do app
```

---

## Vozes disponíveis

| ID | Voz | Estilo |
|---|---|---|
| masculina_grave | Antonio Neural | Voz grave, ideal para rap |
| masculina_jovem | Fabio Neural | Voz jovem e dinâmica |
| feminina_suave | Francisca Neural | Voz feminina suave |
| feminina_potente | Thalita Neural | Voz feminina potente |
