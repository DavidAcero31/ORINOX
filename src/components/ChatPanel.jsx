import ReactMarkdown from "react-markdown";
import { useState } from "react";
import {
  MessageSquareText,
  MoreHorizontal,
  ArrowUp,
  History,
  RefreshCw,
} from "lucide-react";
import "./ChatPanel.css";

const PRODUCT = {
  name: "Cachama Plateada (Por Kg)",
  stock: "500 Kg",
  price: "COP 18,000",
  image:
    "https://images.unsplash.com/photo-1544943910-4c1dc44aab44?q=80&w=200&auto=format&fit=crop",
};

const MATCHES = [
  {
    name: "Restaurante El Estribo",
    place: "Casanare",
    score: 92,
  },
  {
    name: "Mercado Campesino Yopal",
    place: "Casanare",
    score: 85,
  },
];

function ProductCard() {
  return (
    <div className="product-card">
      <div className="product-thumb" aria-hidden="true">
        <svg viewBox="0 0 64 64" width="34" height="34">
          <path
            d="M6 32c8-14 24-18 36-10 6 4 10 8 16 10-6 2-10 6-16 10-12 8-28 4-36-10z"
            fill="var(--green-400)"
            opacity="0.85"
          />
          <circle cx="16" cy="30" r="2.2" fill="var(--bg-0)" />
        </svg>
      </div>

      <div className="product-info">
        <div className="product-name">{PRODUCT.name}</div>

        <div className="product-meta">
          Cantidad disponible: <strong>{PRODUCT.stock}</strong>
        </div>

        <div className="product-meta">
          Precio sugerido: <strong>{PRODUCT.price}</strong>
        </div>

        <div className="product-actions">
          <button type="button" className="btn btn--primary">
            <RefreshCw size={14} />
            Actualizar inventario
          </button>

          <button type="button" className="btn btn--ghost">
            <History size={14} />
            Ver historial de precios
          </button>
        </div>
      </div>
    </div>
  );
}

