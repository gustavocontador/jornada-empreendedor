/**
 * POST /api/contact
 *
 * Recebe mensagens do formulário de contato.
 *
 * [PROVISÓRIO] Enquanto o canal definitivo (e-mail da loja,
 * ferramenta de atendimento…) não é definido, a mensagem é
 * apenas registrada no log do servidor. Ponto de integração:
 * substitua o console.log por um envio real (ex.: Resend,
 * Nodemailer + SMTP, ou webhook para um CRM).
 */

import { NextResponse } from "next/server";
import { isValidEmail } from "@/lib/format";

export async function POST(request: Request) {
  let body: { name?: string; email?: string; phone?: string; message?: string };
  try {
    body = await request.json();
  } catch {
    return NextResponse.json({ error: "Requisição inválida." }, { status: 400 });
  }

  const name = body.name?.trim().slice(0, 120);
  const email = body.email?.trim().slice(0, 200);
  const message = body.message?.trim().slice(0, 2000);

  if (!name || !email || !isValidEmail(email) || !message || message.length < 10) {
    return NextResponse.json(
      { error: "Preencha nome, e-mail válido e mensagem." },
      { status: 422 }
    );
  }

  console.log("[contato] nova mensagem recebida:", {
    name,
    email,
    phone: body.phone?.trim().slice(0, 20),
    message,
  });

  return NextResponse.json({ received: true });
}
