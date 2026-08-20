import type { Metadata } from "next";
import { PolicyPage } from "@/components/PolicyPage";

export const metadata: Metadata = {
  title: "Termos de Uso",
  description: "Termos de uso do site da Petite Vallée.",
  alternates: { canonical: "/termos-de-uso" },
};

export default function TermosDeUsoPage() {
  return (
    <PolicyPage title="Termos de Uso">
      <h2>Sobre a loja</h2>
      <p>
        Este site é operado pela Petite Vallée, marca de produtos artesanais
        de Valinhos, SP. Ao navegar e comprar aqui, você concorda com estes
        termos.
      </p>
      <h2>Produtos e preços</h2>
      <p>
        Trabalhamos com produção artesanal em pequenos lotes, e a
        disponibilidade dos produtos pode variar. Os preços exibidos podem
        ser atualizados; o valor válido é sempre o apresentado na conclusão
        do pedido.
      </p>
      <h2>Pedidos e pagamento</h2>
      <p>
        Um pedido é considerado confirmado somente após a confirmação do
        pagamento pelo provedor. Em caso de recusa ou não pagamento, o pedido
        é cancelado sem qualquer cobrança.
      </p>
      <h2>Propriedade intelectual</h2>
      <p>
        A marca, o logotipo, as fotografias e os textos deste site pertencem
        à Petite Vallée e não podem ser reproduzidos sem autorização.
      </p>
    </PolicyPage>
  );
}
