"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";

import AppShell from "@/components/AppShell";
import CreateTaskModal from "@/components/CreateTaskModal";
import api from "@/lib/api";
import { Project, TaskListResponse, User } from "@/types";

const initialFilters = {
  status: "",
  project_id: "",
  assigned_to: ""
};

export default function TasksPage() {
  const router = useRouter();
  const [tasks, setTasks] = useState<TaskListResponse | null>(null);
  const [projects, setProjects] = useState<Project[]>([]);
  const [users, setUsers] = useState<User[]>([]);
  const [filters, setFilters] = useState(initialFilters);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [page, setPage] = useState(1);

  const loadLookupData = async () => {
    const [projectsResponse, usersResponse] = await Promise.all([
      api.get<Project[]>("/projects"),
      api.get<User[]>("/users")
    ]);
    setProjects(projectsResponse.data);
    setUsers(usersResponse.data);
  };

  const loadTasks = async (nextPage = page) => {
    setLoading(true);
    setError("");

    try {
      const params: Record<string, string | number> = {
        page: nextPage,
        limit: 10
      };
      if (filters.status) {
        params.status = filters.status;
      }
      if (filters.project_id) {
        params.project_id = filters.project_id;
      }
      if (filters.assigned_to) {
        params.assigned_to = filters.assigned_to;
      }

      const response = await api.get<TaskListResponse>("/tasks", {
        params
      });
      setTasks(response.data);
    } catch (err: any) {
      setError(err?.response?.data?.detail || "Unable to load tasks");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    const token = window.localStorage.getItem("token");
    if (!token) {
      router.replace("/login");
      return;
    }

    const bootstrap = async () => {
      try {
        await loadLookupData();
        await loadTasks(1);
      } catch (err: any) {
        setError(err?.response?.data?.detail || "Unable to load task workspace");
        setLoading(false);
      }
    };

    void bootstrap();
  }, [router]);

  useEffect(() => {
    if (!loading && tasks) {
      void loadTasks(page);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [filters, page]);

  return (
    <AppShell
      title="Tasks"
      description="Filter tasks by status, project, or assignee, then add new ones through the modal."
    >
      <section className="card">
        <div className="toolbar">
          <div className="section-intro">
            <h2>Task Board</h2>
            <p className="muted">
              Server-side filtering and pagination are wired to the FastAPI backend.
            </p>
          </div>
          <div className="button-row">
            <button type="button" className="button secondary" onClick={() => void loadTasks(1)}>
              Refresh
            </button>
            <button type="button" className="button primary" onClick={() => setIsModalOpen(true)}>
              Create task
            </button>
          </div>
        </div>

        <div className="grid two" style={{ marginBottom: 20 }}>
          <div className="field-group">
            <label htmlFor="status_filter">Status</label>
            <select
              id="status_filter"
              value={filters.status}
              onChange={(event) => {
                setPage(1);
                setFilters({ ...filters, status: event.target.value });
              }}
            >
              <option value="">All</option>
              <option value="todo">To do</option>
              <option value="in_progress">In progress</option>
              <option value="done">Done</option>
            </select>
          </div>
          <div className="field-group">
            <label htmlFor="project_filter">Project</label>
            <select
              id="project_filter"
              value={filters.project_id}
              onChange={(event) => {
                setPage(1);
                setFilters({ ...filters, project_id: event.target.value });
              }}
            >
              <option value="">All</option>
              {projects.map((project) => (
                <option key={project.id} value={project.id}>
                  {project.name}
                </option>
              ))}
            </select>
          </div>
          <div className="field-group">
            <label htmlFor="assigned_filter">Assigned to</label>
            <select
              id="assigned_filter"
              value={filters.assigned_to}
              onChange={(event) => {
                setPage(1);
                setFilters({ ...filters, assigned_to: event.target.value });
              }}
            >
              <option value="">All</option>
              {users.map((user) => (
                <option key={user.id} value={user.id}>
                  {user.name}
                </option>
              ))}
            </select>
          </div>
        </div>

        {loading ? <p>Loading tasks...</p> : null}
        {error ? <p className="muted">{error}</p> : null}

        <div className="list">
          {tasks?.items.map((task) => (
            <article key={task.id} className="list-item">
              <div className="split">
                <div>
                  <h4>{task.title}</h4>
                  <p className="muted">{task.description || "No description provided."}</p>
                </div>
                <span className={`status ${task.status}`}>{task.status.replace("_", " ")}</span>
              </div>
              <div className="split">
                <div className="pill">Project #{task.project_id}</div>
                <div className="pill">
                  {task.assigned_to ? `Assigned to user #${task.assigned_to}` : "Unassigned"}
                </div>
                <div className="pill">{task.due_date || "No due date"}</div>
              </div>
            </article>
          ))}
        </div>

        {tasks ? (
          <div className="toolbar" style={{ marginTop: 18 }}>
            <span className="muted">
              Page {tasks.page} of {Math.max(1, Math.ceil(tasks.total / tasks.limit))}
            </span>
            <div className="button-row">
              <button
                type="button"
                className="button secondary"
                disabled={page <= 1}
                onClick={() => setPage((current) => Math.max(1, current - 1))}
              >
                Previous
              </button>
              <button
                type="button"
                className="button secondary"
                disabled={tasks.page * tasks.limit >= tasks.total}
                onClick={() => setPage((current) => current + 1)}
              >
                Next
              </button>
            </div>
          </div>
        ) : null}
      </section>

      <CreateTaskModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        onCreated={() => {
          setPage(1);
          void loadTasks(1);
        }}
        projects={projects}
        users={users}
      />
    </AppShell>
  );
}
