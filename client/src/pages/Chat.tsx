import { useEffect, useRef, useState } from "react";
import Layout from "../components/Layout";
import { useAuth } from "../context/AuthContext";
import { api } from "../lib/api";

type Msg = {
  id: number;
  sender_id: number;
  receiver_id: number;
  child_id?: number | null;
  content: string;
  sent_at: string;
};

type UserMini = {
  id: number;
  email: string;
  full_name: string;
  role: "admin" | "teacher" | "parent";
};

export default function Chat() {
  const { token, role } = useAuth();
  const [partnerId, setPartnerId] = useState<number | null>(null);
  const [partnerName, setPartnerName] = useState("");
  const [childId, setChildId] = useState("");
  const [msgs, setMsgs] = useState<Msg[]>([]);
  const [text, setText] = useState("");
  const [loading, setLoading] = useState(false);
  const [sending, setSending] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // búsqueda por nombre
  const [q, setQ] = useState("");
  const [results, setResults] = useState<UserMini[]>([]);
  const [searching, setSearching] = useState(false);

  const listRef = useRef<HTMLDivElement | null>(null);

  async function searchByName() {
    if (!q || q.trim().length < 2) {
      setResults([]);
      return;
    }
    setSearching(true);
    setError(null);
    try {
      // /users/search usa el rol del usuario para filtrar (teacher -> parents)
      const users = await api<UserMini[]>(`/users/search?name=${encodeURIComponent(q)}`, token);
      setResults(users);
    } catch (e: any) {
      setError(e?.message || "Error buscando usuarios.");
    } finally {
      setSearching(false);
    }
  }

  function choosePartner(u: UserMini) {
    setPartnerId(u.id);
    setPartnerName(u.full_name);
    setResults([]);
  }

  async function load() {
    if (!partnerId) return;
    setLoading(true);
    setError(null);
    try {
      const data = await api<Msg[]>(`/messages/with/${partnerId}`, token);
      setMsgs(data);
    } catch (e: any) {
      setError(e?.message || "Error cargando conversación.");
    } finally {
      setLoading(false);
      requestAnimationFrame(() => {
        listRef.current?.scrollTo({ top: listRef.current.scrollHeight, behavior: "smooth" });
      });
    }
  }

  async function send() {
    if (!text.trim() || !partnerId) return;
    setSending(true);
    setError(null);
    try {
      await api(
        "/messages",
        token,
        {
          method: "POST",
          body: JSON.stringify({
            receiver_id: partnerId,
            child_id: childId ? Number(childId) : null,
            content: text.trim(),
          }),
        }
      );
      setText("");
      await load();
    } catch (e: any) {
      setError(e?.message || "No se pudo enviar el mensaje.");
    } finally {
      setSending(false);
    }
  }

  useEffect(() => {
    load();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [partnerId]);

  return (
    <Layout>
      <h1>Chats (profe ↔ padre)</h1>
      <p style={{ color: "#6b7280", fontSize: 12, marginTop: 4 }}>
        {role === "teacher"
          ? "Busca al padre por nombre y chatea."
          : "Puedes buscar al profesor por nombre (si activas la búsqueda para padres)."}
      </p>

      {/* Buscador por nombre */}
      <div style={{ display: "grid", gap: 8, marginTop: 12, marginBottom: 8 }}>
        <div style={{ display: "flex", gap: 8 }}>
          <input
            placeholder={role === "teacher" ? "Nombre del padre (mín. 2 letras)" : "Nombre del profesor"}
            value={q}
            onChange={(e) => setQ(e.target.value)}
            style={{ border: "1px solid #ddd", borderRadius: 8, padding: "6px 10px", flex: 1 }}
          />
          <button
            onClick={searchByName}
            disabled={searching || q.trim().length < 2}
            style={{ padding: "6px 10px", borderRadius: 8, background: "#0f172a", color: "#fff", opacity: searching ? 0.7 : 1 }}
          >
            {searching ? "Buscando…" : "Buscar"}
          </button>
        </div>

        {results.length > 0 && (
          <div style={{ border: "1px solid #eee", borderRadius: 12, background: "#fff", padding: 8 }}>
            {results.map((u) => (
              <button
                key={u.id}
                onClick={() => choosePartner(u)}
                style={{
                  width: "100%",
                  textAlign: "left",
                  padding: "8px 10px",
                  borderRadius: 8,
                  border: "1px solid #f1f5f9",
                  marginBottom: 6,
                  background: "#f8fafc",
                }}
              >
                <div style={{ fontWeight: 600 }}>{u.full_name}</div>
                <div style={{ fontSize: 12, color: "#6b7280" }}>{u.email} • {u.role}</div>
              </button>
            ))}
          </div>
        )}
      </div>

      {/* Destinatario seleccionado + niño opcional */}
      <div style={{ display: "flex", gap: 8, alignItems: "center", marginBottom: 8 }}>
        <div style={{ fontSize: 14, color: "#334155" }}>
          Destinatario: <strong>{partnerName || "—"}</strong>
          {partnerId ? ` (ID ${partnerId})` : ""}
        </div>
        <input
          placeholder="ID del niño (opcional)"
          value={childId}
          onChange={(e) => setChildId(e.target.value)}
          style={{ border: "1px solid #ddd", borderRadius: 8, padding: "6px 10px" }}
        />
        <button
          onClick={load}
          disabled={!partnerId}
          style={{ padding: "6px 10px", borderRadius: 8, background: "#0f172a", color: "#fff", opacity: !partnerId ? 0.6 : 1 }}
        >
          Cargar conversación
        </button>
      </div>

      {/* Estado / errores */}
      {error && (
        <div style={{ color: "#b00020", fontSize: 12, marginBottom: 8 }}>
          {error}
        </div>
      )}

      {/* Lista de mensajes */}
      <div
        ref={listRef}
        style={{
          border: "1px solid #eee",
          borderRadius: 12,
          background: "#fff",
          height: 360,
          overflow: "auto",
          padding: 12,
          marginBottom: 8,
        }}
      >
        {loading && <div style={{ fontSize: 12, color: "#6b7280" }}>Cargando…</div>}
        {!loading && msgs.length === 0 && (
          <div style={{ fontSize: 12, color: "#6b7280" }}>No hay mensajes en esta conversación.</div>
        )}
        {!loading &&
          msgs.map((m) => (
            <MessageBubble key={m.id} msg={m} />
          ))}
      </div>

      {/* Input de envío */}
      <div style={{ display: "flex", gap: 8 }}>
        <input
          className="flex-1"
          placeholder={role === "teacher" ? "Mensaje al padre…" : "Mensaje al profesor…"}
          value={text}
          onChange={(e) => setText(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter" && !e.shiftKey) {
              e.preventDefault();
              send();
            }
          }}
          style={{ flex: 1, border: "1px solid #ddd", borderRadius: 8, padding: "8px 10px" }}
        />
        <button
          onClick={send}
          disabled={!partnerId || sending}
          style={{
            padding: "8px 12px",
            borderRadius: 8,
            background: "#0f172a",
            color: "#fff",
            opacity: sending ? 0.7 : 1,
          }}
        >
          {sending ? "Enviando…" : "Enviar"}
        </button>
      </div>
    </Layout>
  );
}

function MessageBubble({ msg }: { msg: Msg }) {
  // Si quisieras colorear por remitente, compara con tu propio user.id (no lo traemos aquí).
  return (
    <div style={{ marginBottom: 10, display: "grid" }}>
      <div style={{ fontSize: 11, color: "#6b7280" }}>
        #{msg.id} • {new Date(msg.sent_at).toLocaleString()} • de {msg.sender_id} a {msg.receiver_id}
        {msg.child_id ? ` • niño #${msg.child_id}` : ""}
      </div>
      <div
        style={{
          maxWidth: "80%",
          padding: "8px 10px",
          borderRadius: 10,
          background: "#f1f5f9",
          whiteSpace: "pre-wrap",
        }}
      >
        {msg.content}
      </div>
    </div>
  );
}
