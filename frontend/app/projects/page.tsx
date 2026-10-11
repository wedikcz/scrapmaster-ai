'use client';

import { useEffect, useState } from 'react';

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? 'http://localhost:8000';

export default function ProjectsPage() {
  const [projects, setProjects] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [form, setForm] = useState({ title: '', description: '', status: 'active' });

  const loadProjects = async () => {
    setLoading(true);
    try {
      const res = await fetch(`${API_URL}/api/v1/projects`);
      const data = await res.json();
      setProjects(data);
    } catch {
      setProjects([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadProjects();
  }, []);

  const submitProject = async () => {
    const res = await fetch(`${API_URL}/api/v1/projects`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(form),
    });

    if (res.ok) {
      setForm({ title: '', description: '', status: 'active' });
      await loadProjects();
    }
  };

  return (
    <main className="min-h-screen bg-slate-950 p-6 text-slate-100 md:p-10">
      <div className="mx-auto max-w-6xl space-y-6">
        <header>
          <p className="text-sm uppercase tracking-[0.2em] text-teal-300">Projects</p>
          <h1 className="mt-2 text-3xl font-bold">Project board</h1>
        </header>

        <section className="grid gap-6 lg:grid-cols-[0.8fr_1.2fr]">
          <div className="card p-6">
            <h2 className="mb-4 text-xl font-semibold">Create project</h2>
            <div className="space-y-3">
              <input value={form.title} onChange={(e) => setForm({ ...form, title: e.target.value })} className="w-full rounded-lg border border-slate-700 bg-slate-950 p-3 text-white" placeholder="Project title" />
              <select value={form.status} onChange={(e) => setForm({ ...form, status: e.target.value })} className="w-full rounded-lg border border-slate-700 bg-slate-950 p-3 text-white">
                <option value="active">Active</option>
                <option value="review">Review</option>
                <option value="queued">Queued</option>
                <option value="completed">Completed</option>
              </select>
              <textarea value={form.description} onChange={(e) => setForm({ ...form, description: e.target.value })} rows={5} className="w-full rounded-lg border border-slate-700 bg-slate-950 p-3 text-white" placeholder="Project summary" />
              <button onClick={submitProject} className="w-full rounded-lg bg-teal-500 px-4 py-3 font-semibold text-slate-950">Add project</button>
            </div>
          </div>

          <div className="card p-6">
            <h2 className="mb-4 text-xl font-semibold">Active projects</h2>
            {loading ? (
              <div className="text-slate-400">Loading projects…</div>
            ) : projects.length === 0 ? (
              <div className="text-slate-400">No projects yet.</div>
            ) : (
              <div className="space-y-4">
                {projects.map((project) => (
                  <div key={project.id} className="rounded-xl border border-slate-800 bg-slate-950/70 p-4">
                    <div className="flex items-center justify-between gap-3">
                      <a href={`/projects/${project.id}`} className="text-lg font-semibold text-white hover:text-teal-300">{project.title}</a>
                      <span className="rounded-full border border-teal-500/30 bg-teal-500/10 px-2 py-1 text-xs text-teal-300">{project.status}</span>
                    </div>
                    <p className="mt-2 text-sm text-slate-300">{project.description ?? 'No description provided.'}</p>
                  </div>
                ))}
              </div>
            )}
          </div>
        </section>
      </div>
    </main>
  );
}
