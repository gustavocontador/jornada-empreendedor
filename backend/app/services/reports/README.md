# ENGINE DE GERAÇÃO DE RELATÓRIOS PDF

Motor completo para geração de relatórios personalizados da **Jornada do Empreendedor de Sucesso**.

## 📁 Estrutura

```
reports/
├── report_generator.py          # Orquestrador principal
├── chart_generator.py           # Geração de gráficos (Plotly → base64)
├── content_generator.py         # Conteúdo detalhado dos frameworks
├── pdf_renderer.py              # Renderização HTML → PDF (WeasyPrint)
├── templates/
│   ├── styles.css              # CSS profissional para PDFs
│   ├── simplified_template.html # Template 2-3 páginas
│   └── complete_template.html   # Template 15-20 páginas
├── example_usage.py             # Exemplos de uso
└── README.md                    # Este arquivo
```

## 🚀 Uso Rápido

### Gerar Relatório Simplificado (2-3 páginas)

```python
from app.services.reports import ReportGenerator
from app.db.session import SessionLocal

db = SessionLocal()
generator = ReportGenerator(db)

pdf_path = generator.generate_simplified_report(
    result_id="uuid-do-resultado",
    user_id="uuid-do-usuario"
)

print(f"PDF gerado em: {pdf_path}")
db.close()
```

### Gerar Relatório Completo (15-20 páginas)

```python
pdf_path = generator.generate_complete_report(
    result_id="uuid-do-resultado",
    user_id="uuid-do-usuario"
)
```

## 📊 Gráficos Gerados

A engine gera 5 tipos de gráficos profissionais:

1. **DISC** - Barras horizontais com scores D, I, S, C
2. **Espiral Dinâmica** - Radar colorido com 8 níveis
3. **PAEI** - Radar com 4 papéis organizacionais
4. **Eneagrama** - Diagrama circular com tipo destacado
5. **Valores** - Barras com top 5 valores empresariais

Todos os gráficos são gerados em base64 e embedados diretamente no HTML/PDF.

## 📄 Relatório Simplificado

**Estrutura (2-3 páginas):**

### Página 1 - Capa
- Logo e branding
- Nome do usuário
- Data do assessment

### Página 2 - Resumo Executivo
- Perfil DISC (ex: "DI - Líder Persuasivo")
- Cores Espiral (ex: "Laranja-Verde")
- Código PAEI (ex: "PaEi")
- Tipo Eneagrama (ex: "Tipo 3")
- Top 3 Valores

### Página 3 - Gráficos
- Todos os 5 gráficos
- CTA para relatório completo

## 📚 Relatório Completo

**Estrutura (15-20 páginas):**

1. **Capa** (1 pág)
2. **Índice** (1 pág)
3. **Introdução aos Frameworks** (1 pág)
4. **Perfil DISC Detalhado** (2-3 pág)
   - Gráfico
   - Análise de cada dimensão (D, I, S, C)
   - Pontos fortes e cegos
   - Estilo de comunicação
   - Estilo de decisão
5. **Espiral Dinâmica Profunda** (3-4 pág)
   - Gráfico colorido
   - Descrição das cores dominantes (baseado na knowledge base)
   - **Análise de combinações** (ex: Laranja-Azul)
   - Conflitos internos
   - Transições e próximo estágio
   - Aplicações em negócios
   - Red flags
6. **PAEI - Gestão e Liderança** (2-3 pág)
   - Gráfico
   - Interpretação do código
   - **Problemas com pessoas**
   - **Problemas financeiros**
   - Recomendações de contratação
7. **Eneagrama - Autossabotagem** (2-3 pág)
   - Diagrama
   - Tipo + asa + subtipo
   - Motivações profundas
   - Medos inconscientes
   - **Padrões de autossabotagem**
   - Caminhos de crescimento
8. **Valores e Cultura** (1-2 pág)
   - Top 5 valores
   - Arquetipos desejados
   - Gaps
9. **Síntese Integrada** (2 pág)
   - Como frameworks se conectam
   - Padrões dominantes cruzados
10. **Plano de Ação 30/60/90** (2-3 pág)
    - Ações por período
    - Contratações recomendadas
    - Recursos

## 🎨 Cores dos Frameworks

### DISC
```python
DISC_COLORS = {
    'D': '#FF4444',  # Vermelho
    'I': '#FFD700',  # Dourado
    'S': '#4CAF50',  # Verde
    'C': '#2196F3'   # Azul
}
```

