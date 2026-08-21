import type { Metadata } from "next";
import { Lora } from "next/font/google";
import { CartProvider } from "@/lib/cart/CartContext";
import { Header } from "@/components/Header";
import { Footer } from "@/components/Footer";
import { CartDrawer } from "@/components/CartDrawer";
import { WhatsAppButton } from "@/components/WhatsAppButton";
import { brand, getSiteUrl } from "@/lib/brand";
import "@/styles/globals.css";
import "@/styles/site.css";

// Tipografia oficial: Lora em todo o site — a serifada mais
// próxima da usada nos rótulos e no material impresso da marca
// (escolha da cliente, ago/2026).
const lora = Lora({
  subsets: ["latin"],
  variable: "--font-lora",
  display: "swap",
});

const siteUrl = getSiteUrl();

export const metadata: Metadata = {
  metadataBase: new URL(siteUrl),
  title: {
    default: "Petite Vallée — Granolas, mixes e barrinhas artesanais",
    template: "%s · Petite Vallée",
  },
  description:
    "Granolas, mixes de castanhas e sementes e barrinhas artesanais, sem conservantes e sem glúten. Compre direto da Petite Vallée.",
  openGraph: {
    type: "website",
    locale: "pt_BR",
    url: siteUrl,
    siteName: brand.name,
    title: "Petite Vallée — Granolas, mixes e barrinhas artesanais",
    description:
      "Granolas, mixes e barrinhas artesanais, sem conservantes e sem glúten.",
    images: [{ url: brand.logo.src, width: 360, height: 96, alt: brand.name }],
  },
  twitter: {
    card: "summary",
    title: "Petite Vallée — Granolas, mixes e barrinhas artesanais",
    description:
      "Granolas, mixes e barrinhas artesanais, sem conservantes e sem glúten.",
  },
};

// Dados estruturados da organização (usa o logotipo oficial).
const organizationJsonLd = {
  "@context": "https://schema.org",
  "@type": "Organization",
  name: brand.name,
  url: siteUrl,
  logo: `${siteUrl}${brand.logo.src}`,
  address: {
    "@type": "PostalAddress",
    addressLocality: brand.city,
    addressRegion: brand.state,
    addressCountry: "BR",
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="pt-BR" className={lora.variable}>
      <body>
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{
            __html: JSON.stringify(organizationJsonLd),
          }}
        />
        <a href="#conteudo" className="skip-link">
          Pular para o conteúdo
        </a>
        <CartProvider>
          <Header />
          <main id="conteudo">{children}</main>
          <Footer />
          <CartDrawer />
          <WhatsAppButton />
        </CartProvider>
      </body>
    </html>
  );
}
