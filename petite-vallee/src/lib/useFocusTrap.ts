"use client";

/**
 * Trava de foco para diálogos (carrinho lateral, menu mobile).
 * - Move o foco para dentro do painel ao abrir.
 * - Mantém Tab/Shift+Tab circulando dentro do painel.
 * - Fecha com Escape.
 * - Devolve o foco ao elemento que abriu o painel ao fechar.
 */

import { useEffect, useRef, type RefObject } from "react";

const FOCUSABLE =
  'a[href], button:not([disabled]), input:not([disabled]), select:not([disabled]), textarea:not([disabled]), [tabindex]:not([tabindex="-1"])';

export function useFocusTrap(
  containerRef: RefObject<HTMLElement | null>,
  isOpen: boolean,
  onClose: () => void
) {
  const previouslyFocused = useRef<HTMLElement | null>(null);

  useEffect(() => {
    if (!isOpen) return;
    const container = containerRef.current;
    if (!container) return;

    previouslyFocused.current = document.activeElement as HTMLElement | null;

    // Foca o primeiro elemento interativo do painel.
    const focusables = container.querySelectorAll<HTMLElement>(FOCUSABLE);
    (focusables[0] ?? container).focus();

    function handleKeyDown(event: KeyboardEvent) {
      if (event.key === "Escape") {
        event.preventDefault();
        onClose();
        return;
      }
      if (event.key !== "Tab") return;
      const items = container!.querySelectorAll<HTMLElement>(FOCUSABLE);
      if (items.length === 0) return;
      const first = items[0];
      const last = items[items.length - 1];
      const active = document.activeElement;
      if (event.shiftKey && (active === first || !container!.contains(active))) {
        event.preventDefault();
        last.focus();
      } else if (!event.shiftKey && active === last) {
        event.preventDefault();
        first.focus();
      }
    }

    document.addEventListener("keydown", handleKeyDown);

    // Bloqueia a rolagem do fundo enquanto o painel está aberto.
    const previousOverflow = document.body.style.overflow;
    document.body.style.overflow = "hidden";

    return () => {
      document.removeEventListener("keydown", handleKeyDown);
      document.body.style.overflow = previousOverflow;
      // Devolve o foco ao botão que abriu o painel.
      previouslyFocused.current?.focus();
    };
  }, [isOpen, containerRef, onClose]);
}
