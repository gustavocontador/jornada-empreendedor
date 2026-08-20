import type { Metadata } from "next";
import { Fraunces, Karla } from "next/font/google";
import { CartProvider } from "@/lib/cart/CartContext";
import { Header } from "@/components/Header";
import { Footer } from "@/components/Footer";
import { CartDrawer } from "@/components/CartDrawer";
import { brand, getSiteUrl } from "@/lib/brand";
import "@/styles/globals.css";
import "@/styles/site.css";

// Serifada elegante para títulos; sans limpa para corpo/preços/botões.
const fraunces = Fraunces({
  subsets: ["latin"],
  variable: "--font-fraunces",
  display: "swap",
});

const karla = Karla({
  subsets: ["latin"],
  variable: "--font-karla",
  display: "swap",
});

const siteUrl = getSiteUrl();

export const metadata: Metadata = {
  metadataBase: new URL(siteUrl),
  title: {
    default: "Petite Vallée — Produtos artesanais de Valinhos",
    template: "%s · Petite Vallée",
  },
  description:
    "Granolas, mixes e geleias artesanais, feitos à mão em pequenos lotes em Valinhos. Compre direto da Petite Vallée.",
  openGraph: {
    type: "website",
    locale: "pt_BR",
    url: siteUrl,
    siteName: brand.name,
    title: "Petite Vallée — Produtos artesanais de Valinhos",
    description:
      "Granolas, mixes e geleias artesanais, feitos à mão em Valinhos.",
    images: [{ url: brand.logo.src, width: 360, height: 96, alt: brand.name }],
  },
  twitter: {
    card: "summary",
    title: "Petite Vallée — Produtos artesanais de Valinhos",
    description:
      "Granolas, mixes e geleias artesanais, feitos à mão em Valinhos.",
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
    <html lang="pt-BR" className={`${fraunces.variable} ${karla.variable}`}>
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
        </CartProvider>
      </body>
    </html>
  );
}
