/**
 * Abstração do gateway de pagamento — PONTO DE INTEGRAÇÃO.
 *
 * A Petite Vallée ainda não tem conta em um gateway. Enquanto
 * isso, o site roda com o `DemoPaymentProvider`, que NUNCA cria
 * cobranças reais e NUNCA marca pagamentos como aprovados.
 *
 * ── COMO INTEGRAR UM GATEWAY REAL (ex.: Mercado Pago, Pagar.me,
 *    Asaas ou outro provedor brasileiro com Pix e cartão) ──
 *
 * 1. Crie um arquivo neste diretório (ex.: `mercadopago.ts`)
 *    com uma classe que implemente a interface `PaymentProvider`.
 * 2. Use a SDK oficial do provedor no servidor, lendo as chaves
 *    de `process.env.PAYMENT_ACCESS_TOKEN` etc. (ver .env.example).
 * 3. Registre o provedor no `switch` de `getPaymentProvider()`.
 * 4. Defina `PAYMENT_PROVIDER=<nome>` no `.env.local`.
 *
 * Regras inegociáveis (já respeitadas por esta arquitetura):
 * - Toda cobrança é criada NO SERVIDOR, nunca no navegador.
 * - Valores são recalculados no servidor a partir do catálogo
 *   (src/lib/checkout.ts) — o preço enviado pelo navegador é
 *   ignorado.
 * - Dados de cartão NUNCA passam pelo nosso servidor nem são
 *   armazenados: use a biblioteca de tokenização do gateway no
 *   frontend e envie apenas o token.
 * - Webhooks devem ser validados com PAYMENT_WEBHOOK_SECRET
 *   conforme a documentação do provedor.
 */

import type { Order, PaymentStatus } from "@/lib/orders/types";

export interface PixChargeData {
  /** imagem do QR Code em base64, quando fornecida pelo gateway */
  qrCodeBase64?: string;
  /** código "copia e cola" do Pix */
  copyPasteCode?: string;
  /** validade da cobrança (ISO 8601) */
  expiresAt?: string;
}

export interface CreateChargeResult {
  /** id da cobrança no gateway */
  providerChargeId: string;
  status: PaymentStatus;
  pix?: PixChargeData;
  /** URL de checkout seguro hospedado pelo gateway, se aplicável */
  redirectUrl?: string;
}

export interface WebhookVerification {
  valid: boolean;
  providerChargeId?: string;
  status?: PaymentStatus;
}

export interface PaymentProvider {
  readonly name: string;
  /** true quando nenhuma cobrança real pode ser criada */
  readonly isDemo: boolean;
  createCharge(order: Order): Promise<CreateChargeResult>;
  getChargeStatus(providerChargeId: string): Promise<PaymentStatus>;
  /**
   * Valida a autenticidade de uma notificação de webhook e extrai
   * a cobrança e o novo status. Cada gateway documenta seu próprio
   * mecanismo (assinatura HMAC, token no header, etc.).
   */
  verifyWebhook(rawBody: string, headers: Headers): Promise<WebhookVerification>;
}

/**
 * Provedor de demonstração: recusa-se a criar cobranças reais.
 * Usado enquanto PAYMENT_PROVIDER estiver vazio ou igual a "demo".
 */
class DemoPaymentProvider implements PaymentProvider {
  readonly name = "demo";
  readonly isDemo = true;

  async createCharge(): Promise<CreateChargeResult> {
    throw new DemoModeError(
      "O pagamento está em modo de demonstração: nenhuma cobrança real " +
        "foi criada. Configure um gateway em .env.local para ativar " +
        "pagamentos reais."
    );
  }

  async getChargeStatus(): Promise<PaymentStatus> {
    // Em modo demo nada é pago — nunca simular aprovação.
    return "pending";
  }

  async verifyWebhook(): Promise<WebhookVerification> {
    return { valid: false };
  }
}

export class DemoModeError extends Error {}

export function isDemoMode(): boolean {
  const provider = process.env.PAYMENT_PROVIDER?.trim().toLowerCase();
  return !provider || provider === "demo";
}

export function getPaymentProvider(): PaymentProvider {
  const provider = process.env.PAYMENT_PROVIDER?.trim().toLowerCase();
  switch (provider) {
    // ── Registre gateways reais aqui ──
    // case "mercadopago":
    //   return new MercadoPagoProvider();
    // case "pagarme":
    //   return new PagarmeProvider();
    case undefined:
    case "":
    case "demo":
      return new DemoPaymentProvider();
    default:
      throw new Error(
        `PAYMENT_PROVIDER desconhecido: "${provider}". ` +
          "Implemente o provedor em src/lib/payment/ e registre-o " +
          "em getPaymentProvider()."
      );
  }
}
