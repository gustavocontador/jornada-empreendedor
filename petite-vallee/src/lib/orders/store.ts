/**
 * Camada de persistência de pedidos — SUBSTITUÍVEL.
 *
 * Enquanto a loja não tem banco de dados, os pedidos ficam em
 * memória no servidor (eles se perdem quando o processo
 * reinicia — aceitável apenas no modo de demonstração).
 *
 * ⚠️ NUNCA usar esta implementação em produção com vendas reais.
 *
 * PARA O AMBIENTE REAL: crie uma classe que implemente a
 * interface `OrderStore` usando o banco escolhido (Postgres,
 * SQLite, Supabase, PlanetScale...) e troque a exportação
 * `orderStore` no final deste arquivo. Nenhum outro arquivo do
 * projeto precisa mudar.
 */

import { randomUUID } from "crypto";
import type { Order, PaymentStatus } from "./types";

export interface OrderStore {
  create(order: Omit<Order, "id" | "createdAt" | "updatedAt">): Promise<Order>;
  getById(id: string): Promise<Order | undefined>;
  getByProviderId(providerId: string): Promise<Order | undefined>;
  updateStatus(id: string, status: PaymentStatus): Promise<Order | undefined>;
}

class InMemoryOrderStore implements OrderStore {
  private orders = new Map<string, Order>();

  async create(
    data: Omit<Order, "id" | "createdAt" | "updatedAt">
  ): Promise<Order> {
    const now = new Date().toISOString();
    const order: Order = {
      ...data,
      id: `pv-${randomUUID()}`,
      createdAt: now,
      updatedAt: now,
    };
    this.orders.set(order.id, order);
    return order;
  }

  async getById(id: string): Promise<Order | undefined> {
    return this.orders.get(id);
  }

  async getByProviderId(providerId: string): Promise<Order | undefined> {
    for (const order of this.orders.values()) {
      if (order.paymentProviderId === providerId) return order;
    }
    return undefined;
  }

  async updateStatus(
    id: string,
    status: PaymentStatus
  ): Promise<Order | undefined> {
    const order = this.orders.get(id);
    if (!order) return undefined;
    const updated: Order = {
      ...order,
      paymentStatus: status,
      updatedAt: new Date().toISOString(),
    };
    this.orders.set(id, updated);
    return updated;
  }
}

/** Troque esta linha ao conectar um banco de dados real. */
export const orderStore: OrderStore = new InMemoryOrderStore();
