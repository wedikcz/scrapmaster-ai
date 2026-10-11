from datetime import datetime
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.audit_log import AuditLog
from app.models.analysis_run import AnalysisRun


class AuditTrail:
    """Audit trail service for logging all system actions."""

    @staticmethod
    def log(
        db: Session,
        user_id: int | None,
        action: str,
        resource_type: str,
        resource_id: int | None = None,
        status: str = "success",
        details: str | None = None,
        ip_address: str | None = None,
    ) -> AuditLog:
        log_entry = AuditLog(
            user_id=user_id,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            status=status,
            details=details,
            ip_address=ip_address,
        )
        db.add(log_entry)
        db.commit()
        return log_entry

    @staticmethod
    def get_action_count(
        db: Session, action: str, resource_type: str, days: int = 7
    ) -> int:
        cutoff = datetime.utcnow() - __import__("datetime").timedelta(days=days)
        return (
            db.query(func.count(AuditLog.id))
            .filter(
                AuditLog.action == action,
                AuditLog.resource_type == resource_type,
                AuditLog.created_at >= cutoff,
            )
            .scalar()
        )
