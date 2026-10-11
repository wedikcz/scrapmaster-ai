# ScrapMaster Unified API

## Base URL

- Local: `http://localhost:8000`
- Prod: configurable by environment

## Endpoints

### Health

`GET /`

Returns a simple service status object.

Example:

```json
{
  "app": "ScrapMaster Unified",
  "status": "online"
}
```

### Health check

`GET /api/v1/health`

Returns service health.

### Motion analysis

`POST /api/v1/videos/analyze`

Request:

```json
{
  "device_name": "salvaged gearbox",
  "video_url": "https://example.com/clip.mp4",
  "notes": "high wear, noisy operation"
}
```

Response:

```json
{
  "device_name": "salvaged gearbox",
  "mechanism_summary": "Likely cam-and-follower conversion with recurring motion.",
  "motion_profile": {
    "dominant_motion": "reciprocating",
    "cycle_estimate": 0.85,
    "confidence": 0.82
  },
  "likely_faults": ["worn track", "bearing play"],
  "repair_steps": ["inspect follower path", "verify lubrication"],
  "repurpose_options": ["low-force actuator"]
}
```

### Scrap items

- `GET /api/v1/scrap/items`
- `POST /api/v1/scrap/items`

### Projects

- `GET /api/v1/projects`
- `POST /api/v1/projects`

## Notes

This API is intentionally designed to stay compatible with the product direction already established in the AI-first repo while modernizing the overall system into a single coherent platform.
