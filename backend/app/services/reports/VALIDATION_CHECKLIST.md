# ✅ CHECKLIST DE VALIDAÇÃO - ENGINE DE RELATÓRIOS

Use este checklist para validar que a engine está funcionando corretamente.

## 📁 Estrutura de Arquivos

```
✅ Verificar que todos os arquivos foram criados:

backend/app/services/reports/
├── ✅ __init__.py
├── ✅ report_generator.py          (Orquestrador - 25KB)
├── ✅ chart_generator.py           (Gráficos Plotly - 12KB)
├── ✅ content_generator.py         (Interpretações - 48KB)
├── ✅ pdf_renderer.py              (WeasyPrint - 2KB)
├── ✅ example_usage.py             (Exemplos - 5KB)
├── ✅ README.md                    (Documentação - 7KB)
├── ✅ API_INTEGRATION.md           (Guia de API)
├── ✅ VALIDATION_CHECKLIST.md      (Este arquivo)
└── templates/
    ├── ✅ styles.css               (CSS - 8KB)
    ✅ simplified_template.html (2-3 páginas - 5.5KB)
    └── ✅ complete_template.html    (15-20 páginas - 18KB)
```

## 🔧 Dependências

```bash
✅ Verificar instalação:

pip show plotly      # deve ser 5.18.0
pip show kaleido     # deve ser 0.2.1
pip show weasyprint  # deve ser 60.2
pip show Pillow      # deve ser 10.2.0
```

Se alguma dependência estiver faltando:
```bash
pip install plotly==5.18.0 kaleido==0.2.1 weasyprint==60.2 Pillow==10.2.0
```

## 🎨 Validação de Gráficos

```python
# Execute este script para testar geração de gráficos:

from app.services.reports.chart_generator import (
    generate_disc_chart,
    generate_spiral_chart,
    generate_paei_chart,
    generate_enneagram_diagram,
    generate_valores_chart
)

# Teste 1: DISC
disc_scores = {"D": 7.5, "I": 8.2, "S": 4.1, "C": 5.8}
disc_chart = generate_disc_chart(disc_scores)
assert disc_chart.startswith("data:image/png;base64,"), "DISC chart deve ser base64"
print("✅ DISC chart gerado")

# Teste 2: Espiral
spiral_scores = {
    "beige": 2.1, "purple": 3.5, "red": 5.8, "blue": 6.2,
    "orange": 8.5, "green": 5.5, "yellow": 3.2, "turquoise": 1.5
}
spiral_chart = generate_spiral_chart(spiral_scores)
assert spiral_chart.startswith("data:image/png;base64,"), "Spiral chart deve ser base64"
print("✅ Spiral chart gerado")

# Teste 3: PAEI
paei_scores = {"P": 8.1, "A": 3.2, "E": 7.5, "I": 4.1}
paei_chart = generate_paei_chart(paei_scores)
assert paei_chart.startswith("data:image/png;base64,"), "PAEI chart deve ser base64"
print("✅ PAEI chart gerado")

# Teste 4: Eneagrama
enneagram_chart = generate_enneagram_diagram(3)
assert enneagram_chart.startswith("data:image/png;base64,"), "Enneagram chart deve ser base64"
print("✅ Enneagram chart gerado")

# Teste 5: Valores
valores_scores = {
    "Inovação": 8.5, "Resultado": 8.2, "Crescimento": 7.8,
    "Qualidade": 6.5, "Ética": 6.2
}
valores_chart = generate_valores_chart(valores_scores, top_n=5)
assert valores_chart.startswith("data:image/png;base64,"), "Valores chart deve ser base64"
print("✅ Valores chart gerado")

print("\n✅ TODOS OS GRÁFICOS FUNCIONANDO!")
```

**Status:** [ ] Passar em todos os testes

## 📄 Validação de Templates

### Simplified Template

