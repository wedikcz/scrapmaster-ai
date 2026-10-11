from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime


class MotionProfileSchema(BaseModel):
    """Motion profile with complete metrics."""
    dominant_motion: str = Field(..., description="reciprocating, rotary, oscillatory, intermittent, static")
    cycle_estimate: Optional[float] = Field(None, description="Estimated cycle duration in seconds")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Motion classification confidence")
    sampled_frames: int = Field(default=0, description="Number of frames analyzed")
    analysis_method: str = Field(default="realtime-frame-analysis")
    
    min_delta: Optional[float] = None
    max_delta: Optional[float] = None
    avg_delta: Optional[float] = None
    std_dev_delta: Optional[float] = None
    
    velocity_estimate: Optional[float] = None
    acceleration_estimate: Optional[float] = None
    
    anomalies_detected: int = Field(default=0)
    anomaly_rate: float = Field(default=0.0, ge=0.0, le=1.0)
    
    processing_fps: Optional[float] = None
    total_processing_time_ms: Optional[int] = None

    class Config:
        json_schema_extra = {
            "example": {
                "dominant_motion": "reciprocating",
                "cycle_estimate": 0.85,
                "confidence": 0.82,
                "sampled_frames": 30,
                "min_delta": 5.2,
                "max_delta": 45.8,
                "avg_delta": 22.4,
                "std_dev_delta": 9.3,
                "velocity_estimate": 2.1,
                "acceleration_estimate": 0.8,
                "anomalies_detected": 2,
                "anomaly_rate": 0.067,
                "processing_fps": 28.5,
                "total_processing_time_ms": 1200,
            }
        }


class LikelyFaultSchema(BaseModel):
    """Identified fault with severity and analysis."""
    fault_name: str
    fault_description: str
    severity: str = Field(..., description="critical, high, medium, low, info")
    confidence: float = Field(..., ge=0.0, le=1.0)
    probable_causes: list[str] = Field(default_factory=list)
    contributing_factors: list[str] = Field(default_factory=list)
    impact_on_operation: Optional[str] = None
    risk_of_failure: float = Field(default=0.0, ge=0.0, le=1.0)
    estimated_remaining_life_hours: Optional[int] = None

    class Config:
        json_schema_extra = {
            "example": {
                "fault_name": "Worn cam follower",
                "fault_description": "The follower surface shows significant wear patterns",
                "severity": "high",
                "confidence": 0.87,
                "probable_causes": ["lubrication loss", "material fatigue"],
                "contributing_factors": ["high-frequency oscillation", "misalignment"],
                "impact_on_operation": "Reduced precision and increased vibration",
                "risk_of_failure": 0.65,
                "estimated_remaining_life_hours": 120,
            }
        }


class RepairStepSchema(BaseModel):
    """Repair procedure step."""
    step_number: int
    step_title: str
    step_description: str
    difficulty_level: str = Field(default="intermediate", description="beginner, intermediate, advanced, expert")
    estimated_time_minutes: Optional[int] = None
    required_tools: list[str] = Field(default_factory=list)
    required_materials: list[str] = Field(default_factory=list)
    safety_precautions: list[str] = Field(default_factory=list)
    ppe_required: list[str] = Field(default_factory=list)
    success_criteria: Optional[str] = None
    testing_procedure: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "step_number": 1,
                "step_title": "Inspect the cam and follower",
                "step_description": "Carefully examine the contact surfaces for wear, scoring, or debris",
                "difficulty_level": "intermediate",
                "estimated_time_minutes": 15,
                "required_tools": ["magnifying glass", "calipers", "feeler gauges"],
                "required_materials": ["cleaning solvent", "lint-free cloth"],
                "safety_precautions": ["Disconnect power", "Block rotating parts", "Wear gloves"],
                "ppe_required": ["safety glasses", "work gloves"],
                "success_criteria": "No visible scoring or wear patterns exceeding 0.5mm",
                "testing_procedure": "Manually rotate the shaft and feel for smooth engagement",
            }
        }


class RepurposeOptionSchema(BaseModel):
    """Alternative use case for the device."""
    use_case: str
    description: str
    feasibility: float = Field(..., ge=0.0, le=1.0, description="Implementation feasibility score")
    required_modifications: list[str] = Field(default_factory=list)
    required_components: list[str] = Field(default_factory=list)
    estimated_cost_usd: Optional[float] = None
    estimated_implementation_hours: Optional[int] = None
    suitable_for_industrial: bool = False
    suitable_for_hobby: bool = False
    suitable_for_educational: bool = False
    expected_lifespan_hours: Optional[int] = None

    class Config:
        json_schema_extra = {
            "example": {
                "use_case": "Manual actuator for laboratory testing",
                "description": "Convert the reciprocating mechanism into a manual force applicator",
                "feasibility": 0.78,
                "required_modifications": ["remove original drive", "add manual handle", "recalibrate coupling"],
                "required_components": ["stainless steel handle", "rubber grip", "coupling adapter"],
                "estimated_cost_usd": 45.0,
                "estimated_implementation_hours": 2,
                "suitable_for_industrial": False,
                "suitable_for_hobby": True,
                "suitable_for_educational": True,
                "expected_lifespan_hours": 1000,
            }
        }


