import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import Dashboard from "./pages/Dashboard";
import Activities from "./pages/Activities";
import Calendar from "./pages/Calendar";
import Chat from "./pages/Chat";
import Profile from "./pages/Profile";
import Children from "./pages/Children";
import Teacher from "./pages/Teacher";
import Login from "./pages/Login";
import { AuthProvider, useAuth } from "./context/AuthContext";


function RequireAuth({ children }: { children: React.ReactNode }) {
    const { token } = useAuth();
    if (!token) return <Navigate to="/login" replace />;
    return <>{children}</>;
}


function RequireRole({ allowed, children }: { allowed: Array<"admin"|"teacher"|"parent">; children: React.ReactNode }) {
    const { role } = useAuth();
    if (!role || !allowed.includes(role)) return <Navigate to="/" replace />;
    return <>{children}</>;
}


export default function App() {
    return (
        <AuthProvider>
            <BrowserRouter>
                <Routes>
                    <Route path="/login" element={<Login />} />


                    <Route path="/" element={<RequireAuth><Dashboard /></RequireAuth>} />
                    <Route path="/activities" element={<RequireAuth><Activities /></RequireAuth>} />
                    <Route path="/calendar" element={<RequireAuth><Calendar /></RequireAuth>} />
                    <Route path="/chat" element={<RequireAuth><Chat /></RequireAuth>} />
                    <Route path="/profile" element={<RequireAuth><Profile /></RequireAuth>} />


                    <Route path="/children" element={<RequireAuth><RequireRole allowed={["parent"]}><Children /></RequireRole></RequireAuth>} />
                    <Route path="/teacher" element={<RequireAuth><RequireRole allowed={["teacher"]}><Teacher /></RequireRole></RequireAuth>} />


                    <Route path="*" element={<Navigate to="/" replace />} />
                </Routes>
            </BrowserRouter>
        </AuthProvider>
    );
}