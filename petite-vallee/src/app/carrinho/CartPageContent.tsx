"use client";

import { useCart } from "@/lib/cart/CartContext";
import { formatPrice } from "@/lib/format";
import { buildWhatsAppOrderUrl } from "@/lib/whatsapp";
import { CartItem } from "@/components/CartItem";
import { CartShippingEstimate } from "@/components/CartShippingEstimate";
import { EmptyState } from "@/components/EmptyState";
import { LoadingState } from "@/components/LoadingState";
import { ButtonLink } from "@/components/Button";

/** Versão em página inteira do carrinho (além do drawer). */
export function CartPageContent() {
  const { items, subtotalInCents, clearCart, hydrated } = useCart();

  if (!hydrated) {
    return <LoadingState label="Carregando seu carrinho…" />;
  }

  if (items.length === 0) {
    return (
      <EmptyState
        title="Seu carrinho está vazio"
        description="Explore nossos produtos artesanais e escolha os seus favoritos."
        action={<ButtonLink href="/produtos">Ver produtos</ButtonLink>}
      />
    );
  }

  return (
    <div>
      <ul className="cart-drawer__items" style={{ padding: 0 }}>
        {items.map((item) => (
          <CartItem key={item.product.id} item={item} />
        ))}
      </ul>

      <div className="cart-drawer__footer" style={{ borderRadius: "var(--radius-lg)", marginTop: "var(--space-5)" }}>
        <CartShippingEstimate />
        <div className="cart-drawer__subtotal">
          <span>Subtotal</span>
          <strong>{formatPrice(subtotalInCents)}</strong>
        </div>
        <ButtonLink href="/checkout" className="btn--block">
          Finalizar compra
        </ButtonLink>
        <a
          href={buildWhatsAppOrderUrl(items, subtotalInCents)}
          target="_blank"
          rel="noopener noreferrer"
          className="cart-drawer__whatsapp-link"
        >
          ou feche seu pedido pelo WhatsApp
        </a>
        <div className="cart-drawer__secondary-actions">
          <ButtonLink href="/produtos" variant="ghost">
            Continuar comprando
          </ButtonLink>
          <button
            type="button"
            className="link-button link-button--danger"
            onClick={clearCart}
          >
            Esvaziar carrinho
          </button>
        </div>
      </div>
    </div>
  );
}
