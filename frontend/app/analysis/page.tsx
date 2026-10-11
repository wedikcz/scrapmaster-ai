'use client';

import { useEffect, useState } from 'react';
import { AlertCircle, CheckCircle, Loader } from 'lucide-react';

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? 'http://localhost:8000';

type Toast = { id: string; message: string; type: 'success' | 'error' | 'info' };

export default function AnalysisPage() {
  const [deviceName, setDeviceName] = useState('salvaged gearbox');
  const [notes, setNotes] = useState('High wear, noisy movement, suspicious alignment drift.');
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [toasts, setToasts] = useState<Toast[]>([]);

  const addToast = (message: string, type: 'success' | 'error' | 'info') => {
    const id = Date.now().toString();
    setToasts((prev) => [...prev, { id, message, type }]);
    setTimeout(() => setToasts((prev) => prev.filter((t) => t.id !== id)), 3000);
  };

  async function handleSubmit() {
    if (!deviceName.trim()) {
      addToast('Please enter a device name', 'error');
      return;
    }

    setLoading(true);
    setResult(null);
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
      addToast('Analysis complete', 'success');
    } catch (error) {
      addToast('Analysis failed - backend unavailable', 'error');
      setResult({
        device_name: deviceName,
        mechanism_summary: 'Backend is not responding. Please ensure the FastAPI server is running on port 8000.',
        motion_profile: { dominant_motion: 'unknown', cycle_estimate: 0, confidence: 0 },
        likely_faults: ['connection unavailable'],
        repair_steps: ['check backend service', 'verify API startup on port 8000'],
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
            <h2 className="mb-4 text-xl font-semibold">Device information</h2>
            <div className="space-y-4">
              <div>
                <label className="text-xs text-slate-400">Device name</label>
                <input value={deviceName} onChange={(e) => setDeviceName(e.target.value)} className="mt-1 w-full rounded-lg border border-slate-700 bg-slate-950 p-3 text-white" placeholder="e.g., Salvaged gearbox" />
              </div>

              <div>
                <label className="text-xs text-slate-400">Observation notes</label>
                <textarea value={notes} onChange={(e) => setNotes(e.target.value)} rows={8} className="mt-1 w-full rounded-lg border border-slate-700 bg-slate-950 p-3 text-white" placeholder="Describe the condition, wear patterns, operation characteristics..." />
              </div>

              <button onClick={handleSubmit} disabled={loading} className="w-full rounded-lg bg-teal-500 px-4 py-3 font-semibold text-slate-950 hover:bg-teal-400 disabled:opacity-50 flex items-center justify-center gap-2">
                {loading ? (
                  <>
                    <Loader className="h-5 w-5 animate-spin" />
                    <span>Analyzing...</span>
                  </>
                ) : (
                  'Run analysis'
                )}
              </button>
            </div>
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
                  <div className="text-slate-400">Mechanism summary</div>
                  <p className="mt-1 text-slate-200">{result.mechanism_summary}</p>
                </div>
                <div className="grid gap-3 md:grid-cols-2">
                  <div className="rounded-xl bg-slate-950/70 p-4">
                    <div className="text-slate-400">Dominant motion</div>
                    <div className="mt-2 font-semibold text-teal-300">{result.motion_profile?.dominant_motion ?? 'unknown'}</div>
                  </div>
                  <div className="rounded-xl bg-slate-950/70 p-4">
                    <div className="text-slate-400">Confidence</div>
                    <div className="mt-2 font-semibold text-teal-300">{(result.confidence ?? result.motion_profile?.confidence ?? 0).toFixed(2)}</div>
                  </div>
                </div>
                {result.likely_faults && result.likely_faults.length > 0 && (
                  <div>
                    <div className="text-slate-400">Likely faults</div>
                    <ul className="mt-2 list-disc pl-5 space-y-1">
                      {result.likely_faults.map((fault: string) => <li key={fault}>{fault}</li>)}
                    </ul>
                  </div>
                )}
                {result.repair_steps && result.repair_steps.length > 0 && (
                  <div>
                    <div className="text-slate-400">Repair steps</div>
                    <ol className="mt-2 list-decimal pl-5 space-y-1">
                      {result.repair_steps.map((step: string, idx: number) => <li key={idx}>{step}</li>)}
                    </ol>
                  </div>
                )}
                {result.repurpose_options && result.repurpose_options.length > 0 && (
                  <div>
                    <div className="text-slate-400">Repurpose options</div>
                    <ul className="mt-2 list-disc pl-5 space-y-1">
                      {result.repurpose_options.map((option: string) => <li key={option}>{option}</li>)}
                    </ul>
                  </div>
                )}
              </div>
            ) : (
              <div className="text-center py-8 text-slate-400">
                <p>No analysis run yet.</p>
                <p className="mt-1 text-sm">Enter device information and click "Run analysis" to start.</p>
              </div>
            )}
          </div>
        </section>
      </div>

      {/* Toast notifications */}
      <div className="fixed bottom-6 right-6 space-y-2">
        {toasts.map((toast) => (
          <div key={toast.id} className={`flex items-center gap-3 rounded-lg px-4 py-3 text-white shadow-lg ${
            toast.type === 'success' ? 'bg-emerald-600' :
            toast.type === 'error' ? 'bg-red-600' :
            'bg-blue-600'
          }`}>
            {toast.type === 'success' && <CheckCircle className="h-5 w-5" />}
            {toast.type === 'error' && <AlertCircle className="h-5 w-5" />}
            <span>{toast.message}</span>
          </div>
        ))}
      </div>
    </main>
  );
}
