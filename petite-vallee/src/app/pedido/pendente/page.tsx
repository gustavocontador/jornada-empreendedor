import type { Metadata } from "next";
import { ButtonLink } from "@/components/Button";

export const metadata: Metadata = {
  title: "Pedido aguardando pagamento",
  robots: { index: false },
};

export default function PedidoPendentePage() {
  return (
    <div className="order-status-page">
      <span className="order-status-page__icon" aria-hidden="true">
        ⏳
      </span>
      <h1>Aguardando confirmação do pagamento</h1>
      <p>
        Seu pedido foi registrado e estamos aguardando a confirmação do
        pagamento pelo banco ou operadora. Isso costuma levar poucos minutos
        no Pix; no cartão, pode demorar um pouco mais.
      </p>
      <p>
        Assim que o pagamento for confirmado, você receberá um aviso no
        e-mail informado no checkout. Se o pagamento não for concluído, o
        pedido é cancelado automaticamente e nada é cobrado.
      </p>
      <div className="order-status-page__actions">
        <ButtonLink href="/">Voltar ao início</ButtonLink>
      </div>
    </div>
  );
}