function MatchList() {
  return (
    <div className="match-card">
      <div className="match-title">Posibles Compradores (Matching)</div>

      <ul className="match-list">
        {MATCHES.map((m) => (
          <li className="match-row" key={m.name}>
            <div className="match-identity">
              <span className="match-name">{m.name}</span>
              <span className="match-place">{m.place}</span>
            </div>

            <div
              className="match-score"
              style={{ "--score": m.score }}
            >
              {m.score}%
            </div>

            <button type="button" className="btn btn--outline btn--sm">
              Contactar
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default function ChatPanel({ reserveComposerSpace }) {
  const [draft, setDraft] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  // =========================================================
  // ENVIAR MENSAJE A FASTAPI → GEMINI
  // =========================================================

  const sendMessage = async (e) => {
    e.preventDefault();

    const message = draft.trim();

    // No enviar mensajes vacíos
    if (!message || loading) {
      return;
    }

    // Mostrar inmediatamente el mensaje del usuario
    setMessages((prev) => [
      ...prev,
      {
        role: "user",
        content: message,
      },
    ]);

    // Limpiar el input
    setDraft("");

    // Activar estado de carga
    setLoading(true);

    try {
      const response = await fetch("http://localhost:8000/api/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          mensaje: message,
          modulo: "productivo",
        }),
      });

      // Comprobar respuesta HTTP
      if (!response.ok) {
        throw new Error(`Error HTTP: ${response.status}`);
      }

      const data = await response.json();

      // Mostrar respuesta de Gemini
      setMessages((prev) => [
        ...prev,
        {
          role: "ai",
          content:
            data.respuesta ||
            "No recibí una respuesta de LLANO IA.",
        },
      ]);
    } catch (error) {
      console.error("Error conectando con LLANO IA:", error);

      // Mostrar error dentro del chat
      setMessages((prev) => [
        ...prev,
        {
          role: "ai",
          content:
            "No pude conectarme con LLANO IA. Verifica que el servidor FastAPI esté funcionando en http://localhost:8000.",
        },
      ]);
    } finally {
      // Terminar estado de carga
      setLoading(false);
    }
  };

  return (
    <section className="chat-panel">
      {/* =====================================================
          HEADER
      ====================================================== */}

      <header className="chat-header">
        <div className="chat-header-title">
          <MessageSquareText size={16} />

          <span>
            Asistente IA · Finca Los Llanos (Productor)
          </span>
        </div>

        <button
          type="button"
          className="icon-btn"
          aria-label="Más opciones"
        >
          <MoreHorizontal size={18} />
        </button>
      </header>

      {/* =====================================================
          CHAT
      ====================================================== */}

      <div className="chat-log">

        {/* -----------------------------------------------------
            MENSAJE INICIAL DEL USUARIO
        ------------------------------------------------------ */}

        <div className="msg msg--user">
          <p>
            ¿Con cuántos productores del Casanare estamos conectados hoy?
          </p>
        </div>

        {/* -----------------------------------------------------
            RESPUESTA INICIAL DE LLANO IA
        ------------------------------------------------------ */}

        <div className="msg-block">
          <div className="msg-avatar">IA</div>

          <div className="msg-body">
            <span className="msg-sender">
              LLANO IA
            </span>

            <div className="msg msg--ai">
              <p>
                Hoy tienes 14 productores activos en la región.
                Aquí tienes el inventario de pescado más reciente,
                cortesía de la finca Cachama de Yopal:
              </p>
            </div>

            <ProductCard />
          </div>
        </div>

        {/* -----------------------------------------------------
            SEGUNDO MENSAJE INICIAL
        ------------------------------------------------------ */}

        <div className="msg msg--user">
          <p>
            ¿Alguien ha comprado a un productor en el Casanare esta semana?
          </p>
        </div>

        {/* -----------------------------------------------------
            SEGUNDA RESPUESTA INICIAL
        ------------------------------------------------------ */}

        <div className="msg-block">
          <div className="msg-avatar">IA</div>

          <div className="msg-body">
            <span className="msg-sender">
              LLANO IA
            </span>

            <div className="msg msg--ai">
              <p>
                Encontré compradores compatibles con tu inventario
                de pescado, ordenados por afinidad:
              </p>
            </div>

            <MatchList />
          </div>
        </div>

        {/* =====================================================
            MENSAJES DINÁMICOS DE GEMINI
        ====================================================== */}

        {messages.map((message, index) => {
          // -----------------------------------------------
          // MENSAJE DEL USUARIO
          // -----------------------------------------------

          if (message.role === "user") {
            return (
              <div
                className="msg msg--user"
                key={`user-${index}`}
              >
                <p>{message.content}</p>
              </div>
            );
          }

          // -----------------------------------------------
          // RESPUESTA DE LLANO IA
          // -----------------------------------------------

          return (
            <div
              className="msg-block"
              key={`ai-${index}`}
            >
              <div className="msg-avatar">
                IA
              </div>

              <div className="msg-body">
                <span className="msg-sender">
                  LLANO IA
                </span>

                <div className="msg msg--ai">
                  <ReactMarkdown>
                    {message.content}
                  </ReactMarkdown>
                </div>
              </div>
            </div>
          );
        })}

        {/* =====================================================
            INDICADOR DE CARGA
        ====================================================== */}

        {loading && (
          <div className="msg-block">
            <div className="msg-avatar">
              IA
            </div>

            <div className="msg-body">
              <span className="msg-sender">
                LLANO IA
              </span>

              <div className="msg msg--ai">
                <p>
                  Consultando LLANO IA...
                </p>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* =====================================================
          COMPOSITOR
      ====================================================== */}

      <form
        className={`composer ${
          reserveComposerSpace
            ? "composer--offset"
            : ""
        }`}
        onSubmit={sendMessage}
      >
        <input
          value={draft}
          onChange={(e) => setDraft(e.target.value)}
          placeholder="Envía un mensaje..."
          aria-label="Escribe un mensaje para el asistente"
          disabled={loading}
        />

        <button
          type="submit"
          className="send-btn"
          aria-label="Enviar mensaje"
          disabled={loading || !draft.trim()}
        >
          <ArrowUp
            size={17}
            strokeWidth={2.4}
          />
        </button>
      </form>
    </section>
  );
}
