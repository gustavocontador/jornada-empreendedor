"""
Spiral Dynamics Calculator - Cálculo dos níveis de desenvolvimento.

Spiral Dynamics mapeia 8 níveis de valores e visão de mundo:
- Beige (Instinto): Sobrevivência básica
- Purple (Tribal): Lealdade ao grupo, tradições
- Red (Impulsivo): Poder, ação imediata, dominância
- Blue (Tradicional): Ordem, disciplina, regras
- Orange (Moderno): Sucesso, eficiência, conquista
- Green (Pós-moderno): Igualdade, colaboração, bem-estar
- Yellow (Integrador): Pensamento sistêmico, flexibilidade
- Turquoise (Holístico): Visão global, sustentabilidade
"""
from typing import List, Dict, Any, Tuple
from decimal import Decimal
from collections import defaultdict

from app.models.response import Response


def calculate_spiral(responses: List[Response], questions_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Calcula scores Spiral Dynamics a partir das respostas.

    Args:
        responses: Lista de respostas do usuário
        questions_data: Dados do questionário com pontuações

    Returns:
        Dicionário com scores de cada nível e top 3
    """
    # Acumula pontuações brutas para cada cor
    raw_scores = {
        "spiral_beige": 0.0,
        "spiral_purple": 0.0,
        "spiral_red": 0.0,
        "spiral_blue": 0.0,
        "spiral_orange": 0.0,
        "spiral_green": 0.0,
        "spiral_yellow": 0.0,
        "spiral_turquoise": 0.0
    }

    # Contadores para normalização
    question_counts = defaultdict(int)

    # Mapeia respostas
    response_map = {str(r.question_id): r for r in responses}

    # Processa cada pergunta
    for question in questions_data.get("perguntas", []):
        question_id = question.get("id")
        pontuacao = question.get("pontuacao", {})

        # Filtra chaves spiral_
        spiral_keys = [k for k in pontuacao.keys() if k.startswith("spiral_")]
        if not spiral_keys:
            continue

        # Busca resposta
        response = response_map.get(question_id)
        if not response:
            continue

        answer_value = response.answer_value

        # Para perguntas Likert (1-5)
        if question.get("tipo") == "likert_5":
            if isinstance(answer_value, (int, float)):
                likert_value = float(answer_value)
            elif isinstance(answer_value, dict) and "value" in answer_value:
                likert_value = float(answer_value["value"])
            else:
                continue

            # Normaliza Likert para -1 a +1
            normalized_value = (likert_value - 3) / 2

            # Aplica pesos
            for spiral_key in raw_scores.keys():
                if spiral_key in pontuacao:
                    weight = float(pontuacao[spiral_key])
                    raw_scores[spiral_key] += normalized_value * weight
                    question_counts[spiral_key] += 1

    # Normaliza scores para 0-100
    normalized_scores = {}
    for key in raw_scores.keys():
        if question_counts[key] > 0:
            avg_score = raw_scores[key] / question_counts[key]
            normalized_scores[key] = max(0, min(100, (avg_score + 1) * 50))
        else:
            normalized_scores[key] = 0.0

    # Identifica top 3 níveis
    color_names = {
        "spiral_beige": "beige",
        "spiral_purple": "purple",
        "spiral_red": "red",
        "spiral_blue": "blue",
        "spiral_orange": "orange",
        "spiral_green": "green",
        "spiral_yellow": "yellow",
        "spiral_turquoise": "turquoise"
    }

    # Ordena por score
    sorted_colors = sorted(
        [(color_names[k], normalized_scores[k]) for k in raw_scores.keys()],
        key=lambda x: x[1],
        reverse=True
    )

    primary = sorted_colors[0][0] if sorted_colors else "orange"
    secondary = sorted_colors[1][0] if len(sorted_colors) > 1 else None
    tertiary = sorted_colors[2][0] if len(sorted_colors) > 2 else None

    # Detecta combinações problemáticas
    warnings = _detect_spiral_conflicts(primary, secondary, tertiary, normalized_scores)

    return {
        "beige": Decimal(str(round(normalized_scores["spiral_beige"], 2))),
        "purple": Decimal(str(round(normalized_scores["spiral_purple"], 2))),
        "red": Decimal(str(round(normalized_scores["spiral_red"], 2))),
        "blue": Decimal(str(round(normalized_scores["spiral_blue"], 2))),
        "orange": Decimal(str(round(normalized_scores["spiral_orange"], 2))),
        "green": Decimal(str(round(normalized_scores["spiral_green"], 2))),
        "yellow": Decimal(str(round(normalized_scores["spiral_yellow"], 2))),
        "turquoise": Decimal(str(round(normalized_scores["spiral_turquoise"], 2))),
        "primary": primary,
        "secondary": secondary,
        "tertiary": tertiary,
        "description": _get_spiral_description(primary),
        "warnings": warnings
    }


def _detect_spiral_conflicts(
    primary: str,
    secondary: str,
    tertiary: str,
    scores: Dict[str, float]
) -> List[Dict[str, str]]:
    """
    Detecta combinações problemáticas entre níveis Spiral.

    Args:
        primary, secondary, tertiary: Top 3 cores
        scores: Scores normalizados de cada cor

    Returns:
        Lista de avisos sobre conflitos
    """
    warnings = []
    top_colors = [primary, secondary, tertiary]

    # Roxo + Amarelo = Conflito tribal vs sistêmico
    if "purple" in top_colors and "yellow" in top_colors:
        warnings.append({
            "type": "value_conflict",
            "colors": ["purple", "yellow"],
            "description": "Conflito entre lealdade tribal (Roxo) e pensamento sistêmico (Amarelo). Você pode sentir tensão entre pertencer a um grupo e pensar de forma independente.",
            "recommendation": "Reconheça que ambos têm valor em contextos diferentes: use Roxo em relações pessoais íntimas, Amarelo em decisões estratégicas."
        })

    # Vermelho + Verde = Conflito poder vs igualdade
    if "red" in top_colors and "green" in top_colors:
        red_score = scores.get("spiral_red", 0)
        green_score = scores.get("spiral_green", 0)

        if abs(red_score - green_score) < 15:  # Scores similares = conflito maior
            warnings.append({
                "type": "value_conflict",
                "colors": ["red", "green"],
                "description": "Tensão entre assertividade/dominância (Vermelho) e colaboração/igualdade (Verde). Você pode oscilar entre ser muito agressivo e muito passivo.",
                "recommendation": "Pratique 'Assertividade Compassiva': seja direto nos objetivos mas inclusivo no processo. Defina quando usar cada estilo."
            })

    # Azul + Laranja = Pode ser produtivo OU conflitante
    if "blue" in top_colors and "orange" in top_colors:
        blue_score = scores.get("spiral_blue", 0)
        orange_score = scores.get("spiral_orange", 0)

        if blue_score > 70 and orange_score > 70:
            warnings.append({
                "type": "potential_strength",
                "colors": ["blue", "orange"],
                "description": "Combinação forte: disciplina (Azul) + ambição (Laranja). Você pode ser muito produtivo quando estrutura e resultados estão alinhados.",
                "recommendation": "Use essa combinação a seu favor: crie sistemas que gerem resultados previsíveis. Cuidado para não ficar rígido demais."
            })

    # Alto Laranja + Baixo Azul = Sem fundação
    orange_score = scores.get("spiral_orange", 0)
    blue_score = scores.get("spiral_blue", 0)

    if orange_score > 70 and blue_score < 30:
        warnings.append({
            "type": "missing_foundation",
            "colors": ["orange", "blue"],
            "description": "Alto Laranja (ambição) sem fundação Azul (disciplina). Risco de buscar crescimento sem estrutura adequada.",
            "recommendation": "Antes de escalar, crie processos básicos: financeiro, RH, vendas. Você precisa de um pouco de Azul para sustentar o Laranja."
        })

    # Amarelo/Turquesa sem níveis anteriores = Teórico sem prática
    yellow_score = scores.get("spiral_yellow", 0)
    turquoise_score = scores.get("spiral_turquoise", 0)
    avg_lower = (
        scores.get("spiral_red", 0) +
        scores.get("spiral_blue", 0) +
        scores.get("spiral_orange", 0)
    ) / 3

    if (yellow_score > 60 or turquoise_score > 60) and avg_lower < 40:
        warnings.append({
            "type": "transcend_without_include",
            "colors": ["yellow", "turquoise"],
            "description": "Pensamento de 2ª tier (Amarelo/Turquesa) sem dominar níveis anteriores. Risco de ser muito teórico sem execução prática.",
            "recommendation": "Equilibre visão sistêmica com ação concreta. Desenvolva um pouco de Vermelho (ação), Azul (disciplina) e Laranja (resultados)."
        })

    return warnings


def _get_spiral_description(color: str) -> str:
    """
    Retorna descrição do nível Spiral Dynamics.

    Args:
        color: Nome da cor (primary level)

    Returns:
        Descrição do nível
    """
    descriptions = {
        "beige": "Instintivo - Foco em sobrevivência básica, necessidades fisiológicas",
        "purple": "Tribal - Lealdade ao grupo, tradições, rituais, segurança coletiva",
        "red": "Impulsivo/Poder - Ação imediata, assertividade, dominância, viver o momento",
        "blue": "Tradicional/Ordem - Disciplina, estrutura, regras, autoridade, propósito maior",
        "orange": "Moderno/Conquista - Sucesso material, eficiência, inovação, competição",
        "green": "Pós-moderno/Igualitário - Colaboração, bem-estar, igualdade, sustentabilidade",
        "yellow": "Integrador/Sistêmico - Pensamento complexo, flexibilidade, integração de perspectivas",
        "turquoise": "Holístico/Global - Visão planetária, consciência coletiva, sinergia global"
    }

    return descriptions.get(color, f"Nível {color}")
