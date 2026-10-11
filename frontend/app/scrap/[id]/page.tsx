'use client';

import { useEffect, useState } from 'react';

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? 'http://localhost:8000';

export default function ScrapItemDetailPage({ params }: { params: { id: string } }) {
  const [item, setItem] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const load = async () => {
      try {
        const res = await fetch(`${API_URL}/api/v1/scrap/items`);
        const data = await res.json();
        const found = data.find((entry: any) => String(entry.id) === params.id) ?? null;
        setItem(found);
      } catch {
        setItem(null);
      } finally {
        setLoading(false);
      }
    };

    load();
  }, [params.id]);

  if (loading) return <main className="min-h-screen bg-slate-950 p-6 text-slate-100 md:p-10">Loading…</main>;
  if (!item) return <main className="min-h-screen bg-slate-950 p-6 text-slate-100 md:p-10">Scrap item not found.</main>;

  return (
    <main className="min-h-screen bg-slate-950 p-6 text-slate-100 md:p-10">
      <div className="mx-auto max-w-5xl space-y-6">
        <header>
          <p className="text-sm uppercase tracking-[0.2em] text-teal-300">Item detail</p>
          <h1 className="mt-2 text-3xl font-bold">{item.name}</h1>
        </header>

        <section className="grid gap-6 lg:grid-cols-[1.1fr_0.9fr]">
          <div className="card p-6">
            <div className="grid gap-4 md:grid-cols-2">
              <div className="rounded-xl bg-slate-950/70 p-4"><div className="text-sm text-slate-400">Category</div><div className="mt-2 text-lg font-semibold">{item.category}</div></div>
              <div className="rounded-xl bg-slate-950/70 p-4"><div className="text-sm text-slate-400">Condition</div><div className="mt-2 text-lg font-semibold">{item.condition}</div></div>
              <div className="rounded-xl bg-slate-950/70 p-4"><div className="text-sm text-slate-400">Source</div><div className="mt-2 text-lg font-semibold">{item.source}</div></div>
              <div className="rounded-xl bg-slate-950/70 p-4"><div className="text-sm text-slate-400">Value</div><div className="mt-2 text-lg font-semibold">€{Number(item.estimated_value || 0)}</div></div>
            </div>

            <div className="mt-6 rounded-xl bg-slate-950/70 p-4">
              <div className="text-sm text-slate-400">Notes</div>
              <p className="mt-2 text-slate-200">{item.notes || 'No notes recorded.'}</p>
            </div>
          </div>

          <div className="card p-6">
            <h2 className="mb-4 text-xl font-semibold">Recommended actions</h2>
            <ul className="space-y-3 text-sm text-slate-300">
              <li>• Inspect the part for residual charge or wear.</li>
              <li>• Validate salvage value against project needs.</li>
              <li>• Add to a route or repair plan if suitable.</li>
              <li>• Log all safety checks before reuse.</li>
            </ul>
          </div>
        </section>
      </div>
    </main>
  );
}
