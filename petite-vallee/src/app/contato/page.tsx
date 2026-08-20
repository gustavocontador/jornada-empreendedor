import type { Metadata } from "next";
import { SectionTitle } from "@/components/SectionTitle";
import { ContactForm } from "@/components/ContactForm";
import { brand } from "@/lib/brand";

export const metadata: Metadata = {
  title: "Contato",
  description:
    "Fale com a Petite Vallée: dúvidas, pedidos e parcerias. Estamos em Valinhos, SP.",
  alternates: { canonical: "/contato" },
};

export default function ContatoPage() {
  return (
    <section className="editorial">
      <div className="container">
        <SectionTitle
          eyebrow="Fale conosco"
          title="Contato"
          description="Tem alguma dúvida sobre nossos produtos ou quer fazer um pedido especial? Escreva para a gente."
          as="h1"
        />

        <div className="contact-layout">
          <div className="editorial__content">
            <ContactForm />
          </div>

          <div className="contact-info">
            <div className="contact-info__item">
              <h3>Instagram</h3>
              <p>
                {brand.instagramUrl ? (
                  <a href={brand.instagramUrl} target="_blank" rel="noopener noreferrer">
                    Siga a Petite Vallée
                  </a>
                ) : (
                  "Perfil oficial em breve nesta página. [informação pendente]"
                )}
              </p>
            </div>
            <div className="contact-info__item">
              <h3>WhatsApp</h3>
              <p>
                {brand.whatsappUrl ? (
                  <a href={brand.whatsappUrl} target="_blank" rel="noopener noreferrer">
                    Chamar no WhatsApp
                  </a>
                ) : (
                  "Número de atendimento em breve. [informação pendente]"
                )}
              </p>
            </div>
            <div className="contact-info__item">
              <h3>E-mail</h3>
              <p>
                {brand.email ? (
                  <a href={`mailto:${brand.email}`}>{brand.email}</a>
                ) : (
                  "Endereço de e-mail em breve. [informação pendente]"
                )}
              </p>
            </div>
            <div className="contact-info__item">
              <h3>Onde estamos</h3>
              <p>
                {brand.city}, {brand.state} — atendimento online. Horários de
                atendimento serão publicados em breve.
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
