import { useState } from "react";

import Sidebar from "./components/Sidebar";
import ChatPanel from "./components/ChatPanel";
import VerifyPanel from "./components/VerifyPanel";
import Inicio from "./components/Inicio";

import "./App.css";

export default function App() {
  const [activeNav, setActiveNav] = useState("inicio");
  const [showVerify, setShowVerify] = useState(true);

  const handleNavigate = (id) => {
    setActiveNav(id);
  };

  const renderView = () => {
    switch (activeNav) {
      case "inicio":
        return <Inicio />;

      case "agro":
        return (
          <ChatPanel
            reserveComposerSpace={showVerify}
          />
        );

      case "cultura":
        return (
          <ChatPanel
            reserveComposerSpace={showVerify}
          />
        );

      case "turismo":
        return (
          <ChatPanel
            reserveComposerSpace={showVerify}
          />
        );

      case "trazabilidad":
        return (
          <ChatPanel
            reserveComposerSpace={showVerify}
          />
        );

      case "config":
        return (
          <div className="page-placeholder">
            <h1>Configuración</h1>
            <p>Panel de configuración de LLANO IA.</p>
          </div>
        );

      case "ayuda":
        return (
          <div className="page-placeholder">
            <h1>Ayuda</h1>
            <p>Centro de ayuda de LLANO IA.</p>
          </div>
        );

      case "ventas":
        return (
          <div className="page-placeholder">
            <h1>Volumen de Ventas</h1>
            <p>Información de ventas y comportamiento comercial.</p>
          </div>
        );

      case "reservas":
        return (
          <div className="page-placeholder">
            <h1>Reservas Activas</h1>
            <p>Información de reservas turísticas.</p>
          </div>
        );

      default:
        return <Inicio />;
    }
  };

  return (
    <div className="app-shell">

      <Sidebar
        active={activeNav}
        onNavigate={handleNavigate}
      />

      <main className="app-content">
        {renderView()}
      </main>

      {activeNav === "agro" && showVerify && (
        <VerifyPanel
          onClose={() => setShowVerify(false)}
        />
      )}

    </div>
  );
}
