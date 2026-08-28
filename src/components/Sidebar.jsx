import {
  House,
  Sprout,
  Guitar,
  Compass,
  Link2,
  Settings,
  CircleHelp,
  ChevronRight,
  CalendarCheck,
} from "lucide-react";
import "./Sidebar.css";

const NAV_ITEMS = [
  { id: "inicio", label: "Inicio", icon: House },
  { id: "agro", label: "Agroalimentario", icon: Sprout },
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
    <svg
      viewBox="0 0 160 44"
      className="sparkline"
      preserveAspectRatio="none"
    >
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
          <stop
            offset="0%"
            stopColor="var(--green-500)"
            stopOpacity="0.25"
          />
          <stop
            offset="100%"
            stopColor="var(--green-500)"
            stopOpacity="0"
          />
        </linearGradient>
      </defs>
    </svg>
  );
}

export default function Sidebar({ active, onNavigate }) {
  return (
    <aside className="sidebar">
      {/* MARCA */}
      <div className="brand">
        <span className="brand-mark" aria-hidden="true">
          <span className="brand-mark-sun" />
        </span>

        <span className="brand-name">LLANO IA</span>
      </div>

      {/* NAVEGACIÓN PRINCIPAL */}
      <nav className="nav" aria-label="Módulos">
        {NAV_ITEMS.map(({ id, label, icon: Icon }) => (
          <button
            key={id}
            type="button"
            className={`nav-item ${active === id ? "is-active" : ""}`}
            onClick={() => onNavigate(id)}
          >
            <Icon size={17} strokeWidth={2} />
            <span>{label}</span>
          </button>
        ))}
      </nav>

      {/* INDICADORES */}
      <div className="indicators">
        <h3 className="indicators-title">Indicadores Clave</h3>

        <button
          type="button"
          className="indicator-card"
          onClick={() => onNavigate("ventas")}
        >
          <div className="indicator-head">
            <span>Volumen de Ventas (CO)</span>
            <ChevronRight size={15} />
          </div>

          <Sparkline />

          <div className="indicator-value">COP 15.2M</div>
        </button>

        <button
          type="button"
          className="indicator-card indicator-card--amber"
          onClick={() => onNavigate("reservas")}
        >
          <div className="indicator-head">
            <span>Reservas Activas (Turismo)</span>
            <ChevronRight size={15} />
          </div>

          <div className="indicator-row">
            <div className="indicator-value indicator-value--amber">
              34
            </div>

            <CalendarCheck size={22} strokeWidth={1.8} />
          </div>
        </button>
      </div>

      {/* PARTE INFERIOR */}
      <div className="sidebar-foot">
        {FOOT_ITEMS.map(({ id, label, icon: Icon }) => (
          <button
            key={id}
            type="button"
            className={`foot-item ${active === id ? "is-active" : ""}`}
            onClick={() => onNavigate(id)}
          >
            <Icon size={16} strokeWidth={2} />
            <span>{label}</span>
          </button>
        ))}
      </div>
    </aside>
  );
}

