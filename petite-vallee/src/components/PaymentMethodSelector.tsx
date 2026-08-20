"use client";

import type { PaymentMethod } from "@/lib/orders/types";

interface PaymentMethodSelectorProps {
  value: PaymentMethod;
  onChange: (method: PaymentMethod) => void;
}

const METHODS: Array<{
  value: PaymentMethod;
  label: string;
  description: string;
}> = [
  {
    value: "pix",
    label: "Pix",
    description: "Aprovação rápida com QR Code ou copia e cola.",
  },
  {
    value: "credit_card",
    label: "Cartão de crédito",
    description: "Pagamento seguro processado pelo provedor de pagamento.",
  },
];

/** Seleção do método de pagamento (radios estilizados, acessíveis). */
export function PaymentMethodSelector({
  value,
  onChange,
}: PaymentMethodSelectorProps) {
  return (
    <fieldset className="payment-methods">
      <legend className="form-section-title">Forma de pagamento</legend>
      {METHODS.map((method) => (
        <label
          key={method.value}
          className={`payment-methods__option${
            value === method.value ? " payment-methods__option--active" : ""
          }`}
        >
          <input
            type="radio"
            name="paymentMethod"
            value={method.value}
            checked={value === method.value}
            onChange={() => onChange(method.value)}
          />
          <span className="payment-methods__label">{method.label}</span>
          <span className="payment-methods__description">
            {method.description}
          </span>
        </label>
      ))}
    </fieldset>
  );
}
