import type { Metadata } from "next";
import { SectionTitle } from "@/components/SectionTitle";
import { VideoSection } from "@/components/VideoSection";
import { ButtonLink } from "@/components/Button";
import { BotanicalDivider } from "@/components/BotanicalDecoration";

export const metadata: Metadata = {
  title: "Nossa História",
  description:
    "Conheça a Petite Vallée: uma marca criada por mãe e filha em Valinhos, dedicada a produtos artesanais, saudáveis e de alta qualidade.",
  alternates: { canonical: "/nossa-historia" },
};

/**
 * Página editorial da história da marca.
 * Conteúdo restrito ao que foi fornecido oficialmente: marca
 * criada por mãe e filha em Valinhos, foco artesanal e em
 * qualidade. Nomes, datas e histórias pessoais NÃO são inventados.
 */
export default function NossaHistoriaPage() {
  return (
    <section className="editorial">
      <div className="container container--narrow">
        <SectionTitle
          eyebrow="Nossa história"
          title="Feito a quatro mãos, entre mãe e filha"
          as="h1"
          align="center"
        />

        <div className="editorial__content">
          <h2>Como tudo começou</h2>
          <p>
            A Petite Vallée nasceu em <strong>Valinhos</strong>, no interior
            de São Paulo, do encontro entre <strong>mãe e filha</strong> e do
            desejo de criar, com as próprias mãos, alimentos que unissem
            sabor, saúde e cuidado.
          </p>

          <h2>O jeito Petite Vallée de fazer</h2>
          <p>
            Acreditamos que alimento bom se faz sem pressa. Por isso, nossas
            granolas, mixes e geleias são preparados de forma{" "}
            <strong>artesanal, em pequenos lotes</strong>, com ingredientes
            escolhidos com atenção e o mesmo capricho em cada fornada.
          </p>

          <h2>Nosso compromisso</h2>
          <p>
            Da escolha dos ingredientes à embalagem, tudo passa pelas nossas
            mãos. É esse cuidado de família que queremos entregar em cada
            produto: <strong>qualidade alta, de verdade</strong>, para o seu
            dia a dia.
          </p>

          <BotanicalDivider />

          <h2>Em vídeo</h2>
          <VideoSection />

          <div className="editorial__cta">
            <ButtonLink href="/produtos">Conheça nossos produtos</ButtonLink>
          </div>
        </div>
      </div>
    </section>
  );
}
