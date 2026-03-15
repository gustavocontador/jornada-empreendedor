"""
Valores Calculator - Cálculo dos valores empresariais prioritários.

Identifica os 3 valores principais do empreendedor dentre 10 opções:
- Inovação, Disciplina, Resultado, Colaboração, Autonomia
- Excelência, Agilidade, Propósito, Estabilidade, Crescimento
"""
from typing import Any, Optional

from app.models.response import Response


def calculate_valores(responses: list[Response], questions_data: dict[str, Any]) -> dict[str, Any]:
    """
    Calcula valores empresariais a partir das respostas.

    Args:
        responses: Lista de respostas do usuário
        questions_data: Dados do questionário com pontuações

    Returns:
        Dicionário com top 3 valores
    """
    # Mapeia respostas usando YAML ID (extra_data['id']) ao invés de UUID
    response_map = {}
    for r in responses:
        if hasattr(r, 'question') and r.question and r.question.extra_data:
            yaml_id = r.question.extra_data.get('id')
            if yaml_id:
                response_map[yaml_id] = r

    # Busca pergunta de ranking de valores (q086)
    valores_ranking = None
    for question in questions_data.get("perguntas", []):
        if question.get("id") == "q086":
            response = response_map.get("q086")
            if response:
                valores_ranking = response.answer_value
            break

    # Se não encontrou ranking, tenta inferir de perguntas Likert complementares
    if not valores_ranking:
        return _infer_from_likert(responses, questions_data)

    # Processa ranking
    if isinstance(valores_ranking, list):
        # Lista ordenada de valores
        primary = valores_ranking[0] if len(valores_ranking) > 0 else None
        secondary = valores_ranking[1] if len(valores_ranking) > 1 else None
        tertiary = valores_ranking[2] if len(valores_ranking) > 2 else None
    elif isinstance(valores_ranking, dict):
        # Objeto com ranks
        primary = valores_ranking.get("rank_1") or valores_ranking.get("primary")
        secondary = valores_ranking.get("rank_2") or valores_ranking.get("secondary")
        tertiary = valores_ranking.get("rank_3") or valores_ranking.get("tertiary")
    else:
        return _infer_from_likert(responses, questions_data)

    return {
        "primary": primary,
        "secondary": secondary,
        "tertiary": tertiary,
        "description": _get_valor_description(primary),
        "alignment_insights": _check_valores_alignment(primary, secondary, tertiary)
    }


def _infer_from_likert(responses: list[Response], questions_data: dict[str, Any]) -> dict[str, Any]:
    """
    Infere valores a partir de perguntas Likert complementares (q088-q095).

    Args:
        responses: Lista de respostas
        questions_data: Dados do questionário

    Returns:
        Valores inferidos
    """
    valor_scores = {
        "inovacao": 0.0,
        "disciplina": 0.0,
        "resultado": 0.0,
        "colaboracao": 0.0,
        "autonomia": 0.0,
        "excelencia": 0.0,
        "agilidade": 0.0,
        "proposito": 0.0,
        "estabilidade": 0.0,
        "crescimento": 0.0
    }

    # Mapeia respostas usando YAML ID
    response_map = {}
    for r in responses:
        if hasattr(r, 'question') and r.question and r.question.extra_data:
            yaml_id = r.question.extra_data.get('id')
            if yaml_id:
                response_map[yaml_id] = r

    # Perguntas Likert que indicam valores
    valor_questions = {
        "q088": {"excelencia": 0.8, "agilidade": 0.5},
        "q089": {"proposito": 1.0},
        "q090": {"crescimento": 0.8, "estabilidade": -0.7},
        "q091": {"autonomia": 1.0},
        "q092": {"inovacao": 1.0, "excelencia": -0.3},
        "q093": {"disciplina": 1.0},
        "q094": {"resultado": 1.0, "proposito": -0.4},
        "q095": {"colaboracao": 1.0}
    }

    for qid, valor_weights in valor_questions.items():
        response = response_map.get(qid)
        if not response:
            continue

        answer_value = response.answer_value
        if isinstance(answer_value, (int, float)):
            likert_value = float(answer_value)
        elif isinstance(answer_value, dict) and "value" in answer_value:
            likert_value = float(answer_value["value"])
        else:
            continue

        # Normaliza Likert
        normalized = (likert_value - 3) / 2

        # Aplica pesos
        for valor, weight in valor_weights.items():
            valor_scores[valor] += normalized * weight

    # Ordena por score
    sorted_valores = sorted(valor_scores.items(), key=lambda x: x[1], reverse=True)

    primary = sorted_valores[0][0] if sorted_valores else "resultado"
    secondary = sorted_valores[1][0] if len(sorted_valores) > 1 else None
    tertiary = sorted_valores[2][0] if len(sorted_valores) > 2 else None

    return {
        "primary": primary,
        "secondary": secondary,
        "tertiary": tertiary,
        "description": _get_valor_description(primary),
        "alignment_insights": _check_valores_alignment(primary, secondary, tertiary),
        "inferred": True
    }


