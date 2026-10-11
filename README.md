# ScrapMaster AI

ScrapMaster AI is a privacy-first, local-first platform for salvaged hardware recycling, reverse video engineering, mechanical inference, and build guidance generation.

It helps users:
- Analyze video clips of salvaged mechanical devices
- Extract motion characteristics and infer device operation
- Generate repair and repurposing workflows
- Track inventory, projects, schematics, and operational logs
- Work offline with local AI-first inference and optional cloud sync hooks

## Core features

- Inverse video engineering for mechanical systems
- Motion analysis and mechanism inference
- Repair and repurposing guidance generation
- Inventory and scrap tracking
- Project lifecycle management
- Safety-oriented schematic generation for salvaged hardware
- Local-first dashboard with monitoring and export tools

## Project architecture

- Frontend: Next.js app router + Tailwind CSS
- Backend: FastAPI + Pydantic v2 + SQLite
- AI: local-first motion inference, OpenCV-based fallback, and mock analyzer for warm-up environments
- Data: SQLite with modular schema for scrap items, projects, schematics, audit logs, and analysis runs

## Quick start

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

### Docker

```bash
docker compose up --build
```

## API overview

- `POST /api/v1/videos/analyze`
- `GET /api/v1/health`
- `GET /api/v1/scrap/items`
- `POST /api/v1/scrap/items`

## Example output

```json
{
  "device_name": "salvaged gearbox",
  "mechanism_summary": "The mechanism shows alternating linear motion converted to rotary output through a cam-and-follower arrangement.",
  "motion_profile": {
    "dominant_motion": "reciprocating",
    "cycle_estimate": 0.85,
    "confidence": 0.82
  },
  "likely_faults": [
    "worn gear teeth",
    "misaligned cam follower",
    "dragging bearing"
  ],
  "repair_steps": [
    "Inspect the follower track for wear",
    "Check for lubrication loss",
    "Verify that the drive shaft rotates without binding"
  ],
  "repurpose_options": [
    "gearbox-driven actuator",
    "manual feed mechanism",
    "sensory motion pump"
  ]
}
```

## Security and privacy

- Local inference first
- No mandatory commercial cloud dependency
- Exportable logs for auditing
- Safety warnings included by default

## License

MIT
