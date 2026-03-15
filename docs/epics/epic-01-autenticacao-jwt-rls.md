# Epic 1: Autenticação JWT + RLS

**ID:** EPIC-001
**Título:** Sistema de Autenticação com JWT RS256 e Row-Level Security
**Prioridade:** 🔴 P0 (Crítico - Bloqueante para outros épicos)
**Estimativa:** Large (8-10 dias, 2 devs)
**Status:** 📋 Backlog
**Owner:** @pm (Morgan)

---

## Objetivo

Implementar sistema completo de autenticação segura com JWT assimétrico (RS256), refresh tokens, gestão de usuários e Row-Level Security (RLS) no PostgreSQL para isolamento multi-tenant baseado em roles (user, admin, specialist).

---

## Business Value

### Para o Usuário:
- ✅ Login seguro e rápido (< 2s)
- ✅ Sessão persistente com refresh automático
- ✅ Recuperação de senha self-service
- ✅ Dados protegidos com RLS (usuário só vê seus próprios dados)

### Para o Negócio:
- ✅ **Fundação de segurança** para todo o sistema
- ✅ **Compliance LGPD** com controle de acesso granular
- ✅ **Escalabilidade** com autenticação stateless
- ✅ **Auditoria** de acessos e operações

---

## Escopo

### ✅ In Scope

1. **Registro e Login:**
   - Registro com email + senha (validação forte)
   - Login com geração de access token (15min) + refresh token (7 dias)
   - Logout com invalidação de refresh token
   - Verificação de email (link com token expirável)

2. **Recuperação de Senha:**
   - Solicitação de reset via email
   - Link com token (validade 1 hora)
   - Redefinição de senha
   - Notificação de senha alterada

3. **Gestão de Perfil:**
   - Visualizar perfil (/api/v1/users/me)
   - Editar dados cadastrais
   - Alterar senha (com confirmação da senha atual)
   - Deletar conta (com confirmação via email)

4. **Authorization & RLS:**
   - Roles: user, admin, specialist
   - RLS policies no PostgreSQL (users, assessments, reports)
   - Middleware de autorização no FastAPI
   - Verificação de role em endpoints protegidos

5. **JWT RS256:**
   - Chaves assimétricas (private key no backend, public key pode ser distribuída)
   - Access token com claims: sub (user_id), role, exp, type
   - Refresh token armazenado em httpOnly cookie

### ❌ Out of Scope (Fase 2)

- MFA (Multi-Factor Authentication)
- Login social (Google, Facebook)
- SSO (Single Sign-On)
- Biometria
- Histórico de logins

---

## User Stories (Alto Nível)

### US-001.1: Registro de Usuário
**Como** visitante
**Quero** me cadastrar com email e senha
**Para** acessar a plataforma de assessment

**Critérios de Aceitação:**
- [ ] Formulário de registro com validação client-side (email válido, senha forte)
- [ ] Backend valida email único (não duplicado)
- [ ] Senha armazenada com bcrypt (12 rounds)
- [ ] Email de confirmação enviado com link (validade 24h)
- [ ] Usuário criado com role='user' por padrão
- [ ] Mensagem de sucesso: "Cadastro realizado! Verifique seu email."

---

### US-001.2: Login de Usuário
**Como** usuário cadastrado
**Quero** fazer login com email e senha
**Para** acessar meu assessment e relatórios

**Critérios de Aceitação:**
- [ ] Formulário de login com email + senha
- [ ] Backend verifica credenciais (bcrypt compare)
- [ ] Gera access token JWT RS256 (exp: 15min)
- [ ] Gera refresh token (exp: 7 dias, armazenado em httpOnly cookie)
- [ ] Retorna user data + access token
- [ ] Redirect para dashboard após login bem-sucedido
- [ ] Erro 401 se credenciais inválidas: "Email ou senha incorretos"

---

### US-001.3: Refresh Token Automático
**Como** usuário logado
**Quero** que minha sessão seja renovada automaticamente
**Para** não ter que fazer login a cada 15 minutos

**Critérios de Aceitação:**
- [ ] Frontend detecta access token expirando (1min antes)
- [ ] Chama /api/v1/auth/refresh com httpOnly cookie
- [ ] Backend valida refresh token (verifica exp, validade, user ativo)
- [ ] Gera novo access token (15min)
- [ ] Retorna novo access token ao frontend
- [ ] Frontend atualiza token no Zustand store
- [ ] Se refresh token inválido: logout automático + redirect para login

---

### US-001.4: Recuperação de Senha
**Como** usuário que esqueceu a senha
**Quero** receber um link de reset por email
**Para** criar uma nova senha

