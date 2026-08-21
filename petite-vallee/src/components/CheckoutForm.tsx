"use client";

/**
 * Formulário de checkout independente (sem Shopify).
 *
 * - Valida os campos no cliente (mensagens acessíveis) e envia
 *   para /api/checkout, onde tudo é revalidado no servidor.
 * - Em MODO DE DEMONSTRAÇÃO o servidor confirma a validação mas
 *   não cria cobrança; a interface deixa isso explícito e nunca
 *   apresenta um pagamento como aprovado.
 * - Quando um gateway real estiver configurado, a resposta traz a
 *   cobrança (Pix ou redirecionamento seguro do cartão).
 */

import { useEffect, useMemo, useRef, useState } from "react";
import { useRouter } from "next/navigation";
import { useCart } from "@/lib/cart/CartContext";
import {
  formatCep,
  formatCpf,
  formatPhone,
  isValidCep,
  isValidEmail,
  isValidPhone,
} from "@/lib/format";
import { getShippingOptions } from "@/lib/shipping";
import type { PaymentMethod } from "@/lib/orders/types";
import type { CreateChargeResult } from "@/lib/payment/provider";
import { Button } from "./Button";
import { OrderSummary } from "./OrderSummary";
import { PaymentMethodSelector } from "./PaymentMethodSelector";
import { PixPayment } from "./PixPayment";
import { StatusMessage } from "./StatusMessage";
import { EmptyState } from "./EmptyState";
import { ButtonLink } from "./Button";
import { LoadingState } from "./LoadingState";

interface FieldProps {
  id: string;
  label: string;
  error?: string;
  optionalHint?: string;
  children: React.ReactNode;
}

function Field({ id, label, error, optionalHint, children }: FieldProps) {
  return (
    <div className={`form-field${error ? " form-field--error" : ""}`}>
      <label htmlFor={id}>
        {label}
        {optionalHint && <span className="form-field__optional"> {optionalHint}</span>}
      </label>
      {children}
      {error && (
        <p className="form-field__error" id={`${id}-error`} role="alert">
          {error}
        </p>
      )}
    </div>
  );
}

type SubmitState =
  | { phase: "idle" }
  | { phase: "submitting" }
  | { phase: "demo-confirmed"; orderId: string; message: string }
  | { phase: "pix"; orderId: string; totalInCents: number; charge: CreateChargeResult }
  | { phase: "error"; message: string };

