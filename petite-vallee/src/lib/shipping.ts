/**
 * Frete e entrega — arquitetura preparada para o futuro.
 *
 * DEFINIÇÃO DA MARCA (ago/2026): entrega para todo o Brasil
 * pelos Correios, com frete calculado automaticamente pelo CEP
 * no checkout.
 *
 * PONTO DE INTEGRAÇÃO: quando a conta no serviço de frete for
 * criada (SuperFrete e Melhor Envio são gratuitos e cotam
 * Correios pelo CEP), transformar `getShippingOptions` em função
 * assíncrona que consulta a API com o CEP e o peso dos itens
 * (campo weightLabel/peso em src/data/products.ts) e retorna as
 * opções reais (PAC, SEDEX...). Até lá, a única opção exibida é
 * a de demonstração abaixo, com valor R$ 0,00 e claramente
 * identificada na interface.
 *
 * O total final é SEMPRE recalculado no servidor
 * (src/lib/checkout.ts) antes de criar qualquer cobrança.
 */

export interface ShippingOption {
  id: string;
  label: string;
  description: string;
  priceInCents: number;
  isDemo: boolean;
}

export function getShippingOptions(_cep?: string): ShippingOption[] {
  return [
    {
      id: "demo",
      label: "Correios — cálculo por CEP em configuração",
      description:
        "Entregamos para todo o Brasil pelos Correios. O cálculo " +
        "automático do frete pelo CEP está sendo configurado; nenhum " +
        "valor de frete é cobrado no modo de demonstração.",
      priceInCents: 0,
      isDemo: true,
    },
  ];
}

export function getShippingOptionById(id: string): ShippingOption | undefined {
  return getShippingOptions().find((option) => option.id === id);
}