### Espiral Dinâmica
```python
SPIRAL_COLORS = {
    'beige': '#F5DEB3',
    'purple': '#9370DB',
    'red': '#DC143C',
    'blue': '#4169E1',
    'orange': '#FF8C00',
    'green': '#32CD32',
    'yellow': '#FFD700',
    'turquoise': '#40E0D0'
}
```

### PAEI
```python
PAEI_COLORS = {
    'P': '#8B4513',  # Marrom (Produtor)
    'A': '#2F4F4F',  # Cinza escuro (Administrador)
    'E': '#FF6347',  # Tomate (Empreendedor)
    'I': '#4682B4'   # Azul aço (Integrador)
}
```

## 🧠 Knowledge Base

A engine usa conhecimento profundo de **Spiral Dynamics** do livro "Spiral Dynamics in Action" de Don Beck.

Análises incluem:
- Descrições fiéis de cada cor
- Manifestações saudáveis vs não saudáveis em negócios
- Análise de **combinações** (ex: Laranja-Azul vs Laranja-Verde)
- Conflitos internos de combinações
- Transições e sinais de evolução
- Red flags específicos

## ⚙️ Dependências

Certifique-se de ter instalado:

```bash
# Já estão no requirements.txt
plotly==5.18.0
kaleido==0.2.1
weasyprint==60.2
Pillow==10.2.0
```

## 📝 Formato dos Dados

### Estrutura do `Result.scores`:

```json
{
  "disc": {
    "D": 7.5,
    "I": 6.2,
    "S": 4.1,
    "C": 5.8,
    "profile": "DI"
  },
  "spiral": {
    "beige": 2.1,
    "purple": 3.5,
    "red": 5.8,
    "blue": 6.2,
    "orange": 8.5,
    "green": 5.5,
    "yellow": 3.2,
    "turquoise": 1.5,
    "primary": "orange",
    "secondary": "blue"
  },
  "paei": {
    "P": 8.1,
    "A": 3.2,
    "E": 7.5,
    "I": 4.1,
    "code": "PaEi"
  },
  "enneagram": {
    "type": 3,
    "wing": "3w2",
    "subtype": "so"
  },
  "valores": {
    "Inovação": 8.5,
    "Resultado": 8.2,
    "Crescimento": 7.8,
    "primary": "Inovação",
    "secondary": "Resultado"
  },
  "arquetipos": {
    "Herói": 7.5,
    "Mago": 6.8
  }
}
```

## 🎯 Performance

- **Relatório Simplificado:** < 2 segundos
- **Relatório Completo:** < 5 segundos

Gargalos principais:
1. Geração de gráficos (Plotly + Kaleido)
2. Renderização HTML → PDF (WeasyPrint)

## 🧪 Testing

```bash
# Testar apenas geração de gráficos
python app/services/reports/example_usage.py

# Testar relatório completo (requer banco)
# Edite example_usage.py com IDs reais primeiro
```

## 🔧 Troubleshooting

### Erro: "kaleido not found"
```bash
pip install kaleido==0.2.1
```

### Erro: WeasyPrint (Linux)
```bash
# Ubuntu/Debian
sudo apt-get install python3-cffi python3-brotli libpango-1.0-0 libpangoft2-1.0-0

# Fedora
sudo dnf install python3-cffi python3-brotli pango
```

### Erro: WeasyPrint (macOS)
```bash
brew install pango
```

### Gráficos não aparecem no PDF
- Verifique se os gráficos estão sendo gerados em base64
- Confirme que o base64 está sendo embedado no HTML
- Teste abrir o HTML diretamente no navegador antes de gerar PDF

## 📞 Suporte

Para dúvidas ou problemas:
1. Revise este README
2. Execute `example_usage.py` para testar componentes
3. Verifique logs da aplicação
4. Consulte knowledge base de Spiral Dynamics

## 🚦 Status

✅ **Completo e funcional**

Componentes:
- ✅ Gerador de gráficos (5 tipos)
- ✅ Template simplificado
- ✅ Template completo
- ✅ Content generator (interpretações profundas)
- ✅ PDF renderer
- ✅ CSS profissional
- ✅ Orquestrador principal
- ✅ Exemplos de uso
- ✅ Documentação

## 📜 Licença

Proprietary - Jornada do Empreendedor de Sucesso
