# Petite Vallée — E-commerce independente

Loja virtual própria da **Petite Vallée** (Valinhos, SP), construída com
código 100% próprio — **sem Shopify, Wix, Framer ou qualquer construtor
com assinatura**. O código pertence integralmente à Petite Vallée e pode
ser hospedado em qualquer plataforma compatível com Next.js/Node.js e
conectado a qualquer domínio próprio.

## Tecnologias

- [Next.js](https://nextjs.org) (App Router) + React + TypeScript
- CSS moderno com design tokens (sem frameworks de UI)
- Carrinho persistido em `localStorage`
- Arquitetura de pagamento com provedor substituível (Pix e cartão)

## Como rodar localmente

```bash
cd petite-vallee
npm install
cp .env.example .env.local   # preencha quando tiver as chaves
npm run dev                  # http://localhost:3000
```

Build de produção:

```bash
npm run build
npm start
```

## Como publicar

O site roda em qualquer hospedagem com suporte a Next.js/Node.js —
Vercel, Netlify, Railway, Render, Fly.io ou um VPS próprio. Nenhuma
delas exige assinatura para conectar um domínio próprio (a Vercel, por
exemplo, permite domínio próprio no plano gratuito). Passos gerais:

1. Suba este diretório para um repositório GitHub da Petite Vallée.
2. Conecte o repositório à hospedagem escolhida (diretório raiz:
   `petite-vallee`).
3. Configure as variáveis de ambiente do `.env.example`.
4. Aponte o domínio comprado (registro.br, etc.) para a hospedagem.

## Estrutura do projeto

```
petite-vallee/
├── public/
│   ├── brand/logo.svg          ← logotipo (PLACEHOLDER — ver abaixo)
│   └── images/products/        ← fotos dos produtos (placeholders)
├── src/
│   ├── app/                    ← páginas e rotas de API
│   ├── components/             ← componentes reutilizáveis
│   ├── data/products.ts        ← ⭐ CATÁLOGO (edite aqui)
│   ├── lib/
│   │   ├── brand.ts            ← dados da marca (logo, contatos)
│   │   ├── cart/               ← carrinho (Context + localStorage)
│   │   ├── checkout.ts         ← validação de pedidos no servidor
│   │   ├── orders/             ← pedidos (camada substituível)
│   │   ├── payment/            ← gateway de pagamento (substituível)
│   │   └── shipping.ts         ← regras de frete (em definição)
│   └── styles/
│       ├── globals.css         ← ⭐ DESIGN TOKENS (cores, fontes…)
│       └── site.css            ← estilos dos componentes
├── .env.example                ← modelo das variáveis de ambiente
└── README.md
```

## Como gerenciar os produtos

Tudo acontece em **`src/data/products.ts`** — o arquivo tem instruções
detalhadas no topo. Resumo:

| Tarefa | Como fazer |
| --- | --- |
| Adicionar produto | Copie um objeto da lista, mude `id`, `slug`, nome, preço e imagem |
| Remover produto | Apague o objeto (ou use `available: false` para só ocultar a compra) |
| Alterar preço | Edite `priceInCents` — **em centavos**: R$ 29,90 → `2990` |
| Trocar imagem | Substitua o arquivo em `public/images/products/` e ajuste o campo `image` |
| Marcar indisponível | `available: false` |
| Destacar na home | `featured: true` |

## ⚠️ Assets provisórios (substituir pelos oficiais)

Nenhum arquivo oficial (logo, fotos, vídeo) estava disponível neste
repositório quando a primeira versão foi construída. Foram usados
placeholders **claramente identificados**, que devem ser trocados:

1. **Logotipo** — substitua `public/brand/logo.svg` pelo arquivo oficial
   (mantendo o nome, ou atualizando `src/lib/brand.ts`). O favicon
   (`src/app/icon.svg`) também deve ser regenerado a partir da logo
   oficial. *Nenhuma logo nova deve ser criada.*
2. **Fotos dos produtos** — salve as fotos reais em
   `public/images/products/` e atualize o campo `image` de cada produto
   em `src/data/products.ts` (remova `imageIsPlaceholder`).
3. **Descrições** — os textos de produto seguem provisórios até a
   versão manuscrita da marca. Preços, ingredientes, tabela
   nutricional, peso e validade já são os oficiais (ago/2026).
4. **Políticas** — os textos jurídicos são rascunhos marcados para
   revisão nas próprias páginas.

Decisões da marca já aplicadas: o vídeo institucional foi removido do
site; as geleias saíram do catálogo fixo e voltarão como **edições
limitadas** (ver instruções em `src/data/products.ts`); a entrega será
para todo o Brasil pelos Correios com frete por CEP (integração
documentada em `src/lib/shipping.ts`).

## 📋 PARA SER FEITO AINDA (backlog acordado)

Itens que **não travam o uso atual do site**. Numerados para irmos
resolvendo um a um.

### A. Conteúdo — a Petite Vallée envia, o site recebe

- [x] **1.** Fotos reais dos produtos — 4 de 6 aplicadas
      (Tradicional, Naturel, Mix de Castanhas, Mix de Sementes);
      FALTAM as fotos da Granola Sans Sucre e da Barrinha Petite
      Sucrée (seguem com placeholder)
- [x] **2.** Logotipo oficial aplicado (emblema circular) — arquivo
      em `public/brand/logo.png`; favicon segue com a folha
      provisória por legibilidade em tamanho pequeno
- [ ] **3.** Textos manuscritos definitivos (hero, produtos, história)
- [ ] **4.** Alergênicos e instruções de conservação de cada produto
- [ ] **5.** CNPJ / razão social para o rodapé (Decreto 7.962/2013
      do e-commerce)
- [ ] **6.** Revisão final das políticas (privacidade, trocas,
      entrega, termos)

### B. Contas e cadastros — criar (gratuitos), depois eu conecto

- [ ] **7.** Conta no Resend (resend.com) → ativa a notificação de
      venda já implementada (`RESEND_API_KEY` + `ORDER_NOTIFY_EMAIL`)
- [ ] **8.** Conta no gateway de pagamento com Pix + cartão
      (Mercado Pago, Pagar.me ou Asaas)
- [ ] **9.** Conta no SuperFrete ou Melhor Envio (cotação Correios
      por CEP + etiquetas com desconto)
- [ ] **10.** Domínio próprio (registro.br, ~R$ 40/ano)
- [ ] **11.** Catálogo Meta: WhatsApp Business + Instagram Shopping
      com os produtos marcados nos posts (configuração nos apps da
      Meta; o site fornece as páginas de produto para linkar)

### C. Desenvolvimento — fase de lançamento (dependem dos itens B)

- [ ] **12.** Banco de dados de pedidos + número amigável de pedido
- [ ] **13.** Integração do gateway: Pix + cartão, página segura de
      pagamento e confirmação automática via webhook (depende do 8)
- [ ] **14.** Frete real por CEP com valor, prazo e opções no
      carrinho e no checkout + regra de entrega própria para
      CEPs/cidades próximas (depende do 9)
- [ ] **15.** Status completos do pedido (aguardando pagamento →
      entregue) + página de acompanhamento com código de rastreio
- [ ] **16.** Painel com login — aba Pedidos (mudar status, colar
      rastreio, estoque interno) e aba Vendas (receita, nº de
      pedidos, ticket médio, comparação vs. mês anterior, gráfico
      de vendas, mix por produto, receita líquida estimada
      pós-taxas, exportação CSV)
- [ ] **17.** E-mails transacionais ao cliente: confirmação de
      pedido e aviso de envio com rastreio (depende do 7)
- [ ] **18.** "Avise-me quando voltar" nas edições limitadas
      (captura de e-mail para avisar do próximo lote; depende do 7)
- [ ] **19.** Campo "É presente? 🎁" no checkout, com mensagem para
      o cartãozinho
- [ ] **20.** Migração para hospedagem gratuita definitiva
      (Cloudflare) + conexão do domínio (depende do 10)

### Ajustes de interface pedidos

- [x] **22.** Compactar o bloco "Calcular frete e prazo" no carrinho
      lateral — feito: agora fica recolhido num link discreto e só
      abre ao tocar; de quebra, corrigido um estouro de largura do
      rodapé do carrinho em telas pequenas.

### D. Automático quando o conteúdo chegar

- [ ] **21.** Prévias bonitas ao compartilhar links no
      WhatsApp/Instagram (foto + nome + preço) — já preparado,
      passa a valer quando as fotos (item 1) forem adicionadas

### Já implementado e aguardando apenas ativação

- [x] Notificação de novo pedido por e-mail para a equipe (ativa
      com o item 7)
- [x] Estimativa de frete por CEP no carrinho (mostra valores
      reais automaticamente após o item 14)
- [x] Pedido pelo WhatsApp com mensagem pronta + botão discreto de
      WhatsApp no site

## Pagamentos (Pix e cartão)

A loja está em **modo de demonstração** enquanto não há conta em um
gateway: o carrinho e o checkout funcionam, os dados são validados, mas
**nenhuma cobrança real é criada** e nada é apresentado como pago.

Ponto de integração documentado em **`src/lib/payment/provider.ts`**:

1. Escolha um gateway brasileiro com Pix + cartão (Mercado Pago,
   Pagar.me, Asaas…).
2. Implemente a interface `PaymentProvider` num arquivo novo em
   `src/lib/payment/` usando a SDK oficial do provedor.
3. Registre-o em `getPaymentProvider()` e defina `PAYMENT_PROVIDER` no
   `.env.local` com as chaves do gateway.

Garantias já embutidas na arquitetura:

- Cobranças criadas **somente no servidor**; chaves privadas nunca vão
  ao navegador (`.env.local`, fora do git).
- Totais **recalculados no servidor** a partir do catálogo — o preço
  enviado pelo navegador é ignorado.
- Dados de cartão **nunca** tocam nosso servidor: usar a tokenização do
  gateway no frontend.
- Pedido só vira "pago" via **webhook autenticado** do gateway
  (`/api/webhooks/payment`) — nunca porque o cliente chegou à página de
  sucesso.

## Pedidos e banco de dados

Os pedidos usam uma camada substituível (`src/lib/orders/store.ts`).
Hoje é uma implementação em memória, adequada apenas ao modo de
demonstração. Antes de vender de verdade, implemente `OrderStore` com um
banco real (Postgres, Supabase, etc.) e troque a exportação no final do
arquivo.

## Frete

As regras reais ainda não foram definidas. `src/lib/shipping.ts` mostra
hoje uma única opção de demonstração (R$ 0, claramente identificada) e
documenta como adicionar frete fixo, retirada, entrega local ou cálculo
por CEP.

## Rotas

| Rota | Conteúdo |
| --- | --- |
| `/` | Home: hero, catálogo com filtros, convite à história |
| `/produtos` | Catálogo completo |
| `/produto/[slug]` | Página individual do produto |
| `/nossa-historia` | Página editorial + vídeo |
| `/contato` | Formulário e canais de contato |
| `/carrinho` | Página do carrinho (além do drawer lateral) |
| `/checkout` | Checkout independente |
| `/pedido/sucesso` · `/pedido/pendente` · `/pedido/erro` | Status do pedido |
| `/politica-de-*` e `/termos-de-uso` | Páginas jurídicas provisórias |
| `/api/checkout`, `/api/payment/*`, `/api/webhooks/payment` | Backend |

## Design

- Cor predominante: **`#E9EDD9`** (definida em
  `src/styles/globals.css` — não alterar sem autorização).
- Verde-oliva `#74785E` apenas em detalhes (ícones, etiquetas, hovers).
- Tipografia: Lora (serifada) em todo o site, acompanhando os rótulos
  e o material impresso da marca.
- Mobile-first, acessível (foco, ARIA, `prefers-reduced-motion`,
  trava de foco no carrinho e no menu).
