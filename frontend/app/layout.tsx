import "./globals.css";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Mini Project Management System",
  description: "Minimal project and task management frontend"
};

export default function RootLayout({
  children
}: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
