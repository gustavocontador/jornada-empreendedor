"use client";

import { CATEGORY_LABELS, type ProductCategory } from "@/data/products";

export type CategoryFilterValue = ProductCategory | "todos";

interface CategoryFilterProps {
  value: CategoryFilterValue;
  onChange: (value: CategoryFilterValue) => void;
}

const OPTIONS: Array<{ value: CategoryFilterValue; label: string }> = [
  { value: "todos", label: "Todos" },
  ...(Object.entries(CATEGORY_LABELS) as Array<[ProductCategory, string]>).map(
    ([value, label]) => ({ value, label })
  ),
];

/** Filtro de categorias em formato de "pills" acessíveis. */
export function CategoryFilter({ value, onChange }: CategoryFilterProps) {
  return (
    <div
      className="category-filter"
      role="group"
      aria-label="Filtrar produtos por categoria"
    >
      {OPTIONS.map((option) => (
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
