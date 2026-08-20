"use client";

import Link from "next/link";
import { useRef } from "react";
import { useFocusTrap } from "@/lib/useFocusTrap";
import { NAV_LINKS } from "./Header";
import { BotanicalDecoration } from "./BotanicalDecoration";

interface MobileMenuProps {
  open: boolean;
  onClose: () => void;
}

/** Menu hambúrguer acessível: trava de foco, Escape e backdrop. */
export function MobileMenu({ open, onClose }: MobileMenuProps) {
  const panelRef = useRef<HTMLDivElement>(null);
  useFocusTrap(panelRef, open, onClose);

  if (!open) return null;

  return (
    <div className="mobile-menu" id="mobile-menu">
      <div
        className="mobile-menu__backdrop"
        onClick={onClose}
        aria-hidden="true"
      />
      <div
        ref={panelRef}
        className="mobile-menu__panel"
        role="dialog"
        aria-modal="true"
        aria-label="Menu de navegação"
      >
        <div className="mobile-menu__header">
          <BotanicalDecoration size={22} />
          <button
            type="button"
            className="mobile-menu__close"
            onClick={onClose}
            aria-label="Fechar menu"
          >
            <svg width="18" height="18" viewBox="0 0 18 18" aria-hidden="true">
              <path
                d="M2 2l14 14M16 2L2 16"
                stroke="currentColor"
                strokeWidth="1.6"
                strokeLinecap="round"
              />
            </svg>
          </button>
        </div>
        <nav aria-label="Navegação principal">
          <ul className="mobile-menu__list">
            {NAV_LINKS.map((link) => (
              <li key={link.href}>
                <Link
                  href={link.href}
                  className="mobile-menu__link"
                  onClick={onClose}
                >
                  {link.label}
                </Link>
              </li>
            ))}
            <li>
              <Link href="/carrinho" className="mobile-menu__link" onClick={onClose}>
                Carrinho
              </Link>
            </li>
          </ul>
        </nav>
      </div>
    </div>
  );
}
