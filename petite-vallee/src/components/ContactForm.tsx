"use client";

/**
 * Formulário de contato.
 *
 * O backend de envio (e-mail, WhatsApp ou CRM) ainda não foi
 * definido. O formulário valida os campos e envia para
 * /api/contact — hoje o endpoint apenas registra a mensagem no
 * log do servidor e confirma o recebimento; a interface deixa o
 * caráter provisório claro.
 */

import { useState } from "react";
import { isValidEmail } from "@/lib/format";
import { Button } from "./Button";
import { StatusMessage } from "./StatusMessage";

type Phase = "idle" | "sending" | "sent" | "error";

export function ContactForm() {
  const [values, setValues] = useState({
    name: "",
    email: "",
    phone: "",
    message: "",
  });
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [phase, setPhase] = useState<Phase>("idle");

  function set(field: keyof typeof values, value: string) {
    setValues((prev) => ({ ...prev, [field]: value }));
    setErrors((prev) => {
      if (!prev[field]) return prev;
      const next = { ...prev };
      delete next[field];
      return next;
    });
  }

  async function handleSubmit(event: React.FormEvent) {
    event.preventDefault();
    if (phase === "sending" || phase === "sent") return; // impede envio duplicado

    const next: Record<string, string> = {};
    if (!values.name.trim()) next.name = "Informe seu nome.";
    if (!isValidEmail(values.email)) next.email = "Informe um e-mail válido.";
    if (values.message.trim().length < 10)
      next.message = "Escreva uma mensagem com pelo menos 10 caracteres.";
    setErrors(next);
    if (Object.keys(next).length > 0) return;

    setPhase("sending");
    try {
      const res = await fetch("/api/contact", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(values),
      });
      if (!res.ok) throw new Error();
      setPhase("sent");
    } catch {
      setPhase("error");
    }
  }

  if (phase === "sent") {
    return (
      <StatusMessage tone="success" title="Mensagem enviada">
        Obrigada pelo contato! Retornaremos assim que possível.
      </StatusMessage>
    );
  }

  return (
    <form className="contact-form" onSubmit={handleSubmit} noValidate>
      <div className={`form-field${errors.name ? " form-field--error" : ""}`}>
        <label htmlFor="contact-name">Nome</label>
        <input
          id="contact-name"
          name="name"
          autoComplete="name"
          required
          value={values.name}
          onChange={(e) => set("name", e.target.value)}
          aria-invalid={Boolean(errors.name)}
          aria-describedby={errors.name ? "contact-name-error" : undefined}
        />
        {errors.name && (
          <p className="form-field__error" id="contact-name-error" role="alert">
            {errors.name}
          </p>
        )}
      </div>

      <div className="form-row">
        <div className={`form-field${errors.email ? " form-field--error" : ""}`}>
          <label htmlFor="contact-email">E-mail</label>
          <input
            id="contact-email"
            name="email"
            type="email"
            autoComplete="email"
            required
            value={values.email}
            onChange={(e) => set("email", e.target.value)}
            aria-invalid={Boolean(errors.email)}
            aria-describedby={errors.email ? "contact-email-error" : undefined}
          />
          {errors.email && (
            <p className="form-field__error" id="contact-email-error" role="alert">
              {errors.email}
            </p>
          )}
        </div>
        <div className="form-field">
          <label htmlFor="contact-phone">
            Telefone <span className="form-field__optional">(opcional)</span>
          </label>
          <input
            id="contact-phone"
            name="phone"
            type="tel"
            autoComplete="tel"
            value={values.phone}
            onChange={(e) => set("phone", e.target.value)}
          />
        </div>
      </div>

      <div className={`form-field${errors.message ? " form-field--error" : ""}`}>
        <label htmlFor="contact-message">Mensagem</label>
        <textarea
          id="contact-message"
          name="message"
          rows={5}
          required
          value={values.message}
          onChange={(e) => set("message", e.target.value)}
          aria-invalid={Boolean(errors.message)}
          aria-describedby={errors.message ? "contact-message-error" : undefined}
        />
        {errors.message && (
          <p className="form-field__error" id="contact-message-error" role="alert">
            {errors.message}
          </p>
        )}
      </div>

      {phase === "error" && (
        <StatusMessage tone="error" title="Não foi possível enviar">
          Tente novamente em instantes ou fale conosco pelo Instagram.
        </StatusMessage>
      )}

      <Button type="submit" loading={phase === "sending"}>
        Enviar mensagem
      </Button>
    </form>
  );
}
