from __future__ import annotations

from typing import Any

try:
    import cv2
    import numpy as np
except ImportError:  # pragma: no cover
    cv2 = None
    np = None


def _safe_float(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def extract_motion_profile(video_path: str, frame_limit: int = 30) -> dict[str, Any]:
    """Estimate motion characteristics with OpenCV if available, otherwise use a local fallback model."""
    if cv2 is None or np is None:
        return {
            "dominant_motion": "reciprocating",
            "cycle_estimate": 0.9,
            "confidence": 0.79,
            "sampled_frames": frame_limit,
            "fallback_mode": "local-mock-analysis",
        }

    capture = cv2.VideoCapture(video_path)
    if not capture.isOpened():
        return {
            "dominant_motion": "unknown",
            "cycle_estimate": None,
            "confidence": 0.25,
            "sampled_frames": 0,
            "fallback_mode": "video-open-failed",
        }

    frame_index = 0
    motion_scores = []
    prev_gray = None

    while True:
        success, frame = capture.read()
        if not success:
            break
        if frame_index >= frame_limit:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        if prev_gray is not None:
            diff = cv2.absdiff(prev_gray, gray)
            motion_scores.append(float(diff.mean()))
        prev_gray = gray
        frame_index += 1

    capture.release()

    avg_motion = sum(motion_scores) / len(motion_scores) if motion_scores else 0.0
    dominant_motion = "reciprocating" if avg_motion > 15 else "rotary"
    confidence = min(0.95, max(0.4, avg_motion / 100.0))

    return {
        "dominant_motion": dominant_motion,
        "cycle_estimate": round(_safe_float(avg_motion / 30.0, 0.0), 2),
        "confidence": round(confidence, 2),
        "sampled_frames": frame_index,
        "fallback_mode": "opencv-motion-estimation",
    }


def infer_mechanism(summary: str, motion_profile: dict[str, Any]) -> dict[str, Any]:
    dominant_motion = motion_profile.get("dominant_motion", "unknown")
    if dominant_motion == "reciprocating":
        mechanism_summary = (
            "The device likely converts oscillating motion into a cyclic mechanical action through a cam, lever, or link-driven pattern."
        )
        likely_faults = [
            "worn cam follower",
            "misaligned linkage",
            "lubrication loss",
        ]
        repair_steps = [
            "Inspect the linkage and follower for wear or slop.",
            "Lubricate pivots and friction points.",
            "Check that the motion path is not obstructed.",
        ]
        repurpose_options = [
            "manual actuator",
            "gearbox-driven pump",
            "motion-sensing trigger",
        ]
    else:
        mechanism_summary = (
            "The device likely relies on continuous rotary transfer with gear, belt, shaft, or friction coupling behavior."
        )
        likely_faults = [
            "damaged bearing",
            "belt slippage",
            "gear tooth wear",
        ]
        repair_steps = [
            "Inspect for bearing play and axle alignment.",
            "Check for missing or jammed tensioning components.",
            "Verify the rotational path is free of debris.",
        ]
        repurpose_options = [
            "rotary drive unit",
            "generator interface",
            "automated conveyor",
        ]

    safety_warnings = [
        "Disconnect any stored energy before handling the mechanism.",
        "Wear eye protection when testing moving parts.",
        "Assume high current or residual charge on salvaged electromechanical assemblies.",
    ]

    return {
        "device_name": summary or "salvaged mechanism",
        "mechanism_summary": mechanism_summary,
        "motion_profile": motion_profile,
        "likely_faults": likely_faults,
        "repair_steps": repair_steps,
        "repurpose_options": repurpose_options,
        "safety_warnings": safety_warnings,
        "confidence": max(0.0, min(0.99, float(motion_profile.get("confidence", 0.6)))),
    }
