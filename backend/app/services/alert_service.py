from datetime import datetime
from typing import Any

from app.models.alert import Alert
from app.core.database import SessionLocal


class AlertService:
    """Create and manage alerts for analysis completion, safety notices, etc."""

    def create_alert(
        self,
        alert_type: str,
        severity: str,
        title: str,
        message: str,
        related_resource_type: str | None = None,
        related_resource_id: int | None = None,
    ) -> Alert:
        with SessionLocal() as db:
            alert = Alert(
                alert_type=alert_type,
                severity=severity,
                title=title,
                message=message,
                related_resource_type=related_resource_type,
                related_resource_id=related_resource_id,
            )
            db.add(alert)
            db.commit()
            db.refresh(alert)
            return alert

    def create_safety_alert(self, device_name: str, message: str) -> Alert:
        return self.create_alert(
            alert_type="safety_warning",
            severity="critical",
            title=f"Safety warning: {device_name}",
            message=message,
        )

    def create_analysis_alert(self, device_name: str, confidence: float) -> Alert:
        return self.create_alert(
            alert_type="analysis_complete",
            severity="info" if confidence >= 0.7 else "warning",
            title=f"Analysis complete: {device_name}",
            message=f"Mechanism analysis completed with confidence {confidence:.2f}",
        )
