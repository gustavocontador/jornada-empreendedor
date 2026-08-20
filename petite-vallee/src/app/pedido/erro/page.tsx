import type { Metadata } from "next";
import { ButtonLink } from "@/components/Button";

export const metadata: Metadata = {
  title: "Problema com o pagamento",
  robots: { index: false },
};

export default function PedidoErroPage() {
  return (
    <div className="order-status-page">
      <span className="order-status-page__icon" aria-hidden="true">
        !
      </span>
      <h1>Não foi possível concluir o pagamento</h1>
      <p>
        O pagamento foi recusado ou ocorreu um erro durante o processamento.
        Nenhum valor foi cobrado. Você pode tentar novamente com outra forma
        de pagamento — seus itens continuam no carrinho.
      </p>
      <div className="order-status-page__actions">
        <ButtonLink href="/checkout">Tentar novamente</ButtonLink>
        <ButtonLink href="/contato" variant="secondary">
          Falar conosco
        </ButtonLink>
      </div>
    </div>
  );
}
