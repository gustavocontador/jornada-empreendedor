# 🚀 Deploy Rápido - Guia Passo a Passo

## ⏱️ Tempo Total: 20-30 minutos

---

## **PARTE 1: Deploy do Backend (Railway)** 🚂

### **1.1. Criar conta no Railway**
1. Acesse: https://railway.app
2. Clique em "Start a New Project"
3. Faça login com GitHub

### **1.2. Criar projeto Railway**
1. Click "New Project"
2. Escolha "Deploy from GitHub repo"
3. Se ainda não conectou: "Configure GitHub App" → Autorize o repositório
4. ⚠️ **IMPORTANTE:** Primeiro precisamos fazer o commit inicial (veja seção PREPARAÇÃO abaixo)

### **1.3. Adicionar PostgreSQL**
1. No projeto Railway, clique "+ New"
2. Escolha "Database" → "Add PostgreSQL"
3. Railway cria o banco automaticamente
4. Anote a DATABASE_URL (em Variables)

### **1.4. Configurar Variáveis de Ambiente**

No Railway, vá em seu serviço backend → Variables:

```env
DATABASE_URL=${{Postgres.DATABASE_URL}}
SECRET_KEY=<gere um aleatório - veja abaixo>
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7
PROJECT_NAME=Jornada do Empreendedor de Sucesso
APP_VERSION=1.0.0
DEBUG=False
BACKEND_CORS_ORIGINS=https://seu-dominio-vercel.vercel.app
ADMIN_EMAIL=admin@example.com
ADMIN_PASSWORD=<altere para senha segura>
UPLOAD_DIR=/app/uploads
REPORTS_DIR=/app/reports
MAX_UPLOAD_SIZE=10485760
```

**Gerar SECRET_KEY:**
```bash
openssl rand -hex 32
```

### **1.5. Deploy!**
1. Railway detecta Python automaticamente
2. Usa `railway.json` e `Procfile` que já criamos
3. Clique "Deploy"
4. Aguarde ~3-5 minutos
5. Railway fornecerá uma URL: `https://seu-app.railway.app`

---

## **PARTE 2: Deploy do Frontend (Vercel)** ▲

### **2.1. Criar conta no Vercel**
1. Acesse: https://vercel.com
2. "Sign Up" com GitHub
3. Autorize Vercel no GitHub

### **2.2. Importar Projeto**
1. Dashboard Vercel → "Add New..." → "Project"
2. Import do repositório GitHub
3. ⚠️ **Configure Root Directory:**
   - Root Directory: `frontend`
   - Framework Preset: Next.js
   - Build Command: `npm run build` (já detectado)
   - Output Directory: `.next` (já detectado)

### **2.3. Configurar Environment Variable**
Em "Environment Variables":

```env
NEXT_PUBLIC_API_URL=https://seu-app.railway.app
```

⚠️ **Substitua** `seu-app.railway.app` pela URL real do Railway (Parte 1.5)

### **2.4. Deploy!**
1. Clique "Deploy"
2. Aguarde ~2-3 minutos
3. Vercel fornecerá uma URL: `https://seu-projeto.vercel.app`

### **2.5. Atualizar CORS no Backend**
Volte ao Railway → Backend → Variables:
```env
BACKEND_CORS_ORIGINS=https://seu-projeto.vercel.app
```

Clique "Deploy" novamente para aplicar.

---

## **PARTE 3: Testar o Sistema** 🧪

### **3.1. Acessar o Frontend**
1. Abra `https://seu-projeto.vercel.app`
2. Deve ver a landing page

### **3.2. Testar Cadastro**
1. Clique "Iniciar Assessment"
2. Faça cadastro com email/senha
3. Deve redirecionar para questionário

### **3.3. Testar Questionário**
1. Responda algumas perguntas
2. Navegue (anterior/próximo)
3. Verifique auto-save funcionando

### **3.4. Testar Admin**
1. Acesse `https://seu-projeto.vercel.app/admin/dashboard`
2. Login com:
   - Email: `admin@example.com`
   - Senha: a que você configurou no Railway

### **3.5. Verificar API (Swagger)**
1. Acesse `https://seu-app.railway.app/docs`
2. Deve ver documentação Swagger UI

---

## **PREPARAÇÃO: Commit Inicial** 📝

**Antes de fazer deploy no Railway/Vercel, precisamos commitar o código:**

### **Opção A: Criar Repositório GitHub (Recomendado)**

