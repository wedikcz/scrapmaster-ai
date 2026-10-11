import { Activity, AlertTriangle, Cpu, Download, ShieldCheck } from "lucide-react";

const cards = [
  { label: "Motion analyses", value: "184", icon: Activity },
  { label: "Safety alerts", value: "08", icon: AlertTriangle },
  { label: "Local inference", value: "Online", icon: Cpu },
  { label: "Exports", value: "19", icon: Download },
];

export default function Page() {
  return (
    <main className="min-h-screen bg-slate-950 p-6 text-slate-100">
      <div className="mx-auto max-w-7xl space-y-8">
        <header className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
          <div>
            <p className="text-xs uppercase tracking-[0.3em] text-teal-300">ScrapMaster AI</p>
            <h1 className="mt-2 text-4xl font-bold md:text-5xl">Inverse Video Engineering</h1>
          </div>
          <button className="rounded-xl bg-teal-500 px-5 py-3 font-semibold text-slate-950 hover:bg-teal-400">
            New Analysis
          </button>
        </header>

        <section className="grid gap-4 md:grid-cols-4">
          {cards.map(({ label, value, icon: Icon }) => (
            <div key={label} className="card p-5">
              <div className="mb-3 flex items-center justify-between text-sm text-slate-400">
                <span>{label}</span>
                <Icon className="h-5 w-5 text-teal-300" />
              </div>
              <div className="metric">{value}</div>
            </div>
          ))}
        </section>

        <section className="grid gap-6 lg:grid-cols-[1.5fr_0.7fr]">
          <div className="card p-6">
            <div className="mb-4 flex items-center justify-between">
              <h2 className="text-xl font-semibold">Analysis preview</h2>
              <ShieldCheck className="h-5 w-5 text-emerald-400" />
            </div>
            <div className="flex h-64 items-center justify-center rounded-xl border border-dashed border-slate-700 bg-slate-950 text-slate-500">
              Upload salvage video clip / motion overlay preview
            </div>
          </div>

          <aside className="space-y-6">
            <div className="card p-5">
              <h3 className="mb-3 text-lg font-semibold">Safety posture</h3>
              <ul className="space-y-2 text-sm text-slate-300">
                <li>• Disconnect stored energy</li>
                <li>• Handle batteries as hazardous</li>
                <li>• Eye protection around moving parts</li>
              </ul>
            </div>

            <div className="card p-5">
              <h3 className="mb-3 text-lg font-semibold">Smart actions</h3>
              <div className="space-y-2">
                <button className="block w-full rounded-lg bg-slate-800 p-3 text-left hover:bg-slate-700">Generate repair guide</button>
                <button className="block w-full rounded-lg bg-slate-800 p-3 text-left hover:bg-slate-700">Create schematic draft</button>
                <button className="block w-full rounded-lg bg-slate-800 p-3 text-left hover:bg-slate-700">Export analysis log</button>
              </div>
            </div>
          </aside>
        </section>

        <section className="grid gap-6 lg:grid-cols-[0.9fr_1.1fr]">
          <div className="card p-6">
            <h3 className="mb-4 text-xl font-semibold">Mechanism summary</h3>
            <p className="text-slate-300">
              The mechanism likely converts oscillating motion into a cyclic output using a cam-and-follower arrangement,
              with the highest wear risk at the contact interface and pivot points.
            </p>
          </div>

          <div className="card p-6">
            <h3 className="mb-4 text-xl font-semibold">Operational log</h3>
            <div className="space-y-3">
              <div className="rounded-xl bg-slate-950 p-3 text-sm text-slate-300">Gearbox motion inference complete</div>
              <div className="rounded-xl bg-slate-950 p-3 text-sm text-slate-300">Battery pack review flagged</div>
              <div className="rounded-xl bg-slate-950 p-3 text-sm text-slate-300">Motor reuse plan queued</div>
            </div>
          </div>
        </section>
      </div>
    </main>
  );
}
