backend/
├── app/
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── deps.py
│   │   └── routes/
│   │       ├── __init__.py
│   │       ├── health.py
│   │       ├── videos.py
│   │       ├── scrap.py
│   │       └── projects.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── security.py
│   │   ├── logging.py
│   │   └── middleware.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── user.py
│   │   ├── scrap_item.py
│   │   ├── project.py
│   │   ├── analysis_run.py
│   │   ├── schematic.py
│   │   ├── audit_log.py
│   │   └── alert.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── video_analysis.py
│   │   ├── scrap_item.py
│   │   ├── project.py
│   │   └── auth.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── motion_analysis.py
│   │   ├── mechanism_inference.py
│   │   ├── export_service.py
│   │   ├── alert_service.py
│   │   └── local_ai_adapter.py
│   ├── utils/
│   │   ├── __init__.py
│   │   └── validators.py
│   ├── main.py
│   └── startup.py
├── migrations/
│   └── 001_initial_schema.sql
├── tests/
│   ├── __init__.py
│   ├── test_health.py
│   ├── test_videos.py
│   └── test_scrap.py
├── requirements.txt
├── requirements-dev.txt
├── Dockerfile
├── .dockerignore
└── .env.example

frontend/
├── app/
│   ├── api/
│   │   └── client.ts
│   ├── auth/
│   │   ├── layout.tsx
│   │   ├── login/
│   │   │   └── page.tsx
│   │   └── register/
│   │       └── page.tsx
│   ├── dashboard/
│   │   ├── layout.tsx
│   │   ├── page.tsx
│   │   ├── videos/
│   │   │   ├── page.tsx
│   │   │   ├── upload/
│   │   │   │   └── page.tsx
│   │   │   └── [id]/
│   │   │       └── page.tsx
│   │   ├── inventory/
│   │   │   └── page.tsx
│   │   ├── projects/
│   │   │   └── page.tsx
│   │   └── settings/
│   │       └── page.tsx
│   ├── globals.css
│   ├── layout.tsx
│   └── page.tsx
│   ├── loading.tsx
│   └── error.tsx
├── components/
│   ├── dashboard/
│   │   ├── header.tsx
│   │   ├── sidebar.tsx
│   │   ├── metrics.tsx
│   │   ├── alerts.tsx
│   │   └── logs.tsx
│   ├── video/
│   │   ├── upload-card.tsx
│   │   ├── result-panel.tsx
│   │   ├── motion-graph.tsx
│   │   └── timeline.tsx
│   ├── inventory/
│   │   ├── item-card.tsx
│   │   └── item-list.tsx
│   ├── common/
│   │   ├── button.tsx
│   │   ├── card.tsx
│   │   ├── modal.tsx
│   │   └── loading.tsx
│   └── auth/
│       ├── login-form.tsx
│       └── register-form.tsx
├── lib/
│   ├── api.ts
│   ├── auth.ts
│   ├── storage.ts
│   ├── export.ts
│   └── types.ts
├── public/
│   └── favicon.ico
├── package.json
├── package-lock.json
├── tsconfig.json
├── next.config.mjs
├── tailwind.config.ts
├── postcss.config.js
├── .env.example
├── .env.local.example
└── Dockerfile

docs/
├── architecture.md
├── api-contract.md
├── deployment.md
├── security.md
├── video-analysis.md
└── troubleshooting.md

ROOT
├── docker-compose.yml
├── docker-compose.prod.yml
├── titancore.py
├── titancore.sh
├── .gitignore
├── .env.example
├── README.md
└── LICENSE
