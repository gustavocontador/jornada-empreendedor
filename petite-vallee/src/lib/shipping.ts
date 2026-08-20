/**
 * Frete e entrega — arquitetura preparada para o futuro.
 *
 * As regras reais de frete da Petite Vallée AINDA NÃO FORAM
 * DEFINIDAS. Por isso, a única opção disponível hoje é uma opção
 * de demonstração, claramente identificada na interface, com
 * valor R$ 0,00.
 *
 * QUANDO AS REGRAS FOREM DEFINIDAS, basta editar a lista
 * `getShippingOptions` abaixo — por exemplo:
 *   - frete fixo:        { id: "fixo", ..., priceInCents: 1500 }
 *   - retirada local:    { id: "retirada", ..., priceInCents: 0 }
 *   - cálculo por CEP:   transformar a função em assíncrona e
 *     consultar uma API de frete (Correios, Melhor Envio, etc.)
 *     usando o CEP recebido.
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
      label: "Entrega em definição",
      description:
        "As opções e valores de entrega ainda serão configurados. " +
        "Nenhum valor de frete é cobrado no modo de demonstração.",
      priceInCents: 0,
      isDemo: true,
    },
  ];
}

export function getShippingOptionById(id: string): ShippingOption | undefined {
  return getShippingOptions().find((option) => option.id === id);
}
