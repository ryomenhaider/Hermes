import type { Metadata } from "next";
import { Inter, JetBrains_Mono } from "next/font/google";
import "./globals.css";

const inter = Inter({
  variable: "--font-inter",
  subsets: ["latin"],
  display: "swap",
});

const jetbrainsMono = JetBrains_Mono({
  variable: "--font-jetbrains-mono",
  subsets: ["latin"],
  display: "swap",
});

export const metadata: Metadata = {
  title: "Hermes — Data infrastructure for the modern world",
  description:
    "Hermes is a modern data infrastructure SDK for acquiring, processing, and serving structured and unstructured data at scale — from 15+ sources.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
return (
  <html
    lang="en"
    className={`${inter.variable} ${jetbrainsMono.variable}`}
  >
    <body className="min-h-screen bg-midnight text-offwhite antialiased">
      <a href="#main-content" className="skip-to-content">
        Skip to content
      </a>
      {children}
    </body>
  </html>
);
}
