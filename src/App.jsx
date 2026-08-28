import { useState } from "react";
import Sidebar from "./components/Sidebar";
import ChatPanel from "./components/ChatPanel";
import VerifyPanel from "./components/VerifyPanel";
import "./App.css";

export default function App() {
  const [activeNav, setActiveNav] = useState("agro");
  const [showVerify, setShowVerify] = useState(true);

  return (
    <div className="app-shell">
      <Sidebar active={activeNav} onNavigate={setActiveNav} />
      <ChatPanel reserveComposerSpace={showVerify} />
      {showVerify && <VerifyPanel onClose={() => setShowVerify(false)} />}
    </div>
  );
}
