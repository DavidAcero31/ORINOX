import { createContext, useContext, useState } from "react";

const AuthContext = createContext(null);

// Usuario de prueba mientras no hay backend
const MOCK_USER = { username: "12345", password: "user123", role: "usuario" };

export function AuthProvider({ children }) {
  const [user, setUser] = useState(() => {
    const saved = sessionStorage.getItem("orinox_user");
    return saved ? JSON.parse(saved) : null;
  });

  const login = (username, password) => {
    if (username === MOCK_USER.username && password === MOCK_USER.password) {
      const userData = { username, role: MOCK_USER.role };
      setUser(userData);
      sessionStorage.setItem("orinox_user", JSON.stringify(userData));
      return { ok: true };
    }
    return { ok: false, error: "Usuario o contraseña incorrectos" };
  };

  const logout = () => {
    setUser(null);
    sessionStorage.removeItem("orinox_user");
  };

  return (
    <AuthContext.Provider value={{ user, role: user?.role ?? null, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export const useAuth = () => useContext(AuthContext);