def _check_valores_alignment(
    primary: Optional[str],
    secondary: Optional[str],
    tertiary: Optional[str]
) -> list[dict[str, str]]:
    """
    Verifica alinhamento e conflitos entre valores.

    Args:
        primary, secondary, tertiary: Top 3 valores

    Returns:
        Lista de insights sobre alinhamento
    """
    insights = []
    valores = [v for v in [primary, secondary, tertiary] if v]

    # Conflitos comuns
    if "inovacao" in valores and "estabilidade" in valores:
        insights.append({
            "type": "conflict",
            "description": "Tensão entre Inovação e Estabilidade. Você pode oscilar entre mudança e segurança.",
            "resolution": "Crie 'zonas de inovação' (20% tempo) e 'zonas de estabilidade' (processos core). Ambos têm lugar."
        })

    if "resultado" in valores and "proposito" in valores:
        insights.append({
            "type": "balance",
            "description": "Combinação forte: Resultado + Propósito. Você quer ganhar dinheiro COM significado.",
            "tip": "Use propósito como diferencial de mercado. Clientes pagam mais por empresas com propósito claro."
        })

    if "autonomia" in valores and "disciplina" in valores:
        insights.append({
            "type": "conflict",
            "description": "Tensão entre Autonomia (liberdade) e Disciplina (estrutura).",
            "resolution": "Use 'Autonomia dentro de Limites': defina princípios inegociáveis, liberdade no resto."
        })

    if "crescimento" in valores and "excelencia" in valores:
        insights.append({
            "type": "balance",
            "description": "Crescimento + Excelência: Você quer escalar com qualidade. Difícil mas possível.",
            "tip": "Cresça em degraus: escale 50%, depois estabilize e melhore qualidade, depois escale de novo."
        })

    # Valores complementares
    if "inovacao" in valores and "disciplina" in valores:
        insights.append({
            "type": "complementary",
            "description": "Inovação + Disciplina: Raro mas poderoso. Você cria novidades E as executa com rigor.",
            "tip": "Esse é seu diferencial. Muitos inovam sem executar, poucos fazem ambos. Capitalize isso."
        })

    return insights


def _get_valor_description(valor: Optional[str]) -> str:
    """
    Retorna descrição do valor empresarial.

    Args:
        valor: Nome do valor

    Returns:
        Descrição
    """
    descriptions = {
        "inovacao": "Buscar constantemente novas ideias e soluções criativas. Questionar status quo.",
        "disciplina": "Seguir processos, rotinas e estruturas definidas. Consistência acima de tudo.",
        "resultado": "Foco em alcançar metas e entregar performance. Números falam mais alto.",
        "colaboracao": "Trabalho em equipe e construção coletiva. Juntos somos mais fortes.",
        "autonomia": "Liberdade e independência para tomar decisões. Empoderamento individual.",
        "excelencia": "Qualidade superior e atenção aos detalhes. Fazer bem feito ou não fazer.",
        "agilidade": "Velocidade de execução e adaptação rápida. Move fast, break things.",
        "proposito": "Trabalho com significado e impacto social. Lucro com propósito.",
        "estabilidade": "Segurança, previsibilidade e baixo risco. Crescer com solidez.",
        "crescimento": "Expansão, escalabilidade e aumento constante. Sempre maior, sempre melhor."
    }
    return descriptions.get(valor, "")
