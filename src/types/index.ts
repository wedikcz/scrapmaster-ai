/**
 * ScrapMaster AI - Core Type Definitions
 * Production-ready TypeScript interfaces for hardware analysis and project matching
 */

// ============= INDUSTRIAL ANALYSIS SCHEMA =============

export interface MotionProfile {
  accelerationX: number; // m/s²
  accelerationY: number;
  accelerationZ: number;
  velocityMagnitude: number; // m/s
  rotationalVelocity: number; // rad/s
  smoothness: number; // 0-100 quality factor
}

export interface LikelyFault {
  id: string;
  severity: 'CRITICAL' | 'HIGH' | 'MEDIUM' | 'LOW';
  description: string;
  probability: number; // 0-1 confidence
  affectedComponent: string;
  detectedAt: Date;
}

export interface RepairStep {
  sequence: number;
  title: string;
  description: string;
  estimatedTime: number; // minutes
  requiredTools: string[];
  safetyPrecautions: string[];
  difficulty: 'BEGINNER' | 'INTERMEDIATE' | 'ADVANCED';
}

export interface RepurposeOption {
  id: string;
  name: string;
  description: string;
  requiredComponents: string[];
  estimatedValue: number; // USD
  marketDemand: 'HIGH' | 'MEDIUM' | 'LOW';
  complexity: number; // 0-100
}

export interface SafetyWarning {
  id: string;
  level: 'CRITICAL' | 'WARNING' | 'INFO';
  message: string;
  applicableTo: string[]; // component names
  mitigation: string;
}

export interface IndustrialAnalysisResult {
  timestamp: Date;
  sessionId: string;
  motionProfile: MotionProfile;
  likelyFaults: LikelyFault[];
  repairSteps: RepairStep[];
  repurposeOptions: RepurposeOption[];
  safetyWarnings: SafetyWarning[];
  confidence: number; // 0-1
  analysisMethod: 'VIDEO' | 'SENSOR' | 'HYBRID';
}

// ============= HARDWARE INVENTORY SCHEMA =============

export type ComponentCategory =
  | 'MCU'
  | 'ESP32'
  | 'MOTORS'
  | 'SENSORS'
  | 'RELAYS'
  | 'POWER'
  | 'CONNECTORS'
  | 'DISPLAYS'
  | 'COMMUNICATION'
  | 'STORAGE'
  | 'ACTUATORS'
  | 'PROTECTION'
  | 'PASSIVE'
  | 'TOOLS';

export interface InventoryItem {
  id: string;
  category: ComponentCategory;
  name: string;
  quantity: number;
  specifications?: Record<string, string | number>;
  condition: 'NEW' | 'WORKING' | 'FAULTY';
  purchaseDate?: Date;
}

export interface Inventory {
  userId: string;
  items: InventoryItem[];
  lastUpdated: Date;
}

// ============= PROJECT RECIPE SCHEMA =============

export interface RecipeRequirement {
  category: ComponentCategory;
  name: string;
  quantity: number;
  specification?: string;
}

export interface ProjectRecipe {
  id: string;
  name: string;
  description: string;
  difficulty: 'BEGINNER' | 'INTERMEDIATE' | 'ADVANCED';
  estimatedBuildTime: number; // minutes
  requirements: RecipeRequirement[];
  steps: RepairStep[];
  documentation: string; // URL or markdown
  tags: string[];
  thumbnail?: string;
}

export interface ProjectBuildability {
  recipeId: string;
  recipeName: string;
  isBuildable: boolean;
  missingComponents: RecipeRequirement[];
  matchPercentage: number; // 0-100
}

// ============= USER PROJECT STATE =============

export interface UserProject {
  id: string;
  userId: string;
  recipeId: string;
  recipeName: string;
  status: 'PLANNED' | 'IN_PROGRESS' | 'COMPLETED' | 'PAUSED';
  startDate?: Date;
  completionDate?: Date;
  steps: RepairStep[];
  notes: string;
  createdAt: Date;
  updatedAt: Date;
}

// ============= WEBSERIAL TERMINAL =============

export interface SerialPort {
  name: string;
  baudRate: number;
  dataBits: 8 | 7;
  stopBits: 1 | 2;
  parity: 'none' | 'even' | 'odd';
}

export type LogLevel = 'RX' | 'TX' | 'SYS' | 'ERR';

export interface TerminalLog {
  id: string;
  timestamp: Date;
  level: LogLevel;
  message: string;
  color: string;
}

export interface TerminalState {
  isConnected: boolean;
  selectedPort: SerialPort | null;
  logs: TerminalLog[];
  inputBuffer: string;
}

// ============= API RESPONSES =============

export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: {
    code: string;
    message: string;
  };
  timestamp: Date;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  pageSize: number;
  hasMore: boolean;
}
