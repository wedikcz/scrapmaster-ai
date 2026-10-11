import json
from pathlib import Path

from app.core.config import get_settings

settings = get_settings()


class ExportService:
    """Service for exporting report logs and JSON output."""

    def __init__(self, export_dir: str | None = None):
        self.export_dir = Path(export_dir or settings.export_dir)
        self.export_dir.mkdir(parents=True, exist_ok=True)

    def export_analysis_report(self, report: dict, filename: str | None = None) -> str:
        output_name = filename or f"analysis-report-{report.get('device_name', 'unknown').replace(' ', '-').lower()}.json"
        output_path = self.export_dir / output_name
        output_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
        return str(output_path)

    def export_text_summary(self, report: dict, filename: str | None = None) -> str:
        output_name = filename or f"analysis-summary-{report.get('device_name', 'unknown').replace(' ', '-').lower()}.txt"
        text = [
            f"Device: {report.get('device_name', 'unknown')}",
            f"Mechanism summary: {report.get('mechanism_summary', '')}",
            "",
            "Likely faults:",
        ]
        for fault in report.get("likely_faults", []):
            text.append(f"- {fault}")
        text.extend(["", "Repair steps:"])
        for step in report.get("repair_steps", []):
            text.append(f"- {step}")

        output_path = self.export_dir / output_name
        output_path.write_text("\n".join(text), encoding="utf-8")
        return str(output_path)