```bash
✅ Verificar placeholders no simplified_template.html:

- {{css_content}}
- {{user_name}}
- {{assessment_date}}
- {{disc_profile}}
- {{disc_chart}}
- {{spiral_chart}}
- {{paei_chart}}
- {{enneagram_chart}}
- {{top_values}}
```

**Status:** [ ] Todos os placeholders presentes

### Complete Template

```bash
✅ Verificar seções no complete_template.html:

1. Capa
2. Índice
3. Introdução aos Frameworks
4. Perfil DISC Detalhado (2-3 pág)
5. Espiral Dinâmica Profunda (3-4 pág)
6. PAEI - Gestão e Liderança (2-3 pág)
7. Eneagrama - Autossabotagem (2-3 pág)
8. Valores e Cultura (1-2 pág)
9. Síntese Integrada (2 pág)
10. Plano de Ação 30/60/90 (2-3 pág)
```

**Status:** [ ] Todas as seções presentes

## 🎨 Validação de CSS

```bash
✅ Verificar classes CSS em styles.css:

Layout:
- .cover
- .toc
- .section
- .page-break

Boxes:
- .info-box
- .warning-box
- .success-box
- .danger-box
- .summary-card

Gráficos:
- .chart-container
- .chart-caption

Cores Spiral:
- .color-beige até .color-turquoise
- .bg-beige até .bg-turquoise

Cores DISC:
- Vermelho (#FF4444)
- Dourado (#FFD700)
- Verde (#4CAF50)
- Azul (#2196F3)
```

**Status:** [ ] Todas as classes presentes

## 🧠 Validação de Conteúdo (Knowledge Base)

```bash
✅ Verificar interpretações em content_generator.py:

DISC:
- get_disc_profile_title()
- get_disc_full_description()
- get_disc_strengths()
- get_disc_blind_spots()
- get_disc_communication_style()
- get_disc_decision_style()

Spiral:
- get_spiral_color_title()
- get_spiral_color_description()
- get_spiral_healthy_manifestation()
- get_spiral_unhealthy_manifestation()
- get_spiral_combination_analysis()
- get_spiral_combination_conflicts()

PAEI:
- get_paei_profile_name()
- get_paei_full_interpretation()
- get_paei_people_problems()
- get_paei_financial_problems()
- get_paei_hiring_recommendations()

Eneagrama:
- get_enneagram_name()
- get_enneagram_description()
- get_enneagram_motivations()
- get_enneagram_fears()
- get_enneagram_sabotage()
- get_enneagram_business_impact()
```

**Status:** [ ] Todas as funções implementadas

## 🔄 Validação de Integração

### Teste Completo (Mock)

```python
# Execute app/services/reports/example_usage.py

python backend/app/services/reports/example_usage.py

# Deve executar sem erros e mostrar:
# ✓ DISC chart: <bytes> (base64)
# ✓ Spiral chart: <bytes> (base64)
# ✓ PAEI chart: <bytes> (base64)
# ✓ Enneagram chart: <bytes> (base64)
# ✓ Valores chart: <bytes> (base64)
```

**Status:** [ ] Executar sem erros

### Teste com Banco (Opcional)

```python
# Se tiver dados reais no banco:

from app.services.reports import ReportGenerator
from app.db.session import SessionLocal

db = SessionLocal()
generator = ReportGenerator(db)

# Substitua pelos IDs reais:
result_id = "uuid-real"
user_id = "uuid-real"

# Teste simplificado
pdf_path = generator.generate_simplified_report(result_id, user_id)
assert os.path.exists(pdf_path), "PDF simplificado deve ser criado"
print(f"✅ PDF simplificado: {pdf_path}")

# Teste completo
pdf_path = generator.generate_complete_report(result_id, user_id)
assert os.path.exists(pdf_path), "PDF completo deve ser criado"
print(f"✅ PDF completo: {pdf_path}")

db.close()
```

**Status:** [ ] Passar com dados reais

## 📊 Validação de Performance

