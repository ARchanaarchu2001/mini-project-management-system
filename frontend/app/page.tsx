"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";

export default function HomePage() {
  const router = useRouter();

  useEffect(() => {
    const token = window.localStorage.getItem("token");
    router.replace(token ? "/projects" : "/login");
  }, [router]);

  return null;
}
