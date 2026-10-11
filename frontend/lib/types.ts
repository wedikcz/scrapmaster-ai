export interface MotionProfile {
  dominant_motion: string;
  cycle_estimate?: number;
  confidence: number;
  sampled_frames: number;
  analysis_method?: string;
}

export interface VideoAnalysisResponse {
  device_name: string;
  mechanism_summary: string;
  motion_profile: MotionProfile;
  likely_faults: string[];
  repair_steps: string[];
  repurpose_options: string[];
  safety_warnings: string[];
  confidence: number;
}

export interface ScrapItem {
  id: number;
  name: string;
  category?: string;
  description?: string;
  quantity: number;
  status: string;
  created_at: string;
  updated_at: string;
}

export interface Project {
  id: number;
  title: string;
  description?: string;
  status: string;
  priority: string;
  created_at: string;
  updated_at: string;
}
