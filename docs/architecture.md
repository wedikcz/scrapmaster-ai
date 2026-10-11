# ScrapMaster Unified architecture

This project intentionally merges the best parts of the existing experiments into one coherent platform.

## Core idea

The project is centered around three layers:

1. Frontend experience
   - Next.js dashboard for analysis, inventory, projects, and reporting
2. Backend API
   - FastAPI application exposing the product domain and persistence layer
3. AI analysis engine
   - Local-first motion and mechanism inference with optional cloud summary support

## Why this structure is the best merge

### from `scrapmaster-ai`

- strongest product framing
- local-first AI philosophy
- repair and repurpose workflow ideas
- video and mechanism analysis concepts
- FastAPI + Python backend direction

### from `scrapmaster` and `scrapmasterv2`

- React/Next UI patterns
- dashboard concepts and landing-page composition
- experimentation with AI orchestration and GenAI calls
- product polish ideas and app layout patterns

## Product modules

### 1. Inventory

Track salvaged items, worker/operator notes, condition scores, expected reuse, and project links.

### 2. Video analysis

User uploads a clip and gets:

- motion profile
- likely mechanism interpretation
- likely faults
- repair plan
- repurpose opportunities

### 3. Project workflow

Each project may contain:

- multiple scrap items
- multiple analysis runs
- inspection logs
- safety notes
- exportable design summary

### 4. Safety/repair guidance

The system always emphasizes:

- isolation of power sources
- evaluation of stored energy
- mechanical hazard awareness
- safe handling recommendations

## Suggested data model

```text
ScrapItem
- id
- name
- category
- source
- condition
- estimated_value
- created_at

Project
- id
- title
- description
- status
- created_at

VideoAnalysisRun
- id
- project_id
- file_name
- mechanism_summary
- motion_profile
- confidence
- created_at

SafetyLog
- id
- project_id
- title
- details
- severity
```

## Target delivery

The end product should feel like a single vertically integrated platform:

- upload and inspect salvaged hardware
- quote reuse potential
- understand motion and mechanism
- generate guidance and project logs
- keep all work private and local-first