export function CheckoutForm() {
  const router = useRouter();
  const { items, hydrated, clearCart } = useCart();
  const shippingOptions = useMemo(() => getShippingOptions(), []);

  const [values, setValues] = useState({
    fullName: "",
    email: "",
    phone: "",
    cpf: "",
    cep: "",
    street: "",
    number: "",
    complement: "",
    neighborhood: "",
    city: "",
    state: "",
    notes: "",
  });
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [shippingOptionId, setShippingOptionId] = useState(shippingOptions[0].id);
  const [paymentMethod, setPaymentMethod] = useState<PaymentMethod>("pix");
  const [submitState, setSubmitState] = useState<SubmitState>({ phase: "idle" });
  const [demoMode, setDemoMode] = useState<boolean | null>(null);
  const errorSummaryRef = useRef<HTMLDivElement>(null);

  // Pré-preenche o CEP estimado no carrinho, se houver.
  useEffect(() => {
    try {
      const savedCep = window.localStorage.getItem("petite-vallee-cep");
      if (savedCep) {
        setValues((prev) => (prev.cep ? prev : { ...prev, cep: savedCep }));
      }
    } catch {
      // sem localStorage, segue com o campo vazio
    }
  }, []);

  // Descobre se a loja está em modo de demonstração.
  useEffect(() => {
    let cancelled = false;
    fetch("/api/checkout")
      .then((res) => (res.ok ? res.json() : null))
      .then((data: { demoMode?: boolean } | null) => {
        if (!cancelled && data) setDemoMode(Boolean(data.demoMode));
      })
      .catch(() => {
        if (!cancelled) setDemoMode(true);
      });
    return () => {
      cancelled = true;
    };
  }, []);

  function set(field: keyof typeof values, value: string) {
    setValues((prev) => ({ ...prev, [field]: value }));
    setErrors((prev) => {
      if (!prev[field]) return prev;
      const next = { ...prev };
      delete next[field];
      return next;
    });
  }

  function validate(): boolean {
    const next: Record<string, string> = {};
    if (values.fullName.trim().split(/\s+/).length < 2)
      next.fullName = "Informe nome e sobrenome.";
    if (!isValidEmail(values.email)) next.email = "Informe um e-mail válido.";
    if (!isValidPhone(values.phone)) next.phone = "Informe um telefone válido com DDD.";
    if (!isValidCep(values.cep)) next.cep = "Informe um CEP válido (00000-000).";
    if (!values.street.trim()) next.street = "Informe o endereço.";
    if (!values.number.trim()) next.number = "Informe o número.";
    if (!values.neighborhood.trim()) next.neighborhood = "Informe o bairro.";
    if (!values.city.trim()) next.city = "Informe a cidade.";
    if (!/^[A-Za-z]{2}$/.test(values.state.trim()))
      next.state = "Informe a sigla do estado (ex.: SP).";
    setErrors(next);
    if (Object.keys(next).length > 0) {
      errorSummaryRef.current?.focus();
      return false;
    }
    return true;
  }

  async function handleSubmit(event: React.FormEvent) {
    event.preventDefault();
    if (submitState.phase === "submitting") return; // evita envio duplicado
    if (!validate()) return;

    setSubmitState({ phase: "submitting" });
    try {
      const res = await fetch("/api/checkout", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          items: items.map((i) => ({
            productId: i.product.id,
            quantity: i.quantity,
          })),
          customer: {
            fullName: values.fullName,
            email: values.email,
            phone: values.phone,
            cpf: values.cpf || undefined,
            notes: values.notes || undefined,
            address: {
              cep: values.cep,
              street: values.street,
              number: values.number,
              complement: values.complement || undefined,
              neighborhood: values.neighborhood,
              city: values.city,
              state: values.state.toUpperCase(),
            },
          },
          shippingOptionId,
          paymentMethod,
        }),
      });
      const data = await res.json();

      if (!res.ok) {
        if (data.fieldErrors && Object.keys(data.fieldErrors).length > 0) {
          setErrors(data.fieldErrors);
        }
        setSubmitState({
          phase: "error",
          message: data.error ?? "Não foi possível concluir o pedido.",
        });
        return;
      }

      if (data.demoMode) {
        setSubmitState({
          phase: "demo-confirmed",
          orderId: data.orderId,
          message: data.message,
        });
        return;
      }

      // Gateway real configurado:
      const charge = data.charge as CreateChargeResult;
      if (paymentMethod === "pix" && charge.pix) {
        clearCart();
        setSubmitState({
          phase: "pix",
          orderId: data.orderId,
          totalInCents: data.totalInCents,
          charge,
        });
        return;
      }
      if (charge.redirectUrl) {
        clearCart();
        window.location.href = charge.redirectUrl;
        return;
      }
      clearCart();
      router.push(`/pedido/pendente?orderId=${data.orderId}`);
    } catch {
      setSubmitState({
        phase: "error",
        message:
          "Falha de conexão ao enviar o pedido. Verifique sua internet e tente novamente.",
      });
    }
  }

  if (!hydrated) {
    return <LoadingState label="Carregando seu carrinho…" />;
  }

  if (items.length === 0 && submitState.phase !== "pix" && submitState.phase !== "demo-confirmed") {
    return (
      <EmptyState
        title="Seu carrinho está vazio"
        description="Adicione produtos antes de finalizar a compra."
        action={<ButtonLink href="/produtos">Ver produtos</ButtonLink>}
      />
    );
  }

  if (submitState.phase === "pix") {
    return (
      <PixPayment
        orderId={submitState.orderId}
        totalInCents={submitState.totalInCents}
        pix={submitState.charge.pix!}
      />
    );
  }

  if (submitState.phase === "demo-confirmed") {
    return (
      <div className="checkout-demo-result">
        <StatusMessage tone="warning" title="Pagamento em modo de demonstração">
          <p>{submitState.message}</p>
          <p>
            Seus dados foram validados com sucesso, mas <strong>nenhuma
            cobrança foi criada</strong> e nenhum valor foi pago. Assim que a
            loja conectar o provedor de pagamentos (Pix e cartão), esta etapa
            passará a gerar a cobrança real.
          </p>
          <p className="checkout-demo-result__order">
            Referência do pedido de teste: <code>{submitState.orderId}</code>
          </p>
        </StatusMessage>
        <ButtonLink href="/" variant="secondary">
          Voltar à página inicial
        </ButtonLink>
      </div>
    );
  }

  const selectedShipping = shippingOptions.find((o) => o.id === shippingOptionId);

  return (
    <div className="checkout-layout">
      <form className="checkout-form" onSubmit={handleSubmit} noValidate>
        {demoMode !== false && (
          <StatusMessage tone="warning" title="Loja em modo de demonstração">
            O pagamento ainda não está ativo. Você pode preencher o
            formulário e testar o fluxo — nenhuma cobrança real será criada.
          </StatusMessage>
        )}

        <div
          ref={errorSummaryRef}
          tabIndex={-1}
          aria-live="assertive"
          className="checkout-form__error-summary"
        >
          {Object.keys(errors).length > 0 && (
            <StatusMessage tone="error" title="Alguns campos precisam de atenção">
              Revise os campos destacados abaixo.
            </StatusMessage>
          )}
        </div>

        <fieldset>
          <legend className="form-section-title">Seus dados</legend>
          <Field id="fullName" label="Nome completo" error={errors.fullName}>
            <input
              id="fullName"
              name="fullName"
              autoComplete="name"
              required
              value={values.fullName}
              onChange={(e) => set("fullName", e.target.value)}
              aria-invalid={Boolean(errors.fullName)}
              aria-describedby={errors.fullName ? "fullName-error" : undefined}
            />
          </Field>
          <div className="form-row">
            <Field id="email" label="E-mail" error={errors.email}>
              <input
                id="email"
                name="email"
                type="email"
                autoComplete="email"
                inputMode="email"
                required
                value={values.email}
                onChange={(e) => set("email", e.target.value)}
                aria-invalid={Boolean(errors.email)}
                aria-describedby={errors.email ? "email-error" : undefined}
              />
            </Field>
            <Field id="phone" label="Telefone / WhatsApp" error={errors.phone}>
              <input
                id="phone"
                name="phone"
                type="tel"
                autoComplete="tel"
                inputMode="tel"
                required
                placeholder="(19) 99999-9999"
                value={values.phone}
                onChange={(e) => set("phone", formatPhone(e.target.value))}
                aria-invalid={Boolean(errors.phone)}
                aria-describedby={errors.phone ? "phone-error" : undefined}
              />
            </Field>
          </div>
          <Field
            id="cpf"
            label="CPF"
            optionalHint="(opcional — necessário apenas para emissão da cobrança)"
            error={errors.cpf}
          >
            <input
              id="cpf"
              name="cpf"
              inputMode="numeric"
              autoComplete="off"
              placeholder="000.000.000-00"
              value={values.cpf}
              onChange={(e) => set("cpf", formatCpf(e.target.value))}
            />
          </Field>
        </fieldset>

        <fieldset>
          <legend className="form-section-title">Endereço de entrega</legend>
          <div className="form-row">
            <Field id="cep" label="CEP" error={errors.cep}>
              <input
                id="cep"
                name="cep"
                inputMode="numeric"
                autoComplete="postal-code"
                required
                placeholder="00000-000"
                value={values.cep}
                onChange={(e) => set("cep", formatCep(e.target.value))}
                aria-invalid={Boolean(errors.cep)}
                aria-describedby={errors.cep ? "cep-error" : undefined}
              />
            </Field>
            <Field id="state" label="Estado (UF)" error={errors.state}>
              <input
                id="state"
                name="state"
                autoComplete="address-level1"
                required
                maxLength={2}
                placeholder="SP"
                value={values.state}
                onChange={(e) => set("state", e.target.value.toUpperCase())}
                aria-invalid={Boolean(errors.state)}
                aria-describedby={errors.state ? "state-error" : undefined}
              />
            </Field>
          </div>
          <Field id="street" label="Endereço (rua, avenida…)" error={errors.street}>
            <input
              id="street"
              name="street"
              autoComplete="address-line1"
              required
              value={values.street}
              onChange={(e) => set("street", e.target.value)}
              aria-invalid={Boolean(errors.street)}
              aria-describedby={errors.street ? "street-error" : undefined}
            />
          </Field>
          <div className="form-row">
            <Field id="number" label="Número" error={errors.number}>
              <input
                id="number"
                name="number"
                autoComplete="address-line2"
                required
                value={values.number}
                onChange={(e) => set("number", e.target.value)}
                aria-invalid={Boolean(errors.number)}
                aria-describedby={errors.number ? "number-error" : undefined}
              />
            </Field>
            <Field id="complement" label="Complemento" optionalHint="(opcional)">
              <input
                id="complement"
                name="complement"
                value={values.complement}
                onChange={(e) => set("complement", e.target.value)}
              />
            </Field>
          </div>
          <div className="form-row">
            <Field id="neighborhood" label="Bairro" error={errors.neighborhood}>
              <input
                id="neighborhood"
                name="neighborhood"
                required
                value={values.neighborhood}
                onChange={(e) => set("neighborhood", e.target.value)}
                aria-invalid={Boolean(errors.neighborhood)}
                aria-describedby={
                  errors.neighborhood ? "neighborhood-error" : undefined
                }
              />
            </Field>
            <Field id="city" label="Cidade" error={errors.city}>
              <input
                id="city"
                name="city"
                autoComplete="address-level2"
                required
                value={values.city}
                onChange={(e) => set("city", e.target.value)}
                aria-invalid={Boolean(errors.city)}
                aria-describedby={errors.city ? "city-error" : undefined}
              />
            </Field>
          </div>
        </fieldset>

        <fieldset className="shipping-options">
          <legend className="form-section-title">Entrega</legend>
          {shippingOptions.map((option) => (
            <label
              key={option.id}
              className={`shipping-options__option${
                shippingOptionId === option.id
                  ? " shipping-options__option--active"
                  : ""
              }`}
            >
              <input
                type="radio"
                name="shippingOption"
                value={option.id}
                checked={shippingOptionId === option.id}
                onChange={() => setShippingOptionId(option.id)}
              />
              <span className="shipping-options__label">
                {option.label}
                {option.isDemo && (
                  <span className="tag tag--demo">demonstração</span>
                )}
              </span>
              <span className="shipping-options__description">
                {option.description}
              </span>
            </label>
          ))}
        </fieldset>

        <PaymentMethodSelector value={paymentMethod} onChange={setPaymentMethod} />

        <Field id="notes" label="Observações" optionalHint="(opcional)">
          <textarea
            id="notes"
            name="notes"
            rows={3}
            maxLength={500}
            value={values.notes}
            onChange={(e) => set("notes", e.target.value)}
          />
        </Field>

        {submitState.phase === "error" && (
          <StatusMessage tone="error" title="Não foi possível concluir">
            {submitState.message}
          </StatusMessage>
        )}

        <Button
          type="submit"
          loading={submitState.phase === "submitting"}
          className="btn--block btn--large"
        >
          {demoMode !== false
            ? "Revisar pedido (pagamento em demonstração)"
            : paymentMethod === "pix"
              ? "Gerar Pix"
              : "Ir para pagamento seguro"}
        </Button>
        <p className="checkout-form__security-note">
          Seus dados de pagamento nunca ficam armazenados em nosso site — o
          pagamento é processado no ambiente seguro do provedor.
        </p>
      </form>

      <OrderSummary items={items} shippingOption={selectedShipping} />
    </div>
  );
}
