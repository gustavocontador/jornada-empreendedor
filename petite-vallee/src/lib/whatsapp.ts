/**
 * Pedido pelo WhatsApp.
 *
 * Enquanto o gateway de pagamento não está ativo (e mesmo depois,
 * como alternativa), o cliente pode fechar o pedido direto no
 * WhatsApp da Petite Vallée: o carrinho monta uma mensagem pronta
 * com itens, quantidades e subtotal.
 */

import { brand } from "@/lib/brand";
import { formatPrice } from "@/lib/format";
import type { CartItemView } from "@/lib/cart/CartContext";

export function buildWhatsAppOrderUrl(
  items: CartItemView[],
  subtotalInCents: number
): string {
  const lines = items.map(
    (item) =>
      `• ${item.quantity}× ${item.product.name} — ${formatPrice(item.lineTotalInCents)}`
  );
  const message = [
    "Olá, Petite Vallée! Quero fazer um pedido:",
    "",
    ...lines,
    "",
    `Subtotal: ${formatPrice(subtotalInCents)}`,
    "(frete a combinar)",
  ].join("\n");
  return `${brand.whatsappUrl}?text=${encodeURIComponent(message)}`;
}
