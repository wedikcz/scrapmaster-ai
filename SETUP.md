# ScrapMaster Unified - Setup Guide

## Prerequisites

- Python 3.10+
- Node.js 18+
- pip and npm installed

## Backend Setup

### 1. Create virtual environment

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Start the server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

## Frontend Setup

### 1. Install dependencies

```bash
cd frontend
npm install
```

### 2. Start the development server

```bash
npm run dev
```

The app will be available at `http://localhost:3000`

## Using Docker

```bash
# From the root directory
docker compose up --build
```

Access the app at `http://localhost:3000`

## Features

- **Dashboard**: Real-time overview of inventory and projects
- **Inventory**: Add and manage scrap items with condition and value tracking
- **Projects**: Create and track repair/repurposing projects
- **Analysis**: Run AI-based mechanism analysis on salvaged devices
- **Real-time updates**: Live data synchronization between frontend and backend
- **Toast notifications**: User feedback for all actions

## API Endpoints

### Health
- `GET /` - Service status

### Scrap Items
- `GET /api/v1/scrap/items` - List all items
- `GET /api/v1/scrap/items/{id}` - Get item details
- `POST /api/v1/scrap/items` - Create new item

### Projects
- `GET /api/v1/projects` - List all projects
- `GET /api/v1/projects/{id}` - Get project details
- `POST /api/v1/projects` - Create new project

### Analysis
- `POST /api/v1/videos/analyze` - Run device analysis

## Troubleshooting

### Backend connection issues
- Ensure the backend is running on port 8000
- Check `.env` file has `NEXT_PUBLIC_API_URL=http://localhost:8000`

### Database errors
- The app uses SQLite by default
- Database file is created automatically in `backend/scrapmaster.db`

### Port conflicts
- Backend: Change port in `docker-compose.yml` or uvicorn command
- Frontend: `npm run dev -- -p 3001`

## Development Workflow

1. Backend changes auto-reload with `--reload` flag
2. Frontend changes auto-refresh with Next.js HMR
3. Use browser DevTools to debug frontend
4. Use FastAPI's Swagger UI at `http://localhost:8000/docs`
