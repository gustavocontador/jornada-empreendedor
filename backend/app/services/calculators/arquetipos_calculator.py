"""
Arquétipos Calculator - Cálculo dos arquétipos de contratação preferidos.

Identifica os 3 perfis que o empreendedor mais busca contratar:
- Executor, Criativo, Organizador, Vendedor, Analítico
- Empático, Confiável, Técnico, Líder
"""
from typing import Any, Optional

from app.models.response import Response


def calculate_arquetipos(responses: list[Response], questions_data: dict[str, Any]) -> dict[str, Any]:
    """
    Calcula arquétipos de contratação a partir das respostas.

    Args:
        responses: Lista de respostas do usuário
        questions_data: Dados do questionário com pontuações

    Returns:
        Dicionário com top 3 arquétipos
    """
    # Mapeia respostas usando YAML ID (extra_data['id']) ao invés de UUID
    response_map = {}
    for r in responses:
        if hasattr(r, 'question') and r.question and r.question.extra_data:
            yaml_id = r.question.extra_data.get('id')
            if yaml_id:
                response_map[yaml_id] = r

    # Busca pergunta de ranking de arquétipos (q087)
    arquetipos_ranking = None
    for question in questions_data.get("perguntas", []):
        if question.get("id") == "q087":
            response = response_map.get("q087")
            if response:
                arquetipos_ranking = response.answer_value
            break

    # Processa ranking
    if isinstance(arquetipos_ranking, list):
        primary = arquetipos_ranking[0] if len(arquetipos_ranking) > 0 else None
        secondary = arquetipos_ranking[1] if len(arquetipos_ranking) > 1 else None
        tertiary = arquetipos_ranking[2] if len(arquetipos_ranking) > 2 else None
    elif isinstance(arquetipos_ranking, dict):
        primary = arquetipos_ranking.get("rank_1") or arquetipos_ranking.get("primary")
        secondary = arquetipos_ranking.get("rank_2") or arquetipos_ranking.get("secondary")
        tertiary = arquetipos_ranking.get("rank_3") or arquetipos_ranking.get("tertiary")
    else:
        # Fallback: infere de perfil PAEI/DISC
        return _infer_from_profile(responses, questions_data)

    # Gera insights de gap entre perfil e contratação
    gap_insights = _analyze_profile_gaps(primary, secondary, tertiary, responses, questions_data)

    return {
        "primary": primary,
        "secondary": secondary,
        "tertiary": tertiary,
        "description": _get_arquetipo_description(primary),
        "gap_insights": gap_insights
    }


def _infer_from_profile(responses: list[Response], questions_data: dict[str, Any]) -> dict[str, Any]:
    """
    Infere arquétipos preferidos baseado no próprio perfil (complementaridade).

    A lógica: empreendedores tendem a buscar perfis complementares aos seus.

    Args:
        responses: Lista de respostas
        questions_data: Dados do questionário

    Returns:
        Arquétipos inferidos
    """
    # Importa calculadores para inferir perfil
    from app.services.calculators.paei_calculator import calculate_paei
    from app.services.calculators.disc_calculator import calculate_disc

    paei = calculate_paei(responses, questions_data)
    disc = calculate_disc(responses, questions_data)

    # Mapeia PAEI/DISC para arquétipos complementares
    arquetipos_sugeridos = []

    # Alto P = busca Organizador (complementar)
    if paei.get("p", 0) > 65:
        arquetipos_sugeridos.append(("organizador", 3))

    # Alto E = busca Executor (complementar)
    if paei.get("e", 0) > 65:
        arquetipos_sugeridos.append(("executor", 3))

    # Alto A = busca Criativo (complementar)
    if paei.get("a", 0) > 65:
        arquetipos_sugeridos.append(("criativo", 2))

    # Baixo I = busca Empático (complementar)
    if paei.get("i", 0) < 40:
        arquetipos_sugeridos.append(("empatico", 3))

    # Alto D = busca Confiável (estabilidade)
    if disc.get("d", 0) > 65:
        arquetipos_sugeridos.append(("confiavel", 2))

    # Alto C = busca Técnico (similaridade)
    if disc.get("c", 0) > 65:
        arquetipos_sugeridos.append(("tecnico", 2))

    # Ordena por prioridade
    arquetipos_sugeridos.sort(key=lambda x: x[1], reverse=True)

    primary = arquetipos_sugeridos[0][0] if arquetipos_sugeridos else "executor"
    secondary = arquetipos_sugeridos[1][0] if len(arquetipos_sugeridos) > 1 else "organizador"
    tertiary = arquetipos_sugeridos[2][0] if len(arquetipos_sugeridos) > 2 else "analitico"

    return {
        "primary": primary,
        "secondary": secondary,
        "tertiary": tertiary,
        "description": _get_arquetipo_description(primary),
        "gap_insights": [],
        "inferred": True
    }


