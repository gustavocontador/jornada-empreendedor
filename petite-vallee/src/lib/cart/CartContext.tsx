"use client";

/**
 * Carrinho de compras da Petite Vallée.
 *
 * - Estado global via React Context (sem dependências externas).
 * - Persistência em localStorage, lida somente no cliente após a
 *   hidratação (evita erros de renderização no servidor).
 * - Os itens guardam apenas `productId` e `quantity`; preço e nome
 *   são sempre relidos do catálogo, então uma mudança de preço no
 *   arquivo de produtos vale imediatamente para carrinhos antigos.
 */

import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useRef,
  useState,
  type ReactNode,
} from "react";
import { getProductById, type Product } from "@/data/products";

const STORAGE_KEY = "petite-vallee-cart-v1";
const MAX_QUANTITY = 20;

export interface CartLine {
  productId: string;
  quantity: number;
}

export interface CartItemView {
  product: Product;
  quantity: number;
  lineTotalInCents: number;
}

interface CartContextValue {
  /** true após ler o localStorage (evita piscar contagem errada) */
  hydrated: boolean;
  items: CartItemView[];
  itemCount: number;
  subtotalInCents: number;
  isOpen: boolean;
  openCart: () => void;
  closeCart: () => void;
  addItem: (productId: string, quantity?: number) => void;
  setQuantity: (productId: string, quantity: number) => void;
  removeItem: (productId: string) => void;
  clearCart: () => void;
  /** id do último produto adicionado (para feedback "Adicionado!") */
  lastAddedId: string | null;
}

const CartContext = createContext<CartContextValue | null>(null);

function readStoredCart(): CartLine[] {
  try {
    const raw = window.localStorage.getItem(STORAGE_KEY);
    if (!raw) return [];
    const parsed: unknown = JSON.parse(raw);
    if (!Array.isArray(parsed)) return [];
    return parsed
      .filter(
        (line): line is CartLine =>
          typeof line === "object" &&
          line !== null &&
          typeof (line as CartLine).productId === "string" &&
          typeof (line as CartLine).quantity === "number"
      )
      // descarta itens de produtos que saíram do catálogo
      .filter((line) => getProductById(line.productId) !== undefined)
      .map((line) => ({
        productId: line.productId,
        quantity: Math.min(Math.max(1, Math.round(line.quantity)), MAX_QUANTITY),
      }));
  } catch {
    return [];
  }
}

export function CartProvider({ children }: { children: ReactNode }) {
  const [lines, setLines] = useState<CartLine[]>([]);
  const [hydrated, setHydrated] = useState(false);
  const [isOpen, setIsOpen] = useState(false);
  const [lastAddedId, setLastAddedId] = useState<string | null>(null);
  const lastAddedTimer = useRef<ReturnType<typeof setTimeout> | null>(null);

  // Lê o carrinho salvo apenas no cliente, após a primeira renderização.
  useEffect(() => {
    setLines(readStoredCart());
    setHydrated(true);
  }, []);

  // Persiste toda alteração (somente depois da hidratação).
  useEffect(() => {
    if (!hydrated) return;
    try {
      window.localStorage.setItem(STORAGE_KEY, JSON.stringify(lines));
    } catch {
      // localStorage indisponível (modo privado etc.) — carrinho segue em memória
    }
  }, [lines, hydrated]);

  const openCart = useCallback(() => setIsOpen(true), []);
  const closeCart = useCallback(() => setIsOpen(false), []);

  const addItem = useCallback((productId: string, quantity = 1) => {
    const product = getProductById(productId);
    if (!product || !product.available) return;
    setLines((prev) => {
      const existing = prev.find((l) => l.productId === productId);
      if (existing) {
        return prev.map((l) =>
          l.productId === productId
            ? { ...l, quantity: Math.min(l.quantity + quantity, MAX_QUANTITY) }
            : l
        );
      }
      return [...prev, { productId, quantity: Math.min(quantity, MAX_QUANTITY) }];
    });
    setLastAddedId(productId);
    if (lastAddedTimer.current) clearTimeout(lastAddedTimer.current);
    lastAddedTimer.current = setTimeout(() => setLastAddedId(null), 2000);
  }, []);

  const setQuantity = useCallback((productId: string, quantity: number) => {
    setLines((prev) => {
      if (quantity <= 0) return prev.filter((l) => l.productId !== productId);
      return prev.map((l) =>
        l.productId === productId
          ? { ...l, quantity: Math.min(quantity, MAX_QUANTITY) }
          : l
      );
    });
  }, []);

  const removeItem = useCallback((productId: string) => {
    setLines((prev) => prev.filter((l) => l.productId !== productId));
  }, []);

  const clearCart = useCallback(() => setLines([]), []);

  const items = useMemo<CartItemView[]>(
    () =>
      lines.flatMap((line) => {
        const product = getProductById(line.productId);
        if (!product) return [];
        return [
          {
            product,
            quantity: line.quantity,
            lineTotalInCents: product.priceInCents * line.quantity,
          },
        ];
      }),
    [lines]
  );

  const itemCount = useMemo(
    () => items.reduce((sum, item) => sum + item.quantity, 0),
    [items]
  );

  const subtotalInCents = useMemo(
    () => items.reduce((sum, item) => sum + item.lineTotalInCents, 0),
    [items]
  );

  const value = useMemo(
    () => ({
      hydrated,
      items,
      itemCount,
      subtotalInCents,
      isOpen,
      openCart,
      closeCart,
      addItem,
      setQuantity,
      removeItem,
      clearCart,
      lastAddedId,
    }),
    [
      hydrated,
      items,
      itemCount,
      subtotalInCents,
      isOpen,
      openCart,
      closeCart,
      addItem,
      setQuantity,
      removeItem,
      clearCart,
      lastAddedId,
    ]
  );

  return <CartContext.Provider value={value}>{children}</CartContext.Provider>;
}

export function useCart(): CartContextValue {
  const ctx = useContext(CartContext);
  if (!ctx) {
    throw new Error("useCart deve ser usado dentro de <CartProvider>");
  }
  return ctx;
}
