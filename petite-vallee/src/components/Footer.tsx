import Image from "next/image";
import Link from "next/link";
import { brand } from "@/lib/brand";
import { BotanicalDivider } from "./BotanicalDecoration";

const POLICY_LINKS = [
  { href: "/politica-de-privacidade", label: "Política de Privacidade" },
  { href: "/termos-de-uso", label: "Termos de Uso" },
  { href: "/politica-de-entrega", label: "Política de Entrega" },
  { href: "/politica-de-trocas", label: "Trocas e Devoluções" },
];

const NAV = [
  { href: "/", label: "Início" },
  { href: "/produtos", label: "Produtos" },
  { href: "/nossa-historia", label: "Nossa História" },
  { href: "/contato", label: "Contato" },
];

export function Footer() {
  return (
    <footer className="site-footer">
      <div className="container">
        <BotanicalDivider />
        <div className="site-footer__grid">
          <div className="site-footer__brand">
            <Image
              src={brand.logo.src}
              alt={brand.logo.alt}
              width={96}
              height={96}
            />
            <p className="site-footer__tagline">
              Granolas, mixes e barrinhas artesanais, sem conservantes e sem
              glúten.
            </p>
          </div>

          <nav className="site-footer__col" aria-label="Navegação do rodapé">
            <h3 className="site-footer__heading">Navegue</h3>
            <ul>
              {NAV.map((link) => (
                <li key={link.href}>
                  <Link href={link.href}>{link.label}</Link>
                </li>
              ))}
            </ul>
          </nav>

          <nav className="site-footer__col" aria-label="Políticas da loja">
            <h3 className="site-footer__heading">Políticas</h3>
            <ul>
              {POLICY_LINKS.map((link) => (
                <li key={link.href}>
                  <Link href={link.href}>{link.label}</Link>
                </li>
              ))}
            </ul>
          </nav>

          <div className="site-footer__col">
            <h3 className="site-footer__heading">Fale conosco</h3>
            <ul>
              <li>
                <Link href="/contato">Página de contato</Link>
              </li>
              {brand.instagramUrl ? (
                <li>
                  <a href={brand.instagramUrl} rel="noopener noreferrer" target="_blank">
                    Instagram
                  </a>
                </li>
              ) : (
                <li className="site-footer__pending">
                  Instagram — em breve
                </li>
              )}
              {brand.whatsappUrl ? (
                <li>
                  <a href={brand.whatsappUrl} rel="noopener noreferrer" target="_blank">
                    WhatsApp
                  </a>
                </li>
              ) : (
                <li className="site-footer__pending">WhatsApp — em breve</li>
              )}
            </ul>
          </div>
        </div>

        <p className="site-footer__copyright">
          © {new Date().getFullYear()} {brand.name}. Todos os direitos
          reservados.
        </p>
      </div>
    </footer>
  );
}
