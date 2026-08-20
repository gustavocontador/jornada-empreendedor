import type { Metadata } from "next";
import { PolicyPage } from "@/components/PolicyPage";

export const metadata: Metadata = {
  title: "Política de Privacidade",
  description: "Como a Petite Vallée trata os seus dados pessoais.",
  alternates: { canonical: "/politica-de-privacidade" },
};

export default function PoliticaPrivacidadePage() {
  return (
    <PolicyPage title="Política de Privacidade">
      <h2>Quais dados coletamos</h2>
      <p>
        Para processar seu pedido, coletamos apenas os dados necessários:
        nome, e-mail, telefone, endereço de entrega e, quando exigido pelo
        provedor de pagamento, CPF.
      </p>
      <h2>Como usamos os dados</h2>
      <p>
        Os dados são usados exclusivamente para processar pedidos, organizar
        entregas e manter contato sobre a sua compra. Não vendemos nem
        compartilhamos seus dados com terceiros para fins de marketing.
      </p>
      <h2>Pagamentos</h2>
      <p>
        Os dados de pagamento (como número de cartão) são processados
        diretamente pelo provedor de pagamento, em ambiente seguro, e nunca
        ficam armazenados em nossos servidores.
      </p>
      <h2>Seus direitos</h2>
      <p>
        Nos termos da Lei Geral de Proteção de Dados (LGPD), você pode
        solicitar a qualquer momento acesso, correção ou exclusão dos seus
        dados através da nossa página de contato.
      </p>
    </PolicyPage>
  );
}
