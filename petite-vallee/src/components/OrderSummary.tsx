"use client";

import { formatPrice } from "@/lib/format";
import type { CartItemView } from "@/lib/cart/CartContext";
import type { ShippingOption } from "@/lib/shipping";

interface OrderSummaryProps {
  items: CartItemView[];
  shippingOption?: ShippingOption;
}

/** Resumo do pedido exibido no checkout. */
export function OrderSummary({ items, shippingOption }: OrderSummaryProps) {
  const subtotal = items.reduce((sum, i) => sum + i.lineTotalInCents, 0);
  const shipping = shippingOption?.priceInCents ?? 0;

  return (
    <aside className="order-summary" aria-label="Resumo do pedido">
      <h2 className="order-summary__title">Resumo do pedido</h2>
      <ul className="order-summary__items">
        {items.map((item) => (
          <li key={item.product.id} className="order-summary__item">
            <span className="order-summary__item-name">
              {item.quantity}× {item.product.name}
            </span>
            <span>{formatPrice(item.lineTotalInCents)}</span>
          </li>
        ))}
      </ul>
      <dl className="order-summary__totals">
        <div>
          <dt>Subtotal</dt>
          <dd>{formatPrice(subtotal)}</dd>
        </div>
        <div>
          <dt>Frete</dt>
          <dd>
            {shippingOption
              ? shippingOption.isDemo
                ? "a definir"
                : formatPrice(shipping)
              : "—"}
          </dd>
        </div>
        <div className="order-summary__grand-total">
          <dt>Total</dt>
          <dd>{formatPrice(subtotal + shipping)}</dd>
        </div>
      </dl>
      <p className="order-summary__note">
        Os valores são conferidos novamente com segurança antes do
        pagamento.
      </p>
    </aside>
  );
}
