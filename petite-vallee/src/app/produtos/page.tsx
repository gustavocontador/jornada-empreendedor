import type { Metadata } from "next";
import { Catalog } from "@/components/Catalog";
import { SectionTitle } from "@/components/SectionTitle";

export const metadata: Metadata = {
  title: "Produtos",
  description:
    "Granolas, mixes e geleias artesanais da Petite Vallée. Compre direto do nosso ateliê em Valinhos.",
  alternates: { canonical: "/produtos" },
};

export default function ProdutosPage() {
  return (
    <section className="section">
      <div className="container">
        <SectionTitle
          eyebrow="Catálogo"
          title="Nossos produtos"
          description="Feitos à mão, em pequenos lotes, com ingredientes escolhidos com cuidado."
          as="h1"
        />
        <Catalog priorityCount={3} />
      </div>
    </section>
  );
}
