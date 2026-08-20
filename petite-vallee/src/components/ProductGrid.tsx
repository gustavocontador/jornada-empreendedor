import type { Product } from "@/data/products";
import { ProductCard } from "./ProductCard";
import { EmptyState } from "./EmptyState";

interface ProductGridProps {
  products: Product[];
  /** prioriza o carregamento das primeiras imagens (acima da dobra) */
  priorityCount?: number;
}

export function ProductGrid({ products, priorityCount = 0 }: ProductGridProps) {
  if (products.length === 0) {
    return (
      <EmptyState
        title="Nenhum produto nesta categoria"
        description="Escolha outra categoria para continuar explorando."
      />
    );
  }
  return (
    <ul className="product-grid">
      {products.map((product, index) => (
        <li key={product.id}>
          <ProductCard product={product} priority={index < priorityCount} />
        </li>
      ))}
    </ul>
  );
}