```bash
# Já inicializamos o git, agora vamos commitar
cd "/Users/gustavo/Documents/Documentos - MacBook Pro de Gustavo - 1/AIOS/squads/entrepreneur-assessment"

# Adicionar arquivos
git add .

# Commit inicial
git commit -m "Initial commit - Jornada do Empreendedor de Sucesso

Sistema completo de assessment comportamental:
- Backend FastAPI com 6 frameworks
- Frontend Next.js 14
- Engine de relatórios PDF
- 105 perguntas otimizadas
- Algoritmos de scoring funcionais
"

# Criar repositório no GitHub
# 1. Vá em https://github.com/new
# 2. Nome: jornada-empreendedor
# 3. Private ou Public (sua escolha)
# 4. Não adicione README, .gitignore ou license (já temos)
# 5. Clique "Create repository"

# Conectar e push
git remote add origin https://github.com/SEU-USUARIO/jornada-empreendedor.git
git branch -M main
git push -u origin main
```

### **Opção B: Repositório Local (para testes)**
```bash
# Se quiser apenas testar localmente primeiro
cd "/Users/gustavo/Documents/Documentos - MacBook Pro de Gustavo - 1/AIOS/squads/entrepreneur-assessment"
git add .
git commit -m "Initial commit"
```

---

## **TROUBLESHOOTING** 🔧

### **Backend não inicia no Railway**
1. Verifique logs: Railway → seu serviço → Deployments → View Logs
2. Erros comuns:
   - **DATABASE_URL não configurada:** Verifique Variables
   - **SECRET_KEY faltando:** Adicione nas Variables
   - **Requirements.txt:** Verifique se existe em `/backend/requirements.txt`

### **Frontend não conecta ao Backend**
1. Verifique NEXT_PUBLIC_API_URL está correto
2. Verifique CORS no backend inclui domínio do Vercel
3. Teste API diretamente: `https://seu-app.railway.app/health`

### **Erro 401 Unauthorized**
1. Verifique SECRET_KEY é o mesmo no backend
2. Tente fazer logout e login novamente
3. Limpe localStorage do browser

### **PDFs não geram**
1. Railway precisa de espaço em disco
2. Verifique logs do backend
3. Se persistir, considere salvar PDFs em S3 (futuro)

---

## **PÓS-DEPLOY** ✅

### **Segurança**
- [ ] Altere senha do admin padrão
- [ ] Configure domínio customizado (opcional)
- [ ] Ative HTTPS (já vem por padrão)

### **Monitoramento**
- [ ] Configure Sentry para erros (opcional)
- [ ] Configure analytics no frontend (opcional)
- [ ] Configure backups do banco (Railway tem automático)

### **Testes**
- [ ] Cadastro de usuário
- [ ] Login
- [ ] Questionário completo
- [ ] Visualização de resultados
- [ ] Geração de PDF
- [ ] Admin dashboard

---

## **CUSTOS** 💰

### **Railway (Backend + DB)**
- **Gratuito:** $5 de crédito/mês (suficiente para testes)
- **Hobby:** $5/mês após créditos
- **Pro:** $20/mês (para produção)

### **Vercel (Frontend)**
- **Hobby:** Gratuito (perfeito para começar)
- **Pro:** $20/mês (se precisar de mais features)

### **Total Inicial**
- **$0-5/mês** para começar
- **$10-25/mês** para produção

---

## **DOMÍNIOS CUSTOMIZADOS** 🌐

### **Frontend (Vercel)**
1. Vercel → seu projeto → Settings → Domains
2. Adicione: `jornada.seudominio.com`
3. Configure DNS conforme instruções

### **Backend (Railway)**
1. Railway → seu serviço → Settings → Domains
2. Adicione: `api.jornada.seudominio.com`
3. Configure DNS conforme instruções

### **Atualizar CORS**
Lembre de atualizar `BACKEND_CORS_ORIGINS` com novo domínio!

---

## **PRÓXIMOS PASSOS** 🚀

1. ✅ Deploy realizado
2. ✅ Testes básicos funcionando
3. 📧 Configurar email (recuperação de senha - futuro)
4. 🎨 Personalizar branding (logo, cores)
5. 📊 Adicionar analytics
6. 💳 Integrar pagamento (se for vender)
7. 📢 Lançar para primeiros usuários!

---

## **COMANDOS ÚTEIS** 🛠️

### **Ver logs Railway**
```bash
# Instalar Railway CLI (opcional)
npm install -g @railway/cli

# Login
railway login

# Ver logs
railway logs
```

### **Ver logs Vercel**
```bash
# Instalar Vercel CLI (opcional)
npm install -g vercel

# Login
vercel login

# Ver logs
vercel logs
```

### **Redeploy**
- **Railway:** Faz automaticamente a cada push no GitHub
- **Vercel:** Faz automaticamente a cada push no GitHub

### **Rollback**
- **Railway:** Deployments → escolha deploy anterior → "Redeploy"
- **Vercel:** Deployments → escolha deploy anterior → "Promote to Production"

---

## **SUPORTE** 💬

- Railway: https://railway.app/help
- Vercel: https://vercel.com/support
- Documentação deste projeto: `/docs/`

---

**Tempo estimado total:** 20-30 minutos
**Dificuldade:** Fácil
**Custo inicial:** $0-5/mês

**BOA SORTE! 🚀**
