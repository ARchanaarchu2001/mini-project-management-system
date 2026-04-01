"use client";

import { FormEvent, useMemo, useState } from "react";

import api from "@/lib/api";
import { Project, TaskStatus, User } from "@/types";

const defaultForm = {
  title: "",
  description: "",
  status: "todo" as TaskStatus,
  project_id: "",
  assigned_to: "",
  due_date: ""
};

export default function CreateTaskModal({
  isOpen,
  onClose,
  onCreated,
  projects,
  users
}: {
  isOpen: boolean;
  onClose: () => void;
  onCreated: () => void;
  projects: Project[];
  users: User[];
}) {
  const [form, setForm] = useState(defaultForm);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");

  const canSubmit = useMemo(() => {
    return form.title.trim() && form.project_id;
  }, [form.project_id, form.title]);

  if (!isOpen) {
    return null;
  }

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setSubmitting(true);
    setError("");

    try {
      await api.post("/tasks", {
        title: form.title,
        description: form.description || null,
        status: form.status,
        project_id: Number(form.project_id),
        assigned_to: form.assigned_to ? Number(form.assigned_to) : null,
        due_date: form.due_date || null
      });
      setForm(defaultForm);
      onCreated();
      onClose();
    } catch (err: any) {
      setError(err?.response?.data?.detail || "Unable to create task");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="modal-backdrop">
      <div className="card modal">
        <div className="split">
          <div>
            <h2>Create Task</h2>
            <p className="muted">Add a task and assign it to a project or teammate.</p>
          </div>
          <button type="button" className="button secondary" onClick={onClose}>
            Close
          </button>
        </div>
        <form className="stack" onSubmit={handleSubmit}>
          <div className="field-group">
            <label htmlFor="title">Title</label>
            <input
              id="title"
              value={form.title}
              onChange={(event) => setForm({ ...form, title: event.target.value })}
              required
            />
          </div>
          <div className="field-group">
            <label htmlFor="description">Description</label>
            <textarea
              id="description"
              rows={4}
              value={form.description}
              onChange={(event) => setForm({ ...form, description: event.target.value })}
            />
          </div>
          <div className="grid two">
            <div className="field-group">
              <label htmlFor="status">Status</label>
              <select
                id="status"
                value={form.status}
                onChange={(event) =>
                  setForm({ ...form, status: event.target.value as TaskStatus })
                }
              >
                <option value="todo">To do</option>
                <option value="in_progress">In progress</option>
                <option value="done">Done</option>
              </select>
            </div>
            <div className="field-group">
              <label htmlFor="due_date">Due date</label>
              <input
                id="due_date"
                type="date"
                value={form.due_date}
                onChange={(event) => setForm({ ...form, due_date: event.target.value })}
              />
            </div>
          </div>
          <div className="grid two">
            <div className="field-group">
              <label htmlFor="project">Project</label>
              <select
                id="project"
                value={form.project_id}
                onChange={(event) => setForm({ ...form, project_id: event.target.value })}
                required
              >
                <option value="">Select project</option>
                {projects.map((project) => (
                  <option key={project.id} value={project.id}>
                    {project.name}
                  </option>
                ))}
              </select>
            </div>
            <div className="field-group">
              <label htmlFor="assigned_to">Assigned to</label>
              <select
                id="assigned_to"
                value={form.assigned_to}
                onChange={(event) => setForm({ ...form, assigned_to: event.target.value })}
              >
                <option value="">Unassigned</option>
                {users.map((user) => (
                  <option key={user.id} value={user.id}>
                    {user.name} ({user.role})
                  </option>
                ))}
              </select>
            </div>
          </div>
          {error ? <p className="muted">{error}</p> : null}
          <div className="button-row">
            <button type="submit" className="button primary" disabled={!canSubmit || submitting}>
              {submitting ? "Creating..." : "Create task"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
