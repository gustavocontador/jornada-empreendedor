import type { ReactNode } from "react";
import { SectionTitle } from "./SectionTitle";
import { StatusMessage } from "./StatusMessage";

interface PolicyPageProps {
  title: string;
  children: ReactNode;
}

/**
 * Molde das páginas jurídicas. Todos os textos são PROVISÓRIOS e
 * exibem um aviso de revisão — os definitivos devem ser escritos
 * ou revisados juridicamente antes da loja operar com vendas.
 */
export function PolicyPage({ title, children }: PolicyPageProps) {
  return (
    <section className="editorial">
      <div className="container container--narrow">
        <SectionTitle eyebrow="Políticas da loja" title={title} as="h1" />
        <div className="draft-notice">
          <StatusMessage tone="warning" title="Texto provisório">
            Este conteúdo é um rascunho e será revisado antes do início das
            vendas. Ele não constitui o texto jurídico definitivo da loja.
          </StatusMessage>
        </div>
        <div className="editorial__content">{children}</div>
      </div>
    </section>
  );
}
