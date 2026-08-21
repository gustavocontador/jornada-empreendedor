/**
 * POST /api/checkout
 *
 * Recebe os itens do carrinho + dados do cliente, revalida tudo
 * no servidor (preços vêm do catálogo, nunca do navegador),
 * registra o pedido e cria a cobrança no gateway de pagamento.
 *
 * Em MODO DE DEMONSTRAÇÃO (PAYMENT_PROVIDER=demo ou vazio):
 * o pedido é validado e registrado como demonstração, mas
 * NENHUMA cobrança real é criada e nada é apresentado como pago.
 */

import { NextResponse } from "next/server";
import { CheckoutValidationError, validateCheckout } from "@/lib/checkout";
import { notifyNewOrder } from "@/lib/notifications";
import { orderStore } from "@/lib/orders/store";
import {
  DemoModeError,
  getPaymentProvider,
  isDemoMode,
} from "@/lib/payment/provider";

export async function POST(request: Request) {
  let body: unknown;
  try {
    body = await request.json();
  } catch {
    return NextResponse.json(
      { error: "Corpo da requisição inválido." },
      { status: 400 }
    );
  }

  try {
    const checkout = validateCheckout(body);
    const provider = getPaymentProvider();

    const order = await orderStore.create({
      customer: checkout.customer,
      items: checkout.items,
      subtotalInCents: checkout.subtotalInCents,
      shippingInCents: checkout.shippingInCents,
      shippingOptionId: checkout.shippingOptionId,
      totalInCents: checkout.totalInCents,
      paymentMethod: checkout.paymentMethod,
      paymentStatus: "pending",
      isDemo: provider.isDemo,
    });

    // Avisa a equipe sobre o novo pedido (nunca derruba o checkout).
    await notifyNewOrder(order);

    if (provider.isDemo) {
      // Nunca simular um pagamento aprovado: o modo demo devolve
      // o pedido validado e informa claramente que nenhuma
      // cobrança foi criada.
      return NextResponse.json({
        demoMode: true,
        orderId: order.id,
        totalInCents: order.totalInCents,
        message:
          "Pedido validado com sucesso, mas o pagamento está em modo de " +
          "demonstração: nenhuma cobrança real foi criada.",
      });
    }

    const charge = await provider.createCharge(order);
    return NextResponse.json({
      demoMode: false,
      orderId: order.id,
      totalInCents: order.totalInCents,
      charge,
    });
  } catch (error) {
    if (error instanceof CheckoutValidationError) {
      return NextResponse.json(
        { error: error.message, fieldErrors: error.fieldErrors },
        { status: 422 }
      );
    }
    if (error instanceof DemoModeError) {
      return NextResponse.json({ error: error.message }, { status: 503 });
    }
    console.error("[checkout] erro inesperado:", error);
    return NextResponse.json(
      { error: "Não foi possível processar o pedido. Tente novamente." },
      { status: 500 }
    );
  }
}

/** GET /api/checkout — informa se a loja está em modo de demonstração */
export async function GET() {
  return NextResponse.json({ demoMode: isDemoMode() });
}
