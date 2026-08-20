"use client";

import { useCart } from "@/lib/cart/CartContext";
import { formatPrice } from "@/lib/format";
import { CartItem } from "@/components/CartItem";
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
        <div className="cart-drawer__subtotal">
          <span>Subtotal</span>
          <strong>{formatPrice(subtotalInCents)}</strong>
        </div>
        <p className="cart-drawer__note">
          Frete e entrega serão definidos no checkout.
        </p>
        <ButtonLink href="/checkout" className="btn--block">
          Finalizar compra
        </ButtonLink>
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
