'use client';

import { useEffect, useState } from 'react';

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? 'http://localhost:8000';

export default function InventoryPage() {
  const [items, setItems] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [form, setForm] = useState({
    name: '',
    category: 'gearbox',
    source: 'salvage yard',
    condition: 'good',
    estimated_value: '120',
    notes: '',
  });

  const loadItems = async () => {
    setLoading(true);
    try {
      const res = await fetch(`${API_URL}/api/v1/scrap/items`);
      const data = await res.json();
      setItems(data);
    } catch {
      setItems([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadItems();
  }, []);

  const submitItem = async () => {
    const payload = {
      ...form,
      estimated_value: Number(form.estimated_value),
    };

    const res = await fetch(`${API_URL}/api/v1/scrap/items`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });

    if (res.ok) {
      setForm({ name: '', category: 'gearbox', source: 'salvage yard', condition: 'good', estimated_value: '120', notes: '' });
      await loadItems();
    }
  };

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
          <div className="card p-5"><div className="text-sm text-slate-400">Value estimate</div><div className="mt-3 text-3xl font-bold">€{items.reduce((sum, item) => sum + (Number(item.estimated_value) || 0), 0).toFixed(0)}</div></div>
        </section>

        <section className="grid gap-6 lg:grid-cols-[0.9fr_1.1fr]">
          <div className="card p-6">
            <h2 className="mb-4 text-xl font-semibold">Add new item</h2>
            <div className="space-y-3">
              <input value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} className="w-full rounded-lg border border-slate-700 bg-slate-950 p-3 text-white" placeholder="Item name" />
              <div className="grid gap-3 md:grid-cols-2">
                <select value={form.category} onChange={(e) => setForm({ ...form, category: e.target.value })} className="rounded-lg border border-slate-700 bg-slate-950 p-3 text-white">
                  <option value="gearbox">Gearbox</option>
                  <option value="motor">Motor</option>
                  <option value="pump">Pump</option>
                  <option value="switch">Switch</option>
                  <option value="misc">Misc</option>
                </select>
                <input value={form.source} onChange={(e) => setForm({ ...form, source: e.target.value })} className="rounded-lg border border-slate-700 bg-slate-950 p-3 text-white" placeholder="Source" />
              </div>
              <div className="grid gap-3 md:grid-cols-2">
                <select value={form.condition} onChange={(e) => setForm({ ...form, condition: e.target.value })} className="rounded-lg border border-slate-700 bg-slate-950 p-3 text-white">
                  <option value="excellent">Excellent</option>
                  <option value="good">Good</option>
                  <option value="fair">Fair</option>
                  <option value="damaged">Damaged</option>
                </select>
                <input type="number" value={form.estimated_value} onChange={(e) => setForm({ ...form, estimated_value: e.target.value })} className="rounded-lg border border-slate-700 bg-slate-950 p-3 text-white" placeholder="Estimated value" />
              </div>
              <textarea value={form.notes} onChange={(e) => setForm({ ...form, notes: e.target.value })} rows={4} className="w-full rounded-lg border border-slate-700 bg-slate-950 p-3 text-white" placeholder="Notes" />
              <button onClick={submitItem} className="w-full rounded-lg bg-teal-500 px-4 py-3 font-semibold text-slate-950">Save item</button>
            </div>
          </div>

          <div className="card p-6">
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
                        <td className="px-4 py-3">€{Number(item.estimated_value || 0)}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </div>
        </section>
      </div>
    </main>
  );
}
