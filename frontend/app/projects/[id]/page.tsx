'use client';

import { useEffect, useState } from 'react';

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? 'http://localhost:8000';

export default function ProjectDetailPage({ params }: { params: { id: string } }) {
  const [project, setProject] = useState<any>(null);
  const [projects, setProjects] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const load = async () => {
      try {
        const res = await fetch(`${API_URL}/api/v1/projects`);
        const data = await res.json();
        setProjects(data);
        const selected = data.find((item: any) => String(item.id) === params.id) ?? null;
        setProject(selected);
      } catch {
        setProjects([]);
        setProject(null);
      } finally {
        setLoading(false);
      }
    };

    load();
  }, [params.id]);

  if (loading) return <main className="min-h-screen bg-slate-950 p-6 text-slate-100 md:p-10">Loading…</main>;
  if (!project) return <main className="min-h-screen bg-slate-950 p-6 text-slate-100 md:p-10">Project not found.</main>;

  return (
    <main className="min-h-screen bg-slate-950 p-6 text-slate-100 md:p-10">
      <div className="mx-auto max-w-6xl space-y-6">
        <header className="flex items-center justify-between">
          <div>
            <p className="text-sm uppercase tracking-[0.2em] text-teal-300">Project</p>
            <h1 className="mt-2 text-3xl font-bold">{project.title}</h1>
          </div>
          <span className="rounded-full border border-teal-500/30 bg-teal-500/10 px-3 py-1 text-xs text-teal-300">{project.status}</span>
        </header>

        <section className="grid gap-6 lg:grid-cols-[1.1fr_0.9fr]">
          <div className="card p-6">
            <h2 className="mb-3 text-xl font-semibold">Overview</h2>
            <p className="text-slate-300">{project.description ?? 'No description available.'}</p>
            <div className="mt-6 grid gap-4 md:grid-cols-3">
              <div className="rounded-xl bg-slate-950/70 p-4"><div className="text-sm text-slate-400">Parts</div><div className="mt-2 text-2xl font-bold">{projects.length}</div></div>
              <div className="rounded-xl bg-slate-950/70 p-4"><div className="text-sm text-slate-400">AI confidence</div><div className="mt-2 text-2xl font-bold text-teal-300">0.82</div></div>
              <div className="rounded-xl bg-slate-950/70 p-4"><div className="text-sm text-slate-400">Safety</div><div className="mt-2 text-2xl font-bold text-emerald-400">Stable</div></div>
            </div>
          </div>

          <div className="card p-6">
            <h2 className="mb-4 text-xl font-semibold">Recommended next actions</h2>
            <ul className="space-y-3 text-sm text-slate-300">
              <li>• Review part condition and salvage yield</li>
              <li>• Run analysis on the next capture set</li>
              <li>• Check if any energy sources remain live</li>
              <li>• Generate repair and repurpose guidance</li>
            </ul>
          </div>
        </section>
      </div>
    </main>
  );
}
