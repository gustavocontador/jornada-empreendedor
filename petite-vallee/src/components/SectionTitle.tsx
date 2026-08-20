import type { ReactNode } from "react";
import { BotanicalDecoration } from "./BotanicalDecoration";

interface SectionTitleProps {
  eyebrow?: string;
  title: string;
  description?: ReactNode;
  align?: "left" | "center";
  as?: "h1" | "h2";
  id?: string;
}

/** Título de seção com etiqueta discreta e detalhe botânico. */
export function SectionTitle({
  eyebrow,
  title,
  description,
  align = "left",
  as: Heading = "h2",
  id,
}: SectionTitleProps) {
  return (
    <header className={`section-title section-title--${align}`}>
      {eyebrow && (
        <p className="section-title__eyebrow">
          <BotanicalDecoration size={14} />
          <span>{eyebrow}</span>
        </p>
      )}
      <Heading className="section-title__heading" id={id}>
        {title}
      </Heading>
      {description && <p className="section-title__description">{description}</p>}
    </header>
  );
}
