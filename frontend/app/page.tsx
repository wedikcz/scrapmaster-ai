import { Activity, AlertTriangle, Box, Download, Eye, ShieldCheck, Zap } from 'lucide-react';

const metrics = [
  { label: 'Active devices', value: '184', icon: Box },
  { label: 'Motion analyses', value: '32', icon: Activity },
  { label: 'Safety alerts', value: '08', icon: AlertTriangle },
  { label: 'Exports', value: '19', icon: Download },
];

const logs = [
  { title: 'Gearbox motion inference', status: 'Complete', detail: 'Reciprocating motion detected with 82% confidence.' },
  { title: 'Battery pack review', status: 'Review', detail: 'Potential residual charge flagged for isolation.' },
  { title: 'Motor repurpose plan', status: 'Queued', detail: 'Awaiting repair guide generation.' },
];

export default function HomePage() {
  return (
    <main className="min-h-screen bg-slate-950 p-6 text-slate-100 md:p-10">
      <div className="mx-auto max-w-7xl space-y-8">
        <header className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
          <div>
            <p className="text-sm uppercase tracking-[0.2em] text-teal-300">ScrapMaster Unified</p>
            <h1 className="mt-2 text-3xl font-bold md:text-5xl">Reverse engineering for salvage value</h1>
          </div>
          <a
            href="/analysis"
            className="rounded-xl bg-teal-500 px-5 py-3 font-semibold text-slate-950 transition hover:bg-teal-400"
          >
            New analysis run
          </a>
        </header>

        <section className="grid gap-4 md:grid-cols-4">
          {metrics.map(({ label, value, icon: Icon }) => (
            <div key={label} className="card p-5">
              <div className="mb-3 flex items-center justify-between text-sm text-slate-400">
                <span>{label}</span>
                <Icon className="h-4 w-4 text-teal-300" />
              </div>
              <div className="metric">{value}</div>
            </div>
          ))}
        </section>

        <section className="grid gap-6 lg:grid-cols-[1.3fr_0.7fr]">
          <div className="card p-6">
            <div className="mb-5 flex items-center justify-between">
              <div>
                <p className="text-sm uppercase tracking-[0.2em] text-slate-400">Analysis</p>
                <h2 className="mt-2 text-2xl font-semibold">Mechanism overview</h2>
              </div>
              <Eye className="h-6 w-6 text-teal-300" />
            </div>

            <div className="mb-6 rounded-2xl border border-dashed border-slate-700 bg-slate-950/80 p-6">
              <div className="flex h-52 items-center justify-center rounded-xl border border-slate-800 bg-slate-900 text-sm text-slate-400">
                Video preview / motion overlay area
              </div>
            </div>

            <div className="space-y-4">
              <div>
                <p className="text-sm text-slate-400">Mechanism summary</p>
                <p className="mt-1 text-lg text-slate-100">
                  The mechanism likely converts alternating motion into a cyclic output via a cam-and-follower system,
                  indicating wear at the contact interface and mild lubrication loss.
                </p>
              </div>
              <div className="grid gap-3 md:grid-cols-2">
                <div className="rounded-xl bg-slate-950/80 p-4">
                  <p className="text-sm text-slate-400">Motion profile</p>
                  <p className="mt-2 font-semibold text-teal-300">Reciprocating</p>
                </div>
                <div className="rounded-xl bg-slate-950/80 p-4">
                  <p className="text-sm text-slate-400">Confidence</p>
                  <p className="mt-2 font-semibold text-teal-300">82%</p>
                </div>
              </div>
            </div>
          </div>

          <aside className="space-y-6">
            <div className="card p-5">
              <div className="mb-4 flex items-center justify-between">
                <h3 className="text-lg font-semibold">Safety posture</h3>
                <ShieldCheck className="h-5 w-5 text-emerald-400" />
              </div>
              <ul className="space-y-3 text-sm text-slate-300">
                <li>• Isolate energy sources before testing.</li>
                <li>• Respect high-voltage accumulators and stored charge.</li>
                <li>• Wear eye protection around moving contact parts.</li>
              </ul>
            </div>

            <div className="card p-5">
              <div className="mb-4 flex items-center justify-between">
                <h3 className="text-lg font-semibold">Smart actions</h3>
                <Zap className="h-5 w-5 text-amber-400" />
              </div>
              <div className="space-y-2 text-sm text-slate-300">
                <button className="block w-full rounded-lg bg-slate-800 p-3 text-left hover:bg-slate-700">Generate repair guide</button>
                <button className="block w-full rounded-lg bg-slate-800 p-3 text-left hover:bg-slate-700">Create schematic draft</button>
                <button className="block w-full rounded-lg bg-slate-800 p-3 text-left hover:bg-slate-700">Export analysis log</button>
              </div>
            </div>
          </aside>
        </section>

        <section className="grid gap-6 lg:grid-cols-[0.9fr_1.1fr]">
          <div className="card p-6">
            <h3 className="mb-4 text-xl font-semibold">Recommended actions</h3>
            <ol className="space-y-3 text-sm text-slate-300">
              <li>1. Inspect the follower path for wear and debris.</li>
              <li>2. Lubricate all mechanical pivots before cycling the system.</li>
              <li>3. Check for bearing play and shaft alignment.</li>
              <li>4. Consider repurposing as a low-force actuator or feed mechanism.</li>
            </ol>
          </div>

          <div className="card p-6">
            <h3 className="mb-4 text-xl font-semibold">Operational logs</h3>
            <div className="space-y-4">
              {logs.map((item) => (
                <div key={item.title} className="rounded-xl border border-slate-800 bg-slate-950/80 p-4">
                  <div className="flex items-center justify-between gap-3">
                    <p className="font-medium text-white">{item.title}</p>
                    <span className="rounded-full bg-slate-800 px-2 py-1 text-xs text-teal-300">{item.status}</span>
                  </div>
                  <p className="mt-2 text-sm text-slate-400">{item.detail}</p>
                </div>
              ))}
            </div>
          </div>
        </section>
      </div>
    </main>
  );
}
