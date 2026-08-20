import type { Metadata } from "next";
import { SectionTitle } from "@/components/SectionTitle";
import { CartPageContent } from "./CartPageContent";

export const metadata: Metadata = {
  title: "Carrinho",
  description: "Revise os itens do seu carrinho na Petite Vallée.",
  alternates: { canonical: "/carrinho" },
  robots: { index: false },
};

export default function CarrinhoPage() {
  return (
    <section className="section">
      <div className="container container--narrow">
        <SectionTitle eyebrow="Sua seleção" title="Carrinho" as="h1" />
        <CartPageContent />
      </div>
    </section>
  );
}
