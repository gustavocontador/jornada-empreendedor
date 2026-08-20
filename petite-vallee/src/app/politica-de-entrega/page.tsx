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
      <h2>Regras em definição</h2>
      <p>
        As modalidades de entrega da Petite Vallée (entrega local em
        Valinhos e região, retirada e envio por transportadora), os prazos e
        os valores de frete estão sendo definidos e serão publicados nesta
        página antes do início das vendas.
      </p>
      <h2>O que já podemos garantir</h2>
      <p>
        Nossos produtos são preparados e embalados com cuidado para chegarem
        à sua casa em perfeitas condições. O prazo de preparo será informado
        na confirmação do pedido.
      </p>
    </PolicyPage>
  );
}
