/**
 * POST /api/payment/create
 *
 * Cria (ou recria) a cobrança de um pedido já registrado — por
 * exemplo, quando o cliente volta para pagar um Pix expirado.
 * A cobrança é sempre criada no servidor com o total oficial do
 * pedido; nenhum valor vindo do navegador é utilizado.
 */

import { NextResponse } from "next/server";
import { orderStore } from "@/lib/orders/store";
import { DemoModeError, getPaymentProvider } from "@/lib/payment/provider";

export async function POST(request: Request) {
  let body: { orderId?: string };
  try {
    body = await request.json();
  } catch {
    return NextResponse.json(
      { error: "Corpo da requisição inválido." },
      { status: 400 }
    );
  }

  const order = body.orderId ? await orderStore.getById(body.orderId) : undefined;
  if (!order) {
    return NextResponse.json(
      { error: "Pedido não encontrado." },
      { status: 404 }
    );
  }

  const provider = getPaymentProvider();
  if (provider.isDemo) {
    return NextResponse.json(
      {
        demoMode: true,
        error:
          "O pagamento está em modo de demonstração: nenhuma cobrança " +
          "real pode ser criada.",
      },
      { status: 503 }
    );
  }

  try {
    const charge = await provider.createCharge(order);
    return NextResponse.json({ orderId: order.id, charge });
  } catch (error) {
    if (error instanceof DemoModeError) {
      return NextResponse.json({ error: error.message }, { status: 503 });
    }
    console.error("[payment/create] erro:", error);
    return NextResponse.json(
      { error: "Não foi possível criar a cobrança. Tente novamente." },
      { status: 502 }
    );
  }
}
