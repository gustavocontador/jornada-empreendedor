import Link from "next/link";
import type { ButtonHTMLAttributes, ReactNode } from "react";

type Variant = "primary" | "secondary" | "ghost";

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: Variant;
  loading?: boolean;
  children: ReactNode;
}

/**
 * Botão padrão da loja. O CTA principal usa a cor "ameixa
 * profunda" (--color-button); o verde-oliva aparece apenas como
 * detalhe de hover/borda, nunca como preenchimento dominante.
 */
export function Button({
  variant = "primary",
  loading = false,
  disabled,
  children,
  className,
  ...rest
}: ButtonProps) {
  return (
    <button
      className={`btn btn--${variant}${className ? ` ${className}` : ""}`}
      disabled={disabled || loading}
      aria-busy={loading || undefined}
      {...rest}
    >
      {loading && <span className="btn__spinner" aria-hidden="true" />}
      <span>{children}</span>
    </button>
  );
}

interface ButtonLinkProps {
  href: string;
  variant?: Variant;
  children: ReactNode;
  className?: string;
}

export function ButtonLink({
  href,
  variant = "primary",
  children,
  className,
}: ButtonLinkProps) {
  return (
    <Link
      href={href}
      className={`btn btn--${variant}${className ? ` ${className}` : ""}`}
    >
      <span>{children}</span>
    </Link>
  );
}
