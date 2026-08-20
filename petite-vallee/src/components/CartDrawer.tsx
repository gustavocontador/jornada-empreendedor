"use client";

import Link from "next/link";
import { useRef } from "react";
import { formatPrice } from "@/lib/format";
import { useCart } from "@/lib/cart/CartContext";
import { useFocusTrap } from "@/lib/useFocusTrap";
import { CartItem } from "./CartItem";
import { EmptyState } from "./EmptyState";
import { ButtonLink } from "./Button";

/**
 * Carrinho lateral (drawer). Acessível: role="dialog", trava de
 * foco enquanto aberto, fecha com Escape/backdrop e devolve o
 * foco ao botão que o abriu.
 */
export function CartDrawer() {
  const { isOpen, closeCart, items, subtotalInCents, clearCart } = useCart();
  const panelRef = useRef<HTMLDivElement>(null);
  useFocusTrap(panelRef, isOpen, closeCart);

  if (!isOpen) return null;

  return (
    <div className="cart-drawer">
      <div
        className="cart-drawer__backdrop"
        onClick={closeCart}
        aria-hidden="true"
      />
      <div
        ref={panelRef}
        className="cart-drawer__panel"
        role="dialog"
        aria-modal="true"
        aria-label="Carrinho de compras"
      >
        <header className="cart-drawer__header">
          <h2 className="cart-drawer__title">Seu carrinho</h2>
          <button
            type="button"
            className="cart-drawer__close"
            onClick={closeCart}
            aria-label="Fechar carrinho"
          >
            <svg width="18" height="18" viewBox="0 0 18 18" aria-hidden="true">
              <path
                d="M2 2l14 14M16 2L2 16"
                stroke="currentColor"
                strokeWidth="1.6"
                strokeLinecap="round"
              />
            </svg>
          </button>
        </header>

        {items.length === 0 ? (
          <div className="cart-drawer__empty">
            <EmptyState
              title="Seu carrinho está vazio"
              description="Explore nossos produtos artesanais e escolha os seus favoritos."
              action={
                <button type="button" className="btn btn--secondary" onClick={closeCart}>
                  <span>Continuar comprando</span>
                </button>
              }
            />
          </div>
        ) : (
          <>
            <ul className="cart-drawer__items">
              {items.map((item) => (
                <CartItem key={item.product.id} item={item} />
              ))}
            </ul>

            <footer className="cart-drawer__footer">
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
                <button type="button" className="link-button" onClick={closeCart}>
                  Continuar comprando
                </button>
                <button
                  type="button"
                  className="link-button link-button--danger"
                  onClick={clearCart}
                >
                  Esvaziar carrinho
                </button>
              </div>
              <Link href="/carrinho" className="cart-drawer__full-link" onClick={closeCart}>
                Ver página do carrinho
              </Link>
            </footer>
          </>
        )}
      </div>
    </div>
  );
}
