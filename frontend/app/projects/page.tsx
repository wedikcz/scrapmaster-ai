'use client';

import { useEffect, useState } from 'react';

export default function ProjectsPage() {
  const [projects, setProjects] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`${process.env.NEXT_PUBLIC_API_URL ?? 'http://localhost:8000'}/api/v1/projects`)
      .then((res) => res.json())
      .then((data) => setProjects(data))
      .catch(() => setProjects([]))
      .finally(() => setLoading(false));
  }, []);

  return (
    <main className="min-h-screen bg-slate-950 p-6 text-slate-100 md:p-10">
      <div className="mx-auto max-w-6xl space-y-6">
        <header>
          <p className="text-sm uppercase tracking-[0.2em] text-teal-300">Projects</p>
          <h1 className="mt-2 text-3xl font-bold">Project board</h1>
        </header>

        {loading ? (
          <div className="card p-6 text-slate-400">Loading projects…</div>
        ) : projects.length === 0 ? (
          <div className="card p-6 text-slate-400">No projects yet.</div>
        ) : (
          <div className="grid gap-4 md:grid-cols-2">
            {projects.map((project) => (
              <div key={project.id} className="card p-5">
                <div className="mb-2 flex items-center justify-between">
                  <h2 className="text-xl font-semibold">{project.title}</h2>
                  <span className="rounded-full border border-teal-500/30 bg-teal-500/10 px-2 py-1 text-xs text-teal-300">{project.status}</span>
                </div>
                <p className="text-sm text-slate-300">{project.description ?? 'No description provided.'}</p>
              </div>
            ))}
          </div>
        )}
      </div>
    </main>
  );
}
