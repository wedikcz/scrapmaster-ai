import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "ScrapMaster AI",
  description: "Inverse video engineering dashboard for scrap hardware and repair workflows",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
