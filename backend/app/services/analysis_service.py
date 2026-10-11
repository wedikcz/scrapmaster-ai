from __future__ import annotations

from typing import Any

from app.schemas.video import VideoAnalysisRequest, VideoAnalysisResponse
from app.services.motion_analysis import extract_motion_profile, infer_mechanism


class MotionAnalysisService:
    def analyze(self, request: VideoAnalysisRequest) -> VideoAnalysisResponse:
        motion_profile = extract_motion_profile("sample-video.mp4", frame_limit=request.frame_count or 30)
        mechanism = infer_mechanism(request.device_name, motion_profile)

        return VideoAnalysisResponse(
            device_name=request.device_name,
            mechanism_summary=mechanism["mechanism_summary"],
            motion_profile={
                "dominant_motion": mechanism["motion_profile"]["dominant_motion"],
                "cycle_estimate": mechanism["motion_profile"].get("cycle_estimate"),
                "confidence": mechanism["motion_profile"].get("confidence", 0.0),
                "sampled_frames": mechanism["motion_profile"].get("sampled_frames", 0),
            },
            likely_faults=mechanism["likely_faults"],
            repair_steps=mechanism["repair_steps"],
            repurpose_options=mechanism["repurpose_options"],
            safety_warnings=mechanism["safety_warnings"],
            confidence=mechanism["confidence"],
        )