```bash
✅ Medir tempo de geração:

import time

# Simplificado
start = time.time()
pdf_path = generator.generate_simplified_report(result_id, user_id)
duration = time.time() - start
print(f"Tempo simplificado: {duration:.2f}s")
assert duration < 3, "Deve gerar em menos de 3s"

# Completo
start = time.time()
pdf_path = generator.generate_complete_report(result_id, user_id)
duration = time.time() - start
print(f"Tempo completo: {duration:.2f}s")
assert duration < 7, "Deve gerar em menos de 7s"
```

**Targets:**
- Simplificado: < 2s ✅
- Completo: < 5s ✅

**Status:** [ ] Performance adequada

## 📝 Validação Visual dos PDFs

### Checklist Visual - Relatório Simplificado

```bash
Abra o PDF gerado e verifique:

Página 1 (Capa):
- [ ] Logo/título visível e bonito
- [ ] Nome do usuário aparece corretamente
- [ ] Data do assessment está correta
- [ ] Gradiente roxo/azul está aplicado

Página 2 (Resumo):
- [ ] Perfil DISC aparece (ex: "DI - Líder Persuasivo")
- [ ] Cores Espiral aparecem (ex: "Laranja-Verde")
- [ ] Código PAEI aparece (ex: "PaEi - Visionário Desorganizado")
- [ ] Tipo Eneagrama aparece (ex: "Tipo 3 - O Realizador")
- [ ] Top 3 valores aparecem
- [ ] Boxes coloridos estão formatados

Página 3 (Gráficos):
- [ ] Gráfico DISC aparece (barras horizontais)
- [ ] Gráfico Espiral aparece (radar colorido)
- [ ] Gráfico PAEI aparece (radar 4 eixos)
- [ ] Diagrama Eneagrama aparece (círculo com tipo destacado)
- [ ] CTA para relatório completo aparece
```

### Checklist Visual - Relatório Completo

```bash
Abra o PDF gerado e verifique:

Estrutura Geral:
- [ ] Capa (página 1)
- [ ] Índice (página 2)
- [ ] 15-20 páginas no total
- [ ] Quebras de página adequadas
- [ ] Headers/footers com numeração

Conteúdo:
- [ ] Todas as seções do índice estão presentes
- [ ] Gráficos aparecem em alta resolução
- [ ] Textos estão bem formatados (não quebrados)
- [ ] Boxes coloridos estão visíveis
- [ ] Análise de combinações Espiral está presente
- [ ] Problemas com pessoas/financeiros (PAEI) estão presentes
- [ ] Padrões de autossabotagem (Eneagrama) estão presentes
- [ ] Plano de ação 30/60/90 está presente
- [ ] Footer com branding aparece

Qualidade:
- [ ] Fontes legíveis (11pt corpo, 20pt títulos)
- [ ] Espaçamento adequado entre seções
- [ ] Cores fiéis aos frameworks
- [ ] Sem erros de português
- [ ] Sem placeholders não substituídos (ex: {{nome}})
```

**Status:** [ ] Visual aprovado

## 🔒 Validação de Segurança

```bash
✅ Verificar:

- [ ] PDFs são salvos em diretório seguro (não web-accessible)
- [ ] Nomes de arquivo não expõem informações sensíveis
- [ ] Validação de ownership (user só acessa seus relatórios)
- [ ] Rate limiting implementado
- [ ] Limpeza de arquivos antigos (cronjob)
```

**Status:** [ ] Segurança ok

## 📱 Validação de Responsividade

```bash
✅ Testar PDF em diferentes viewers:

- [ ] Adobe Acrobat Reader
- [ ] Preview (macOS)
- [ ] Chrome PDF viewer
- [ ] Mobile (iOS Safari, Android Chrome)
```

**Status:** [ ] Funciona em todos os viewers

## 🧪 Testes Automatizados

