/**
 * ═══════════════════════════════════════════════════════════════
 * CATÁLOGO DA PETITE VALLÉE
 * ───────────────────────────────────────────────────────────────
 * Este é o único arquivo que precisa ser editado para gerenciar
 * os produtos da loja. Nenhum banco de dados é necessário nesta
 * primeira versão.
 *
 * COMO ADICIONAR UM PRODUTO:
 *   1. Copie um dos objetos abaixo e cole no final da lista.
 *   2. Dê um `id` único (ex.: "pv-009") e um `slug` amigável
 *      (letras minúsculas e hífens; ele vira a URL
 *      /produto/<slug>).
 *   3. Preencha nome, categoria, descrições, preço, ingredientes
 *      e tabela nutricional (dados oficiais do rótulo).
 *   4. Salve a foto em `public/images/products/` e aponte o
 *      campo `image` para ela (ex.: "/images/products/nova.jpg").
 *
 * COMO REMOVER UM PRODUTO:
 *   Apague o objeto correspondente da lista (ou marque
 *   `available: false` para apenas ocultar o botão de compra).
 *
 * COMO ALTERAR UM PREÇO:
 *   Edite `priceInCents`. O valor é SEMPRE em centavos:
 *     R$ 29,90  →  priceInCents: 2990
 *
 * PRODUTOS DE EDIÇÃO LIMITADA (ex.: geleias):
 *   As geleias saíram do catálogo fixo e voltarão de tempos em
 *   tempos. Quando uma edição limitada entrar, adicione o
 *   produto normalmente com `limited: true` — o card exibirá a
 *   etiqueta "Edição limitada". Quando acabar, remova o objeto
 *   ou marque `available: false`.
 *
 * COMO DESTACAR UM PRODUTO NA PÁGINA INICIAL:
 *   Defina `featured: true`. Produtos destacados aparecem
 *   primeiro na vitrine.
 *
 * FONTE DOS DADOS:
 *   Ingredientes, porções, tabela nutricional, peso e validade
 *   vêm dos rótulos oficiais fornecidos pela Petite Vallée
 *   (ago/2026). Os PREÇOS seguem provisórios até confirmação.
 * ═══════════════════════════════════════════════════════════════
 */

export type ProductCategory = "granolas" | "mixes" | "barrinhas" | "geleias";

export interface NutritionFacts {
  /** rótulo da porção, ex.: "40g" */
  portionLabel: string;
  energyKcal: number;
  carbsG: number;
  proteinG: number;
  totalFatG: number;
  fiberG: number;
}

export interface Product {
  id: string;
  slug: string;
  name: string;
  category: ProductCategory;
  shortDescription: string;
  description?: string;
  priceInCents: number;
  image: string;
  /** true enquanto a foto oficial do produto não for adicionada */
  imageIsPlaceholder?: boolean;
  available: boolean;
  featured: boolean;
  /** edição limitada (ex.: geleias sazonais) — exibe etiqueta no card */
  limited?: boolean;
  /** peso exibido ao cliente, ex.: "300g" ou "200g · 10 unidades" */
  weightLabel?: string;
  /** lista oficial de ingredientes, na ordem do rótulo */
  ingredients?: string[];
  nutrition?: NutritionFacts;
  /** selos oficiais do rótulo, ex.: "Sem conservantes" */
  badges?: string[];
  /** validade indicada no rótulo, ex.: "45 dias" */
  shelfLife?: string;
}

export const CATEGORY_LABELS: Record<ProductCategory, string> = {
  granolas: "Granolas",
  mixes: "Mixes",
  barrinhas: "Barrinhas",
  geleias: "Geleias",
};

const COMMON_BADGES = ["Sem conservantes", "Sem glúten"];

