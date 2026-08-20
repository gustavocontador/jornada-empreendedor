"use client";

import Image from "next/image";
import Link from "next/link";
import { useState } from "react";
import { brand } from "@/lib/brand";
import { useCart } from "@/lib/cart/CartContext";
import { MobileMenu } from "./MobileMenu";

export const NAV_LINKS = [
  { href: "/", label: "Início" },
  { href: "/produtos", label: "Produtos" },
  { href: "/nossa-historia", label: "Nossa História" },
  { href: "/contato", label: "Contato" },
] as const;

/**
 * Header aderente e minimalista: logo, navegação, carrinho com
 * contador dinâmico e menu hambúrguer no mobile.
 */
export function Header() {
  const { itemCount, openCart, hydrated } = useCart();
  const [menuOpen, setMenuOpen] = useState(false);

  return (
    <header className="site-header">
      <div className="site-header__inner container">
        <button
          type="button"
          className="site-header__menu-button"
          aria-label="Abrir menu de navegação"
          aria-expanded={menuOpen}
          aria-controls="mobile-menu"
          onClick={() => setMenuOpen(true)}
        >
          <svg width="22" height="16" viewBox="0 0 22 16" aria-hidden="true">
            <path
              d="M1 1h20M1 8h20M1 15h20"
              stroke="currentColor"
              strokeWidth="1.6"
              strokeLinecap="round"
            />
          </svg>
        </button>

        <Link href="/" className="site-header__logo" aria-label="Petite Vallée — página inicial">
          <Image
            src={brand.logo.src}
            alt={brand.logo.alt}
            width={180}
            height={48}
            priority
            unoptimized
          />
        </Link>

        <nav className="site-header__nav" aria-label="Navegação principal">
          {NAV_LINKS.map((link) => (
            <Link key={link.href} href={link.href} className="site-header__link">
              {link.label}
            </Link>
          ))}
        </nav>

        <button
          type="button"
          className="site-header__cart"
          onClick={openCart}
          aria-label={
            hydrated && itemCount > 0
              ? `Abrir carrinho, ${itemCount} ${itemCount === 1 ? "item" : "itens"}`
              : "Abrir carrinho"
          }
        >
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" aria-hidden="true">
            <path
              d="M4.5 7.5h15l-1.2 11a2 2 0 0 1-2 1.8H7.7a2 2 0 0 1-2-1.8l-1.2-11z"
              stroke="currentColor"
              strokeWidth="1.5"
              strokeLinejoin="round"
            />
            <path
              d="M8.5 10V6a3.5 3.5 0 0 1 7 0v4"
              stroke="currentColor"
              strokeWidth="1.5"
              strokeLinecap="round"
            />
          </svg>
          {hydrated && itemCount > 0 && (
            <span className="site-header__cart-count" aria-hidden="true">
              {itemCount}
            </span>
          )}
        </button>
      </div>

      <MobileMenu open={menuOpen} onClose={() => setMenuOpen(false)} />
    </header>
  );
}
