import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import {
  CATEGORY_LABELS,
  getProductBySlug,
  products,
} from "@/data/products";
import { formatPrice } from "@/lib/format";
import { getSiteUrl } from "@/lib/brand";
import { ProductImage } from "@/components/ProductImage";
import { AddToCartSection } from "./AddToCartSection";

interface PageProps {
  params: Promise<{ slug: string }>;
}

export function generateStaticParams() {
  return products.map((product) => ({ slug: product.slug }));
}

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const { slug } = await params;
  const product = getProductBySlug(slug);
  if (!product) return {};
  return {
    title: product.name,
    description: product.shortDescription,
    alternates: { canonical: `/produto/${product.slug}` },
    openGraph: {
      title: product.name,
      description: product.shortDescription,
      images: [{ url: product.image, alt: product.name }],
    },
  };
}

export default async function ProdutoPage({ params }: PageProps) {
  const { slug } = await params;
  const product = getProductBySlug(slug);
  if (!product) notFound();

  const siteUrl = getSiteUrl();
  // Dados estruturados de produto (sem avaliações falsas).
  const productJsonLd = {
    "@context": "https://schema.org",
    "@type": "Product",
    name: product.name,
    description: product.shortDescription,
    image: `${siteUrl}${product.image}`,
    category: CATEGORY_LABELS[product.category],
    brand: { "@type": "Brand", name: "Petite Vallée" },
    offers: {
      "@type": "Offer",
      url: `${siteUrl}/produto/${product.slug}`,
      priceCurrency: "BRL",
      price: (product.priceInCents / 100).toFixed(2),
      availability: product.available
        ? "https://schema.org/InStock"
        : "https://schema.org/OutOfStock",
    },
  };

  return (
    <div className="container">
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(productJsonLd) }}
      />
      <article className="product-page">
        <div className="product-page__media">
          <ProductImage
            product={product}
            sizes="(max-width: 860px) 100vw, 50vw"
            priority
          />
        </div>
        <div>
          <p className="product-card__category">
            {CATEGORY_LABELS[product.category]}
          </p>
          <h1>{product.name}</h1>
          <p className="product-page__price">
            {formatPrice(product.priceInCents)}
            <small>preço provisório — sujeito a confirmação</small>
          </p>
          <p className="product-page__description">
            {product.description ?? product.shortDescription}
          </p>

          <AddToCartSection productId={product.id} available={product.available} />

          <Link href="/produtos" className="product-page__back">
            ← Voltar para todos os produtos
          </Link>
        </div>
      </article>
    </div>
  );
}