export const products: Product[] = [
  {
    id: "pv-001",
    slug: "granola-tradicional",
    name: "Granola Tradicional",
    category: "granolas",
    // [PROVISÓRIO] descrição aguardando texto manuscrito da cliente
    shortDescription:
      "A clássica da casa: crocante, dourada no forno em pequenos lotes.",
    description:
      "Granola assada em pequenos lotes até o ponto certo de crocância, " +
      "adoçada com açúcar de coco e melado de cana. Vai bem com iogurte, " +
      "frutas, açaí — ou direto do pote.",
    priceInCents: 2990, // [PROVISÓRIO] R$ 29,90 — aguardando preço oficial
    image: "/images/products/granola-tradicional.svg",
    imageIsPlaceholder: true,
    available: true,
    featured: true,
    weightLabel: "300g",
    ingredients: [
      "Aveia Flocos Grossos",
      "Óleo de Coco Orgânico",
      "Extrato de Baunilha",
      "Uva Passa Preta",
      "Uva Passa Branca",
      "Mix de Castanhas",
      "Fita de Coco",
      "Cranberry",
      "Açúcar de Coco",
      "Melado de Cana",
      "Sal",
    ],
    nutrition: {
      portionLabel: "40g",
      energyKcal: 183.4,
      carbsG: 24.7,
      proteinG: 4.1,
      totalFatG: 8.4,
      fiberG: 2.8,
    },
    badges: COMMON_BADGES,
    shelfLife: "45 dias",
  },
  {
    id: "pv-002",
    slug: "granola-naturel",
    name: "Granola Naturel",
    category: "granolas",
    // [PROVISÓRIO] descrição aguardando texto manuscrito da cliente
    shortDescription:
      "Leve e delicada, adoçada com eritritol, para o dia a dia.",
    description:
      "A versão mais leve da nossa granola, adoçada com eritritol, de " +
      "sabor suave para comer todo dia sem enjoar.",
    priceInCents: 3190, // [PROVISÓRIO] R$ 31,90 — aguardando preço oficial
    image: "/images/products/granola-naturel.svg",
    imageIsPlaceholder: true,
    available: true,
    featured: true,
    weightLabel: "300g",
    ingredients: [
      "Aveia Flocos Grossos",
      "Óleo de Coco Orgânico",
      "Extrato de Baunilha",
      "Uva Passa Preta",
      "Uva Passa Branca",
      "Mix de Castanhas",
      "Fita de Coco",
      "Cranberry",
      "Eritritol",
      "Sal",
    ],
    nutrition: {
      portionLabel: "40g",
      energyKcal: 176.2,
      carbsG: 24.4,
      proteinG: 4.4,
      totalFatG: 9.0,
      fiberG: 3.0,
    },
    badges: COMMON_BADGES,
    shelfLife: "45 dias",
  },
  {
    id: "pv-006",
    slug: "granola-sans-sucre",
    name: "Granola Sans Sucre",
    category: "granolas",
    // [PROVISÓRIO] descrição aguardando texto manuscrito da cliente
    shortDescription:
      "Sem adição de açúcar: a doçura fica por conta das tâmaras.",
    description:
      "Granola sem adição de açúcar — a doçura vem das tâmaras e das " +
      "frutas secas. Crocância artesanal para o café da manhã de todo dia.",
    priceInCents: 3290, // [PROVISÓRIO] R$ 32,90 — aguardando preço oficial
    image: "/images/products/granola-sans-sucre.svg",
    imageIsPlaceholder: true,
    available: true,
    featured: true,
    weightLabel: "300g",
    ingredients: [
      "Aveia Flocos Grossos",
      "Óleo de Coco Orgânico",
      "Extrato de Baunilha",
      "Uva Passa Preta",
      "Uva Passa Branca",
      "Mix de Castanhas",
      "Fita de Coco",
      "Cranberry",
      "Tâmaras",
      "Sal",
    ],
    nutrition: {
      portionLabel: "40g",
      energyKcal: 183.4,
      carbsG: 24.7,
      proteinG: 4.1,
      totalFatG: 8.4,
      fiberG: 2.8,
    },
    badges: COMMON_BADGES,
    shelfLife: "45 dias",
  },
  {
    id: "pv-003",
    slug: "mix-de-castanhas",
    name: "Mix de Castanhas",
    category: "mixes",
    // [PROVISÓRIO] descrição aguardando texto manuscrito da cliente
    shortDescription:
      "Sete castanhas selecionadas, com pecan caramelizada no meio.",
    description:
      "Castanhas selecionadas na medida — com direito a pecan " +
      "caramelizada — para o lanche da tarde, a tábua de queijos ou " +
      "aquela visita de última hora.",
    priceInCents: 3490, // [PROVISÓRIO] R$ 34,90 — aguardando preço oficial
    image: "/images/products/mix-de-castanhas.svg",
    imageIsPlaceholder: true,
    available: true,
    featured: true,
    weightLabel: "300g",
    ingredients: [
      "Castanha de Caju",
      "Pistache",
      "Castanha do Pará",
      "Pecan Caramelizada",
      "Nozes Mariposa",
      "Avelã",
      "Amêndoa",
      "Sal",
    ],
    nutrition: {
      portionLabel: "30g",
      energyKcal: 183.1,
      carbsG: 6.3,
      proteinG: 4.8,
      totalFatG: 16.8,
      fiberG: 2.2,
    },
    badges: COMMON_BADGES,
    shelfLife: "45 dias",
  },
  {
    id: "pv-004",
    slug: "mix-de-sementes",
    name: "Mix de Sementes",
    category: "mixes",
    // [PROVISÓRIO] descrição aguardando texto manuscrito da cliente
    shortDescription:
      "Abóbora e girassol tostadas com sal, para incrementar qualquer prato.",
    description:
      "Sementes de abóbora e girassol com um toque de sal — crocância e " +
      "sabor para saladas, frutas, iogurtes e pães.",
    priceInCents: 2690, // [PROVISÓRIO] R$ 26,90 — aguardando preço oficial
    image: "/images/products/mix-de-sementes.svg",
    imageIsPlaceholder: true,
    available: true,
    featured: true,
    weightLabel: "300g",
    ingredients: ["Semente de Abóbora", "Semente de Girassol", "Sal"],
    nutrition: {
      portionLabel: "30g",
      energyKcal: 171.4,
      carbsG: 4.6,
      proteinG: 7.7,
      totalFatG: 15.0,
      fiberG: 2.2,
    },
    badges: COMMON_BADGES,
    shelfLife: "45 dias",
  },
  {
    id: "pv-007",
    slug: "barrinha-petite-sucree",
    name: "Barrinha Petite Sucrée",
    category: "barrinhas",
    // [PROVISÓRIO] descrição aguardando texto manuscrito da cliente
    shortDescription:
      "A barrinha da casa: 10 unidades para levar para qualquer lugar.",
    description:
      "A barrinha artesanal da Petite Vallée: chia, sementes, noz pecan e " +
      "cranberry, adoçada com eritritol. Caixa com 10 unidades, para a " +
      "bolsa, a mochila e a gaveta do escritório.",
    priceInCents: 2990, // [PROVISÓRIO] R$ 29,90 — aguardando preço oficial
    image: "/images/products/barrinha-petite-sucree.svg",
    imageIsPlaceholder: true,
    available: true,
    featured: true,
    weightLabel: "200g · 10 unidades",
    ingredients: [
      "Chia",
      "Semente de Abóbora",
      "Noz Pecan",
      "Eritritol",
      "Cranberry",
      "Óleo de Coco",
      "Extrato de Baunilha",
      "Sal",
    ],
    nutrition: {
      portionLabel: "20g",
      energyKcal: 90,
      carbsG: 8.4,
      proteinG: 2.7,
      totalFatG: 7.1,
      fiberG: 1.9,
    },
    badges: COMMON_BADGES,
    shelfLife: "45 dias",
  },
  // ── Geleias: edição limitada ──
  // As geleias (morango, mirtilo, frutas vermelhas) voltarão de
  // tempos em tempos. Quando houver uma edição disponível,
  // adicione-a aqui com `category: "geleias"` e `limited: true`.
];

/** Busca um produto pelo slug (usado nas páginas /produto/[slug]) */
export function getProductBySlug(slug: string): Product | undefined {
  return products.find((p) => p.slug === slug);
}

/** Busca um produto pelo id (usado na validação do servidor) */
export function getProductById(id: string): Product | undefined {
  return products.find((p) => p.id === id);
}

/** Categorias que possuem ao menos um produto (para o filtro) */
export function getActiveCategories(): ProductCategory[] {
  return (Object.keys(CATEGORY_LABELS) as ProductCategory[]).filter((cat) =>
    products.some((p) => p.category === cat)
  );
}

/** Produtos de uma categoria, destacados primeiro */
export function getProductsByCategory(
  category: ProductCategory | "todos"
): Product[] {
  const list =
    category === "todos"
      ? products
      : products.filter((p) => p.category === category);
  return [...list].sort(
    (a, b) => Number(b.featured) - Number(a.featured)
  );
}
