/**
 * POST /api/webhooks/payment
 *
 * Endpoint que o gateway de pagamento chama para notificar
 * mudanças de status (pago, recusado, cancelado, expirado,
 * reembolsado).
 *
 * A confirmação REAL de pagamento vem exclusivamente daqui —
 * nunca do fato de o cliente ter chegado à página de sucesso.
 *
 * Cada provedor tem seu próprio mecanismo de autenticação
 * (assinatura HMAC com PAYMENT_WEBHOOK_SECRET, token em header,
 * etc.); a validação é delegada a `provider.verifyWebhook()`,
 * implementada junto com o gateway escolhido.
 */

import { NextResponse } from "next/server";
import { orderStore } from "@/lib/orders/store";
import { getPaymentProvider } from "@/lib/payment/provider";

export async function POST(request: Request) {
  const provider = getPaymentProvider();

  if (provider.isDemo) {
    // Em modo demo nenhum gateway está configurado; qualquer
    // notificação recebida é ignorada por segurança.
    return NextResponse.json(
      { error: "Nenhum gateway de pagamento configurado." },
      { status: 503 }
    );
  }

  const rawBody = await request.text();
  const verification = await provider.verifyWebhook(rawBody, request.headers);

  if (!verification.valid) {
    console.warn("[webhook] notificação com assinatura inválida rejeitada");
    return NextResponse.json({ error: "Assinatura inválida." }, { status: 401 });
  }

  if (!verification.providerChargeId || !verification.status) {
    return NextResponse.json({ received: true });
  }

  const order = await orderStore.getByProviderId(verification.providerChargeId);
  if (!order) {
    console.warn(
      `[webhook] cobrança ${verification.providerChargeId} sem pedido associado`
    );
    return NextResponse.json({ received: true });
  }

  await orderStore.updateStatus(order.id, verification.status);
  return NextResponse.json({ received: true });
}