```python
# Criar arquivo: backend/tests/services/test_reports.py

import pytest
from app.services.reports.chart_generator import generate_disc_chart
from app.services.reports import ReportGenerator

def test_generate_disc_chart():
    """Testa geração de gráfico DISC."""
    scores = {"D": 7.5, "I": 8.2, "S": 4.1, "C": 5.8}
    chart = generate_disc_chart(scores)
    assert chart.startswith("data:image/png;base64,")
    assert len(chart) > 1000  # Base64 de uma imagem deve ter pelo menos 1KB

def test_generate_simplified_report(db_session, mock_result, mock_user):
    """Testa geração de relatório simplificado."""
    generator = ReportGenerator(db_session)
    pdf_path = generator.generate_simplified_report(
        result_id=str(mock_result.id),
        user_id=str(mock_user.id)
    )
    assert os.path.exists(pdf_path)
    assert pdf_path.endswith(".pdf")
    assert os.path.getsize(pdf_path) > 10000  # Pelo menos 10KB

# Executar testes:
# pytest backend/tests/services/test_reports.py -v
```

**Status:** [ ] Testes passando

## ✅ CHECKLIST FINAL

```
ESTRUTURA:
✅ [ ] Todos os 12 arquivos criados
✅ [ ] Templates HTML completos
✅ [ ] CSS profissional presente

DEPENDÊNCIAS:
✅ [ ] Plotly instalado
✅ [ ] Kaleido instalado
✅ [ ] WeasyPrint instalado
✅ [ ] Pillow instalado

FUNCIONALIDADE:
✅ [ ] Gráficos gerando corretamente
✅ [ ] PDFs sendo criados
✅ [ ] Templates renderizando
✅ [ ] Conteúdo personalizado

QUALIDADE:
✅ [ ] Visual aprovado
✅ [ ] Performance adequada (< 2s simplificado, < 5s completo)
✅ [ ] Sem erros de português
✅ [ ] Knowledge base aplicada (Spiral Dynamics)

INTEGRAÇÃO:
✅ [ ] API endpoints definidos
✅ [ ] Schemas criados
✅ [ ] Modelo Report no banco
✅ [ ] Documentação completa

SEGURANÇA:
✅ [ ] Validação de ownership
✅ [ ] Rate limiting considerado
✅ [ ] Arquivos em diretório seguro

TESTES:
✅ [ ] Testes unitários
✅ [ ] Testes de integração
✅ [ ] Teste manual visual
```

## 🎉 APROVAÇÃO FINAL

```
✅ Engine APROVADA quando:

- [ ] Todos os checkboxes acima estão marcados
- [ ] Relatórios gerados visualmente perfeitos
- [ ] Performance dentro dos targets
- [ ] Integração com API funcionando
- [ ] Testes automatizados passando

Assinatura: ________________  Data: __/__/____
```

## 📞 Troubleshooting

### Problema: Gráficos não aparecem no PDF

**Solução:**
```python
# Verifique se kaleido está instalado
pip install -U kaleido==0.2.1

# Teste geração de gráfico isoladamente
from app.services.reports.chart_generator import generate_disc_chart
chart = generate_disc_chart({"D": 7, "I": 8, "S": 5, "C": 6})
print(chart[:100])  # Deve mostrar "data:image/png;base64,..."
```

### Problema: WeasyPrint com erro de rendering

**Solução:**
```bash
# macOS
brew install pango

# Ubuntu/Debian
sudo apt-get install python3-cffi python3-brotli libpango-1.0-0

# Verificar instalação
python -c "from weasyprint import HTML; print('OK')"
```

### Problema: Performance lenta

**Diagnóstico:**
```python
import time

# Medir cada etapa
start = time.time()
charts = generator._generate_charts(scores)
print(f"Charts: {time.time() - start:.2f}s")

start = time.time()
html = generator._render_template(template, data)
print(f"Template: {time.time() - start:.2f}s")

start = time.time()
render_pdf_from_html(html, output_path)
print(f"PDF: {time.time() - start:.2f}s")
```

---

**Data da última validação:** _____________

**Validado por:** _____________

**Status:** [ ] ✅ APROVADO  [ ] ❌ PENDENTE  [ ] ⚠️ COM RESSALVAS
