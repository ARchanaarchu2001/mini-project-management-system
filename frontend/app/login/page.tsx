"use client";

import { FormEvent, useEffect, useState } from "react";
import { useRouter } from "next/navigation";

import api from "@/lib/api";

export default function LoginPage() {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const token = window.localStorage.getItem("token");
    if (token) {
      router.replace("/projects");
    }
  }, [router]);

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setLoading(true);
    setError("");

    try {
      const response = await api.post("/auth/login", { email, password });
      window.localStorage.setItem("token", response.data.access_token);
      router.replace("/projects");
    } catch (err: any) {
      setError(err?.response?.data?.detail || "Unable to sign in");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="login-shell">
      <section className="login-panel">
        <article className="login-hero">
          <div>
            <div className="pill">Workspace Access</div>
            <h1>Manage delivery from a cleaner, calmer control room.</h1>
            <p>
              Sign in to review projects, filter active work, and create new tasks without leaving
              the same focused workspace.
            </p>
          </div>
          <div className="login-points">
            <div className="login-point">
              <strong>Projects</strong>
              <span className="muted">See every initiative in one place.</span>
            </div>
            <div className="login-point">
              <strong>Tasks</strong>
              <span className="muted">Track status, owners, and due dates.</span>
            </div>
            <div className="login-point">
              <strong>JWT Auth</strong>
              <span className="muted">Secure access backed by your FastAPI API.</span>
            </div>
          </div>
        </article>

        <section className="card login-card">
          <div className="section-intro">
            <div className="pill">Sign In</div>
            <h2>Welcome back</h2>
            <p className="muted">Use your registered account to enter the project workspace.</p>
          </div>
          <form className="stack" onSubmit={handleSubmit}>
            <div className="field-group">
              <label htmlFor="email">Email</label>
              <input
                id="email"
                type="email"
                value={email}
                onChange={(event) => setEmail(event.target.value)}
                required
              />
            </div>
            <div className="field-group">
              <label htmlFor="password">Password</label>
              <input
                id="password"
                type="password"
                value={password}
                onChange={(event) => setPassword(event.target.value)}
                required
              />
            </div>
            {error ? <p className="muted">{error}</p> : null}
            <div className="button-row">
              <button type="submit" className="button primary" disabled={loading}>
                {loading ? "Signing in..." : "Login"}
              </button>
            </div>
          </form>
        </section>
      </section>
    </main>
  );
}
