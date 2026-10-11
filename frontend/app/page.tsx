'use client';

import { useEffect, useState } from 'react';
import { Loader } from 'lucide-react';

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? 'http://localhost:8000';

export default function HomePage() {
  const [stats, setStats] = useState({ items: 0, projects: 0, total_value: 0 });
  const [loading, setLoading] = useState(true);
  const [apiStatus, setApiStatus] = useState<'online' | 'offline'>('offline');

  useEffect(() => {
    const loadStats = async () => {
      try {
        // Check API status
        const healthRes = await fetch(`${API_URL}/`);
        setApiStatus(healthRes.ok ? 'online' : 'offline');

        // Load inventory data
        const itemsRes = await fetch(`${API_URL}/api/v1/scrap/items`);
        const items = itemsRes.ok ? await itemsRes.json() : [];

        // Load projects data
        const projectsRes = await fetch(`${API_URL}/api/v1/projects`);
        const projects = projectsRes.ok ? await projectsRes.json() : [];

        const total_value = items.reduce((sum: number, item: any) => sum + (Number(item.estimated_value) || 0), 0);

        setStats({
          items: items.length,
          projects: projects.length,
          total_value,
        });
      } finally {
        setLoading(false);
      }
    };

    loadStats();
    const interval = setInterval(loadStats, 3000); // Refresh every 3 seconds
    return () => clearInterval(interval);
  }, []);

  return (
    <main className="min-h-screen bg-slate-950 p-6 text-slate-100 md:p-10">
      <div className="mx-auto max-w-7xl space-y-8">
        <header className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
          <div>
            <p className="text-sm uppercase tracking-[0.22em] text-teal-300">ScrapMaster Unified</p>
            <h1 className="mt-2 text-3xl font-bold md:text-5xl">Reverse engineering for salvage value</h1>
          </div>
          <div className="flex items-center gap-2">
            <div className={`h-3 w-3 rounded-full ${ apiStatus === 'online' ? 'bg-emerald-500 animate-pulse' : 'bg-red-500' }`} />
            <span className="text-sm">{apiStatus === 'online' ? 'API Online' : 'API Offline'}</span>
          </div>
        </header>

        <section className="grid gap-4 md:grid-cols-4">
          <div className="card p-5">
            <div className="mb-3 flex items-center justify-between text-sm text-slate-400">
              <span>Scrap items</span>
              {loading && <Loader className="h-4 w-4 animate-spin" />}
            </div>
            <div className="metric text-teal-300">{stats.items}</div>
          </div>
          <div className="card p-5">
            <div className="mb-3 flex items-center justify-between text-sm text-slate-400">
              <span>Active projects</span>
              {loading && <Loader className="h-4 w-4 animate-spin" />}
            </div>
            <div className="metric text-teal-300">{stats.projects}</div>
          </div>
          <div className="card p-5">
            <div className="mb-3 flex items-center justify-between text-sm text-slate-400">
              <span>Total value</span>
              {loading && <Loader className="h-4 w-4 animate-spin" />}
            </div>
            <div className="metric text-emerald-400">€{stats.total_value.toFixed(0)}</div>
          </div>
          <div className="card p-5">
            <div className="mb-3 flex items-center justify-between text-sm text-slate-400">
              <span>AI confidence</span>
            </div>
            <div className="metric text-teal-300">0.82</div>
          </div>
        </section>

        <section className="grid gap-6 lg:grid-cols-[1.3fr_0.7fr]">
          <div className="card p-6">
            <div className="mb-5 flex items-center justify-between">
              <div>
                <p className="text-sm uppercase tracking-[0.2em] text-slate-400">Latest features</p>
                <h2 className="mt-2 text-2xl font-semibold">Quick access</h2>
              </div>
            </div>

            <div className="grid gap-3 md:grid-cols-2">
              <a href="/inventory" className="rounded-xl border border-slate-800 bg-slate-950/70 p-5 hover:border-slate-700 hover:bg-slate-900 transition">
                <div className="text-sm text-slate-400">Manage inventory</div>
                <div className="mt-2 text-lg font-semibold text-teal-300">Scrap Items</div>
              </a>
              <a href="/projects" className="rounded-xl border border-slate-800 bg-slate-950/70 p-5 hover:border-slate-700 hover:bg-slate-900 transition">
                <div className="text-sm text-slate-400">Track projects</div>
                <div className="mt-2 text-lg font-semibold text-teal-300">Projects</div>
              </a>
              <a href="/analysis" className="rounded-xl border border-slate-800 bg-slate-950/70 p-5 hover:border-slate-700 hover:bg-slate-900 transition">
                <div className="text-sm text-slate-400">Run AI analysis</div>
                <div className="mt-2 text-lg font-semibold text-teal-300">Analysis</div>
              </a>
              <a href="/dashboard" className="rounded-xl border border-slate-800 bg-slate-950/70 p-5 hover:border-slate-700 hover:bg-slate-900 transition">
                <div className="text-sm text-slate-400">Ops monitoring</div>
                <div className="mt-2 text-lg font-semibold text-teal-300">Dashboard</div>
              </a>
            </div>
          </div>

          <aside className="space-y-6">
            <div className="card p-5">
              <div className="mb-4 flex items-center justify-between">
                <h3 className="text-lg font-semibold">Status</h3>
              </div>
              <div className="space-y-3 text-sm text-slate-300">
                <div className="flex items-center gap-2">
                  <div className="h-2 w-2 rounded-full bg-emerald-500" />
                  <span>Backend: {apiStatus === 'online' ? 'Connected' : 'Disconnected'}</span>
                </div>
                <div className="flex items-center gap-2">
                  <div className="h-2 w-2 rounded-full bg-emerald-500" />
                  <span>Database: Active</span>
                </div>
                <div className="flex items-center gap-2">
                  <div className="h-2 w-2 rounded-full bg-teal-500" />
                  <span>AI: Local mode</span>
                </div>
              </div>
            </div>

            <div className="card p-5">
              <h3 className="mb-4 text-lg font-semibold">Getting started</h3>
              <ol className="space-y-3 text-sm text-slate-300">
                <li>
                  <span className="font-semibold text-teal-300">1.</span> Add scrap items
                </li>
                <li>
                  <span className="font-semibold text-teal-300">2.</span> Create projects
                </li>
                <li>
                  <span className="font-semibold text-teal-300">3.</span> Run analysis
                </li>
              </ol>
            </div>
          </aside>
        </section>
      </div>
    </main>
  );
}
