import {
    Sprout,
    Guitar,
    Compass,
    Link2,
    Settings,
    CircleHelp,
    ChevronRight,
    CalendarCheck,
    LogOut
} from "lucide-react";
import "./Sidebar.css";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext"

const NAV_ITEMS = [
    { id: "agro", label: "Agroalimentario", icon: Sprout, active: true },
    { id: "cultura", label: "Cultura Llanera", icon: Guitar },
    { id: "turismo", label: "Turismo y Experiencias", icon: Compass },
    { id: "trazabilidad", label: "Trazabilidad Blockchain", icon: Link2 },
];

const FOOT_ITEMS = [
    { id: "config", label: "Configuración", icon: Settings },
    { id: "ayuda", label: "Ayuda", icon: CircleHelp },
];

function Sparkline() {
    return (
        <svg viewBox="0 0 160 44" className="sparkline" preserveAspectRatio="none">
            <polyline
                points="0,32 14,30 28,34 42,22 56,26 70,14 84,18 98,10 112,16 126,6 140,10 160,3"
                fill="none"
                stroke="var(--green-400)"
                strokeWidth="2.5"
                strokeLinecap="round"
                strokeLinejoin="round"
            />
            <polyline
                points="0,32 14,30 28,34 42,22 56,26 70,14 84,18 98,10 112,16 126,6 140,10 160,3 160,44 0,44"
                fill="url(#sparkFill)"
                stroke="none"
            />
            <defs>
                <linearGradient id="sparkFill" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stopColor="var(--green-500)" stopOpacity="0.25" />
                    <stop offset="100%" stopColor="var(--green-500)" stopOpacity="0" />
                </linearGradient>
            </defs>
        </svg>
    );
}

export default function Sidebar({ active, onNavigate }) {
    const { user, role, logout } = useAuth();
    const navigate = useNavigate();

    const handleLogout = () => {
        logout();
        navigate("/login", { replace: true });
    };

    return (
        <aside className="sidebar">
            <div className="brand">
                <span className="brand-mark" aria-hidden="true">
                    <span className="brand-mark-sun" />
                </span>
                <span className="brand-name">LLANO IA</span>
            </div>

            <nav className="nav" aria-label="Módulos">
                {NAV_ITEMS.map(({ id, label, icon: Icon }) => (
                    <button
                        key={id}
                        className={`nav-item ${active === id ? "is-active" : ""}`}
                        onClick={() => onNavigate(id)}
                    >
                        <Icon size={17} strokeWidth={2} />
                        <span>{label}</span>
                    </button>
                ))}
            </nav>

            <div className="indicators">
                <h3 className="indicators-title">Indicadores Clave</h3>

                <button className="indicator-card">
                    <div className="indicator-head">
                        <span>Volumen de Ventas (CO)</span>
                        <ChevronRight size={15} />
                    </div>
                    <Sparkline />
                    <div className="indicator-value">COP 15.2M</div>
                </button>

                <button className="indicator-card indicator-card--amber">
                    <div className="indicator-head">
                        <span>Reservas Activas (Turismo)</span>
                        <ChevronRight size={15} />
                    </div>
                    <div className="indicator-row">
                        <div className="indicator-value indicator-value--amber">34</div>
                        <CalendarCheck size={22} strokeWidth={1.8} />
                    </div>
                </button>
            </div>

            <div className="sidebar-foot">
                {FOOT_ITEMS.map(({ id, label, icon: Icon }) => (
                    <button key={id} className="foot-item">
                        <Icon size={16} strokeWidth={2} />
                        <span>{label}</span>
                    </button>
                ))}
                <button className="foot-item foot-item--logout" onClick={handleLogout}>
                    <LogOut size={16} strokeWidth={2} />
                    <span>Cerrar sesión</span>
                </button>
            </div>
        </aside>
    );
}
