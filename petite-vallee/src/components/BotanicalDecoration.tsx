/**
 * Pequeno ramo botânico inspirado nas folhas do logotipo.
 * Usado apenas como detalhe discreto (etiquetas, divisores) —
 * nunca competindo com as fotografias dos produtos.
 */

interface BotanicalDecorationProps {
  size?: number;
  className?: string;
}

export function BotanicalDecoration({
  size = 18,
  className,
}: BotanicalDecorationProps) {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 24 24"
      fill="none"
      aria-hidden="true"
      className={className}
    >
      <path
        d="M8 20 C 8 12, 13 7, 16 4"
        stroke="var(--color-accent)"
        strokeWidth="1.4"
        strokeLinecap="round"
      />
      <path
        d="M11.5 13.5 c -2.6 -0.4 -4.2 -2 -4.6 -4.4 c 2.8 0.2 4.3 1.8 4.6 4.4 z"
        fill="var(--color-accent)"
        opacity="0.8"
      />
      <path
        d="M14 9 c -2 -0.8 -3 -2.6 -2.6 -4.6 c 2.4 0.6 3 2.6 2.6 4.6 z"
        fill="var(--color-accent)"
        opacity="0.55"
      />
    </svg>
  );
}

/** Divisor horizontal delicado com o ramo ao centro. */
export function BotanicalDivider() {
  return (
    <div className="botanical-divider" aria-hidden="true">
      <span className="botanical-divider__line" />
      <BotanicalDecoration size={20} />
      <span className="botanical-divider__line" />
    </div>
  );
}
