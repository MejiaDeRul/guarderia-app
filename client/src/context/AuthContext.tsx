import { createContext, useContext, useMemo, useState } from "react";
import { api, postLogin } from "../lib/api";


type Role = "admin" | "teacher" | "parent" | null;


type AuthState = {
    token: string | null;
    role: Role;
    email: string | null;
};


type AuthCtx = AuthState & {
    login: (email: string, password: string) => Promise<void>;
    logout: () => void;
};


const Ctx = createContext<AuthCtx | null>(null);
    export const useAuth = () => {
    const ctx = useContext(Ctx);
    if (!ctx) throw new Error("AuthProvider missing");
    return ctx;
};


export function AuthProvider({ children }: { children: React.ReactNode }) {
        const [state, setState] = useState<AuthState>(() => ({
            token: localStorage.getItem("token"),
            role: (localStorage.getItem("role") as Role) || null,
            email: localStorage.getItem("email"),
        }));


    async function login(email: string, password: string) {
        const data = await postLogin(email, password);
        const token = data.access_token;
        const me = await api<{ id: number; email: string; role: Role }>("/users/me", token);
        localStorage.setItem("token", token);
        localStorage.setItem("role", String(me.role));
        localStorage.setItem("email", String(me.email));
        setState({ token, role: me.role, email: me.email });
    }


    function logout() {
        localStorage.removeItem("token");
        localStorage.removeItem("role");
        localStorage.removeItem("email");
        setState({ token: null, role: null, email: null });
    }


    const value = useMemo(() => ({ ...state, login, logout }), [state]);
    return <Ctx.Provider value={value}>{children}</Ctx.Provider>;
}