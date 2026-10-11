'use client';

import { useEffect, useState } from 'react';
import { AlertCircle, CheckCircle, Loader } from 'lucide-react';

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? 'http://localhost:8000';

type Toast = { id: string; message: string; type: 'success' | 'error' | 'info' };

export default function InventoryPage() {
  const [items, setItems] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [toasts, setToasts] = useState<Toast[]>([]);
  const [form, setForm] = useState({
    name: '',
    category: 'gearbox',
    source: 'salvage yard',
    condition: 'good',
    estimated_value: '120',
    notes: '',
  });

  const addToast = (message: string, type: 'success' | 'error' | 'info') => {
    const id = Date.now().toString();
    setToasts((prev) => [...prev, { id, message, type }]);
    setTimeout(() => setToasts((prev) => prev.filter((t) => t.id !== id)), 3000);
  };

  const loadItems = async () => {
    setLoading(true);
    try {
      const res = await fetch(`${API_URL}/api/v1/scrap/items`);
      if (!res.ok) throw new Error('Failed to load items');
      const data = await res.json();
      setItems(data);
    } catch (error) {
      addToast('Failed to load scrap items', 'error');
      setItems([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadItems();
  }, []);

  const submitItem = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!form.name.trim()) {
      addToast('Please enter an item name', 'error');
      return;
    }

    setSubmitting(true);
    try {
      const payload = {
        ...form,
        estimated_value: Number(form.estimated_value),
      };

      const res = await fetch(`${API_URL}/api/v1/scrap/items`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });

      if (!res.ok) throw new Error('Failed to create item');

      addToast(`Added "${form.name}" to inventory`, 'success');
      setForm({ name: '', category: 'gearbox', source: 'salvage yard', condition: 'good', estimated_value: '120', notes: '' });
      await loadItems();
    } catch (error) {
      addToast('Failed to save item', 'error');
    } finally {
      setSubmitting(false);
    }
  };

  const totalValue = items.reduce((sum, item) => sum + (Number(item.estimated_value) || 0), 0);

  return (
    <main className="min-h-screen bg-slate-950 p-6 text-slate-100 md:p-10">
      <div className="mx-auto max-w-6xl space-y-6">
        <header className="flex items-center justify-between">
          <div>
            <p className="text-sm uppercase tracking-[0.2em] text-teal-300">Inventory</p>
            <h1 className="mt-2 text-3xl font-bold">Scrap records</h1>
          </div>
          <a href="/analysis" className="rounded-lg bg-teal-500 px-4 py-2 font-semibold text-slate-950 hover:bg-teal-400">
            Analyze device
          </a>
        </header>

        <section className="grid gap-4 md:grid-cols-3">
          <div className="card p-5">
            <div className="text-sm text-slate-400">Tracked parts</div>
            <div className="mt-3 text-3xl font-bold text-teal-300">{items.length}</div>
          </div>
          <div className="card p-5">
            <div className="text-sm text-slate-400">Avg. condition</div>
            <div className="mt-3 text-3xl font-bold text-teal-300">{items.length ? 'B+' : '—'}</div>
          </div>
          <div className="card p-5">
            <div className="text-sm text-slate-400">Total value</div>
            <div className="mt-3 text-3xl font-bold text-emerald-400">€{totalValue.toFixed(0)}</div>
          </div>
        </section>

        <section className="grid gap-6 lg:grid-cols-[0.9fr_1.1fr]">
          <div className="card p-6">
            <h2 className="mb-4 text-xl font-semibold">Add new item</h2>
            <form onSubmit={submitItem} className="space-y-3">
              <div>
                <label className="text-xs text-slate-400">Item name</label>
                <input value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} className="mt-1 w-full rounded-lg border border-slate-700 bg-slate-950 p-3 text-white" placeholder="e.g., Salvaged gearbox" />
              </div>
              <div className="grid gap-3 md:grid-cols-2">
                <div>
                  <label className="text-xs text-slate-400">Category</label>
                  <select value={form.category} onChange={(e) => setForm({ ...form, category: e.target.value })} className="mt-1 w-full rounded-lg border border-slate-700 bg-slate-950 p-3 text-white">
                    <option value="gearbox">Gearbox</option>
                    <option value="motor">Motor</option>
                    <option value="pump">Pump</option>
                    <option value="switch">Switch</option>
                    <option value="misc">Misc</option>
                  </select>
                </div>
                <div>
                  <label className="text-xs text-slate-400">Source</label>
                  <input value={form.source} onChange={(e) => setForm({ ...form, source: e.target.value })} className="mt-1 w-full rounded-lg border border-slate-700 bg-slate-950 p-3 text-white" placeholder="e.g., Salvage yard" />
                </div>
              </div>
              <div className="grid gap-3 md:grid-cols-2">
                <div>
                  <label className="text-xs text-slate-400">Condition</label>
                  <select value={form.condition} onChange={(e) => setForm({ ...form, condition: e.target.value })} className="mt-1 w-full rounded-lg border border-slate-700 bg-slate-950 p-3 text-white">
                    <option value="excellent">Excellent</option>
                    <option value="good">Good</option>
                    <option value="fair">Fair</option>
                    <option value="damaged">Damaged</option>
                  </select>
                </div>
                <div>
                  <label className="text-xs text-slate-400">Estimated value (€)</label>
                  <input type="number" value={form.estimated_value} onChange={(e) => setForm({ ...form, estimated_value: e.target.value })} className="mt-1 w-full rounded-lg border border-slate-700 bg-slate-950 p-3 text-white" />
                </div>
              </div>
              <div>
                <label className="text-xs text-slate-400">Notes</label>
                <textarea value={form.notes} onChange={(e) => setForm({ ...form, notes: e.target.value })} rows={3} className="mt-1 w-full rounded-lg border border-slate-700 bg-slate-950 p-3 text-white" placeholder="Condition notes, wear patterns, etc." />
              </div>
              <button type="submit" disabled={submitting} className="w-full rounded-lg bg-teal-500 px-4 py-3 font-semibold text-slate-950 hover:bg-teal-400 disabled:opacity-50">
                {submitting ? 'Saving...' : 'Save item'}
              </button>
            </form>
          </div>

          <div className="card p-6">
            <h2 className="mb-4 text-xl font-semibold">Items in inventory</h2>
            {loading ? (
              <div className="flex items-center justify-center gap-2 py-8 text-slate-400">
                <Loader className="h-5 w-5 animate-spin" />
                <span>Loading items...</span>
              </div>
            ) : items.length === 0 ? (
              <div className="rounded-xl border border-dashed border-slate-700 bg-slate-950/50 p-8 text-center text-slate-400">
                <p>No scrap items yet.</p>
                <p className="mt-1 text-sm">Add your first item on the left.</p>
              </div>
            ) : (
              <div className="space-y-2 max-h-96 overflow-y-auto">
                {items.map((item) => (
                  <a key={item.id} href={`/scrap/${item.id}`} className="block rounded-lg border border-slate-800 bg-slate-950/40 p-4 hover:bg-slate-900/60 transition">
                    <div className="flex items-center justify-between gap-2">
                      <div className="flex-1">
                        <p className="font-semibold text-white">{item.name}</p>
                        <p className="text-xs text-slate-400">{item.category} • {item.condition}</p>
                      </div>
                      <div className="text-right">
                        <p className="font-semibold text-teal-300">€{Number(item.estimated_value || 0)}</p>
                      </div>
                    </div>
                  </a>
                ))}
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
