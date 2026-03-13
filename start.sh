#!/bin/bash

# Script para iniciar a aplicação Jornada do Empreendedor

echo "🚀 Iniciando Jornada do Empreendedor de Sucesso..."
echo ""

# Backend
echo "📦 Configurando Backend..."
cd backend

# Ativar venv
source venv/bin/activate

# Criar tabelas no banco (forçar criação direta via Python)
echo "🗄️  Criando tabelas no banco de dados..."
python3 << 'PYTHON_SCRIPT'
from app.db.base import Base
from app.core.config import settings
from sqlalchemy import create_engine

# Importar todos os modelos
from app.models.user import User
from app.models.assessment import Assessment
from app.models.question import Question
from app.models.response import Response
from app.models.result import Result
from app.models.report import Report

# Criar engine
engine = create_engine(str(settings.DATABASE_URL))

# Criar todas as tabelas
Base.metadata.create_all(bind=engine)
print("✅ Tabelas criadas com sucesso!")
PYTHON_SCRIPT

# Iniciar backend em background
echo "🔧 Iniciando servidor backend na porta 8000..."
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!
echo "Backend PID: $BACKEND_PID"

# Aguardar backend iniciar
sleep 5

cd ..

# Frontend
echo ""
echo "🎨 Iniciando Frontend na porta 3001..."
cd frontend
npm run dev &
FRONTEND_PID=$!
echo "Frontend PID: $FRONTEND_PID"

echo ""
echo "✅ Aplicação iniciada com sucesso!"
echo ""
echo "📍 URLs de acesso:"
echo "   Frontend: http://localhost:3001"
echo "   Backend API: http://localhost:8000"
echo "   API Docs: http://localhost:8000/docs"
echo ""
echo "🛑 Para parar a aplicação, execute:"
echo "   kill $BACKEND_PID $FRONTEND_PID"
echo ""
echo "   Ou pressione Ctrl+C e depois execute:"
echo "   pkill -f uvicorn"
echo "   pkill -f 'next dev'"
echo ""

# Manter o script rodando
wait
