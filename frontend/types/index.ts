export type UserRole = "admin" | "developer";

export type TaskStatus = "todo" | "in_progress" | "done";

export interface User {
  id: number;
  name: string;
  email: string;
  role: UserRole;
}

export interface Project {
  id: number;
  name: string;
  description: string | null;
  created_by: number;
}

export interface Task {
  id: number;
  title: string;
  description: string | null;
  status: TaskStatus;
  project_id: number;
  assigned_to: number | null;
  due_date: string | null;
}

export interface TaskListResponse {
  items: Task[];
  page: number;
  limit: number;
  total: number;
}
