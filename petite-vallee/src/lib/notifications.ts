/**
 * Notificação de novo pedido para a equipe da Petite Vallée.
 *
 * Sempre que um pedido é registrado no checkout, a loja é avisada
 * por e-mail — assim nenhum pedido fica esquecido.
 *
 * COMO ATIVAR (gratuito):
 *   1. Crie uma conta em https://resend.com (plano gratuito:
 *      100 e-mails/dia — muito mais que o necessário).
 *   2. Gere uma API Key e defina no .env.local / hospedagem:
 *        RESEND_API_KEY=re_...
 *        ORDER_NOTIFY_EMAIL=petitevalle.nuts@gmail.com
 *   3. (Opcional) Verifique o domínio próprio no Resend e defina
 *        ORDER_NOTIFY_FROM="Petite Vallée <pedidos@seudominio>"
 *      Sem isso, usa o remetente de testes do Resend.
 *
 * Enquanto as variáveis não existirem, a notificação é apenas
 * registrada no log do servidor. O envio NUNCA derruba o
 * checkout: qualquer falha aqui é só registrada.
 */

import { formatPrice } from "@/lib/format";
import type { Order } from "@/lib/orders/types";

export async function notifyNewOrder(order: Order): Promise<void> {
  const summaryLines = [
    order.isDemo
      ? "⚠️ PEDIDO DE DEMONSTRAÇÃO — nenhum pagamento real foi criado."
      : "Novo pedido recebido!",
    "",
    `Pedido: ${order.id}`,
    `Cliente: ${order.customer.fullName}`,
    `E-mail: ${order.customer.email}`,
    `Telefone: ${order.customer.phone}`,
    "",
    "Itens:",
    ...order.items.map(
      (item) =>
        `  • ${item.quantity}× ${item.name} — ${formatPrice(item.lineTotalInCents)}`
    ),
    "",
    `Subtotal: ${formatPrice(order.subtotalInCents)}`,
    `Frete: ${formatPrice(order.shippingInCents)}`,
    `Total: ${formatPrice(order.totalInCents)}`,
    `Pagamento: ${order.paymentMethod === "pix" ? "Pix" : "Cartão de crédito"} (${order.paymentStatus})`,
    "",
    `Entrega: ${order.customer.address.street}, ${order.customer.address.number}` +
      (order.customer.address.complement ? ` (${order.customer.address.complement})` : "") +
      ` — ${order.customer.address.neighborhood}, ${order.customer.address.city}/${order.customer.address.state} — CEP ${order.customer.address.cep}`,
    order.customer.notes ? `Observações: ${order.customer.notes}` : "",
  ]
    .filter((line) => line !== "")
    .join("\n");

  const apiKey = process.env.RESEND_API_KEY;
  const to = process.env.ORDER_NOTIFY_EMAIL;

  if (!apiKey || !to) {
    console.log(
      "[pedido] notificação por e-mail inativa (defina RESEND_API_KEY e " +
        "ORDER_NOTIFY_EMAIL). Resumo do pedido:\n" +
        summaryLines
    );
    return;
  }

  try {
    const response = await fetch("https://api.resend.com/emails", {
      method: "POST",
      headers: {
        Authorization: `Bearer ${apiKey}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        from:
          process.env.ORDER_NOTIFY_FROM ||
          "Petite Vallée <onboarding@resend.dev>",
        to: [to],
        subject: order.isDemo
          ? `[TESTE] Pedido de demonstração — ${formatPrice(order.totalInCents)}`
          : `🌿 Novo pedido — ${formatPrice(order.totalInCents)}`,
        text: summaryLines,
      }),
    });
    if (!response.ok) {
      console.error(
        "[pedido] falha ao enviar notificação:",
        response.status,
        await response.text()
      );
    }
  } catch (error) {
    console.error("[pedido] erro ao enviar notificação:", error);
  }
}
