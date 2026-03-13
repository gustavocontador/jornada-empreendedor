# 🚀 Guia de Deploy - Jornada do Empreendedor de Sucesso

## Checklist Pré-Deploy

### Backend
- [ ] Variáveis de ambiente configuradas
- [ ] SECRET_KEY gerado (seguro, aleatório)
- [ ] Banco de dados PostgreSQL configurado
- [ ] Migrations rodadas (`alembic upgrade head`)
- [ ] Admin password alterado
- [ ] CORS configurado com domínio de produção
- [ ] Testes passando
- [ ] Logs configurados
- [ ] Backups configurados

### Frontend
- [ ] NEXT_PUBLIC_API_URL configurado (prod)
- [ ] Build funciona (`npm run build`)
- [ ] Environment variables configuradas
- [ ] Analytics configurado (opcional)
- [ ] SEO tags configuradas

---

## Opção 1: Deploy Manual (VPS)

### Backend (FastAPI)

**1. Preparar servidor:**
```bash
# Atualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar Python 3.11
sudo apt install python3.11 python3.11-venv python3-pip -y

# Instalar PostgreSQL
sudo apt install postgresql postgresql-contrib -y

# Instalar Nginx
sudo apt install nginx -y
```

**2. Configurar PostgreSQL:**
```bash
sudo -u postgres psql

CREATE DATABASE jornada_empreendedor;
CREATE USER jornada_user WITH PASSWORD 'senha_segura';
GRANT ALL PRIVILEGES ON DATABASE jornada_empreendedor TO jornada_user;
\q
```

