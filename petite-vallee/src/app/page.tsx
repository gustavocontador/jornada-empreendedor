import type { Metadata } from "next";
import Image from "next/image";
import { Catalog } from "@/components/Catalog";
import { SectionTitle } from "@/components/SectionTitle";
import { ButtonLink } from "@/components/Button";
import { VideoSection } from "@/components/VideoSection";
import { BotanicalDecoration } from "@/components/BotanicalDecoration";
import { products } from "@/data/products";

export const metadata: Metadata = {
  alternates: { canonical: "/" },
};

const heroProduct = products.find((p) => p.slug === "granola-tradicional");

/**
 * Página inicial: hero compacto (o catálogo aparece logo abaixo),
 * vitrine com filtros, resumo da história e seção de vídeo.
 */
export default function HomePage() {
  return (
    <>
      {/* ── Hero: apresenta a marca sem empurrar o catálogo ── */}
      <section className="hero">
        <div className="container hero__inner">
          <div>
            <p className="hero__eyebrow">
              <BotanicalDecoration size={16} />
              Feito à mão em Valinhos
            </p>
            <h1 className="hero__title">
              Granolas, mixes e geleias artesanais, feitos por mãe e filha.
            </h1>
            <p className="hero__text">
              Cada lote da Petite Vallée é preparado em pequenas quantidades,
              com ingredientes escolhidos com cuidado — do nosso ateliê em
              Valinhos para a sua mesa.
            </p>
            <div className="hero__actions">
              <ButtonLink href="#produtos">Conheça nossos produtos</ButtonLink>
              <ButtonLink href="/nossa-historia" variant="secondary">
                Nossa história
              </ButtonLink>
            </div>
          </div>
          {heroProduct && (
            <div className="hero__media">
              <Image
                src={heroProduct.image}
                alt={`${heroProduct.name} — imagem provisória, foto oficial em breve`}
                fill
                sizes="(max-width: 900px) 100vw, 45vw"
                priority
                unoptimized={heroProduct.image.endsWith(".svg")}
                style={{ objectFit: "cover" }}
              />
            </div>
          )}
        </div>
      </section>

      {/* ── Catálogo logo na página inicial ── */}
      <section className="section section--surface" id="produtos" aria-labelledby="titulo-produtos">
        <div className="container">
          <SectionTitle
            eyebrow="Nossos produtos"
            title="Escolha os seus favoritos"
            description="Tudo é feito de forma artesanal, em pequenos lotes. Adicione ao carrinho direto por aqui."
            id="titulo-produtos"
          />
          <Catalog priorityCount={2} />
        </div>
      </section>

      {/* ── Nossa história (resumo) ── */}
      <section className="section" aria-labelledby="titulo-historia">
        <div className="container story-preview">
          <div>
            <SectionTitle
              eyebrow="Nossa história"
              title="Uma marca criada por mãe e filha"
              id="titulo-historia"
            />
            <div className="story-preview__text">
              <p>
                A Petite Vallée nasceu em Valinhos, do encontro entre duas
                gerações e do desejo de fazer, com as próprias mãos, alimentos
                saudáveis e de alta qualidade.
              </p>
              <p>
                Granolas, mixes e geleias são preparados de forma artesanal,
                em pequenos lotes, com atenção a cada detalhe — do ingrediente
                à embalagem.
              </p>
            </div>
            <div className="editorial__cta">
              <ButtonLink href="/nossa-historia" variant="secondary">
                Conheça nossa história
              </ButtonLink>
            </div>
          </div>
          <VideoSection />
        </div>
      </section>
    </>
  );
}
