"use client";

import {
  CATEGORY_LABELS,
  getActiveCategories,
  type ProductCategory,
} from "@/data/products";

export type CategoryFilterValue = ProductCategory | "todos";

interface CategoryFilterProps {
  value: CategoryFilterValue;
  onChange: (value: CategoryFilterValue) => void;
}

/**
 * Filtro de categorias em formato de "pills" acessíveis.
 * Mostra apenas categorias que têm produtos no catálogo — assim
 * a categoria "Geleias" some sozinha enquanto não houver uma
 * edição limitada à venda, e volta quando houver.
 */
export function CategoryFilter({ value, onChange }: CategoryFilterProps) {
  const options: Array<{ value: CategoryFilterValue; label: string }> = [
    { value: "todos", label: "Todos" },
    ...getActiveCategories().map((cat) => ({
      value: cat,
      label: CATEGORY_LABELS[cat],
    })),
  ];

  return (
    <div
      className="category-filter"
      role="group"
      aria-label="Filtrar produtos por categoria"
    >
      {options.map((option) => (
        <button
          key={option.value}
          type="button"
          className={`category-filter__pill${
            value === option.value ? " category-filter__pill--active" : ""
          }`}
          aria-pressed={value === option.value}
          onClick={() => onChange(option.value)}
        >
          {option.label}
        </button>
      ))}
    </div>
  );
}
