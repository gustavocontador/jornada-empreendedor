"use client";

/**
 * Exibição da cobrança Pix.
 *
 * Quando um gateway real estiver configurado, o /api/checkout
 * devolve `charge.pix` com QR Code, código copia e cola e
 * validade — e este componente os exibe, consultando
 * /api/payment/status periodicamente até a confirmação.
 *
 * Em modo de demonstração este componente não é usado (nenhuma
 * cobrança é criada).
 */

import { useEffect, useState } from "react";
import type { PixChargeData } from "@/lib/payment/provider";
import { formatPrice } from "@/lib/format";
import { StatusMessage } from "./StatusMessage";

interface PixPaymentProps {
  orderId: string;
  totalInCents: number;
  pix: PixChargeData;
}

export function PixPayment({ orderId, totalInCents, pix }: PixPaymentProps) {
  const [copied, setCopied] = useState(false);
  const [status, setStatus] = useState<string>("pending");

  // Consulta o status do pedido a cada 6s enquanto aguarda o Pix.
  useEffect(() => {
    if (status !== "pending") return;
    const interval = setInterval(async () => {
      try {
        const res = await fetch(`/api/payment/status?orderId=${orderId}`);
        if (!res.ok) return;
        const data = (await res.json()) as { paymentStatus?: string };
        if (data.paymentStatus && data.paymentStatus !== "pending") {
          setStatus(data.paymentStatus);
          if (data.paymentStatus === "paid") {
            window.location.href = `/pedido/sucesso?orderId=${orderId}`;
          }
        }
      } catch {
        // falha de rede transitória: tenta de novo no próximo ciclo
      }
    }, 6000);
    return () => clearInterval(interval);
  }, [orderId, status]);

  async function copyCode() {
    if (!pix.copyPasteCode) return;
    try {
      await navigator.clipboard.writeText(pix.copyPasteCode);
      setCopied(true);
      setTimeout(() => setCopied(false), 2500);
    } catch {
      setCopied(false);
    }
  }

  return (
    <div className="pix-payment">
      <h2 className="pix-payment__title">Pague com Pix</h2>
      <p className="pix-payment__amount">Valor: {formatPrice(totalInCents)}</p>

      {pix.qrCodeBase64 && (
        /* eslint-disable-next-line @next/next/no-img-element */
        <img
          className="pix-payment__qr"
          src={`data:image/png;base64,${pix.qrCodeBase64}`}
          alt="QR Code para pagamento via Pix"
          width={220}
          height={220}
        />
      )}

      {pix.copyPasteCode && (
        <div className="pix-payment__copy">
          <label htmlFor="pix-code">Código Pix copia e cola</label>
          <textarea id="pix-code" readOnly rows={3} value={pix.copyPasteCode} />
          <button type="button" className="btn btn--secondary" onClick={copyCode}>
            <span>{copied ? "Código copiado ✓" : "Copiar código"}</span>
          </button>
        </div>
      )}

      {pix.expiresAt && (
        <p className="pix-payment__expiry">
          Este código é válido até{" "}
          {new Date(pix.expiresAt).toLocaleString("pt-BR")}.
        </p>
      )}

      <StatusMessage tone="info" title="Aguardando pagamento">
        Assim que o Pix for confirmado pelo banco, esta página será
        atualizada automaticamente.
      </StatusMessage>
    </div>
  );
}
