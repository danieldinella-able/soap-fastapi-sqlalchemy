# SOAP + FastAPI + SQLAlchemy — Monorepo

Questo repository contiene due servizi distinti:
- `soap_server`: espone un servizio SOAP (Spyne) con catalogo libri e ordini.
- `rest_api`: espone un'API REST (FastAPI) che consuma il servizio SOAP per restituire dati in JSON.

La struttura è stata organizzata per separare chiaramente i due servizi e semplificare deploy e sviluppo.

## Struttura del Progetto

- `services/soap_server/`
  - `app/` codice del server SOAP (`server.py`, `models.py`, `db.py`, `data_seed.py`, `soap_types.py`)
  - `Dockerfile`, `requirements.txt`
- `services/rest_api/`
  - `rest_app/` codice FastAPI (`main.py`, router `api/routers/books.py`, provider SOAP, schemi, ecc.)
  - `Dockerfile`, `requirements.txt`
- `scripts/check_soap_client.py` script di test rapido del client SOAP (Zeep)
- `.env`, `.env.example` variabili d'ambiente
- `docker-compose.yml` definisce i servizi `postgres`, `soap_server`, `rest_api`

## Prerequisiti

- Docker e Docker Compose (consigliato per l'esecuzione completa)
- In alternativa, Python 3.11+ per esecuzione locale senza Docker

## Avvio Rapido con Docker Compose

1) Copia le variabili di esempio e personalizza se necessario:

```
cp .env.example .env
```

- Variabili chiave:
  - `POSTGRES_URI` (usato da REST API, driver `asyncpg`), es.: `postgresql+asyncpg://appuser:apppass@postgres:5432/app_test`
  - `SOAP_WSDL_URL` (usato da REST API per chiamare SOAP), default: `http://soap_server:8001/?wsdl`
  - `DATABASE_URL` (usato dal SOAP server), default: SQLite locale nel container

2) Build e avvio dei servizi:

```
docker compose up --build -d
```

3) Inizializza il DB del SOAP server (crea tabelle e inserisce libri demo):

```
docker compose exec soap_server python -m app.data_seed
```

4) Verifica:

- SOAP WSDL: http://localhost:8001/?wsdl
- REST endpoint libri: http://localhost:8000/api/books/list

5) Log (opzionale):

```
docker compose logs -f soap_server
# oppure
docker compose logs -f rest_api
```

6) Arresto:

```
docker compose down
# aggiungi -v se vuoi rimuovere anche i volumi (Postgres)
```

## Esecuzione Locale (senza Docker)

Puoi avviare i due servizi singolarmente in due terminali.

### 1) Avviare il SOAP Server (Spyne)

```
python -m venv .venv-soap && source .venv-soap/bin/activate
pip install -r services/soap_server/requirements.txt
export DATABASE_URL=sqlite:///./soap.db  # o Postgres, se preferisci
cd services/soap_server
python -m app.data_seed   # crea tabelle + dati demo
python -m app.server      # espone il servizio su http://localhost:8001/?wsdl
```

Test rapido del client SOAP:

```
python scripts/check_soap_client.py
```

### 2) Avviare la REST API (FastAPI)

In un altro terminale:

```
python -m venv .venv-rest && source .venv-rest/bin/activate
pip install -r services/rest_api/requirements.txt
cp .env.example .env  # se non l'hai già fatto
export SOAP_WSDL_URL=http://localhost:8001/?wsdl
# Configura anche POSTGRES_URI se vuoi connetterti a Postgres locale

uvicorn rest_app.main:app \
  --host 0.0.0.0 --port 8000 \
  --app-dir services/rest_api \
  --reload
```

Endpoint REST disponibile su: http://localhost:8000/api/books/list

## Configurazione e Ambiente

- Il modulo di configurazione della REST API legge da `.env` (vedi `app/core/config/settings.py`).
- Variabili principali:
  - `POSTGRES_URI`: stringa di connessione SQLAlchemy async (`postgresql+asyncpg://...`).
  - `SOAP_WSDL_URL`: URL del WSDL esposto dal SOAP server.
  - `UVICORN_*`: settaggi del server uvicorn.
  - `DATABASE_URL`: (SOAP server) stringa DB per SQLAlchemy sync (es. `sqlite:///./soap.db`).

## API

- REST:
  - `GET /api/books/list` → lista di libri, schema: `{ isbn: str, title: str, author?: str, price?: number }`
- SOAP:
  - `ListBooks()` → elenco libri
  - `GetBook(isbn)` → dettaglio libro o fault `Client.BookNotFound`

## Note e Troubleshooting

- Se `ListBooks` ritorna vuoto o il SOAP server lancia errori, assicurati di aver eseguito il seeding (`docker compose exec soap_server python -m app.data_seed`).
- Se la REST API non risolve il WSDL, verifica `SOAP_WSDL_URL` nel `.env` o nelle variabili d'ambiente attive.
- Per Postgres, verifica che `POSTGRES_URI` punti al servizio `postgres` del compose o alla tua istanza locale.
- I log sono formattati per essere leggibili in ambienti diversi (VSCode/PyCharm/produzione); regola `log_level` in `.env` se necessario.

## Sviluppo

- I pacchetti Python sono organizzati come moduli: `rest_app` per la REST API e `app` per il SOAP server (all'interno di `services/soap_server`).
- Aggiungi `__init__.py` nelle nuove cartelle Python che crei.
- Mantieni import assoluti coerenti: per la REST usa `from rest_app...`; per il SOAP usa `from app...` (dato il contesto del suo container/cartella).

Buon lavoro!