class SafetyWarningSchema(BaseModel):
    """Critical safety warning."""
    warning_type: str = Field(..., description="electrical, mechanical, chemical, thermal, biological, unknown")
    severity: str = Field(..., description="critical, high, medium, low, info")
    warning_title: str
    warning_description: str
    hazard_identification: str
    potential_harm: str
    affected_components: list[str] = Field(default_factory=list)
    mitigation_steps: list[str] = Field(default_factory=list)
    ppe_recommended: list[str] = Field(default_factory=list)
    isolation_procedures: Optional[str] = None
    regulatory_standard: Optional[str] = None
    compliance_status: str = Field(default="unknown", description="compliant, non_compliant, unknown")

    class Config:
        json_schema_extra = {
            "example": {
                "warning_type": "mechanical",
                "severity": "critical",
                "warning_title": "Rotating shaft hazard",
                "warning_description": "Unguarded rotating shaft can cause severe entanglement injury",
                "hazard_identification": "Rotating shaft at 1800 RPM with exposed surface",
                "potential_harm": "Severe lacerations, bone fractures, or amputation",
                "affected_components": ["main drive shaft", "coupling"],
                "mitigation_steps": [
                    "Always install shaft guard before operation",
                    "Disconnect power and lockout/tagout before servicing",
                    "Never reach into rotating mechanism",
                ],
                "ppe_recommended": ["safety glasses", "steel-toed boots", "close-fitting clothing"],
                "isolation_procedures": "Disconnect main power, verify no residual motion",
                "regulatory_standard": "OSHA 1910.212",
                "compliance_status": "non_compliant",
            }
        }


class AnalysisConfidenceSchema(BaseModel):
    """Overall analysis confidence and quality assessment."""
    overall_confidence: float = Field(..., ge=0.0, le=1.0, description="Combined confidence across all components")
    confidence_level: str = Field(..., description="high, medium, low, very_low")
    
    motion_analysis_confidence: float = Field(default=0.0, ge=0.0, le=1.0)
    fault_detection_confidence: float = Field(default=0.0, ge=0.0, le=1.0)
    repair_guidance_confidence: float = Field(default=0.0, ge=0.0, le=1.0)
    repurpose_confidence: float = Field(default=0.0, ge=0.0, le=1.0)
    safety_assessment_confidence: float = Field(default=0.0, ge=0.0, le=1.0)
    
    data_quality_score: float = Field(default=0.0, ge=0.0, le=1.0)
    sample_completeness: float = Field(default=0.0, ge=0.0, le=1.0)
    model_applicability: float = Field(default=0.0, ge=0.0, le=1.0)
    
    identified_limitations: list[str] = Field(default_factory=list)
    uncertainty_sources: list[str] = Field(default_factory=list)
    recommended_next_steps: list[str] = Field(default_factory=list)
    data_collection_recommendations: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "overall_confidence": 0.82,
                "confidence_level": "medium",
                "motion_analysis_confidence": 0.87,
                "fault_detection_confidence": 0.79,
                "repair_guidance_confidence": 0.81,
                "repurpose_confidence": 0.74,
                "safety_assessment_confidence": 0.88,
                "data_quality_score": 0.83,
                "sample_completeness": 0.95,
                "model_applicability": 0.76,
                "identified_limitations": [
                    "Low light conditions affected frame quality",
                    "Limited device type historical data",
                    "Partial view of critical components",
                ],
                "uncertainty_sources": [
                    "Unknown maintenance history",
                    "Unclear loading conditions",
                    "Possible prior repairs",
                ],
                "recommended_next_steps": [
                    "Perform detailed visual inspection of cam surface",
                    "Measure wear depth with precision instruments",
                    "Request device operating history from user",
                ],
                "data_collection_recommendations": "Additional high-resolution footage from multiple angles would improve analysis confidence by 15-20%",
            }
        }


class CompleteAnalysisResponseSchema(BaseModel):
    """Complete analysis output with all components."""
    device_name: str
    mechanism_summary: str
    
    motion_profile: MotionProfileSchema
    likely_faults: list[LikelyFaultSchema] = Field(default_factory=list)
    repair_steps: list[RepairStepSchema] = Field(default_factory=list)
    repurpose_options: list[RepurposeOptionSchema] = Field(default_factory=list)
    safety_warnings: list[SafetyWarningSchema] = Field(default_factory=list)
    confidence_assessment: AnalysisConfidenceSchema
    
    timestamp: datetime
    analysis_session_id: str
    processing_time_ms: int
