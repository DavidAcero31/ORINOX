import React from "react";
import "./Inicio.css";

const Inicio = ({ onSelectModule }) => {
  return (
    <main className="inicio-container">

      <div className="inicio-content">

        <div className="bot-icon">
          🤖
        </div>

        <h1>ORINOX AI</h1>

        <h2>
          Inteligencia que conecta el territorio
        </h2>

        <p className="inicio-description">
          Soy ORINOX AI, un agente inteligente diseñado para
          conectar productores, comerciantes, prestadores
          culturales y turistas con nuevas oportunidades
          dentro de la Orinoquía.
        </p>

        <p className="inicio-question">
          ¿Qué deseas explorar?
        </p>

        <div className="module-grid">

          <button
            className="module-card"
            onClick={() => onSelectModule("agroalimentario")}
          >
            <span className="module-icon">🌱</span>

            <div>
              <h3>Agroalimentario</h3>

              <p>
                Compra, venta y comercialización
                de productos de la región.
              </p>
            </div>

            <span className="arrow">→</span>
          </button>


          <button
            className="module-card"
            onClick={() => onSelectModule("cultura")}
          >
            <span className="module-icon">🐎</span>

            <div>
              <h3>Cultura Llanera</h3>

              <p>
                Tradiciones, artesanías,
                gastronomía y oficios.
              </p>
            </div>

            <span className="arrow">→</span>
          </button>


          <button
            className="module-card"
            onClick={() => onSelectModule("turismo")}
          >
            <span className="module-icon">🏞️</span>

            <div>
              <h3>Turismo y Experiencias</h3>

              <p>
                Descubre experiencias
                auténticas del territorio.
              </p>
            </div>

            <span className="arrow">→</span>
          </button>

        </div>

      </div>

    </main>
  );
};

export default Inicio;