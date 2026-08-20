import type { Metadata } from "next";
import Image from "next/image";
import { Catalog } from "@/components/Catalog";
import { SectionTitle } from "@/components/SectionTitle";
import { ButtonLink } from "@/components/Button";
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
            {/* [PROVISÓRIO] textos aguardando a versão manuscrita da cliente */}
            <h1 className="hero__title">
              Granola crocante, mixes na medida e geleia de verdade.
            </h1>
            <p className="hero__text">
              Tudo artesanal, assado e preparado em pequenos lotes, direto de
              Valinhos. Escolha os seus e receba em casa.
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

      {/* ── Convite para a história (o conteúdo completo, com o vídeo,
            vive em /nossa-historia) ── */}
      <section className="section" aria-labelledby="titulo-historia">
        <div className="container">
          <SectionTitle
            eyebrow="Quem faz"
            title="Prazer, somos a Petite Vallée"
            description="Uma marca de Valinhos, nascida do trabalho de mãe e filha. A história completa — e o vídeo — estão na nossa página."
            id="titulo-historia"
            align="center"
          />
          <div className="editorial__cta" style={{ textAlign: "center", marginTop: 0 }}>
            <ButtonLink href="/nossa-historia" variant="secondary">
              Conheça nossa história
            </ButtonLink>
          </div>
        </div>
      </section>
    </>
  );
}
