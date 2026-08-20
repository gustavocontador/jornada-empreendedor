import type { Metadata } from "next";
import { SectionTitle } from "@/components/SectionTitle";
import { CheckoutForm } from "@/components/CheckoutForm";

export const metadata: Metadata = {
  title: "Checkout",
  description: "Finalize sua compra na Petite Vallée com segurança.",
  alternates: { canonical: "/checkout" },
  robots: { index: false },
};

export default function CheckoutPage() {
  return (
    <section className="section">
      <div className="container">
        <SectionTitle
          eyebrow="Quase lá"
          title="Finalizar compra"
          description="Preencha seus dados com calma — levamos poucos minutos."
          as="h1"
        />
        <CheckoutForm />
      </div>
    </section>
  );
}
