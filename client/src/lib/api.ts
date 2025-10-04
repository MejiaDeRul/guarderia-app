const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";


export async function api<T>(path: string, token: string | null, init?: RequestInit): Promise<T> {
    const res = await fetch(`${API_URL}${path}`, {
        ...init,
        headers: {
            "Content-Type": "application/json",
            ...(init?.headers || {}),
            ...(token ? { Authorization: `Bearer ${token}` } : {}),
        },
    });
    if (!res.ok) throw new Error(await res.text());
    return res.json();
}


export async function postLogin(email: string, password: string): Promise<{ access_token: string; token_type: string }>{
    const form = new URLSearchParams();
    form.set("username", email);
    form.set("password", password);
    const res = await fetch(`${API_URL}/auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: form,
    });
    if (!res.ok) throw new Error("Credenciales inválidas");
    return res.json();
}