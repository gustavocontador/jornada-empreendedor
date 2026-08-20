import type { ReactNode } from "react";

type Tone = "info" | "success" | "error" | "warning";

interface StatusMessageProps {
  tone?: Tone;
  title?: string;
  children: ReactNode;
  role?: "status" | "alert";
}

/** Mensagem de status acessível (formulários, checkout, avisos). */
export function StatusMessage({
  tone = "info",
  title,
  children,
  role,
}: StatusMessageProps) {
  const resolvedRole = role ?? (tone === "error" ? "alert" : "status");
  return (
    <div className={`status-message status-message--${tone}`} role={resolvedRole}>
      {title && <strong className="status-message__title">{title}</strong>}
      <div className="status-message__body">{children}</div>
    </div>
  );
}
