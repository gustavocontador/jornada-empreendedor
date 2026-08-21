"use client";

import Link from "next/link";
import { CATEGORY_LABELS, type Product } from "@/data/products";
import { formatPrice } from "@/lib/format";
import { useCart } from "@/lib/cart/CartContext";
import { ProductImage } from "./ProductImage";

interface ProductCardProps {
  product: Product;
  priority?: boolean;
}

/**
 * Card de produto: fotografia em destaque, categoria, nome,
 * descrição curta, preço e botão de compra com feedback
 * "Adicionado!". Produtos indisponíveis mantêm o card visível,
 * sem botão de compra.
 */
export function ProductCard({ product, priority = false }: ProductCardProps) {
  const { addItem, openCart, lastAddedId, hydrated } = useCart();
  const justAdded = lastAddedId === product.id;

  function handleAdd() {
    addItem(product.id);
    openCart();
  }

  return (
    <article className="product-card">
      <Link
        href={`/produto/${product.slug}`}
        className="product-card__media"
        aria-label={`Ver detalhes de ${product.name}`}
      >
        <ProductImage product={product} priority={priority} />
        {product.limited && (
          <span className="product-card__badge product-card__badge--limited">
            Edição limitada
          </span>
        )}
        {!product.available && (
          <span className="product-card__badge product-card__badge--unavailable">
            Indisponível no momento
          </span>
        )}
      </Link>

      <div className="product-card__body">
        <p className="product-card__category">
          {CATEGORY_LABELS[product.category]}
          {product.weightLabel && ` · ${product.weightLabel}`}
        </p>
        <h3 className="product-card__name">
          <Link href={`/produto/${product.slug}`}>{product.name}</Link>
        </h3>
        <p className="product-card__description">{product.shortDescription}</p>

        <div className="product-card__footer">
          <p className="product-card__price">
            {formatPrice(product.priceInCents)}
          </p>

          {product.available ? (
            <button
              type="button"
              className={`btn btn--primary btn--small${justAdded ? " btn--added" : ""}`}
              onClick={handleAdd}
              disabled={!hydrated}
              aria-label={
                justAdded
                  ? `${product.name} adicionado ao carrinho`
                  : `Adicionar ${product.name} ao carrinho`
              }
            >
              <span aria-hidden="true">
                {justAdded ? "Adicionado ✓" : "Adicionar ao carrinho"}
              </span>
            </button>
          ) : (
            <span className="product-card__unavailable-note">
              Avisaremos quando voltar
            </span>
          )}
        </div>
      </div>
    </article>
  );
}
