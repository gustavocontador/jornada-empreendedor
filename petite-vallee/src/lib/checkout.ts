/**
 * Validação de checkout NO SERVIDOR.
 *
 * O navegador envia apenas ids de produto, quantidades, a opção
 * de frete e os dados do cliente. Preços e totais são SEMPRE
 * recalculados aqui a partir do catálogo oficial
 * (src/data/products.ts) — nunca confiamos no valor vindo do
 * cliente.
 */

import { getProductById } from "@/data/products";
import { getShippingOptionById } from "@/lib/shipping";
import { isValidCep, isValidEmail, isValidPhone } from "@/lib/format";
import type {
  CustomerData,
  OrderItem,
  PaymentMethod,
} from "@/lib/orders/types";

const BR_STATES = new Set([
  "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA",
  "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN",
  "RS", "RO", "RR", "SC", "SP", "SE", "TO",
]);

export interface CheckoutRequestBody {
  items: Array<{ productId: string; quantity: number }>;
  customer: CustomerData;
  shippingOptionId: string;
  paymentMethod: PaymentMethod;
}

export interface ValidatedCheckout {
  items: OrderItem[];
  customer: CustomerData;
  shippingOptionId: string;
  subtotalInCents: number;
  shippingInCents: number;
  totalInCents: number;
  paymentMethod: PaymentMethod;
}

export class CheckoutValidationError extends Error {
  constructor(
    message: string,
    public readonly fieldErrors: Record<string, string> = {}
  ) {
    super(message);
  }
}

function requireText(
  value: unknown,
  field: string,
  label: string,
  errors: Record<string, string>,
  maxLength = 200
): string {
  const text = typeof value === "string" ? value.trim() : "";
  if (!text) errors[field] = `Informe ${label}.`;
  return text.slice(0, maxLength);
}

export function validateCheckout(body: unknown): ValidatedCheckout {
  if (typeof body !== "object" || body === null) {
    throw new CheckoutValidationError("Requisição inválida.");
  }
  const { items, customer, shippingOptionId, paymentMethod } =
    body as Partial<CheckoutRequestBody>;

  // ── Itens: preços vêm do catálogo, nunca do navegador ──
  if (!Array.isArray(items) || items.length === 0) {
    throw new CheckoutValidationError("O carrinho está vazio.");
  }
  const orderItems: OrderItem[] = items.map((raw) => {
    const product =
      typeof raw?.productId === "string"
        ? getProductById(raw.productId)
        : undefined;
    if (!product) {
      throw new CheckoutValidationError(
        "Um dos produtos do carrinho não existe mais no catálogo."
      );
    }
    if (!product.available) {
      throw new CheckoutValidationError(
        `O produto "${product.name}" está indisponível no momento.`
      );
    }
    const quantity = Math.round(Number(raw.quantity));
    if (!Number.isFinite(quantity) || quantity < 1 || quantity > 20) {
      throw new CheckoutValidationError(
        `Quantidade inválida para "${product.name}".`
      );
    }
    return {
      productId: product.id,
      slug: product.slug,
      name: product.name,
      unitPriceInCents: product.priceInCents,
      quantity,
      lineTotalInCents: product.priceInCents * quantity,
    };
  });

  // ── Dados do cliente ──
  const errors: Record<string, string> = {};
  const c = (customer ?? {}) as Partial<CustomerData>;
  const address = (c.address ?? {}) as Partial<CustomerData["address"]>;

  const fullName = requireText(c.fullName, "fullName", "seu nome completo", errors);
  if (fullName && fullName.split(/\s+/).length < 2) {
    errors.fullName = "Informe nome e sobrenome.";
  }
  const email = requireText(c.email, "email", "seu e-mail", errors);
  if (email && !isValidEmail(email)) errors.email = "E-mail inválido.";
  const phone = requireText(c.phone, "phone", "seu telefone", errors, 20);
  if (phone && !isValidPhone(phone)) errors.phone = "Telefone inválido.";

  const cep = requireText(address.cep, "cep", "seu CEP", errors, 9);
  if (cep && !isValidCep(cep)) errors.cep = "CEP inválido.";
  const street = requireText(address.street, "street", "o endereço", errors);
  const number = requireText(address.number, "number", "o número", errors, 20);
  const neighborhood = requireText(address.neighborhood, "neighborhood", "o bairro", errors);
  const city = requireText(address.city, "city", "a cidade", errors);
  const state = requireText(address.state, "state", "o estado", errors, 2).toUpperCase();
  if (state && !BR_STATES.has(state)) errors.state = "Estado inválido.";

  if (Object.keys(errors).length > 0) {
    throw new CheckoutValidationError(
      "Alguns campos precisam de atenção.",
      errors
    );
  }

  // ── Frete: valor oficial vem do servidor ──
  const shipping = getShippingOptionById(
    typeof shippingOptionId === "string" ? shippingOptionId : ""
  );
  if (!shipping) {
    throw new CheckoutValidationError("Opção de entrega inválida.");
  }

  // ── Método de pagamento ──
  if (paymentMethod !== "pix" && paymentMethod !== "credit_card") {
    throw new CheckoutValidationError("Método de pagamento inválido.");
  }

  const subtotalInCents = orderItems.reduce(
    (sum, item) => sum + item.lineTotalInCents,
    0
  );

  return {
    items: orderItems,
    customer: {
      fullName,
      email,
      phone,
      cpf: typeof c.cpf === "string" ? c.cpf.trim().slice(0, 14) : undefined,
      address: {
        cep,
        street,
        number,
        complement:
          typeof address.complement === "string"
            ? address.complement.trim().slice(0, 100)
            : undefined,
        neighborhood,
        city,
        state,
      },
      notes:
        typeof c.notes === "string" ? c.notes.trim().slice(0, 500) : undefined,
    },
    shippingOptionId: shipping.id,
    subtotalInCents,
    shippingInCents: shipping.priceInCents,
    totalInCents: subtotalInCents + shipping.priceInCents,
    paymentMethod,
  };
}
