import type { ReactNode } from "react";
import { BotanicalDecoration } from "./BotanicalDecoration";

interface EmptyStateProps {
  title: string;
  description?: string;
  action?: ReactNode;
}

/** Estado vazio delicado (carrinho vazio, filtro sem resultados). */
export function EmptyState({ title, description, action }: EmptyStateProps) {
  return (
    <div className="empty-state">
      <BotanicalDecoration size={32} />
      <h3 className="empty-state__title">{title}</h3>
      {description && <p className="empty-state__description">{description}</p>}
      {action && <div className="empty-state__action">{action}</div>}
    </div>
  );
}
