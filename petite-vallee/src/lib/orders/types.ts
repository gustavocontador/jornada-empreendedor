/**
 * Tipos do domínio de pedidos.
 */

export interface CustomerData {
  fullName: string;
  email: string;
  phone: string;
  /** Coletado somente quando o gateway de pagamento exigir */
  cpf?: string;
  address: {
    cep: string;
    street: string;
    number: string;
    complement?: string;
    neighborhood: string;
    city: string;
    state: string;
  };
  notes?: string;
}

export interface OrderItem {
  productId: string;
  slug: string;
  name: string;
  unitPriceInCents: number;
  quantity: number;
  lineTotalInCents: number;
}

export type PaymentMethod = "pix" | "credit_card";

export type PaymentStatus =
  | "pending"
  | "paid"
  | "declined"
  | "cancelled"
  | "expired"
  | "refunded";

export interface Order {
  id: string;
  customer: CustomerData;
  items: OrderItem[];
  subtotalInCents: number;
  shippingInCents: number;
  shippingOptionId: string;
  totalInCents: number;
  paymentMethod: PaymentMethod;
  paymentStatus: PaymentStatus;
  /** id da cobrança no gateway de pagamento, quando existir */
  paymentProviderId?: string;
  /** true quando o pedido foi criado em modo de demonstração */
  isDemo: boolean;
  createdAt: string;
  updatedAt: string;
}
