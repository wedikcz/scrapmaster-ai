'use client';

import { useEffect, useState } from 'react';

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? 'http://localhost:8000';

export default function AnalysisPage() {
  const [deviceName, setDeviceName] = useState('salvaged gearbox');
  const [notes, setNotes] = useState('High wear, noisy movement, suspicious alignment drift.');
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  async function handleSubmit() {
    setLoading(true);
    try {
      const res = await fetch(`${API_URL}/api/v1/videos/analyze`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ device_name: deviceName, notes }),
      });

      if (!res.ok) {
        throw new Error('Analysis failed');
      }

      const data = await res.json();
      setResult(data);
    } catch {
      setResult({
        device_name: deviceName,
        mechanism_summary: 'The backend is not responding. This is a demo fallback state.',
        motion_profile: { dominant_motion: 'unknown', cycle_estimate: 0, confidence: 0 },
        likely_faults: ['connection unavailable', 'offline analysis'],
        repair_steps: ['check backend service', 'verify API startup'],
        repurpose_options: ['manual inspection workflow'],
      });
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="min-h-screen bg-slate-950 p-6 text-slate-100 md:p-10">
      <div className="mx-auto max-w-6xl space-y-6">
        <header>
          <p className="text-sm uppercase tracking-[0.2em] text-teal-300">Analysis</p>
          <h1 className="mt-2 text-3xl font-bold">Reverse engineering run</h1>
        </header>

        <section className="grid gap-6 lg:grid-cols-[0.9fr_1.1fr]">
          <div className="card p-6">
            <label className="mb-3 block text-sm text-slate-300">Device name</label>
            <input value={deviceName} onChange={(e) => setDeviceName(e.target.value)} className="mb-4 w-full rounded-lg border border-slate-700 bg-slate-950 p-3 text-white" />

            <label className="mb-3 block text-sm text-slate-300">Notes</label>
            <textarea value={notes} onChange={(e) => setNotes(e.target.value)} rows={7} className="w-full rounded-lg border border-slate-700 bg-slate-950 p-3 text-white" />

            <button onClick={handleSubmit} className="mt-5 w-full rounded-lg bg-teal-500 px-4 py-3 font-semibold text-slate-950">
              {loading ? 'Analyzing…' : 'Run analysis'}
            </button>
          </div>

          <div className="card p-6">
            <h2 className="mb-4 text-xl font-semibold">Analysis result</h2>
            {result ? (
              <div className="space-y-5 text-sm text-slate-300">
                <div>
                  <div className="text-slate-400">Device</div>
                  <div className="mt-1 text-xl font-semibold text-white">{result.device_name}</div>
                </div>
                <div>
                  <div className="text-slate-400">Summary</div>
                  <p className="mt-1 text-slate-200">{result.mechanism_summary}</p>
                </div>
                <div className="grid gap-3 md:grid-cols-2">
                  <div className="rounded-xl bg-slate-950/70 p-4">
                    <div className="text-slate-400">Motion</div>
                    <div className="mt-2 font-semibold text-teal-300">{result.motion_profile?.dominant_motion ?? 'unknown'}</div>
                  </div>
                  <div className="rounded-xl bg-slate-950/70 p-4">
                    <div className="text-slate-400">Confidence</div>
                    <div className="mt-2 font-semibold text-teal-300">{result.confidence ?? result.motion_profile?.confidence ?? '—'}</div>
                  </div>
                </div>
                <div>
                  <div className="text-slate-400">Likely faults</div>
                  <ul className="mt-2 list-disc pl-5">
                    {(result.likely_faults ?? []).map((fault: string) => <li key={fault}>{fault}</li>)}
                  </ul>
                </div>
                <div>
                  <div className="text-slate-400">Repair steps</div>
                  <ul className="mt-2 list-disc pl-5">
                    {(result.repair_steps ?? []).map((step: string) => <li key={step}>{step}</li>)}
                  </ul>
                </div>
              </div>
            ) : (
              <div className="text-slate-400">No results yet. Run a device analysis.</div>
            )}
          </div>
        </section>
      </div>
    </main>
  );
}
