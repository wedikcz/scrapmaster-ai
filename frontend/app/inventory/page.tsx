'use client';

import { useEffect, useState } from 'react';

export default function InventoryPage() {
  const [items, setItems] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`${process.env.NEXT_PUBLIC_API_URL ?? 'http://localhost:8000'}/api/v1/scrap/items`)
      .then((res) => res.json())
      .then((data) => setItems(data))
      .catch(() => setItems([]))
      .finally(() => setLoading(false));
  }, []);

  return (
    <main className="min-h-screen bg-slate-950 p-6 text-slate-100 md:p-10">
      <div className="mx-auto max-w-6xl space-y-6">
        <header className="flex items-center justify-between">
          <div>
            <p className="text-sm uppercase tracking-[0.2em] text-teal-300">Inventory</p>
            <h1 className="mt-2 text-3xl font-bold">Scrap records</h1>
          </div>
          <a href="/analysis" className="rounded-lg bg-teal-500 px-4 py-2 font-semibold text-slate-950">Analyze device</a>
        </header>

        <section className="grid gap-4 md:grid-cols-3">
          <div className="card p-5"><div className="text-sm text-slate-400">Tracked parts</div><div className="mt-3 text-3xl font-bold">{items.length}</div></div>
          <div className="card p-5"><div className="text-sm text-slate-400">Avg. condition</div><div className="mt-3 text-3xl font-bold">{items.length ? 'B+' : '—'}</div></div>
          <div className="card p-5"><div className="text-sm text-slate-400">Value estimate</div><div className="mt-3 text-3xl font-bold">{items.reduce((sum, item) => sum + (Number(item.estimated_value) || 0), 0).toFixed(0)}</div></div>
        </section>

        <section className="card p-6">
          <h2 className="mb-4 text-xl font-semibold">Items</h2>
          {loading ? (
            <div className="text-slate-400">Loading…</div>
          ) : items.length === 0 ? (
            <div className="text-slate-400">No scrap items yet.</div>
          ) : (
            <div className="overflow-hidden rounded-xl border border-slate-800">
              <table className="min-w-full text-left text-sm">
                <thead className="bg-slate-900 text-slate-300">
                  <tr>
                    <th className="px-4 py-3">Name</th>
                    <th className="px-4 py-3">Category</th>
                    <th className="px-4 py-3">Condition</th>
                    <th className="px-4 py-3">Value</th>
                  </tr>
                </thead>
                <tbody>
                  {items.map((item) => (
                    <tr key={item.id} className="border-t border-slate-800 bg-slate-950/40">
                      <td className="px-4 py-3">{item.name}</td>
                      <td className="px-4 py-3">{item.category}</td>
                      <td className="px-4 py-3">{item.condition}</td>
                      <td className="px-4 py-3">€{item.estimated_value}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </section>
      </div>
    </main>
  );
}
