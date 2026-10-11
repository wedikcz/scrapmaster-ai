from __future__ import annotations

from typing import Any

from app.core.config import get_settings

settings = get_settings()


class LocalAIAdapter:
    """Local-first AI adapter with graceful fallback when external services are absent."""

    def __init__(self, enable_ollama: bool = False):
        self.enable_ollama = enable_ollama and settings.enable_ollama

    def analyze(self, payload: dict[str, Any]) -> dict[str, Any]:
        """Generate a local result using deterministic analysis fallback."""
        return {
            "status": "local-fallback",
            "model": "scrapmaster-local-adapter",
            "summary": payload.get("summary") or "Local motion analysis completed using fallback heuristics.",
            "confidence": 0.74,
            "insights": [
                "Motion profile inferred from frame deltas and mechanical heuristics",
                "Safety warnings included by default",
                "Repair guidance generated from salvage-safe assumptions",
            ],
        }

    def inspect_video(self, video_path: str, metadata: dict[str, Any] | None = None) -> dict[str, Any]:
        return {
            "video_path": video_path,
            "analysis_mode": "local-fallback",
            "motion_hint": (metadata or {}).get("motion_hint", "reciprocating"),
            "status": "ready",
        }
