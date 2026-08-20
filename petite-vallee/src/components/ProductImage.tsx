import Image from "next/image";
import type { Product } from "@/data/products";

interface ProductImageProps {
  product: Product;
  sizes?: string;
  priority?: boolean;
}

/**
 * Fotografia do produto.
 * Enquanto a foto oficial não existe, o catálogo usa placeholders
 * SVG claramente identificados (imageIsPlaceholder: true) — o
 * next/image não precisa otimizá-los. Quando as fotos reais
 * (.jpg/.webp) forem adicionadas, a otimização automática de
 * imagens do Next.js passa a valer sem mudar este componente.
 */
export function ProductImage({
  product,
  sizes = "(max-width: 640px) 100vw, (max-width: 1024px) 50vw, 33vw",
  priority = false,
}: ProductImageProps) {
  const isSvgPlaceholder = product.image.endsWith(".svg");
  return (
    <Image
      src={product.image}
      alt={
        product.imageIsPlaceholder
          ? `${product.name} — imagem provisória, foto oficial em breve`
          : product.name
      }
      fill
      sizes={sizes}
      priority={priority}
      unoptimized={isSvgPlaceholder}
      className="product-image"
    />
  );
}
