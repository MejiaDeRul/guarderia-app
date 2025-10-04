import { useEffect, useState } from "react";
import Layout from "../components/Layout";
import { useAuth } from "../context/AuthContext";
import { api } from "../lib/api";

type EventItem = {
  id: number;
  title: string;
  description?: string | null;
  start_at: string;
  end_at: string;
  class_group_id?: number | null;
  child_id?: number | null;
};

export default function Activities() {
  const { token } = useAuth();
  const [events, setEvents] = useState<EventItem[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let mounted = true;
    (async () => {
      try {
        const data = await api<EventItem[]>("/events", token);
        if (!mounted) return;
        // Orden: próximas primero
        setEvents(
          [...data].sort(
            (a, b) => new Date(a.start_at).getTime() - new Date(b.start_at).getTime()
          )
        );
      } finally {
        if (mounted) setLoading(false);
      }
    })();
    return () => {
      mounted = false;
    };
  }, [token]);

  return (
    <Layout>
      <h1>Actividades</h1>
      {loading ? (
        <p>Cargando…</p>
      ) : events.length === 0 ? (
        <p className="text-sm" style={{ color: "#6b7280" }}>
          No hay actividades programadas.
        </p>
      ) : (
        <ul style={{ marginTop: 12, display: "grid", gap: 8 }}>
          {events.map((ev) => (
            <li key={ev.id} style={{ border: "1px solid #eee", borderRadius: 12, padding: 12 }}>
              <div style={{ fontWeight: 600 }}>{ev.title}</div>
              <div style={{ fontSize: 12, color: "#6b7280" }}>
                {new Date(ev.start_at).toLocaleString()} — {new Date(ev.end_at).toLocaleString()}
              </div>
              {ev.description && <div style={{ marginTop: 6 }}>{ev.description}</div>}
            </li>
          ))}
        </ul>
      )}
    </Layout>
  );
}