**Critérios de Aceitação:**
- [ ] Formulário de "Esqueci minha senha" (apenas email)
- [ ] Backend gera token de reset (UUID, validade 1h)
- [ ] Salva token no DB (tabela password_resets)
- [ ] Envia email com link: /reset-password?token={token}
- [ ] Usuário clica no link, é direcionado para formulário de nova senha
- [ ] Backend valida token (existe, não expirado, não usado)
- [ ] Atualiza senha (bcrypt), marca token como usado
- [ ] Envia email de confirmação: "Sua senha foi alterada"

---

### US-001.5: Admin Visualiza Todos os Participantes
**Como** admin
**Quero** ver lista de todos os usuários e seus assessments
**Para** gerenciar a plataforma

**Critérios de Aceitação:**
- [ ] Endpoint GET /api/v1/admin/participantes (requer role='admin')
- [ ] RLS policy permite admin ver todos os registros
- [ ] Retorna: user_id, name, email, created_at, assessment status, reports
- [ ] Frontend exibe lista com filtros (nome, email, status)
- [ ] Paginação (50 por página)
- [ ] Erro 403 se user sem role='admin' tentar acessar

---

### US-001.6: Row-Level Security Protege Dados
**Como** usuário comum
**Quero** que outros usuários não vejam meus dados
**Para** garantir privacidade

**Critérios de Aceitação:**
- [ ] RLS habilitado em todas as tabelas (users, assessments, compact_reports, full_reports)
- [ ] Policy: user só vê próprios registros (WHERE user_id = current_user_id())
- [ ] Policy: admin/specialist vê todos os registros
- [ ] Teste: user A não consegue acessar assessment de user B (erro 404)
- [ ] Teste: admin consegue acessar assessments de todos os users

---

## Critérios de Aceitação do Epic

### Técnicos

- [ ] **JWT RS256:** Access token gerado com chaves assimétricas
- [ ] **Refresh Token:** Armazenado em httpOnly cookie, rotacionado a cada renovação
- [ ] **Bcrypt:** Senhas hasheadas com salt rounds = 12
- [ ] **RLS Policies:** Implementadas e testadas em PostgreSQL
- [ ] **Middleware:** Verifica JWT e role em todas as rotas protegidas
- [ ] **Email Service:** Envio de emails de confirmação e reset (via SMTP ou SendGrid)
- [ ] **Test Coverage:** 85%+ (unit + integration tests)
- [ ] **Error Handling:** Erros padronizados (401, 403, 404, 422, 500)

### Funcionais

- [ ] Usuário consegue se registrar, confirmar email, fazer login
- [ ] Sessão renovada automaticamente com refresh token
- [ ] Recuperação de senha funcional (end-to-end)
- [ ] Admin vê todos os usuários, user comum vê apenas seus dados
- [ ] Logout invalida refresh token (não pode ser reutilizado)

### Performance

- [ ] Login completo (credenciais → token) em < 500ms (p95)
- [ ] Refresh token em < 200ms (p95)
- [ ] Verificação de JWT em < 50ms (p99)

### Segurança

- [ ] **Nenhuma senha em plain text** (nem em logs)
- [ ] **Rate limiting:** 5 tentativas de login/min por IP
- [ ] **Token expiration:** Access 15min, Refresh 7 dias
- [ ] **HTTPS only** em produção
- [ ] **CORS** configurado (apenas origens permitidas)

---

## Dependências

### Bloqueia

- ✅ **Epic 2:** Assessment (precisa de autenticação para criar/submeter)
- ✅ **Epic 3:** Relatório Compacto (precisa de user_id para associar relatório)
- ✅ **Epic 4:** Relatório Full (precisa de role='specialist' para editar feedback)
- ✅ **Epic 5:** Painel Admin (precisa de role='admin' para acessar)
- ✅ **Epic 6:** Pagamentos (precisa de user_id para associar compra)

### É Bloqueado Por

- ⚠️ **Epic 7:** Setup Monorepo (precisa de estrutura base backend/frontend)

---

## Tech Stack

### Backend (Python)

- **FastAPI 0.115+:** Framework web
- **python-jose[cryptography]:** JWT RS256
- **passlib[bcrypt]:** Hashing de senhas
- **SQLAlchemy 2.x async:** ORM
- **Alembic:** Migrations
- **PostgreSQL 16+:** Database com RLS
- **Pydantic v2:** Validação de schemas

### Frontend (TypeScript)

- **Next.js 15+ App Router**
- **Zustand:** State management (authStore)
- **React Hook Form:** Formulários
- **Zod:** Validação client-side

### Infrastructure

