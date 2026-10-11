import time
import json
from typing import Any, Optional
from pathlib import Path
import logging

from app.core.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

class RealtimeMotionProcessor:
    """Real-time motion analysis processor with streaming updates."""

    def __init__(self, session_id: str, max_frames: int = 60):
        self.session_id = session_id
        self.max_frames = max_frames
        self.frame_history = []
        self.motion_deltas = []
        self.motion_classifications = []
        self.motion_anomalies = []
        self.start_time = time.time()
        self.processing_times = []
        self.current_confidence = 0.0
        self.motion_profile = {
            "dominant_motion": "unknown",
            "cycle_estimate": None,
            "confidence": 0.0,
            "sampled_frames": 0,
            "anomalies_detected": 0,
        }

    def process_frame_delta(
        self, 
        frame_index: int, 
        delta_value: float,
        previous_deltas: list[float] | None = None
    ) -> dict[str, Any]:
        """Process a single frame motion delta in real-time."""
        process_start = time.time()
        
        self.motion_deltas.append(delta_value)
        self.frame_history.append(frame_index)
        
        # Classify motion type based on current and historical deltas
        motion_type = self._classify_motion_type(delta_value, previous_deltas or [])
        self.motion_classifications.append(motion_type)
        
        # Detect anomalies
        is_anomaly = self._detect_anomaly(delta_value)
        if is_anomaly:
            self.motion_anomalies.append(frame_index)
            self.motion_profile["anomalies_detected"] += 1
        
        # Calculate real-time metrics
        velocity = self._estimate_velocity(frame_index)
        acceleration = self._estimate_acceleration(frame_index)
        
        # Update confidence
        self.current_confidence = self._update_confidence()
        self.motion_profile["confidence"] = self.current_confidence
        self.motion_profile["sampled_frames"] = frame_index + 1
        
        # Update dominant motion
        if len(self.motion_classifications) > 5:
            self.motion_profile["dominant_motion"] = self._determine_dominant_motion()
        
        process_time = (time.time() - process_start) * 1000
        self.processing_times.append(process_time)
        
        return {
            "frame_index": frame_index,
            "motion_delta": float(delta_value),
            "motion_type": motion_type,
            "confidence_score": self.current_confidence,
            "velocity_estimate": velocity,
            "acceleration_estimate": acceleration,
            "is_anomaly": is_anomaly,
            "anomaly_score": float(delta_value) / 100.0 if is_anomaly else 0.0,
            "processing_time_ms": process_time,
            "interim_profile": self.motion_profile.copy(),
        }

    def _classify_motion_type(self, delta: float, previous: list[float]) -> str:
        """Classify motion type based on pattern."""
        if delta < 10:
            return "static"
        
        if len(previous) >= 2:
            # Check for oscillation (alternating high/low deltas)
            if previous[-1] > 15 and delta < 10:
                return "oscillatory"
            if previous[-1] < 10 and delta > 15:
                return "oscillatory"
            
            # Check for sustained motion (consistent deltas)
            avg_prev = sum(previous[-5:]) / min(5, len(previous)) if previous else 0
            if abs(delta - avg_prev) < 5:
                return "sustained"
        
        if 20 <= delta <= 40:
            return "reciprocating"
        elif delta > 40:
            return "rotary"
        else:
            return "intermittent"

    def _detect_anomaly(self, delta: float) -> bool:
        """Detect motion anomalies."""
        if len(self.motion_deltas) < 3:
            return False
        
        avg_delta = sum(self.motion_deltas[-10:]) / min(10, len(self.motion_deltas))
        threshold = avg_delta * 2.5
        
        return delta > threshold or delta < (avg_delta * 0.1)

    def _estimate_velocity(self, frame_index: int) -> float:
        """Estimate velocity from motion delta."""
        if frame_index == 0:
            return 0.0
        
        if len(self.motion_deltas) < 2:
            return float(self.motion_deltas[-1])
        
        return float(self.motion_deltas[-1] - self.motion_deltas[-2])

    def _estimate_acceleration(self, frame_index: int) -> float:
        """Estimate acceleration from velocity changes."""
        if frame_index < 2 or len(self.motion_deltas) < 3:
            return 0.0
        
        v1 = self.motion_deltas[-1] - self.motion_deltas[-2]
        v0 = self.motion_deltas[-2] - self.motion_deltas[-3]
        
        return float(v1 - v0)

    def _update_confidence(self) -> float:
        """Update overall confidence based on processed frames."""
        if len(self.motion_deltas) < 3:
            return 0.5
        
        avg_delta = sum(self.motion_deltas) / len(self.motion_deltas)
        confidence = min(0.95, max(0.4, avg_delta / 100.0))
        
        # Adjust for anomaly detection
        if self.motion_anomalies:
            anomaly_ratio = len(self.motion_anomalies) / len(self.motion_deltas)
            confidence *= (1 - anomaly_ratio * 0.1)
        
        return round(confidence, 2)

    def _determine_dominant_motion(self) -> str:
        """Determine dominant motion type from classifications."""
        from collections import Counter
        
        if not self.motion_classifications:
            return "unknown"
        
        counts = Counter(self.motion_classifications[-20:])
        dominant, _ = counts.most_common(1)[0]
        
        return dominant

    def finalize_analysis(self) -> dict[str, Any]:
        """Finalize analysis and return complete motion profile."""
        elapsed_ms = (time.time() - self.start_time) * 1000
        
        if len(self.motion_deltas) > 0:
            avg_delta = sum(self.motion_deltas) / len(self.motion_deltas)
            cycle_estimate = round(avg_delta / 30.0, 2) if avg_delta > 0 else None
        else:
            cycle_estimate = None
        
        avg_processing_time = sum(self.processing_times) / len(self.processing_times) if self.processing_times else 0
        fps = 1000.0 / avg_processing_time if avg_processing_time > 0 else 0
        
        return {
            "session_id": self.session_id,
            "dominant_motion": self.motion_profile["dominant_motion"],
            "cycle_estimate": cycle_estimate,
            "confidence": self.motion_profile["confidence"],
            "sampled_frames": self.motion_profile["sampled_frames"],
            "anomalies_detected": self.motion_profile["anomalies_detected"],
            "total_processing_time_ms": elapsed_ms,
            "average_frame_processing_ms": avg_processing_time,
            "processing_fps": fps,
            "motion_statistics": {
                "min_delta": float(min(self.motion_deltas)) if self.motion_deltas else 0,
                "max_delta": float(max(self.motion_deltas)) if self.motion_deltas else 0,
                "avg_delta": float(sum(self.motion_deltas) / len(self.motion_deltas)) if self.motion_deltas else 0,
                "std_dev": self._calculate_std_dev(),
            },
            "method": "realtime-frame-analysis",
        }

    def _calculate_std_dev(self) -> float:
        """Calculate standard deviation of motion deltas."""
        if len(self.motion_deltas) < 2:
            return 0.0
        
        mean = sum(self.motion_deltas) / len(self.motion_deltas)
        variance = sum((x - mean) ** 2 for x in self.motion_deltas) / len(self.motion_deltas)
        
        return float(variance ** 0.5)
