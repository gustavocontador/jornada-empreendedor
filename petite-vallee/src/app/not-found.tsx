import { ButtonLink } from "@/components/Button";
import { BotanicalDecoration } from "@/components/BotanicalDecoration";

export default function NotFound() {
  return (
    <div className="order-status-page">
      <BotanicalDecoration size={40} />
      <h1>Página não encontrada</h1>
      <p>
        O endereço que você procurou não existe ou foi movido. Que tal
        conhecer nossos produtos?
      </p>
      <div className="order-status-page__actions">
        <ButtonLink href="/produtos">Ver produtos</ButtonLink>
        <ButtonLink href="/" variant="secondary">
          Voltar ao início
        </ButtonLink>
      </div>
    </div>
  );
}
