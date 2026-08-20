import type { Metadata } from "next";
import { ButtonLink } from "@/components/Button";

export const metadata: Metadata = {
  title: "Pedido confirmado",
  robots: { index: false },
};

/**
 * Página de sucesso. Importante: o cliente só é direcionado para
 * cá quando o GATEWAY confirma o pagamento (via webhook) — chegar
 * a esta página não é, por si só, prova de pagamento.
 */
export default function PedidoSucessoPage() {
  return (
    <div className="order-status-page">
      <span className="order-status-page__icon" aria-hidden="true">
        ✓
      </span>
      <h1>Pagamento confirmado!</h1>
      <p>
        Recebemos a confirmação do seu pagamento e seu pedido já está sendo
        preparado com carinho. Você receberá as atualizações pelo e-mail
        informado no checkout.
      </p>
      <div className="order-status-page__actions">
        <ButtonLink href="/produtos" variant="secondary">
          Continuar comprando
        </ButtonLink>
        <ButtonLink href="/">Voltar ao início</ButtonLink>
      </div>
    </div>
  );
}
