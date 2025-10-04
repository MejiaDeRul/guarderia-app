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

export default function Calendar() {
  const { token, role } = useAuth();
  const [groupId, setGroupId] = useState("");
  const [childId, setChildId] = useState("");
  const [events, setEvents] = useState<EventItem[]>([]);
  const [loading, setLoading] = useState(false);

  async function reload() {
    setLoading(true);
    try {
      let data: EventItem[] = [];
      if (groupId) data = await api(`/events/by-class/${groupId}`, token);
      else if (childId) data = await api(`/events/by-child/${childId}`, token);
      else data = await api(`/events`, token);
      setEvents(
        data.sort((a, b) => new Date(a.start_at).getTime() - new Date(b.start_at).getTime())
      );
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    reload();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <Layout>
      <h1>Calendario</h1>

      {/* Filtros */}
      <div style={{ display: "flex", gap: 8, marginTop: 12, marginBottom: 8 }}>
        <input
          placeholder="ID grupo (opcional)"
          value={groupId}
          onChange={(e) => setGroupId(e.target.value)}
          style={{ border: "1px solid #ddd", borderRadius: 8, padding: "6px 10px" }}
        />
        <input
          placeholder="ID niño (opcional)"
          value={childId}
          onChange={(e) => setChildId(e.target.value)}
          style={{ border: "1px solid #ddd", borderRadius: 8, padding: "6px 10px" }}
        />
        <button
          onClick={reload}
          style={{
            padding: "6px 10px",
            borderRadius: 8,
            background: "#0f172a",
            color: "#fff",
          }}
        >
          Buscar
        </button>
      </div>

      {/* Crear evento (solo teacher) */}
      {role === "teacher" && <CreateEvent onCreated={reload} token={token} />}

      {/* Lista */}
      {loading ? (
        <p>Cargando…</p>
      ) : events.length === 0 ? (
        <p className="text-sm" style={{ color: "#6b7280" }}>
          No hay eventos para el filtro seleccionado.
        </p>
      ) : (
        <ul style={{ display: "grid", gap: 8, marginTop: 8 }}>
          {events.map((ev) => (
            <li key={ev.id} style={{ border: "1px solid #eee", borderRadius: 12, padding: 12 }}>
              <div style={{ fontWeight: 600 }}>{ev.title}</div>
              <div style={{ fontSize: 12, color: "#6b7280" }}>
                {new Date(ev.start_at).toLocaleString()} — {new Date(ev.end_at).toLocaleString()}
              </div>
              {ev.description && <div style={{ marginTop: 6 }}>{ev.description}</div>}
              <div style={{ fontSize: 12, color: "#6b7280", marginTop: 4 }}>
                {ev.class_group_id ? `Grupo #${ev.class_group_id}` : ""}
                {ev.child_id ? `  Niño #${ev.child_id}` : ""}
              </div>
            </li>
          ))}
        </ul>
      )}
    </Layout>
  );
}

function CreateEvent({ token, onCreated }: { token: string | null; onCreated: () => void }) {
  const [title, setTitle] = useState("");
  const [desc, setDesc] = useState("");
  const [start, setStart] = useState(""); // datetime-local
  const [end, setEnd] = useState("");
  const [groupId, setGroupId] = useState("");
  const [childId, setChildId] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [saving, setSaving] = useState(false);

  function toIsoZ(local: string) {
    // Convierte un input datetime-local a ISO UTC (Z)
    if (!local) return "";
    const d = new Date(local);
    return new Date(d.getTime() - d.getTimezoneOffset() * 60000).toISOString();
  }

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);
    if (!title || !start || !end) {
      setError("Título, inicio y fin son obligatorios.");
      return;
    }
    setSaving(true);
    try {
      await api(
        "/events",
        token,
        {
          method: "POST",
          body: JSON.stringify({
            title,
            description: desc || null,
            start_at: toIsoZ(start),
            end_at: toIsoZ(end),
            class_group_id: groupId ? Number(groupId) : null,
            child_id: childId ? Number(childId) : null,
          }),
        }
      );
      setTitle(""); setDesc(""); setStart(""); setEnd(""); setGroupId(""); setChildId("");
      onCreated();
    } catch (err: any) {
      setError(err?.message || "Error creando evento");
    } finally {
      setSaving(false);
    }
  }

  return (
    <form onSubmit={submit} style={{ display: "grid", gap: 8, marginTop: 12, padding: 12, border: "1px solid #eee", borderRadius: 12 }}>
      <strong>Crear evento (profesor)</strong>
      <input placeholder="Título" value={title} onChange={(e) => setTitle(e.target.value)}
        style={{ border: "1px solid #ddd", borderRadius: 8, padding: "6px 10px" }} />
      <textarea placeholder="Descripción (opcional)" value={desc} onChange={(e) => setDesc(e.target.value)}
        style={{ border: "1px solid #ddd", borderRadius: 8, padding: "6px 10px", minHeight: 64 }} />
      <div style={{ display: "flex", gap: 8 }}>
        <div style={{ display: "grid" }}>
          <label style={{ fontSize: 12, color: "#6b7280" }}>Inicio</label>
          <input type="datetime-local" value={start} onChange={(e) => setStart(e.target.value)}
            style={{ border: "1px solid #ddd", borderRadius: 8, padding: "6px 10px" }} />
        </div>
        <div style={{ display: "grid" }}>
          <label style={{ fontSize: 12, color: "#6b7280" }}>Fin</label>
          <input type="datetime-local" value={end} onChange={(e) => setEnd(e.target.value)}
            style={{ border: "1px solid #ddd", borderRadius: 8, padding: "6px 10px" }} />
        </div>
      </div>
      <div style={{ display: "flex", gap: 8 }}>
        <input placeholder="ID grupo (opcional)" value={groupId} onChange={(e) => setGroupId(e.target.value)}
          style={{ border: "1px solid #ddd", borderRadius: 8, padding: "6px 10px" }} />
        <input placeholder="ID niño (opcional)" value={childId} onChange={(e) => setChildId(e.target.value)}
          style={{ border: "1px solid #ddd", borderRadius: 8, padding: "6px 10px" }} />
      </div>
      {error && <div style={{ color: "#b00020", fontSize: 12 }}>{error}</div>}
      <button disabled={saving}
        style={{ padding: "8px 12px", borderRadius: 8, background: "#0f172a", color: "#fff", opacity: saving ? 0.7 : 1 }}>
        {saving ? "Creando…" : "Crear evento"}
      </button>
    </form>
  );
}
