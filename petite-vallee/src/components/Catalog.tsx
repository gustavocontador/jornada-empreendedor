"use client";

import { useState } from "react";
import { getProductsByCategory } from "@/data/products";
import { CategoryFilter, type CategoryFilterValue } from "./CategoryFilter";
import { ProductGrid } from "./ProductGrid";

interface CatalogProps {
  priorityCount?: number;
}

/** Vitrine completa: filtro de categorias + grade de produtos. */
export function Catalog({ priorityCount = 0 }: CatalogProps) {
  const [category, setCategory] = useState<CategoryFilterValue>("todos");
  const products = getProductsByCategory(category);

  return (
    <div className="catalog">
      <CategoryFilter value={category} onChange={setCategory} />
      <ProductGrid products={products} priorityCount={priorityCount} />
    </div>
  );
}
