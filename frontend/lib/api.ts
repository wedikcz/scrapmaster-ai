export const dynamic = 'force-dynamic';

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? 'http://localhost:8000';

export type ScrapItem = {
  id: number;
  name: string;
  category: string;
  source: string;
  condition: string;
  estimated_value: number;
  notes?: string | null;
};

export async function fetchScrapItems(): Promise<ScrapItem[]> {
  const res = await fetch(`${API_URL}/api/v1/scrap/items`, { cache: 'no-store' });
  if (!res.ok) {
    throw new Error('Failed to load scrap items');
  }
  return res.json();
}

export async function fetchProjects(): Promise<Array<{ id: number; title: string; status: string; description?: string | null }>> {
  const res = await fetch(`${API_URL}/api/v1/projects`, { cache: 'no-store' });
  if (!res.ok) {
    throw new Error('Failed to load projects');
  }
  return res.json();
}

export async function analyzeDevice(payload: { device_name: string; notes?: string; video_url?: string }) {
  const res = await fetch(`${API_URL}/api/v1/videos/analyze`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });

  if (!res.ok) {
    throw new Error('Analysis request failed');
  }

  return res.json();
}
