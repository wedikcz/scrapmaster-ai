import './globals.css';
import type { Metadata } from 'next';
import Link from 'next/link';

export const metadata: Metadata = {
  title: 'ScrapMaster Unified',
  description: 'Local-first scrap hardware recycling and inverse video engineering platform',
};

const navItems = [
  { href: '/', label: 'Dashboard' },
  { href: '/inventory', label: 'Inventory' },
  { href: '/projects', label: 'Projects' },
  { href: '/analysis', label: 'Analysis' },
  { href: '/dashboard', label: 'Ops view' },
];

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-slate-950 text-slate-100 antialiased">
        <div className="mx-auto flex min-h-screen max-w-[1700px] gap-6 p-4 md:p-6">
          <aside className="hidden w-72 shrink-0 rounded-2xl border border-slate-800 bg-slate-900/80 p-5 shadow-2xl shadow-slate-950/50 lg:block">
            <div className="mb-8">
              <p className="text-xs uppercase tracking-[0.28em] text-teal-300">ScrapMaster</p>
              <h1 className="mt-2 text-2xl font-bold text-white">Unified</h1>
            </div>

            <nav className="space-y-2">
              {navItems.map((item) => (
                <Link
                  key={item.href}
                  href={item.href}
                  className="flex items-center rounded-xl border border-transparent px-3 py-2 text-sm text-slate-300 transition hover:border-slate-700 hover:bg-slate-800 hover:text-white"
                >
                  {item.label}
                </Link>
              ))}
            </nav>

            <div className="mt-8 rounded-2xl border border-teal-500/30 bg-teal-500/10 p-4">
              <p className="text-xs uppercase tracking-[0.22em] text-teal-300">Status</p>
              <p className="mt-2 text-sm text-slate-200">Local AI mode active</p>
            </div>
          </aside>

          <main className="flex-1 overflow-hidden rounded-2xl border border-slate-800 bg-slate-950/80 shadow-2xl shadow-slate-950/40">
            {children}
          </main>
        </div>
      </body>
    </html>
  );
}
