import './globals.css';
import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'ScrapMaster AI',
  description: 'Local-first scrap hardware recycling and inverse video engineering platform',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
