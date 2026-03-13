"""
Enneagram Calculator - Cálculo do tipo de Eneagrama.

Eneagrama identifica 9 tipos de personalidade baseados em motivações profundas:
1. Perfeccionista - Busca fazer certo, evita erros
2. Prestativo - Busca ser amado, evita ser rejeitado
3. Realizador - Busca sucesso, evita fracasso
4. Individualista - Busca identidade única, evita ser comum
5. Investigador - Busca conhecimento, evita incompetência
6. Leal/Questionador - Busca segurança, evita perigo
7. Entusiasta - Busca prazer, evita dor
8. Desafiador - Busca controle, evita vulnerabilidade
9. Pacificador - Busca paz, evita conflito
"""
from typing import List, Dict, Any, Optional
from collections import defaultdict

from app.models.response import Response


def calculate_enneagram(responses: List[Response], questions_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Calcula tipo de Eneagrama a partir das respostas.

    Args:
        responses: Lista de respostas do usuário
        questions_data: Dados do questionário com pontuações

    Returns:
        Dicionário com tipo, wing e subtype
    """
    # Acumula pontuações brutas para cada tipo
    raw_scores = {f"enneagram_{i}": 0.0 for i in range(1, 10)}

    # Contadores para normalização
    question_counts = defaultdict(int)

    # Mapeia respostas
    response_map = {str(r.question_id): r for r in responses}

    # Processa cada pergunta
    for question in questions_data.get("perguntas", []):
        question_id = question.get("id")
        pontuacao = question.get("pontuacao", {})

        # Filtra chaves enneagram_
        ennea_keys = [k for k in pontuacao.keys() if k.startswith("enneagram_")]
        if not ennea_keys:
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
            for ennea_key in raw_scores.keys():
                if ennea_key in pontuacao:
                    weight = float(pontuacao[ennea_key])
                    raw_scores[ennea_key] += normalized_value * weight
                    question_counts[ennea_key] += 1

    # Normaliza scores
    normalized_scores = {}
    for key in raw_scores.keys():
        if question_counts[key] > 0:
            avg_score = raw_scores[key] / question_counts[key]
            normalized_scores[key] = max(0, min(100, (avg_score + 1) * 50))
        else:
            normalized_scores[key] = 0.0

    # Identifica tipo primário (maior score)
    sorted_types = sorted(
        [(int(k.split("_")[1]), normalized_scores[k]) for k in raw_scores.keys()],
        key=lambda x: x[1],
        reverse=True
    )

    primary_type = sorted_types[0][0] if sorted_types else 3
    primary_score = sorted_types[0][1] if sorted_types else 0

    # Identifica wing (asa) - tipos adjacentes
    wing = _identify_wing(primary_type, normalized_scores)

    # Identifica subtype (instintivo) baseado em padrões de resposta
    subtype = _identify_subtype(primary_type, responses, questions_data, normalized_scores)

    # Gera insights do tipo
    insights = _get_enneagram_insights(primary_type, wing, primary_score)

    return {
        "type": primary_type,
        "wing": wing,
        "subtype": subtype,
        "description": _get_enneagram_description(primary_type),
        "core_motivation": _get_core_motivation(primary_type),
        "core_fear": _get_core_fear(primary_type),
        "insights": insights,
        "scores": {str(t): round(normalized_scores[f"enneagram_{t}"], 2) for t in range(1, 10)}
    }


def _identify_wing(primary_type: int, scores: Dict[str, float]) -> Optional[str]:
    """
    Identifica a asa (wing) do tipo primário.

    Wing é o tipo adjacente com maior pontuação.

    Args:
        primary_type: Tipo primário (1-9)
        scores: Scores normalizados de todos os tipos

    Returns:
        Wing no formato "Xw9" ou None
    """
    # Tipos adjacentes (circular: 9->1, 1->2, ..., 8->9)
    adjacent = {
        1: [9, 2],
        2: [1, 3],
        3: [2, 4],
        4: [3, 5],
        5: [4, 6],
        6: [5, 7],
        7: [6, 8],
        8: [7, 9],
        9: [8, 1]
    }

    neighbors = adjacent.get(primary_type, [])
    if not neighbors:
        return None

    # Compara scores dos adjacentes
    neighbor_scores = [(n, scores.get(f"enneagram_{n}", 0)) for n in neighbors]
    neighbor_scores.sort(key=lambda x: x[1], reverse=True)

    wing_type = neighbor_scores[0][0]
    wing_score = neighbor_scores[0][1]

    # Só considera wing se score for significativo (> 40)
    if wing_score > 40:
        return f"{primary_type}w{wing_type}"

    return None


def _identify_subtype(
    primary_type: int,
    responses: List[Response],
    questions_data: Dict[str, Any],
    ennea_scores: Dict[str, float]
) -> Optional[str]:
    """
    Identifica subtipo instintivo (sp/so/sx).

    sp (self-preservation): Segurança, conforto, recursos
    so (social): Pertencimento, status, grupo
    sx (sexual/one-to-one): Intensidade, conexão profunda

    Args:
        primary_type: Tipo primário
        responses: Respostas do usuário
        questions_data: Dados do questionário
        ennea_scores: Scores de eneagrama

    Returns:
        Subtipo ou None
    """
    # Heurística baseada em padrões de comportamento
    # (Simplificada - idealmente seria um questionário separado)

    subtype_indicators = {
        "sp": 0.0,  # self-preservation
        "so": 0.0,  # social
        "sx": 0.0   # sexual/one-to-one
    }

    # Analisa padrões específicos
    response_map = {str(r.question_id): r for r in responses}

    # sp indicators: segurança, estabilidade, processos
    sp_questions = ["q015", "q049", "q076"]  # Valoriza estabilidade, crescer devagar, busca segurança
    for qid in sp_questions:
        resp = response_map.get(qid)
        if resp and isinstance(resp.answer_value, (int, float)):
            subtype_indicators["sp"] += float(resp.answer_value) / 5.0

    # so indicators: grupo, colaboração, networking
    so_questions = ["q012", "q032", "q038"]  # Networking, igualdade, opinião do grupo
    for qid in so_questions:
        resp = response_map.get(qid)
        if resp and isinstance(resp.answer_value, (int, float)):
            subtype_indicators["so"] += float(resp.answer_value) / 5.0

    # sx indicators: intensidade, confronto, paixão
    sx_questions = ["q007", "q010", "q079"]  # Controle, não tem medo de confronto, vulnerabilidade
    for qid in sx_questions:
        resp = response_map.get(qid)
        if resp and isinstance(resp.answer_value, (int, float)):
            subtype_indicators["sx"] += float(resp.answer_value) / 5.0

    # Identifica dominante
    dominant = max(subtype_indicators.items(), key=lambda x: x[1])

    if dominant[1] > 1.5:  # Threshold mínimo
        return dominant[0]

    return None


def _get_enneagram_insights(primary_type: int, wing: Optional[str], score: float) -> List[Dict[str, str]]:
    """
    Gera insights específicos do tipo para empreendedores.

    Args:
        primary_type: Tipo primário (1-9)
        wing: Wing identificada
        score: Score do tipo primário

    Returns:
        Lista de insights
    """
    insights_map = {
        1: [
            {
                "area": "Perfeccionismo",
                "insight": "Seu padrão de exigência pode atrasar decisões e gerar frustração na equipe.",
                "action": "Pratique 'Bom o Suficiente': defina critério mínimo aceitável e libere. Perfeição é inimiga do feito."
            },
            {
                "area": "Crítica Interna",
                "insight": "Você é seu próprio crítico mais severo, o que gera estresse constante.",
                "action": "Separe 'padrão de qualidade' de 'autocrítica destrutiva'. Use auto-compaixão como ferramenta de produtividade."
            }
        ],
        2: [
            {
                "area": "Limites",
                "insight": "Você dá muito de si esperando reciprocidade, o que pode gerar ressentimento.",
                "action": "Estabeleça limites claros. Ajude porque QUER, não porque espera algo em troca. Pratique dizer 'não'."
            }
        ],
        3: [
            {
                "area": "Autenticidade",
                "insight": "Seu valor não está apenas em conquistas. Você é mais do que seus resultados.",
                "action": "Reserve tempo semanal para atividades sem 'propósito produtivo'. Pratique ser ao invés de apenas fazer."
            }
        ],
        4: [
            {
                "area": "Singularidade",
                "insight": "Seu desejo de ser único pode dificultar seguir melhores práticas comprovadas.",
                "action": "Você pode ser autêntico E aprender com outros. Singularidade vem de como você aplica, não de inventar tudo do zero."
            }
        ],
        5: [
            {
                "area": "Ação vs Análise",
                "insight": "Você busca acumular conhecimento antes de agir, o que pode gerar paralisia.",
                "action": "Adote 'Aprender Fazendo': 70% ação, 30% estudo. Conhecimento sem aplicação é apenas teoria."
            }
        ],
        6: [
            {
                "area": "Confiança",
                "insight": "Seu excesso de preparação para problemas pode gerar ansiedade e paralisia.",
                "action": "Planeje para cenário provável, não para pior cenário. Use 'Pre-mortem' uma vez, depois execute."
            }
        ],
        7: [
            {
                "area": "Foco",
                "insight": "Seu entusiasmo gera muitas ideias, mas dificuldade em completar projetos.",
                "action": "Regra '3 antes de N': Finalize 3 projetos antes de começar novos. Prazer também vem de completar."
            }
        ],
        8: [
            {
                "area": "Controle",
                "insight": "Sua necessidade de controle pode afastar pessoas e bloquear delegação.",
                "action": "Pratique 'Controlar Resultados, Não Processos'. Defina metas claras e deixe equipe escolher o como."
            }
        ],
        9: [
            {
                "area": "Priorização",
                "insight": "Você se perde em tarefas menores evitando decisões importantes.",
                "action": "Use 'Top 3 do Dia': toda manhã, identifique 3 tarefas críticas. Faça ANTES de qualquer outra coisa."
            }
        ]
    }

    return insights_map.get(primary_type, [])


def _get_enneagram_description(tipo: int) -> str:
    """Retorna descrição do tipo de Eneagrama."""
    descriptions = {
        1: "O Perfeccionista - Principled, Purposeful, Self-Controlled, and Perfectionistic",
        2: "O Prestativo - Generous, Demonstrative, People-Pleasing, and Possessive",
        3: "O Realizador - Adaptable, Excelling, Driven, and Image-Conscious",
        4: "O Individualista - Expressive, Dramatic, Self-Absorbed, and Temperamental",
        5: "O Investigador - Perceptive, Innovative, Secretive, and Isolated",
        6: "O Leal - Engaging, Responsible, Anxious, and Suspicious",
        7: "O Entusiasta - Spontaneous, Versatile, Acquisitive, and Scattered",
        8: "O Desafiador - Self-Confident, Decisive, Willful, and Confrontational",
        9: "O Pacificador - Receptive, Reassuring, Complacent, and Resigned"
    }
    return descriptions.get(tipo, f"Tipo {tipo}")


def _get_core_motivation(tipo: int) -> str:
    """Retorna motivação central do tipo."""
    motivations = {
        1: "Ser bom, ter integridade, fazer o certo",
        2: "Ser amado, ser necessário, ser valorizado",
        3: "Ter sucesso, ser admirado, ser valioso",
        4: "Ser único, ser autêntico, ser especial",
        5: "Ser competente, ser capaz, entender o mundo",
        6: "Ter segurança, ter certeza, ter apoio",
        7: "Ser feliz, ter prazer, evitar dor",
        8: "Ser forte, estar no controle, proteger-se",
        9: "Ter paz interior, manter harmonia, evitar conflito"
    }
    return motivations.get(tipo, "")


def _get_core_fear(tipo: int) -> str:
    """Retorna medo central do tipo."""
    fears = {
        1: "Ser corrupto, mau, imperfeito",
        2: "Ser rejeitado, não ser amado",
        3: "Ser desvalorizado, fracassar",
        4: "Não ter identidade, ser comum",
        5: "Ser incompetente, não saber",
        6: "Estar sem apoio, estar em perigo",
        7: "Estar preso em dor, perder oportunidades",
        8: "Ser controlado, ser vulnerável",
        9: "Ter conflito, perder conexão"
    }
    return fears.get(tipo, "")
