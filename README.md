# Development Setup

## Environment

Copy both `.env.example` files and adjust the values:

```bash
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env
```

## Backend

### Prerequisites

- Python 3.13

### Setup

Create and activate a virtual environment from the `backend` folder:

```bash
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

Install pip-tools:

```bash
pip install pip-tools
```

### Update dependencies

First time or after changes in `requirements.in`:

```bash
pip-compile requirements.in
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Database

Start PostgreSQL via Docker:

```bash
docker compose up db
```

Run migrations:

```bash
flask db upgrade
```

### Start

```bash
flask run
```

---

## Frontend

### Prerequisites

- Node.js 22+
- npm 10+

### Install dependencies

From the `frontend` folder:

```bash
npm ci
```

### Start

```bash
npm run dev
```

---

## Docker (full stack)

### Development

```bash
docker compose up --build
```

Once running, the services are available at:

| Service  | URL                   |
| -------- | --------------------- |
| Frontend | http://localhost:3000 |
| Backend  | http://localhost:5000 |
| Database | localhost:5432        |

### Production

Create both `.env` files and fill in the real values:

```bash
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env
```

Then start the stack:

```bash
docker compose -f docker-compose.yml up --build
```
