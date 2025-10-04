import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";


export default function Login() {
    const nav = useNavigate();
    const { login } = useAuth();
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);


    async function onSubmit(e: React.FormEvent) {
        e.preventDefault();
        setLoading(true);
        setError(null);
        try {
            await login(email, password);
            nav("/", { replace: true });
        } catch (err: any) {
            setError(err?.message || "Error de autenticación");
        } finally {
            setLoading(false);
        }
    }


    return (
        <div style={{ minHeight: "100vh", display: "grid", placeItems: "center" }}>
            <form onSubmit={onSubmit} style={{ background: "#fff", padding: 24, borderRadius: 12, width: 360, boxShadow: "0 2px 10px rgba(0,0,0,.08)" }}>
                <h1 style={{ fontSize: 20, marginBottom: 12 }}>Iniciar sesión</h1>
                <label style={{ fontSize: 12 }}>Correo</label>
                <input style={{ width: "100%", padding: 8, margin: "6px 0 12px", border: "1px solid #ddd", borderRadius: 8 }} value={email} onChange={(e) => setEmail(e.target.value)} placeholder="admin@demo.com" />
                <label style={{ fontSize: 12 }}>Contraseña</label>
                <input type="password" style={{ width: "100%", padding: 8, margin: "6px 0 12px", border: "1px solid #ddd", borderRadius: 8 }} value={password} onChange={(e) => setPassword(e.target.value)} placeholder="Admin123!" />
                {error && <div style={{ color: "#b00020", fontSize: 12, marginBottom: 8 }}>{error}</div>}
                <button disabled={loading} style={{ width: "100%", padding: 10, borderRadius: 8, background: "#0f172a", color: "#fff" }}>
                {loading ? "Accediendo…" : "Entrar"}
                </button>
                <p style={{ fontSize: 12, color: "#6b7280", marginTop: 8 }}>Tip: crea el admin con POST /auth/bootstrap-admin si aún no existe.</p>
            </form>
        </div>
    );
}