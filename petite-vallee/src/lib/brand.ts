/**
 * Referências centrais da marca.
 *
 * LOGOTIPO OFICIAL (ago/2026): emblema circular "Nuts — Petite
 * Vallée". O arquivo deve existir em public/brand/logo.png,
 * recortado em QUADRADO com o círculo centralizado. Para trocar
 * a logo no futuro, basta substituir esse arquivo (mesmo nome).
 * Todos os usos (header, footer, Open Graph, dados estruturados)
 * leem deste arquivo, então a troca acontece em um único lugar.
 */

export const brand = {
  name: "Petite Vallée",
  tagline: "Granolas, mixes e barrinhas artesanais",
  logo: {
    src: "/brand/logo.png",
    width: 512,
    height: 512,
    alt: "Petite Vallée",
    isPlaceholder: false,
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
