import { useState } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import styles from "./Login.module.css";

export default function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const { login } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  const from = location.state?.from?.pathname || "/";

  const handleSubmit = (e) => {
    e.preventDefault();
    setError("");
    const result = login(username, password);
    if (result.ok) {
      navigate(from, { replace: true });
    } else {
      setError(result.error);
    }
  };

  return (
    <div className={styles.container}>
      <form className={styles.card} onSubmit={handleSubmit}>
        <div className={styles.brand}>
          <span className={styles.brandMark} aria-hidden="true">
            <span className={styles.brandMarkSun} />
          </span>
          <span className={styles.brandName}>LLANO IA</span>
        </div>

        <p className={styles.subtitle}>Inicia sesión para continuar</p>

        {error && <div className={styles.error}>{error}</div>}

        <label className={styles.label}>
          Usuario
          <input
            className={styles.input}
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            autoComplete="username"
            required
          />
        </label>

        <label className={styles.label}>
          Contraseña
          <input
            className={styles.input}
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            autoComplete="current-password"
            required
          />
        </label>

        <button className={styles.button} type="submit">
          Entrar
        </button>

        <p className={styles.hint}>Usuario de prueba: 12345 / user123</p>
      </form>
    </div>
  );
}