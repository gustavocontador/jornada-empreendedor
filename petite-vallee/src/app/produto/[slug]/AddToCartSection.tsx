"use client";

import { useState } from "react";
import { useCart } from "@/lib/cart/CartContext";
import { Button } from "@/components/Button";

interface AddToCartSectionProps {
  productId: string;
  available: boolean;
}

/** Seletor de quantidade + botão de compra da página de produto. */
export function AddToCartSection({ productId, available }: AddToCartSectionProps) {
  const { addItem, openCart, lastAddedId, hydrated } = useCart();
  const [quantity, setQuantity] = useState(1);
  const justAdded = lastAddedId === productId;

  if (!available) {
    return (
      <p className="product-card__unavailable-note">
        Este produto está indisponível no momento. Avisaremos quando voltar.
      </p>
    );
  }

  return (
    <div className="product-card__footer" style={{ justifyContent: "flex-start" }}>
      <div className="quantity-stepper" role="group" aria-label="Quantidade">
        <button
          type="button"
          onClick={() => setQuantity((q) => Math.max(1, q - 1))}
          aria-label="Diminuir quantidade"
        >
          −
        </button>
        <span aria-live="polite">{quantity}</span>
        <button
          type="button"
          onClick={() => setQuantity((q) => Math.min(20, q + 1))}
          aria-label="Aumentar quantidade"
        >
          +
        </button>
      </div>
      <Button
        onClick={() => {
          addItem(productId, quantity);
          openCart();
        }}
        disabled={!hydrated}
      >
        {justAdded ? "Adicionado ✓" : "Adicionar ao carrinho"}
      </Button>
    </div>
  );
}
