# Avvio dell'architettura

Guida rapida per avviare l’applicazione FastAPI con PostgreSQL (Docker) e SQLAlchemy asincrono.

## Prerequisiti
- Docker e Docker Compose installati.
- Python 3.11+ e `pip` per eseguire l’app in locale.
- File `.env` presente nella root (già incluso nel repo, modificabile all’occorrenza).

## 1) Avviare il database PostgreSQL (Docker)
Esegui dalla root del progetto:

```bash
docker-compose up -d postgres
# (opzionale) verifica che sia in esecuzione
docker ps | grep postgres
# (opzionale) segui i log
docker-compose logs -f postgres
```

## 2) Avviare l’API FastAPI con Uvicorn
Installa le dipendenze e lancia il server (ambiente virtuale consigliato):

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn --env-file .env app.main:app --reload
```

- L’opzione `--env-file .env` assicura il caricamento delle variabili d’ambiente (es. `POSTGRES_URI`).
- L’opzione `--reload` abilita il reload automatico in sviluppo.

## 3) Verifica degli endpoint
Apri il browser su:

- Documentazione interattiva: http://localhost:8000/docs
- Schema OpenAPI: http://localhost:8000/openapi.json

## Troubleshooting
- `.env` non caricato: usa sempre `--env-file .env` con Uvicorn o avvia dalla root del progetto.
- Connessione al DB rifiutata: assicurati che `docker-compose up -d postgres` sia attivo e che `POSTGRES_URI` punti a `localhost:5432` in `.env`.
- Porta occupata: modifica `UVICORN_PORT` in `.env` oppure aggiungi `--port 8001` al comando Uvicorn.