- **Supabase:** PostgreSQL managed + RLS
- **SendGrid / SMTP:** Envio de emails
- **Railway:** Backend deploy
- **Vercel:** Frontend deploy

---

## Database Schema (Essencial para Epic 1)

```sql
-- Tabela users
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  full_name VARCHAR(255) NOT NULL,
  role VARCHAR(50) DEFAULT 'user', -- 'user', 'admin', 'specialist'
  email_verified BOOLEAN DEFAULT FALSE,
  is_active BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  last_login TIMESTAMPTZ
);

-- Tabela refresh_tokens
CREATE TABLE refresh_tokens (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  token VARCHAR(255) UNIQUE NOT NULL,
  expires_at TIMESTAMPTZ NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  revoked_at TIMESTAMPTZ
);

-- Tabela password_resets
CREATE TABLE password_resets (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  token VARCHAR(255) UNIQUE NOT NULL,
  expires_at TIMESTAMPTZ NOT NULL,
  used_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- RLS Policies
ALTER TABLE users ENABLE ROW LEVEL SECURITY;

CREATE POLICY user_data ON users
  FOR ALL USING (
    id = current_user_id() OR
    EXISTS (SELECT 1 FROM users WHERE id = current_user_id() AND role IN ('admin', 'specialist'))
  );
```

---

## API Endpoints

| Método | Endpoint | Descrição | Auth |
|--------|----------|-----------|------|
| POST | /api/v1/auth/register | Registra novo usuário | Público |
| POST | /api/v1/auth/verify-email | Verifica email com token | Público |
| POST | /api/v1/auth/login | Login (retorna access + refresh) | Público |
| POST | /api/v1/auth/refresh | Renova access token | Cookie |
| POST | /api/v1/auth/logout | Logout (invalida refresh token) | JWT |
| POST | /api/v1/auth/forgot-password | Solicita reset de senha | Público |
| POST | /api/v1/auth/reset-password | Redefine senha com token | Público |
| GET | /api/v1/users/me | Perfil do usuário logado | JWT |
| PATCH | /api/v1/users/me | Atualiza perfil | JWT |
| DELETE | /api/v1/users/me | Deleta conta | JWT |
| GET | /api/v1/admin/participantes | Lista todos os usuários | JWT + admin |

---

## Riscos e Mitigações

| Risco | Probabilidade | Impacto | Mitigação |
|-------|--------------|---------|-----------|
| **Chaves RS256 perdidas** | Baixa | Alto | Backup de chaves em secrets manager (Railway Secrets, Vercel Env Vars) |
| **Refresh token roubado** | Média | Alto | httpOnly cookie + SameSite=Strict + rotação a cada uso |
| **Brute force login** | Alta | Médio | Rate limiting (5 tentativas/min) + CAPTCHA após 3 falhas |
| **Email não enviado** | Média | Médio | Retry logic (3 tentativas) + fallback SMTP |
| **RLS policy incorreta** | Baixa | Alto | Testes de integração específicos para RLS + code review |

---

## Testes Críticos

### Unit Tests

- [ ] JWT generation/validation (RS256)
- [ ] Bcrypt hashing/verification
- [ ] Token expiration logic
- [ ] Refresh token rotation

### Integration Tests

- [ ] Fluxo completo: register → verify-email → login → refresh → logout
- [ ] Fluxo de recuperação de senha: forgot-password → reset-password
- [ ] RLS policies: user comum não vê dados de outro user
- [ ] Admin vê todos os dados

### E2E Tests (Playwright)

- [ ] Registro de usuário (happy path)
- [ ] Login e acesso ao dashboard
- [ ] Logout e redirect para login
- [ ] Recuperação de senha (end-to-end)

---

## Métricas de Sucesso

### Técnicas

- **Test Coverage:** 85%+
- **Login Performance:** < 500ms (p95)
- **Refresh Performance:** < 200ms (p95)
- **Zero passwords in logs**

### Funcionais

- **Taxa de sucesso de registro:** > 95%
- **Taxa de sucesso de login:** > 98%
- **Taxa de confirmação de email:** > 70% (24h)
- **Taxa de sucesso de reset de senha:** > 90%

---

## Handoff para @sm (Story Creation)

**Próximo passo:** @sm (River) cria stories detalhadas para cada user story listada acima.

**Formato esperado:** Stories granulares (1-3 dias cada) seguindo template AIOS de story.

**Priorização:** US-001.2 (Login) → US-001.1 (Registro) → US-001.3 (Refresh) → US-001.4 (Reset Senha) → US-001.5 (Admin) → US-001.6 (RLS)

---

**Criado por:** @pm (Morgan)
**Data:** 2026-03-15
**Versão:** 1.0.0

— Morgan, planejando o futuro 📊