**3. Deploy da aplicação:**
```bash
# Clonar repo (ou upload)
cd /var/www
git clone <repo-url> jornada-backend
cd jornada-backend/backend

# Criar venv
python3.11 -m venv venv
source venv/bin/activate

# Instalar deps
pip install -r requirements.txt

# Configurar .env
nano .env
# Preencha com dados de produção

# Rodar migrations
alembic upgrade head

# Testar
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

**4. Configurar Systemd (auto-restart):**
```bash
sudo nano /etc/systemd/system/jornada-backend.service
```

```ini
[Unit]
Description=Jornada Backend
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/var/www/jornada-backend/backend
Environment="PATH=/var/www/jornada-backend/backend/venv/bin"
ExecStart=/var/www/jornada-backend/backend/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl start jornada-backend
sudo systemctl enable jornada-backend
sudo systemctl status jornada-backend
```

**5. Configurar Nginx:**
```bash
sudo nano /etc/nginx/sites-available/jornada-backend
```

```nginx
server {
    listen 80;
    server_name api.jornada.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/jornada-backend /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

**6. SSL (Let's Encrypt):**
```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d api.jornada.com
```

---

### Frontend (Next.js)

**1. Build local:**
```bash
cd frontend
npm run build
# Cria pasta .next/
```

**2. Upload para servidor:**
```bash
# Via SCP ou rsync
rsync -avz .next node_modules package.json servidor:/var/www/jornada-frontend/
```

**3. Configurar PM2:**
```bash
# No servidor
npm install -g pm2

cd /var/www/jornada-frontend
pm2 start npm --name "jornada-frontend" -- start
pm2 startup
pm2 save
```

**4. Nginx:**
```nginx
server {
    listen 80;
    server_name jornada.com www.jornada.com;

    location / {
        proxy_pass http://127.0.0.1:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

---

## Opção 2: Deploy com Docker

### Docker Compose (Full Stack)

**docker-compose.yml:**
```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: jornada_empreendedor
      POSTGRES_USER: jornada_user
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - jornada-network

  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql://jornada_user:${DB_PASSWORD}@postgres:5432/jornada_empreendedor
      SECRET_KEY: ${SECRET_KEY}
    depends_on:
      - postgres
    networks:
      - jornada-network
    volumes:
      - ./backend/reports:/app/reports

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      NEXT_PUBLIC_API_URL: http://backend:8000
    depends_on:
      - backend
    networks:
      - jornada-network

volumes:
  postgres_data:

networks:
  jornada-network:
    driver: bridge
```

**Deploy:**
```bash
# Criar .env
echo "DB_PASSWORD=senha_super_segura" > .env
echo "SECRET_KEY=$(openssl rand -hex 32)" >> .env

# Build e start
docker-compose up -d

# Migrations
docker-compose exec backend alembic upgrade head

# Logs
docker-compose logs -f
```

---

## Opção 3: Deploy em Serviços Cloud

### Backend (Railway, Render, Heroku)

**Railway:**
1. Conectar repositório GitHub
2. Configurar variáveis de ambiente
3. Railway detecta FastAPI automaticamente
4. Deploy automático

**Render:**
1. New Web Service
2. Build Command: `pip install -r requirements.txt`
3. Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. Adicionar PostgreSQL (Database)
5. Configurar env vars

### Frontend (Vercel - Recomendado)

**Vercel:**
```bash
cd frontend

# Install Vercel CLI
npm install -g vercel

# Deploy
vercel

# Configurar
# - Build Command: npm run build
# - Output Directory: .next
# - Environment Variable: NEXT_PUBLIC_API_URL
```

---

## Opção 4: AWS (Produção Enterprise)

### Backend (Elastic Beanstalk + RDS)

1. **RDS (PostgreSQL):**
   - Create database instance
   - PostgreSQL 15
   - db.t3.micro (dev) ou db.t3.medium (prod)
   - Enable backups

2. **Elastic Beanstalk:**
   ```bash
   eb init jornada-backend
   eb create jornada-prod
   eb deploy
   ```

3. **Environment Variables:**
   - Configure via EB Console ou `.ebextensions/`

### Frontend (S3 + CloudFront)

1. **Build:**
   ```bash
   npm run build
   next export  # Static export
   ```

2. **Upload to S3:**
   ```bash
   aws s3 sync out/ s3://jornada-frontend/
   ```

3. **CloudFront:**
   - Create distribution
   - Origin: S3 bucket
   - Enable HTTPS
   - Custom domain

---

## Backups

### Banco de Dados

**Automático (diário):**
```bash
# Cron job
0 2 * * * pg_dump -U jornada_user jornada_empreendedor | gzip > /backups/jornada_$(date +\%Y\%m\%d).sql.gz
```

**Manual:**
```bash
pg_dump -U jornada_user jornada_empreendedor > backup.sql
```

**Restore:**
```bash
psql -U jornada_user jornada_empreendedor < backup.sql
```

### Arquivos (Relatórios PDFs)

```bash
# Sync para S3
aws s3 sync /var/www/jornada-backend/reports s3://jornada-reports-backup/
```

---

## Monitoramento

### Logs

**Backend:**
```bash
# Systemd
journalctl -u jornada-backend -f

# Docker
docker-compose logs -f backend

# Arquivo
tail -f /var/log/jornada-backend.log
```

**Frontend:**
```bash
# PM2
pm2 logs jornada-frontend

# Docker
docker-compose logs -f frontend
```

### Performance

**Sentry** (Erros):
```bash
pip install sentry-sdk

# app/main.py
import sentry_sdk
sentry_sdk.init(dsn="...")
```

**New Relic** (APM):
```bash
pip install newrelic
newrelic-admin run-program uvicorn app.main:app
```

---

## Segurança

### SSL/TLS
- Use Let's Encrypt (gratuito)
- Redirect HTTP → HTTPS
- HSTS headers

### Firewall
```bash
sudo ufw allow 22    # SSH
sudo ufw allow 80    # HTTP
sudo ufw allow 443   # HTTPS
sudo ufw enable
```

### Rate Limiting (Nginx)
```nginx
limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;

location / {
    limit_req zone=api burst=20 nodelay;
}
```

### Updates
```bash
# Automático (Ubuntu)
sudo apt install unattended-upgrades
sudo dpkg-reconfigure --priority=low unattended-upgrades
```

---

## Troubleshooting

### Backend não inicia
```bash
# Verificar logs
journalctl -u jornada-backend -n 50

# Testar manualmente
cd /var/www/jornada-backend/backend
source venv/bin/activate
uvicorn app.main:app --reload
```

### Erro de conexão com DB
```bash
# Testar conexão
psql -U jornada_user -d jornada_empreendedor -h localhost

# Verificar .env
cat .env | grep DATABASE_URL
```

### Frontend 404
```bash
# Rebuild
npm run build

# Restart PM2
pm2 restart jornada-frontend

# Verificar logs
pm2 logs jornada-frontend
```

---

## Checklist Pós-Deploy

- [ ] Testar cadastro de usuário
- [ ] Testar login
- [ ] Fazer assessment completo
- [ ] Verificar cálculo de resultados
- [ ] Gerar relatório PDF
- [ ] Download de PDF funciona
- [ ] Admin dashboard acessível
- [ ] HTTPS funcionando
- [ ] Backups configurados
- [ ] Monitoring ativo
- [ ] Logs sendo coletados
- [ ] Alterar senha admin padrão
- [ ] Documentar credenciais em local seguro

---

## Rollback

### Método 1: Git
```bash
git revert <commit-hash>
git push origin main
# Deploy automático ou manual
```

### Método 2: Backup
```bash
# Restore DB
psql -U jornada_user jornada_empreendedor < backup_pre_deploy.sql

# Restore code
git checkout <previous-tag>
# Redeploy
```

---

## Custos Estimados (Mensal)

### Opção 1: VPS + Vercel
- VPS (DigitalOcean): $12-24
- Vercel (Frontend): $0-20
- **Total:** $12-44/mês

### Opção 2: Railway + Vercel
- Railway (Backend + DB): $5-20
- Vercel (Frontend): $0-20
- **Total:** $5-40/mês

### Opção 3: AWS
- EC2 (t3.micro): $8
- RDS (db.t3.micro): $15
- S3 + CloudFront: $1-5
- **Total:** $24-28/mês

---

**Versão:** 1.0.0
**Atualizado:** 2026-03-13
