import type { Metadata } from "next";
import {
  Fraunces,
  Karla,
  Cormorant_Garamond,
  Nunito_Sans,
  Playfair_Display,
  Source_Sans_3,
  Lora,
  Figtree,
} from "next/font/google";

/**
 * ⚠️ PÁGINA TEMPORÁRIA DE ESCOLHA DE FONTES
 *
 * Mostra o mesmo trecho do site em 4 combinações tipográficas
 * para a cliente escolher. Não aparece no menu, no sitemap nem
 * nos buscadores. Depois da escolha:
 *   1. Aplicar a dupla escolhida em src/app/layout.tsx;
 *   2. Apagar esta pasta (src/app/preview-fontes).
 */

export const metadata: Metadata = {
  title: "Escolha de fontes",
  robots: { index: false, follow: false },
};

const fraunces = Fraunces({ subsets: ["latin"], display: "swap" });
const karla = Karla({ subsets: ["latin"], display: "swap" });
const cormorant = Cormorant_Garamond({
  subsets: ["latin"],
  weight: ["500", "600"],
  display: "swap",
});
const nunitoSans = Nunito_Sans({ subsets: ["latin"], display: "swap" });
const playfair = Playfair_Display({ subsets: ["latin"], display: "swap" });
const sourceSans = Source_Sans_3({ subsets: ["latin"], display: "swap" });
const lora = Lora({ subsets: ["latin"], display: "swap" });
const figtree = Figtree({ subsets: ["latin"], display: "swap" });

const OPTIONS = [
  {
    id: "A",
    label: "Opção A — Fraunces + Karla (atual)",
    serif: fraunces.style.fontFamily,
    sans: karla.style.fontFamily,
  },
  {
    id: "B",
    label: "Opção B — Cormorant Garamond + Nunito Sans",
    serif: cormorant.style.fontFamily,
    sans: nunitoSans.style.fontFamily,
  },
  {
    id: "C",
    label: "Opção C — Playfair Display + Source Sans",
    serif: playfair.style.fontFamily,
    sans: sourceSans.style.fontFamily,
  },
  {
    id: "D",
    label: "Opção D — Lora + Figtree",
    serif: lora.style.fontFamily,
    sans: figtree.style.fontFamily,
  },
];

export default function PreviewFontesPage() {
  return (
    <section className="section">
      <div className="container container--narrow">
        <header className="section-title">
          <h1 className="section-title__heading">Qual fonte combina mais?</h1>
          <p className="section-title__description">
            O mesmo trecho do site, escrito de quatro jeitos. Repare nos
            títulos, no texto corrido, no preço e no botão — e responda com a
            letra da sua preferida (pode escolher título de uma e texto de
            outra também).
          </p>
        </header>

        {OPTIONS.map((option) => (
          <article
            key={option.id}
            className="editorial__content"
            style={{ marginBottom: "var(--space-6)" }}
          >
            <p
              style={{
                fontFamily: option.sans,
                fontSize: "var(--text-xs)",
                fontWeight: 700,
                letterSpacing: "0.16em",
                textTransform: "uppercase",
                color: "var(--color-accent-dark)",
                marginBottom: "var(--space-3)",
              }}
            >
              {option.label}
            </p>
            <h2
              style={{
                fontFamily: option.serif,
                fontSize: "var(--text-2xl)",
                lineHeight: 1.15,
                marginBottom: "var(--space-3)",
              }}
            >
              Granola crocante, mixes na medida e geleia de verdade.
            </h2>
            <p
              style={{
                fontFamily: option.sans,
                color: "var(--color-text-secondary)",
                marginBottom: "var(--space-4)",
              }}
            >
              Tudo artesanal, assado e preparado em pequenos lotes, direto de
              Valinhos. Vai bem com iogurte, frutas, açaí — ou direto do pote.
            </p>
            <p
              style={{
                fontFamily: option.serif,
                fontSize: "var(--text-lg)",
                marginBottom: "var(--space-4)",
              }}
            >
              R$ 29,90
            </p>
            <span
              className="btn btn--primary btn--small"
              style={{ fontFamily: option.sans, pointerEvents: "none" }}
            >
              <span>Adicionar ao carrinho</span>
            </span>
          </article>
        ))}
      </div>
    </section>
  );
}
