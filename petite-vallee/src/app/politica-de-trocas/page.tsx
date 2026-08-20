import type { Metadata } from "next";
import { PolicyPage } from "@/components/PolicyPage";

export const metadata: Metadata = {
  title: "Política de Trocas e Devoluções",
  description: "Trocas e devoluções na Petite Vallée.",
  alternates: { canonical: "/politica-de-trocas" },
};

export default function PoliticaTrocasPage() {
  return (
    <PolicyPage title="Trocas e Devoluções">
      <h2>Direito de arrependimento</h2>
      <p>
        Conforme o Código de Defesa do Consumidor, em compras feitas pela
        internet você pode desistir da compra em até 7 (sete) dias corridos
        após o recebimento, com devolução integral do valor pago.
      </p>
      <h2>Produtos com problema</h2>
      <p>
        Se o seu pedido chegar danificado ou com qualquer problema, fale com
        a gente pela página de contato assim que possível, de preferência com
        fotos. Faremos a troca ou o reembolso sem burocracia.
      </p>
      <h2>Detalhes em definição</h2>
      <p>
        Os procedimentos completos de troca (endereço de devolução, prazos de
        análise e reenvio) serão detalhados nesta página antes do início das
        vendas.
      </p>
    </PolicyPage>
  );
}
