import { useState } from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { AuthProvider } from "./context/AuthContext";
import ProtectedRoute from "./components/ProtectedRoute";
import Login from "./pages/Login";
import Sidebar from "./components/Sidebar";
import ChatPanel from "./components/ChatPanel";
import VerifyPanel from "./components/VerifyPanel";
import "./App.css";

export default function App() {
  const [activeNav, setActiveNav] = useState("agro");
  const [showVerify, setShowVerify] = useState(true);

  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route
            path="/login"
            element={<Login />}
          />
          <Route
            path="/*"
            element={
              <ProtectedRoute>
                <div className="app-shell">
                  <Sidebar active={activeNav} onNavigate={setActiveNav} />
                  <ChatPanel reserveComposerSpace={showVerify} />
                  {showVerify && <VerifyPanel onClose={() => setShowVerify(false)} />}
                </div>
              </ProtectedRoute>
            }
          />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}
