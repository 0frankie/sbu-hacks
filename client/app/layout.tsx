import type { Metadata } from "next";
import LeftSidebar from "@/components/ui/left-sidebar";
import Header from "@/components/ui/header";
import { cookies } from "next/headers";

import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "The Perfect Shot",
  description: "Analyze your basketball shots",
};

export default async function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  const cookieStore = await cookies();
  const theme = cookieStore.get('theme');
  return (
    <html lang="en" data-theme={theme === undefined ? 'light' : theme?.value}>
      <body
        className={`${geistSans.variable} ${geistMono.variable} bg-background-50 text-text antialiased h-dvh`}
      >
        <div className="flex flex-col min-h-lvh h-fit">
          <Header />
          <div className="flex flex-row w-screen min-h-lvh h-fit">
            <LeftSidebar />
            <div className="w-full rounded bg-background mx-2">
              {children}
            </div>
          </div>
        </div>

      </body>
    </html>
  );
}
