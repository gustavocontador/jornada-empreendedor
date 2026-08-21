"use client";

/**
 * Estimativa de frete pelo CEP, direto no carrinho — o cliente vê
 * as opções de entrega antes de preencher o checkout.
 *
 * Enquanto a integração de frete (Correios via SuperFrete/Melhor
 * Envio) não está ativa, mostra a opção de demonstração de
 * src/lib/shipping.ts com aviso honesto. Quando a integração
 * chegar, este componente passa a exibir valores e prazos reais
 * sem mudar de lugar. O CEP digitado fica salvo e pré-preenche o
 * checkout.
 */

import { useState } from "react";
import { formatCep, isValidCep } from "@/lib/format";
import { getShippingOptions } from "@/lib/shipping";
import { formatPrice } from "@/lib/format";

export const CEP_STORAGE_KEY = "petite-vallee-cep";

export function CartShippingEstimate() {
  const [cep, setCep] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [options, setOptions] = useState<ReturnType<typeof getShippingOptions> | null>(null);

  function handleEstimate() {
    if (!isValidCep(cep)) {
      setError("Informe um CEP válido (00000-000).");
      setOptions(null);
      return;
    }
    setError(null);
    setOptions(getShippingOptions(cep));
    try {
      window.localStorage.setItem(CEP_STORAGE_KEY, cep);
    } catch {
      // sem localStorage, segue sem persistir
    }
  }

  return (
    <div className="shipping-estimate">
      <label htmlFor="cart-cep" className="shipping-estimate__label">
        Calcular frete e prazo
      </label>
      <div className="shipping-estimate__row">
        <input
          id="cart-cep"
          inputMode="numeric"
          autoComplete="postal-code"
          placeholder="Seu CEP"
          value={cep}
          onChange={(e) => {
            setCep(formatCep(e.target.value));
            setError(null);
          }}
          onKeyDown={(e) => {
            if (e.key === "Enter") {
              e.preventDefault();
              handleEstimate();
            }
          }}
          aria-invalid={Boolean(error)}
          aria-describedby={error ? "cart-cep-error" : undefined}
        />
        <button type="button" className="btn btn--secondary btn--small" onClick={handleEstimate}>
          <span>Calcular</span>
        </button>
      </div>
      {error && (
        <p className="form-field__error" id="cart-cep-error" role="alert">
          {error}
        </p>
      )}
      {options && (
        <ul className="shipping-estimate__results" aria-live="polite">
          {options.map((option) => (
            <li key={option.id} className="shipping-estimate__result">
              <span className="shipping-estimate__result-label">
                {option.label}
                {option.isDemo && <span className="tag tag--demo">demonstração</span>}
              </span>
              <span className="shipping-estimate__result-price">
                {option.isDemo ? "a definir" : formatPrice(option.priceInCents)}
              </span>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
