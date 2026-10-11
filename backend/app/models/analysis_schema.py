from datetime import datetime
from sqlalchemy import String, Text, Integer, Float, DateTime, Boolean, JSON, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column
import enum

from app.core.database import Base
from app.models.base import TimestampMixin, UserMixin


class MotionTypeEnum(str, enum.Enum):
    """Motion classification types."""
    RECIPROCATING = "reciprocating"
    ROTARY = "rotary"
    OSCILLATORY = "oscillatory"
    INTERMITTENT = "intermittent"
    STATIC = "static"
    UNKNOWN = "unknown"


class FaultSeverityEnum(str, enum.Enum):
    """Fault severity levels."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class MotionProfile(Base, TimestampMixin):
    """Complete motion analysis profile with real-time metrics."""
    __tablename__ = "motion_profiles"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    analysis_run_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    
    # Core motion classification
    dominant_motion: Mapped[str] = mapped_column(
        SQLEnum(MotionTypeEnum),
        default=MotionTypeEnum.UNKNOWN,
        nullable=False
    )
    cycle_estimate: Mapped[float | None] = mapped_column(Float, nullable=True)
    confidence: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    sampled_frames: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    analysis_method: Mapped[str] = mapped_column(String(100), default="realtime-frame-analysis")
    
    # Motion statistics
    min_delta: Mapped[float] = mapped_column(Float, nullable=True)
    max_delta: Mapped[float] = mapped_column(Float, nullable=True)
    avg_delta: Mapped[float] = mapped_column(Float, nullable=True)
    std_dev_delta: Mapped[float] = mapped_column(Float, nullable=True)
    
    # Velocity and acceleration
    velocity_estimate: Mapped[float | None] = mapped_column(Float, nullable=True)
    acceleration_estimate: Mapped[float | None] = mapped_column(Float, nullable=True)
    
    # Anomaly detection
    anomalies_detected: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    anomaly_rate: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    
    # Performance metrics
    processing_fps: Mapped[float] = mapped_column(Float, nullable=True)
    total_processing_time_ms: Mapped[int] = mapped_column(Integer, nullable=True)
    
    # Additional metadata
    motion_classification_data: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    
    def __repr__(self) -> str:
        return f"<MotionProfile(id={self.id}, motion={self.dominant_motion}, confidence={self.confidence})>"


class LikelyFault(Base, TimestampMixin):
    """Identified fault and issue predictions."""
    __tablename__ = "likely_faults"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    analysis_run_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    motion_profile_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    
    # Fault identification
    fault_name: Mapped[str] = mapped_column(String(200), nullable=False)
    fault_description: Mapped[str] = mapped_column(Text, nullable=False)
    severity: Mapped[str] = mapped_column(
        SQLEnum(FaultSeverityEnum),
        default=FaultSeverityEnum.MEDIUM,
        nullable=False
    )
    confidence: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    
    # Root cause analysis
    probable_causes: Mapped[list[str]] = mapped_column(JSON, default=[], nullable=False)
    contributing_factors: Mapped[list[str]] = mapped_column(JSON, default=[], nullable=False)
    
    # Impact assessment
    impact_on_operation: Mapped[str] = mapped_column(Text, nullable=True)
    risk_of_failure: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    estimated_remaining_life_hours: Mapped[int | None] = mapped_column(Integer, nullable=True)
    
    # Additional context
    related_motion_patterns: Mapped[str | None] = mapped_column(Text, nullable=True)
    
    def __repr__(self) -> str:
        return f"<LikelyFault(id={self.id}, fault={self.fault_name}, severity={self.severity})>"


class RepairStep(Base, TimestampMixin):
    """Recommended repair and maintenance procedures."""
    __tablename__ = "repair_steps"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    analysis_run_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    likely_fault_id: Mapped[int | None] = mapped_column(Integer, nullable=True, index=True)
    
    # Step sequence
    step_number: Mapped[int] = mapped_column(Integer, nullable=False)
    step_title: Mapped[str] = mapped_column(String(200), nullable=False)
    step_description: Mapped[str] = mapped_column(Text, nullable=False)
    
    # Repair details
    difficulty_level: Mapped[str] = mapped_column(String(50), default="intermediate")  # beginner, intermediate, advanced, expert
    estimated_time_minutes: Mapped[int | None] = mapped_column(Integer, nullable=True)
    required_tools: Mapped[list[str]] = mapped_column(JSON, default=[], nullable=False)
    required_materials: Mapped[list[str]] = mapped_column(JSON, default=[], nullable=False)
    
    # Safety considerations
    safety_precautions: Mapped[list[str]] = mapped_column(JSON, default=[], nullable=False)
    ppe_required: Mapped[list[str]] = mapped_column(JSON, default=[], nullable=False)
    
    # Verification
    success_criteria: Mapped[str] = mapped_column(Text, nullable=True)
    testing_procedure: Mapped[str] = mapped_column(Text, nullable=True)
    
    def __repr__(self) -> str:
        return f"<RepairStep(step={self.step_number}, title={self.step_title})>"


class RepurposeOption(Base, TimestampMixin):
    """Alternative use cases and repurposing recommendations."""
    __tablename__ = "repurpose_options"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    analysis_run_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    motion_profile_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    
    # Repurposing information
    use_case: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    feasibility: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)  # 0-1
    
    # Requirements
    required_modifications: Mapped[list[str]] = mapped_column(JSON, default=[], nullable=False)
    required_components: Mapped[list[str]] = mapped_column(JSON, default=[], nullable=False)
    estimated_cost_usd: Mapped[float | None] = mapped_column(Float, nullable=True)
    estimated_implementation_hours: Mapped[int | None] = mapped_column(Integer, nullable=True)
    
    # Application suitability
    suitable_for_industrial: Mapped[bool] = mapped_column(Boolean, default=False)
    suitable_for_hobby: Mapped[bool] = mapped_column(Boolean, default=False)
    suitable_for_educational: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # Additional information
    expected_lifespan_hours: Mapped[int | None] = mapped_column(Integer, nullable=True)
    performance_metrics: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    
    def __repr__(self) -> str:
        return f"<RepurposeOption(id={self.id}, use_case={self.use_case}, feasibility={self.feasibility})>"


class SafetyWarning(Base, TimestampMixin):
    """Critical safety warnings and hazard identification."""
    __tablename__ = "safety_warnings"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    analysis_run_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    
    # Warning severity and classification
    warning_type: Mapped[str] = mapped_column(String(100), nullable=False)  # electrical, mechanical, chemical, thermal, etc.
    severity: Mapped[str] = mapped_column(
        SQLEnum(FaultSeverityEnum),
        default=FaultSeverityEnum.HIGH,
        nullable=False
    )
    warning_title: Mapped[str] = mapped_column(String(200), nullable=False)
    warning_description: Mapped[str] = mapped_column(Text, nullable=False)
    
    # Hazard details
    hazard_identification: Mapped[str] = mapped_column(Text, nullable=False)
    potential_harm: Mapped[str] = mapped_column(Text, nullable=False)
    affected_components: Mapped[list[str]] = mapped_column(JSON, default=[], nullable=False)
    
    # Mitigation strategies
    mitigation_steps: Mapped[list[str]] = mapped_column(JSON, default=[], nullable=False)
    ppe_recommended: Mapped[list[str]] = mapped_column(JSON, default=[], nullable=False)
    isolation_procedures: Mapped[str] = mapped_column(Text, nullable=True)
    
    # Regulatory compliance
    regulatory_standard: Mapped[str | None] = mapped_column(String(100), nullable=True)
    compliance_status: Mapped[str] = mapped_column(String(50), default="unknown")  # compliant, non_compliant, unknown
    
    # Additional context
    historical_incident_data: Mapped[str | None] = mapped_column(Text, nullable=True)
    
    def __repr__(self) -> str:
        return f"<SafetyWarning(id={self.id}, type={self.warning_type}, severity={self.severity})>"


class AnalysisConfidence(Base, TimestampMixin):
    """Confidence metrics and quality assessment for entire analysis."""
    __tablename__ = "analysis_confidence"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    analysis_run_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True, unique=True)
    
    # Overall confidence
    overall_confidence: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)  # 0-1
    confidence_level: Mapped[str] = mapped_column(String(50))  # high, medium, low, very_low
    
    # Component confidence scores
    motion_analysis_confidence: Mapped[float] = mapped_column(Float, default=0.0)
    fault_detection_confidence: Mapped[float] = mapped_column(Float, default=0.0)
    repair_guidance_confidence: Mapped[float] = mapped_column(Float, default=0.0)
    repurpose_confidence: Mapped[float] = mapped_column(Float, default=0.0)
    safety_assessment_confidence: Mapped[float] = mapped_column(Float, default=0.0)
    
    # Quality metrics
    data_quality_score: Mapped[float] = mapped_column(Float, default=0.0)  # Based on input quality
    sample_completeness: Mapped[float] = mapped_column(Float, default=0.0)  # Percentage of frames analyzed
    model_applicability: Mapped[float] = mapped_column(Float, default=0.0)  # How well model fits device type
    
    # Uncertainty factors
    identified_limitations: Mapped[list[str]] = mapped_column(JSON, default=[], nullable=False)
    uncertainty_sources: Mapped[list[str]] = mapped_column(JSON, default=[], nullable=False)
    
    # Recommendations for improvement
    recommended_next_steps: Mapped[list[str]] = mapped_column(JSON, default=[], nullable=False)
    data_collection_recommendations: Mapped[str | None] = mapped_column(Text, nullable=True)
    
    def __repr__(self) -> str:
        return f"<AnalysisConfidence(analysis_id={self.analysis_run_id}, overall={self.overall_confidence})>"
