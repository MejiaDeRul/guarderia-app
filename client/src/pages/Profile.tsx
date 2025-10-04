import Layout from "../components/Layout";
import { useAuth } from "../context/AuthContext";

export default function Profile() {
  const { email, role } = useAuth();

  return (
    <Layout>
      <h1>Mi perfil</h1>
      <div
        style={{
          marginTop: 12,
          padding: 16,
          border: "1px solid #eee",
          borderRadius: 12,
          maxWidth: 480,
        }}
      >
        <div style={{ color: "#6b7280", fontSize: 12 }}>Correo</div>
        <div style={{ fontWeight: 600, marginBottom: 8 }}>{email}</div>

        <div style={{ color: "#6b7280", fontSize: 12 }}>Rol</div>
        <div style={{ fontWeight: 600, textTransform: "capitalize" }}>{role}</div>
      </div>
    </Layout>
  );
}
