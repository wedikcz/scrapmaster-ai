export default function DashboardPage() {
  return (
    <main className="min-h-screen p-6 md:p-10">
      <div className="mx-auto max-w-7xl space-y-8">
        <header className="flex flex-col gap-3 md:flex-row md:items-center md:justify-between">
          <div>
            <p className="text-sm uppercase tracking-[0.22em] text-teal-300">Ops view</p>
            <h1 className="mt-2 text-3xl font-bold text-white">Operations dashboard</h1>
          </div>
          <a href="/analysis" className="rounded-xl bg-teal-500 px-5 py-3 font-semibold text-slate-950 transition hover:bg-teal-400">
            Launch analysis
          </a>
        </header>

        <section className="grid gap-4 md:grid-cols-4">
          <div className="card p-5">
            <div className="text-sm text-slate-400">System health</div>
            <div className="mt-3 text-3xl font-bold text-emerald-400">99.2%</div>
          </div>
          <div className="card p-5">
            <div className="text-sm text-slate-400">Open projects</div>
            <div className="mt-3 text-3xl font-bold text-white">12</div>
          </div>
          <div className="card p-5">
            <div className="text-sm text-slate-400">AI confidence</div>
            <div className="mt-3 text-3xl font-bold text-teal-300">0.82</div>
          </div>
          <div className="card p-5">
            <div className="text-sm text-slate-400">Export queue</div>
            <div className="mt-3 text-3xl font-bold text-amber-300">08</div>
          </div>
        </section>

        <section className="grid gap-6 lg:grid-cols-[1.3fr_0.7fr]">
          <div className="card p-6">
            <h2 className="mb-4 text-xl font-semibold text-white">Recent runs</h2>
            <div className="space-y-4">
              {[
                ['Gearbox inference', 'Complete', '82% confidence'],
                ['Battery module review', 'Review', 'Residual charge flagged'],
                ['Motor drive repurpose', 'Queued', 'Awaiting generation'],
              ].map(([title, status, detail]) => (
                <div key={title} className="rounded-xl border border-slate-800 bg-slate-950/70 p-4">
                  <div className="flex items-center justify-between gap-3">
                    <p className="font-medium text-white">{title}</p>
                    <span className="rounded-full bg-slate-800 px-2 py-1 text-xs text-teal-300">{status}</span>
                  </div>
                  <p className="mt-2 text-sm text-slate-400">{detail}</p>
                </div>
              ))}
            </div>
          </div>

          <div className="card p-6">
            <h2 className="mb-4 text-xl font-semibold text-white">Safety checklist</h2>
            <ul className="space-y-3 text-sm text-slate-300">
              <li>• Isolate energy before test cycles</li>
              <li>• Verify no residual charge remains</li>
              <li>• Keep fasteners and guards in place</li>
              <li>• Wear eye protection during inspection</li>
            </ul>
          </div>
        </section>
      </div>
    </main>
  );
}
