# botIntermediario

Bot de Discord minimalista en Python que reenvía mensajes de usuarios a un webhook de n8n.

## Estructura propuesta

```text
botIntermediario/
├── bot/
│   ├── __init__.py
│   ├── config.py
│   ├── discord_bot.py
│   ├── handler.py
│   ├── main.py
│   └── n8n_client.py
├── examples/
│   └── n8n-workflow.json
├── tests/
│   ├── test_handler.py
│   └── test_n8n_client.py
├── .env.example
├── .gitignore
├── docker-compose.yml
├── Dockerfile
├── README.md
└── requirements.txt
```

## Arquitectura

`Discord -> Bot Python -> Webhook n8n -> procesamiento externo -> Discord Webhook`

## Configuración

1. Copia el archivo de ejemplo:

```bash
cp .env.example .env
```

2. Completa variables:

```env
DISCORD_BOT_TOKEN=
N8N_WEBHOOK_URL=
MESSAGE_PREFIX=
HTTP_TIMEOUT_SECONDS=15
LOG_LEVEL=INFO
```

- `MESSAGE_PREFIX` es opcional (ejemplo: `!bot`). Si está vacío, procesa todos los mensajes de usuarios.
- El bot **no responde en Discord**; solo envía datos a n8n.

## Payload enviado a n8n

```json
{
  "content": "texto escrito por el usuario",
  "author_id": "ID del usuario",
  "author_name": "nombre del usuario",
  "guild_id": "ID del servidor",
  "channel_id": "ID del canal",
  "message_id": "ID del mensaje",
  "timestamp": "fecha ISO 8601"
}
```

## Workflow n8n de ejemplo

Importa `examples/n8n-workflow.json` y reemplaza la URL del nodo `Send to Discord Webhook` con el Incoming Webhook real del canal.

## Crear bot en Discord Developer Portal

1. Ve a https://discord.com/developers/applications
2. Crea una nueva aplicación.
3. En **Bot**, crea el bot y copia el token.
4. Activa **Message Content Intent** en Privileged Gateway Intents.
5. En **OAuth2 > URL Generator** selecciona:
   - Scopes: `bot`
   - Bot Permissions: `View Channels`, `Read Message History`, `Send Messages` (si el bot también fuera a responder; aquí no es necesario responder, pero `View/Read` sí para escuchar)
6. Usa la URL generada para invitarlo al servidor.

## Intents y permisos necesarios

- `message_content` intent habilitado en código y en el portal.
- Permisos mínimos del bot en el canal: ver canal y leer mensajes.

## Ejecución local

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m bot.main
```

## Docker

Construir imagen:

```bash
docker build -t discord-n8n-relay .
```

Ejecutar con compose:

```bash
docker compose up --build -d
```

## Inicializar Git y subir a GitHub

```bash
git init
git add .
git commit -m "feat: minimal discord to n8n relay bot"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/TU_REPO.git
git push -u origin main
```

## Pruebas

```bash
pytest -q
```

Cobertura validada por tests unitarios:
- Ignora mensajes de bots.
- Ignora mensajes sin prefijo cuando hay prefijo configurado.
- Envía payload correcto a n8n.
- Maneja errores HTTP y timeouts.
