"use client";

import Image from "next/image";
import { formatPrice } from "@/lib/format";
import { useCart, type CartItemView } from "@/lib/cart/CartContext";

interface CartItemProps {
  item: CartItemView;
}

/** Linha de item no carrinho: foto, nome, quantidade e remoção. */
export function CartItem({ item }: CartItemProps) {
  const { setQuantity, removeItem } = useCart();
  const { product, quantity } = item;

  return (
    <li className="cart-item">
      <div className="cart-item__media">
        <Image
          src={product.image}
          alt=""
          width={72}
          height={72}
          unoptimized={product.image.endsWith(".svg")}
        />
      </div>
      <div className="cart-item__info">
        <p className="cart-item__name">{product.name}</p>
        <p className="cart-item__unit-price">
          {formatPrice(product.priceInCents)} cada
        </p>
        <div className="cart-item__controls">
          <div
            className="quantity-stepper"
            role="group"
            aria-label={`Quantidade de ${product.name}`}
          >
            <button
              type="button"
              onClick={() => setQuantity(product.id, quantity - 1)}
              aria-label={`Diminuir quantidade de ${product.name}`}
            >
              −
            </button>
            <span aria-live="polite">{quantity}</span>
            <button
              type="button"
              onClick={() => setQuantity(product.id, quantity + 1)}
              aria-label={`Aumentar quantidade de ${product.name}`}
            >
              +
            </button>
          </div>
          <button
            type="button"
            className="cart-item__remove"
            onClick={() => removeItem(product.id)}
          >
            Remover
          </button>
        </div>
      </div>
      <p className="cart-item__total">{formatPrice(item.lineTotalInCents)}</p>
    </li>
  );
}
