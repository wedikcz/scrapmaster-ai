# ScrapMaster AI architecture notes

## Repository layout

- `backend/` — FastAPI application, Pydantic schemas, SQLite models, and motion analysis services.
- `frontend/` — Next.js dashboard and client-side interface.
- `docs/` — design notes, API contracts, and deployment guidance.

## Core modules

### Inverse video engineering module

The video pipeline is designed to accept clips of mechanically operating salvage devices and estimate motion patterns using OpenCV when available. If OpenCV is unavailable, the system falls back to a deterministic mock analysis to keep the app usable during local setup or warm-up.

### Data model

- `scrap_items` — inventory records for salvaged and reusable materials
- `projects` — high-level build or repair tasks
- `schematics` — generated explanation or technical diagrams
- `analysis_runs` — inference results from mechanism analysis
- `app_logs` — operational logs and export history

### API contract

```json
{
  "device_name": "salvaged gearbox",
  "notes": "Observed repeated motion with a cam-driven return cycle.",
  "motion_hint": "reciprocating",
  "video_duration_seconds": 12.4,
  "frame_count": 30
}
```

Response:

```json
{
  "device_name": "salvaged gearbox",
  "mechanism_summary": "The mechanism likely converts oscillating motion into a cyclic mechanical action.",
  "motion_profile": {
    "dominant_motion": "reciprocating",
    "cycle_estimate": 0.9,
    "confidence": 0.82,
    "sampled_frames": 30
  },
  "likely_faults": ["worn cam follower", "misaligned linkage"],
  "repair_steps": ["Inspect follower path", "Relubricate pivots", "Verify alignment"],
  "repurpose_options": ["manual actuator", "motion trigger"],
  "safety_warnings": ["Disconnect stored energy before testing."]
}
```

## Deployment notes

- Local backend: `uvicorn app.main:app --reload`
- Local frontend: `npm run dev`
- Containerized stack: `docker compose up --build`

## Future enhancements

- Real frame-level motion tracking
- Local vector search over datasheets and repair notes
- Secure auth and role-based access
- Offline-first storage using IndexedDB and cache sync
- Cloud-sync adapters for remote collaboration
