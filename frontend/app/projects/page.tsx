'use client';

import { useEffect, useState } from 'react';
import { AlertCircle, CheckCircle, Loader } from 'lucide-react';

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? 'http://localhost:8000';

type Toast = { id: string; message: string; type: 'success' | 'error' | 'info' };

export default function ProjectsPage() {
  const [projects, setProjects] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [toasts, setToasts] = useState<Toast[]>([]);
  const [form, setForm] = useState({ title: '', description: '', status: 'active' });

  const addToast = (message: string, type: 'success' | 'error' | 'info') => {
    const id = Date.now().toString();
    setToasts((prev) => [...prev, { id, message, type }]);
    setTimeout(() => setToasts((prev) => prev.filter((t) => t.id !== id)), 3000);
  };

  const loadProjects = async () => {
    setLoading(true);
    try {
      const res = await fetch(`${API_URL}/api/v1/projects`);
      if (!res.ok) throw new Error('Failed to load projects');
      const data = await res.json();
      setProjects(data);
    } catch (error) {
      addToast('Failed to load projects', 'error');
      setProjects([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadProjects();
    // Refresh every 5 seconds for real-time updates
    const interval = setInterval(loadProjects, 5000);
    return () => clearInterval(interval);
  }, []);

  const submitProject = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!form.title.trim()) {
      addToast('Please enter a project title', 'error');
      return;
    }

    setSubmitting(true);
    try {
      const res = await fetch(`${API_URL}/api/v1/projects`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(form),
      });

      if (!res.ok) throw new Error('Failed to create project');

      addToast(`Created project "${form.title}"`, 'success');
      setForm({ title: '', description: '', status: 'active' });
      await loadProjects();
    } catch (error) {
      addToast('Failed to save project', 'error');
    } finally {
      setSubmitting(false);
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
            <form onSubmit={submitProject} className="space-y-3">
              <div>
                <label className="text-xs text-slate-400">Project title</label>
                <input value={form.title} onChange={(e) => setForm({ ...form, title: e.target.value })} className="mt-1 w-full rounded-lg border border-slate-700 bg-slate-950 p-3 text-white" placeholder="e.g., Gearbox restoration" />
              </div>
              <div>
                <label className="text-xs text-slate-400">Status</label>
                <select value={form.status} onChange={(e) => setForm({ ...form, status: e.target.value })} className="mt-1 w-full rounded-lg border border-slate-700 bg-slate-950 p-3 text-white">
                  <option value="active">Active</option>
                  <option value="review">Review</option>
                  <option value="queued">Queued</option>
                  <option value="completed">Completed</option>
                </select>
              </div>
              <div>
                <label className="text-xs text-slate-400">Description</label>
                <textarea value={form.description} onChange={(e) => setForm({ ...form, description: e.target.value })} rows={5} className="mt-1 w-full rounded-lg border border-slate-700 bg-slate-950 p-3 text-white" placeholder="Project details and objectives..." />
              </div>
              <button type="submit" disabled={submitting} className="w-full rounded-lg bg-teal-500 px-4 py-3 font-semibold text-slate-950 hover:bg-teal-400 disabled:opacity-50">
                {submitting ? 'Creating...' : 'Add project'}
              </button>
            </form>
          </div>

          <div className="card p-6">
            <h2 className="mb-4 text-xl font-semibold">Active projects ({projects.length})</h2>
            {loading ? (
              <div className="flex items-center justify-center gap-2 py-8 text-slate-400">
                <Loader className="h-5 w-5 animate-spin" />
                <span>Loading projects...</span>
              </div>
            ) : projects.length === 0 ? (
              <div className="rounded-xl border border-dashed border-slate-700 bg-slate-950/50 p-8 text-center text-slate-400">
                <p>No projects yet.</p>
                <p className="mt-1 text-sm">Create your first project on the left.</p>
              </div>
            ) : (
              <div className="space-y-3 max-h-96 overflow-y-auto">
                {projects.map((project) => (
                  <a key={project.id} href={`/projects/${project.id}`} className="block rounded-lg border border-slate-800 bg-slate-950/40 p-4 hover:bg-slate-900/60 transition">
                    <div className="flex items-start justify-between gap-3">
                      <div className="flex-1">
                        <p className="font-semibold text-white">{project.title}</p>
                        <p className="mt-1 text-sm text-slate-400 line-clamp-1">{project.description || 'No description'}</p>
                      </div>
                      <span className={`whitespace-nowrap rounded-full border px-2 py-1 text-xs font-semibold ${
                        project.status === 'active' ? 'border-teal-500/30 bg-teal-500/10 text-teal-300' :
                        project.status === 'review' ? 'border-amber-500/30 bg-amber-500/10 text-amber-300' :
                        project.status === 'completed' ? 'border-emerald-500/30 bg-emerald-500/10 text-emerald-300' :
                        'border-slate-700 bg-slate-800 text-slate-300'
                      }`}>{project.status}</span>
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
