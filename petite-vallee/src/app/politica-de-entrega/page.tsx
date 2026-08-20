import type { Metadata } from "next";
import { PolicyPage } from "@/components/PolicyPage";

export const metadata: Metadata = {
  title: "Política de Entrega",
  description: "Como funcionam as entregas da Petite Vallée.",
  alternates: { canonical: "/politica-de-entrega" },
};

export default function PoliticaEntregaPage() {
  return (
    <PolicyPage title="Política de Entrega">
      <h2>Como entregamos</h2>
      <p>
        A Petite Vallée entrega para todo o Brasil pelos Correios. O valor e
        o prazo do frete serão calculados automaticamente pelo CEP durante o
        checkout.
      </p>
      <h2>Em configuração</h2>
      <p>
        O cálculo automático de frete está em fase de configuração e será
        ativado antes do início das vendas. Os prazos de preparo e postagem
        dos pedidos serão publicados nesta página.
      </p>
      <h2>Embalagem</h2>
      <p>
        Os produtos são preparados e embalados para chegar à sua casa em
        perfeitas condições.
      </p>
    </PolicyPage>
  );
}
