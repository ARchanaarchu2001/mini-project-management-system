"use client";

import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";

export default function AppShell({
  title,
  description,
  children
}: {
  title: string;
  description: string;
  children: React.ReactNode;
}) {
  const pathname = usePathname();
  const router = useRouter();

  const logout = () => {
    window.localStorage.removeItem("token");
    router.replace("/login");
  };

  return (
    <main className="page-shell">
      <nav className="nav">
        <Link href="/projects" aria-current={pathname === "/projects" ? "page" : undefined}>
          Projects
        </Link>
        <Link href="/tasks" aria-current={pathname === "/tasks" ? "page" : undefined}>
          Tasks
        </Link>
        <button type="button" onClick={logout}>
          Logout
        </button>
      </nav>
      <section className="hero">
        <div>
          <div className="pill">Mini PM System</div>
          <h1>{title}</h1>
        </div>
        <p>{description}</p>
      </section>
      {children}
    </main>
  );
}