def _analyze_profile_gaps(
    primary: Optional[str],
    secondary: Optional[str],
    tertiary: Optional[str],
    responses: list[Response],
    questions_data: dict[str, Any]
) -> list[dict[str, str]]:
    """
    Analisa gaps entre o que busca contratar e o próprio perfil.

    Args:
        primary, secondary, tertiary: Arquétipos preferidos
        responses: Respostas do usuário
        questions_data: Dados do questionário

    Returns:
        Lista de insights sobre gaps
    """
    from app.services.calculators.paei_calculator import calculate_paei
    from app.services.calculators.valores_calculator import calculate_valores

    paei = calculate_paei(responses, questions_data)
    valores = calculate_valores(responses, questions_data)

    insights = []
    arquetipos = [a for a in [primary, secondary, tertiary] if a]

    # Busca Executores mas tem perfil E alto
    if "executor" in arquetipos and paei.get("e", 0) > 70:
        insights.append({
            "type": "critical_gap",
            "description": "Você busca Executores mas seu perfil é Empreendedor (gerador de ideias).",
            "warning": "CRÍTICO: Você pode contratar executores e depois frustrá-los com mudanças constantes.",
            "action": "Antes de contratar executor, garanta que projeto está 80% definido. Permita que executor finalize sem mudanças."
        })

    # Busca Criativos mas também tem perfil E alto
    if "criativo" in arquetipos and paei.get("e", 0) > 70:
        insights.append({
            "type": "redundancy",
            "description": "Você busca Criativos mas já é criativo. Risco de ter muitas ideias e pouca execução.",
            "action": "Contrate 1 Criativo para cada 2 Executores. Você + Criativo = sobrecarga de ideias."
        })

    # Busca Organizadores mas não valoriza disciplina
    if "organizador" in arquetipos:
        valor_primary = valores.get("primary")
        if valor_primary and valor_primary != "disciplina":
            insights.append({
                "type": "value_mismatch",
                "description": "Você busca Organizadores mas seu valor primário não é Disciplina.",
                "warning": "Organizadores precisam que você RESPEITE os processos que criam.",
                "action": "Se contrata organizador, comprometa-se a seguir sistemas que ele criar. Ou não contrate."
            })

    # Busca Empáticos mas tem perfil I baixo
    if "empatico" in arquetipos and paei.get("i", 0) < 40:
        insights.append({
            "type": "awareness",
            "description": "Você busca Empáticos provavelmente porque reconhece que não é seu forte.",
            "positive": "Boa autoconsciência! Você sabe que precisa complementar seu perfil.",
            "action": "Dê autonomia para Empáticos cuidarem da cultura. Não microgere esse aspecto."
        })

    # Busca Analíticos mas tem perfil C baixo
    if "analitico" in arquetipos:
        from app.services.calculators.disc_calculator import calculate_disc
        disc = calculate_disc(responses, questions_data)

        if disc.get("c", 0) < 40:
            insights.append({
                "type": "awareness",
                "description": "Você busca Analíticos porque reconhece que não é forte em análise/detalhes.",
                "action": "Confie nos dados que Analíticos trazem, mesmo que vá contra sua intuição. Esse é o valor deles."
            })

    # Busca Líderes mas tem perfil D alto
    if "lider" in arquetipos:
        from app.services.calculators.disc_calculator import calculate_disc
        disc = calculate_disc(responses, questions_data)

        if disc.get("d", 0) > 70:
            insights.append({
                "type": "conflict_risk",
                "description": "Você busca Líderes mas também tem perfil de liderança forte.",
                "warning": "Risco de choque: dois líderes fortes podem gerar conflito de ego.",
                "action": "Defina claramente áreas de liderança. Você lidera estratégia, ele/ela lidera operação (ou vice-versa)."
            })

    return insights


def _get_arquetipo_description(arquetipo: Optional[str]) -> str:
    """
    Retorna descrição do arquétipo de contratação.

    Args:
        arquetipo: Nome do arquétipo

    Returns:
        Descrição
    """
    descriptions = {
        "executor": "Executor Incansável - Pessoa que faz acontecer, entrega resultado, não precisa de supervisão. 'Vai que dá'.",
        "criativo": "Criativo Inovador - Traz ideias novas, pensa fora da caixa, questiona status quo. Adora problema sem solução óbvia.",
        "organizador": "Organizador Metódico - Cria processos, documenta tudo, mantém ordem. Ama checklists e SOPs.",
        "vendedor": "Vendedor Nato - Persuasivo, carismático, fecha negócios. Convence qualquer um de qualquer coisa.",
        "analitico": "Analítico Estratégico - Pensa estrategicamente, analisa dados, toma decisões lógicas. Planilha é sua linguagem.",
        "empatico": "Empático Integrador - Une pessoas, resolve conflitos, mantém clima positivo. O 'coração' da empresa.",
        "confiavel": "Confiável Estável - Consistente, leal, previsível. Você sabe que ele/ela vai estar lá amanhã e sempre.",
        "tecnico": "Técnico Especialista - Expert em sua área, resolve problemas complexos. A pessoa que 'sabe como fazer'.",
        "lider": "Líder Natural - Inspira pessoas, assume responsabilidade, toma frente. Outros naturalmente o/a seguem."
    }
    return descriptions.get(arquetipo, "")
