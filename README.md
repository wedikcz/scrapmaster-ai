# ScrapMaster Unified

ScrapMaster Unified combines the best ideas from the TypeScript experiments and the AI-first Python platform into one coherent product:

- Next.js frontend for the control room and user workflows
- FastAPI backend for API, business logic, and data processing
- Local-first AI analysis for salvaged hardware and mechanism inference
- Scrap inventory, project management, safety review, and repair guidance
- Optional cloud summarization layer for richer explanations without forcing external dependency

## Product vision

ScrapMaster is a privacy-first platform for reverse engineering, salvage reuse, and build guidance generation for discarded hardware. It helps users:

- analyze video clips of salvaged mechanisms
- infer motion and assembly behavior from raw footage
- track scrap inventory and project history
- identify likely faults and safe reuse options
- generate repair, repurposing, and safety workflows

## Unified architecture

```text
scrapmaster/
├── frontend/                # Next.js dashboard and control room
├── backend/                 # FastAPI API + business logic
├── ai/                      # inference and motion-analysis modules
├── docs/                    # project and API documentation
├── scripts/                 # maintenance and setup scripts
├── docker-compose.yml       # local orchestration
├── .env.example             # environment template
├── README.md                # project entry point
├── LICENSE                  # project license
└── .gitignore
```

## Stack

- Frontend: Next.js App Router + TypeScript + Tailwind CSS
- Backend: FastAPI + Pydantic + SQLAlchemy + SQLite
- AI: OpenCV + NumPy + local-first heuristics + optional LLM summarization
- Ops: Docker Compose for local development

## Merge logic

The merged product keeps the strongest parts of the project family:

- `scrapmaster-ai` is the source of truth for AI, safety, and workflow direction
- `scrapmaster` and `scrapmasterv2` contribute the dashboard patterns, orchestration ideas, and iterative UX direction
- the final app is not a duplicate of both TypeScript repos; it is a single modern product built around one backend and one frontend

## Getting started

### 1) Copy environment

```bash
cp .env.example .env
```

### 2) Run backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 3) Run frontend

```bash
cd frontend
npm install
npm run dev
```

### 4) Run with Docker

```bash
docker compose up --build
```

## API overview

- `GET /` — service status
- `GET /api/v1/health` — health check
- `POST /api/v1/videos/analyze` — video analysis request
- `GET /api/v1/scrap/items` — list scrap items
- `POST /api/v1/scrap/items` — create a scrap item
- `GET /api/v1/projects` — list projects
- `POST /api/v1/projects` — create a project

## Core features

- Inverse video engineering for salvaged hardware
- Motion analysis and mechanism inference
- Scrap and inventory tracking
- Project lifecycle and repair planning
- Safety-oriented guidance generation
- Local-first AI flow with optional cloud enhancement
- Exportable operational logs and reports

## Safety and privacy

- Local inference first
- No lock-in to cloud-only processing
- Safety warnings by default
- Transparent records and exportable logs

## Suggested next milestones

1. unify the data model for scrap items, projects, videos, and analyses
2. finalize the AI inference flow for motion and mechanism detection
3. connect the Next.js dashboard to the API
4. add project pages, inventory management, and export tools
5. prepare deployment and single-command setup with Docker

## License

MIT
