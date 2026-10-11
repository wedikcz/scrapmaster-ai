def analyze_video(device_name: str, notes: str = "", video_url: str | None = None) -> dict:
    normalized_name = (device_name or "salvaged device").strip()
    note_text = (notes or "").lower()

    if "gear" in normalized_name.lower() or "gearbox" in normalized_name.lower():
        mechanism_summary = "The mechanism likely converts alternating motion into cyclic output via a gear train and cam-like engagement pattern."
        motion_profile = {"dominant_motion": "reciprocating", "cycle_estimate": 0.85, "confidence": 0.82}
        likely_faults = ["worn gear teeth", "bearing play", "misaligned follower track"]
        repair_steps = [
            "Inspect the follower path for wear and debris.",
            "Check lubrication and shaft alignment.",
            "Verify no binding occurs under load."
        ]
        repurpose_options = ["low-force actuator", "manual feed mechanism", "drive linkage output"]
    elif "motor" in normalized_name.lower() or "pump" in normalized_name.lower():
        mechanism_summary = "The unit likely uses rotary conversion and frictional load management with partial torque loss under repeated cycling."
        motion_profile = {"dominant_motion": "rotary", "cycle_estimate": 1.1, "confidence": 0.76}
        likely_faults = ["brush wear", "worn bearing", "heat-induced resistance"]
        repair_steps = [
            "Inspect the commutator and brush path.",
            "Check for bearing looseness or overheating.",
            "Measure current draw under no-load conditions."
        ]
        repurpose_options = ["small pump drive", "rotary actuator", "generator prime mover"]
    else:
        mechanism_summary = "The mechanism appears to convert intermittent motion into a repeated mechanical action with a moderate contact wear profile."
        motion_profile = {"dominant_motion": "oscillatory", "cycle_estimate": 0.7, "confidence": 0.7}
        likely_faults = ["contact wear", "alignment drift", "lubrication loss"]
        repair_steps = [
            "Inspect all moving contact interfaces.",
            "Check the alignment and spacing of linkages.",
            "Verify safe operation before deep cycling."
        ]
        repurpose_options = ["manual drive assist", "light-duty actuator", "prototype motion stage"]

    if "battery" in note_text or "voltage" in note_text:
        likely_faults.insert(0, "residual charge risk")
        repair_steps.insert(0, "Isolate all power sources and verify zero-energy state before handling.")

    if video_url:
        mechanism_summary += f" Source footage was included from {video_url}."

    return {
        "device_name": normalized_name,
        "mechanism_summary": mechanism_summary,
        "motion_profile": motion_profile,
        "likely_faults": likely_faults,
        "repair_steps": repair_steps,
        "repurpose_options": repurpose_options,
        "confidence": motion_profile["confidence"],
    }
