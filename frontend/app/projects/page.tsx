"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";

import AppShell from "@/components/AppShell";
import api from "@/lib/api";
import { Project } from "@/types";

export default function ProjectsPage() {
  const router = useRouter();
  const [projects, setProjects] = useState<Project[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const token = window.localStorage.getItem("token");
    if (!token) {
      router.replace("/login");
      return;
    }

    const loadProjects = async () => {
      try {
        const response = await api.get<Project[]>("/projects");
        setProjects(response.data);
      } catch (err: any) {
        setError(err?.response?.data?.detail || "Unable to load projects");
      } finally {
        setLoading(false);
      }
    };

    void loadProjects();
  }, [router]);

  return (
    <AppShell
      title="Projects"
      description="A minimal overview of the projects currently being managed in the system."
    >
      <section className="card">
        <div className="toolbar">
          <div className="section-intro">
            <h2>Project List</h2>
            <p className="muted">
              Read-only view for the frontend. Project creation is available via API.
            </p>
          </div>
          <div className="pill">{projects.length} total</div>
        </div>
        {loading ? <p>Loading projects...</p> : null}
        {error ? <p className="muted">{error}</p> : null}
        {!loading && !projects.length ? <p className="muted">No projects available yet.</p> : null}
        <div className="list">
          {projects.map((project) => (
            <article key={project.id} className="list-item">
              <h3>{project.name}</h3>
              <p className="muted">{project.description || "No description provided."}</p>
              <div className="pill">Created by user #{project.created_by}</div>
            </article>
          ))}
        </div>
      </section>
    </AppShell>
  );
}
