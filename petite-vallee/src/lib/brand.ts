/**
 * Referências centrais da marca.
 *
 * ⚠️ O arquivo em /public/brand/logo.svg é um PLACEHOLDER
 * tipográfico provisório. Quando o arquivo oficial do logotipo
 * for fornecido pela Petite Vallée:
 *   1. Salve-o em public/brand/ (ex.: logo.svg ou logo.png).
 *   2. Atualize os caminhos abaixo, se o nome mudar.
 *   3. Gere o favicon a partir do próprio arquivo oficial e
 *      substitua src/app/icon.svg.
 * Todos os usos (header, footer, Open Graph, dados estruturados)
 * leem deste arquivo, então a troca acontece em um único lugar.
 */

export const brand = {
  name: "Petite Vallée",
  tagline: "Granolas, mixes e barrinhas artesanais",
  logo: {
    src: "/brand/logo.svg",
    width: 360,
    height: 96,
    alt: "Petite Vallée",
    /** true enquanto o arquivo oficial não for adicionado */
    isPlaceholder: true,
  },
  instagramHandle: "@petitevallee.nuts",
  instagramUrl: "https://www.instagram.com/petitevallee.nuts",
  whatsappUrl: "https://wa.me/5511998280631",
  email: "petitevalle.nuts@gmail.com",
  phone: "(11) 99828-0631",
  city: "Valinhos",
  state: "SP",
} as const;

export function getSiteUrl(): string {
  return (
    process.env.NEXT_PUBLIC_SITE_URL?.replace(/\/$/, "") ||
    "http://localhost:3000"
  );
}
