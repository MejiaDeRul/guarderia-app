import { Link } from "react-router-dom";
import { useAuth } from "../context/AuthContext";


export default function Layout({ children }: { children: React.ReactNode }) {
    const { email, role, logout } = useAuth();
    return (
        <div style={{ fontFamily: "system-ui, sans-serif" }}>
            <header style={{ display: "flex", alignItems: "center", justifyContent: "space-between", padding: 16, borderBottom: "1px solid #eee" }}>
                <nav style={{ display: "flex", gap: 12, alignItems: "center" }}>
                    <strong>👶 Guardería</strong>
                    <Link to="/">Inicio</Link>
                    <Link to="/activities">Actividades</Link>
                    <Link to="/calendar">Calendario</Link>
                    <Link to="/chat">Chats</Link>
                    <Link to="/profile">Perfil</Link>
                    {role === "parent" && <Link to="/children">Mis niños</Link>}
                    {role === "teacher" && <Link to="/teacher">Profesor</Link>}
                </nav>
                <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
                    <span style={{ fontSize: 12, color: "#6b7280" }}>{email} • {role}</span>
                    <button onClick={logout} style={{ padding: "6px 10px", borderRadius: 8, background: "#0f172a", color: "#fff" }}>Salir</button>
                </div>
            </header>
            <main style={{ padding: 16 }}>{children}</main>
        </div>
    );
}