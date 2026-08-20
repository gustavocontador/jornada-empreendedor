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
 *   2. Dê um `id` único (ex.: "pv-006") e um `slug` amigável
 *      (letras minúsculas e hífens; ele vira a URL
 *      /produto/<slug>).
 *   3. Preencha nome, categoria, descrições e preço.
 *   4. Salve a foto em `public/images/products/` e aponte o
 *      campo `image` para ela (ex.: "/images/products/nova.jpg").
 *
 * COMO REMOVER UM PRODUTO:
 *   Apague o objeto correspondente da lista (ou marque
 *   `available: false` para apenas ocultar o botão de compra).
 *
 * COMO ALTERAR UM PREÇO:
 *   Edite `priceInCents`. O valor é SEMPRE em centavos para
 *   evitar erros de arredondamento:
 *     R$ 29,90  →  priceInCents: 2990
 *     R$ 8,50   →  priceInCents: 850
 *
 * COMO TROCAR UMA IMAGEM:
 *   Substitua o arquivo em `public/images/products/` mantendo o
 *   mesmo nome, ou atualize o campo `image` com o novo caminho.
 *
 * COMO MARCAR UM PRODUTO COMO INDISPONÍVEL:
 *   Defina `available: false`. O card continua visível com o
 *   aviso "Indisponível no momento" e sem botão de compra.
 *
 * COMO DESTACAR UM PRODUTO NA PÁGINA INICIAL:
 *   Defina `featured: true`. Produtos destacados aparecem
 *   primeiro na vitrine da home.
 *
 * IMPORTANTE — dados ainda não fornecidos oficialmente:
 *   Os preços e descrições abaixo são PROVISÓRIOS e estão
 *   marcados como tal. Peso, ingredientes, tabela nutricional e
 *   validade só devem ser adicionados quando forem fornecidos
 *   pela Petite Vallée — nunca inventados.
 * ═══════════════════════════════════════════════════════════════
 */

export type ProductCategory = "granolas" | "mixes" | "geleias";

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
}

export const CATEGORY_LABELS: Record<ProductCategory, string> = {
  granolas: "Granolas",
  mixes: "Mixes",
  geleias: "Geleias",
};

export const products: Product[] = [
  {
    id: "pv-001",
    slug: "granola-tradicional",
    name: "Granola Tradicional",
    category: "granolas",
    // [PROVISÓRIO] descrição aguardando texto oficial
    shortDescription:
      "Nossa granola clássica, assada de forma artesanal em pequenos lotes.",
    description:
      "A receita que apresenta a Petite Vallée: uma granola crocante, " +
      "assada de forma artesanal em pequenos lotes, para acompanhar frutas, " +
      "iogurtes e o seu café da manhã. (Descrição provisória — o texto " +
      "oficial, com ingredientes e peso, será publicado em breve.)",
    priceInCents: 2990, // [PROVISÓRIO] R$ 29,90 — aguardando preço oficial
    image: "/images/products/granola-tradicional.svg",
    imageIsPlaceholder: true,
    available: true,
    featured: true,
  },
  {
    id: "pv-002",
    slug: "granola-naturel",
    name: "Granola Naturel",
    category: "granolas",
    // [PROVISÓRIO] descrição aguardando texto oficial
    shortDescription:
      "Uma versão leve e delicada da nossa granola, feita à mão.",
    description:
      "A Granola Naturel é a versão mais leve e delicada da casa, preparada " +
      "à mão com o mesmo cuidado artesanal de sempre. (Descrição provisória — " +
      "o texto oficial, com ingredientes e peso, será publicado em breve.)",
    priceInCents: 3190, // [PROVISÓRIO] R$ 31,90 — aguardando preço oficial
    image: "/images/products/granola-naturel.svg",
    imageIsPlaceholder: true,
    available: true,
    featured: true,
  },
  {
    id: "pv-003",
    slug: "mix-de-castanhas",
    name: "Mix de Castanhas",
    category: "mixes",
    // [PROVISÓRIO] descrição aguardando texto oficial
    shortDescription:
      "Seleção artesanal de castanhas para o dia a dia e para receber bem.",
    description:
      "Uma seleção artesanal de castanhas, pensada para o lanche do dia a " +
      "dia, para a tábua de queijos e para receber bem. (Descrição " +
      "provisória — o texto oficial, com composição e peso, será publicado " +
      "em breve.)",
    priceInCents: 3490, // [PROVISÓRIO] R$ 34,90 — aguardando preço oficial
    image: "/images/products/mix-de-castanhas.svg",
    imageIsPlaceholder: true,
    available: true,
    featured: true,
  },
  {
    id: "pv-004",
    slug: "mix-de-sementes",
    name: "Mix de Sementes",
    category: "mixes",
    // [PROVISÓRIO] descrição aguardando texto oficial
    shortDescription:
      "Combinação de sementes selecionadas para saladas, frutas e iogurtes.",
    description:
      "Uma combinação de sementes selecionadas para enriquecer saladas, " +
      "frutas, iogurtes e pães. (Descrição provisória — o texto oficial, " +
      "com composição e peso, será publicado em breve.)",
    priceInCents: 2690, // [PROVISÓRIO] R$ 26,90 — aguardando preço oficial
    image: "/images/products/mix-de-sementes.svg",
    imageIsPlaceholder: true,
    available: true,
    featured: true,
  },
  {
    id: "pv-005",
    slug: "geleia-de-morango",
    name: "Geleia de Morango",
    category: "geleias",
    // [PROVISÓRIO] descrição aguardando texto oficial
    shortDescription:
      "Geleia artesanal de morango, feita em panelas pequenas, sem pressa.",
    description:
      "Nossa geleia de morango é feita de forma artesanal, em panelas " +
      "pequenas e sem pressa, para acompanhar pães, torradas e a granola da " +
      "casa. (Descrição provisória — o texto oficial, com ingredientes e " +
      "peso, será publicado em breve.)",
    priceInCents: 2490, // [PROVISÓRIO] R$ 24,90 — aguardando preço oficial
    image: "/images/products/geleia-de-morango.svg",
    imageIsPlaceholder: true,
    available: true,
    featured: true,
  },
];

/** Busca um produto pelo slug (usado nas páginas /produto/[slug]) */
export function getProductBySlug(slug: string): Product | undefined {
  return products.find((p) => p.slug === slug);
}

/** Busca um produto pelo id (usado na validação do servidor) */
export function getProductById(id: string): Product | undefined {
  return products.find((p) => p.id === id);
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
