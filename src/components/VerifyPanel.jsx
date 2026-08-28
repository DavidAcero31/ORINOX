import { ShieldCheck, ChevronRight, X } from "lucide-react";
import "./VerifyPanel.css";

function PseudoQR() {
  // Decorative traceability code, styled like a QR + branding-iron mark —
  // not a scannable code, just the visual signature of a verified lot.
  const cells = [
    "1110101",
    "1001011",
    "0110110",
    "1101001",
    "0011101",
    "1010010",
    "0101110",
  ];
  return (
    <svg viewBox="0 0 98 98" className="qr" role="img" aria-label="Código de verificación del lote">
      <rect x="0" y="0" width="98" height="98" rx="10" fill="#0c110d" />
      {cells.map((row, ri) =>
        [...row].map((bit, ci) =>
          bit === "1" ? (
            <rect
              key={`${ri}-${ci}`}
              x={8 + ci * 12}
              y={8 + ri * 12}
              width="9"
              height="9"
              rx="1.5"
              fill="var(--green-400)"
              opacity={0.9}
            />
          ) : null
        )
      )}
      <rect x="8" y="8" width="20" height="20" rx="4" fill="none" stroke="var(--green-400)" strokeWidth="2.5" />
      <rect x="70" y="8" width="20" height="20" rx="4" fill="none" stroke="var(--green-400)" strokeWidth="2.5" />
      <rect x="8" y="70" width="20" height="20" rx="4" fill="none" stroke="var(--green-400)" strokeWidth="2.5" />
    </svg>
  );
}

export default function VerifyPanel({ onClose }) {
  return (
    <div className="verify-panel">
      <button className="verify-close" onClick={onClose} aria-label="Cerrar verificación">
        <X size={14} />
      </button>
      <div className="verify-qr-wrap">
        <PseudoQR />
      </div>
      <div className="verify-info">
        <dl>
          <div>
            <dt>Productor</dt>
            <dd>Finca Casanare</dd>
          </div>
          <div>
            <dt>Producto</dt>
            <dd>Carne de Res (Corte Selección)</dd>
          </div>
          <div>
            <dt>Lote</dt>
            <dd className="mono">CAS-BN-1023</dd>
          </div>
          <div>
            <dt>Origen</dt>
            <dd>Yopal, Casanare, Colombia</dd>
          </div>
        </dl>

        <div className="verify-badge">
          <ShieldCheck size={16} />
          <div>
            <span>Blockchain Verified</span>
            <small>Verificado en cadena de bloques</small>
          </div>
        </div>

        <button className="verify-details">
          Ver más detalles
          <ChevronRight size={15} />
        </button>
      </div>
    </div>
  );
}
