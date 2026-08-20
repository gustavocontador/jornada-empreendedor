/**
 * GET /api/payment/status?orderId=...
 *
 * Consulta o status de pagamento de um pedido. A página de
 * "aguardando Pix" pode consultar este endpoint periodicamente.
 *
 * A fonte da verdade é o registro do pedido, atualizado pelo
 * webhook do gateway — nunca o navegador.
 */

import { NextResponse } from "next/server";
import { orderStore } from "@/lib/orders/store";

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const orderId = searchParams.get("orderId");
  if (!orderId) {
    return NextResponse.json(
      { error: "Informe o parâmetro orderId." },
      { status: 400 }
    );
  }

  const order = await orderStore.getById(orderId);
  if (!order) {
    return NextResponse.json(
      { error: "Pedido não encontrado." },
      { status: 404 }
    );
  }

  return NextResponse.json({
    orderId: order.id,
    paymentStatus: order.paymentStatus,
    isDemo: order.isDemo,
    updatedAt: order.updatedAt,
  });
}
