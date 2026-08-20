import type { Metadata } from "next";
import { Catalog } from "@/components/Catalog";
import { SectionTitle } from "@/components/SectionTitle";

export const metadata: Metadata = {
  title: "Produtos",
  description:
    "Granolas, mixes de castanhas e sementes e barrinhas artesanais da Petite Vallée, sem conservantes e sem glúten.",
  alternates: { canonical: "/produtos" },
};

export default function ProdutosPage() {
  return (
    <section className="section">
      <div className="container">
        <SectionTitle
          eyebrow="Catálogo"
          title="Nossos produtos"
          description="Feitos à mão, em pequenos lotes, sem conservantes e sem glúten."
          as="h1"
        />
        <Catalog priorityCount={3} />
      </div>
    </section>
  );
}
