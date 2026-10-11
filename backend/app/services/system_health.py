import logging
import psutil
from datetime import datetime
from app.core.config import get_settings
from app.core.database import SessionLocal
from app.models.realtime import RealtimeMetric

logger = logging.getLogger(__name__)
settings = get_settings()

class SystemHealthMonitor:
    """Monitor and report system health metrics in real-time."""
    
    def __init__(self):
        self.start_time = datetime.utcnow()
        self.active_sessions = 0
        self.completed_sessions = 0
        self.failed_sessions = 0
        self.last_error = None

    def get_system_metrics(self) -> dict:
        """Get current system health metrics."""
        cpu_percent = psutil.cpu_percent(interval=0.1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        return {
            "cpu_usage_percent": cpu_percent,
            "memory_usage_percent": memory.percent,
            "memory_available_mb": memory.available / (1024 * 1024),
            "disk_usage_percent": disk.percent,
            "disk_free_gb": disk.free / (1024 * 1024 * 1024),
        }

    def get_health_status(self) -> str:
        """Determine overall health status."""
        metrics = self.get_system_metrics()
        
        if (metrics["cpu_usage_percent"] > 90 or 
            metrics["memory_usage_percent"] > 85 or 
            metrics["disk_usage_percent"] > 90):
            return "critical"
        
        if (metrics["cpu_usage_percent"] > 75 or 
            metrics["memory_usage_percent"] > 75 or 
            metrics["disk_usage_percent"] > 75):
            return "degraded"
        
        return "healthy"

    def get_uptime_seconds(self) -> int:
        """Get system uptime in seconds."""
        return int((datetime.utcnow() - self.start_time).total_seconds())

    def record_metric(self, metric_name: str, value: float, unit: str | None = None, tags: str | None = None):
        """Record a real-time metric to database."""
        try:
            with SessionLocal() as db:
                metric = RealtimeMetric(
                    metric_name=metric_name,
                    metric_value=value,
                    unit=unit,
                    tags=tags,
                )
                db.add(metric)
                db.commit()
        except Exception as e:
            logger.error(f"Failed to record metric {metric_name}: {str(e)}")

    def record_error(self, error_message: str):
        """Record an error for monitoring."""
        self.last_error = error_message
        self.failed_sessions += 1
        self.record_metric("errors_recorded", 1, tags=f"error_type=analysis")

    def get_performance_report(self) -> dict:
        """Get detailed performance report."""
        metrics = self.get_system_metrics()
        uptime = self.get_uptime_seconds()
        
        return {
            "status": self.get_health_status(),
            "timestamp": datetime.utcnow().isoformat(),
            "system_metrics": metrics,
            "session_stats": {
                "active": self.active_sessions,
                "completed": self.completed_sessions,
                "failed": self.failed_sessions,
                "total": self.active_sessions + self.completed_sessions + self.failed_sessions,
            },
            "uptime_seconds": uptime,
            "last_error": self.last_error,
            "alerts": self._generate_alerts(metrics),
        }

    def _generate_alerts(self, metrics: dict) -> list[str]:
        """Generate system alerts based on metrics."""
        alerts = []
        
        if metrics["cpu_usage_percent"] > 85:
            alerts.append(f"High CPU usage: {metrics['cpu_usage_percent']:.1f}%")
        
        if metrics["memory_usage_percent"] > 80:
            alerts.append(f"High memory usage: {metrics['memory_usage_percent']:.1f}%")
        
        if metrics["disk_usage_percent"] > 85:
            alerts.append(f"High disk usage: {metrics['disk_usage_percent']:.1f}%")
        
        if metrics["memory_available_mb"] < 256:
            alerts.append(f"Low available memory: {metrics['memory_available_mb']:.0f}MB")
        
        if metrics["disk_free_gb"] < 1:
            alerts.append(f"Low disk space: {metrics['disk_free_gb']:.2f}GB free")
        
        return alerts

health_monitor = SystemHealthMonitor()
