"""
Interpretations Generator - Gera interpretações profundas baseadas em todos os frameworks.

Usa conhecimento de Spiral Dynamics, DISC, PAEI, Eneagrama e valores
para gerar insights personalizados e detectar problemas.
"""
from typing import List, Dict, Any

from app.models.response import Response


def generate_interpretations(
    disc: Dict[str, Any],
    spiral: Dict[str, Any],
    paei: Dict[str, Any],
    enneagram: Dict[str, Any],
    valores: Dict[str, Any],
    arquetipos: Dict[str, Any],
    responses: List[Response],
    questions_data: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Gera interpretações profundas baseadas em todos os scores.

    Args:
        disc, spiral, paei, enneagram, valores, arquetipos: Scores de cada framework
        responses: Respostas do usuário
        questions_data: Dados do questionário

    Returns:
        Dicionário com interpretações estruturadas
    """
    interpretations = {
        "perfil_geral": _generate_general_profile(disc, spiral, paei, enneagram, valores),
        "forcas": _identify_strengths(disc, spiral, paei, enneagram, valores),
        "desafios": _identify_challenges(disc, spiral, paei, enneagram, valores),
        "blind_spots": _identify_blind_spots(disc, spiral, paei, enneagram),
        "gestao_pessoas": _analyze_people_management(spiral, paei, enneagram, valores, arquetipos),
        "gestao_financeira": _analyze_financial_management(spiral, paei, enneagram, responses, questions_data),
        "potencial_crescimento": _analyze_growth_potential(spiral, paei, valores),
        "recomendacoes_desenvolvimento": _generate_development_recommendations(
            disc, spiral, paei, enneagram, valores
        )
    }

    return interpretations


def _generate_general_profile(
    disc: Dict[str, Any],
    spiral: Dict[str, Any],
    paei: Dict[str, Any],
    enneagram: Dict[str, Any],
    valores: Dict[str, Any]
) -> str:
    """Gera descrição geral do perfil do empreendedor."""
    disc_profile = disc.get("profile", "")
    spiral_primary = spiral.get("primary", "orange")
    paei_code = paei.get("code", "")
    ennea_type = enneagram.get("type", 3)
    valor_primary = valores.get("primary", "resultado")

    profile = f"Você é um empreendedor com perfil {disc_profile} (DISC), "
    profile += f"operando principalmente no nível {spiral_primary.upper()} da Espiral Dinâmica, "
    profile += f"com estilo de gestão {paei_code} (PAEI). "
    profile += f"Sua motivação profunda é do tipo {ennea_type} do Eneagrama, "
    profile += f"e seu valor empresarial primário é {valor_primary.upper()}."

    return profile


def _identify_strengths(
    disc: Dict[str, Any],
    spiral: Dict[str, Any],
    paei: Dict[str, Any],
    enneagram: Dict[str, Any],
    valores: Dict[str, Any]
) -> List[Dict[str, str]]:
    """Identifica forças do empreendedor."""
    strengths = []

    # Forças baseadas em DISC
    if disc.get("d", 0) > 70:
        strengths.append({
            "area": "Assertividade e Resultados",
            "description": "Você é decisivo e orientado a resultados. Não tem medo de tomar decisões difíceis.",
            "leverage": "Use essa força para momentos críticos que exigem ação rápida e liderança firme."
        })

    if disc.get("i", 0) > 70:
        strengths.append({
            "area": "Influência e Networking",
            "description": "Você é carismático e sabe persuadir pessoas. Networking é natural para você.",
            "leverage": "Use essa força em vendas, parcerias e construção de marca pessoal."
        })

    # Forças baseadas em Spiral
    spiral_primary = spiral.get("primary", "orange")

    if spiral_primary == "orange":
        strengths.append({
            "area": "Eficiência e Inovação (Laranja)",
            "description": "Você busca constantemente formas mais eficientes de fazer as coisas. Orientado a metas e sucesso.",
            "leverage": "Capitalize sua ambição estruturada. Você consegue competir E inovar simultaneamente."
        })

    elif spiral_primary == "yellow":
        strengths.append({
            "area": "Pensamento Sistêmico (Amarelo)",
            "description": "Você vê padrões complexos e consegue integrar múltiplas perspectivas. Visão estratégica avançada.",
            "leverage": "Raríssimo entre empreendedores. Use para criar modelos de negócio únicos e adaptáveis."
        })

    elif spiral_primary == "green":
        strengths.append({
            "area": "Cultura e Propósito (Verde)",
            "description": "Você cria ambientes colaborativos e valoriza propósito acima de lucro puro.",
            "leverage": "Use para atrair talentos de alta qualidade que buscam significado, não apenas salário."
        })

    # Forças baseadas em PAEI
    paei_high = [k.split("_")[1] for k, v in paei.items() if isinstance(v, (int, float)) and float(v) > 70]

    if "p" in paei_high:
        strengths.append({
            "area": "Execução (PAEI-P)",
            "description": "Você entrega resultados tangíveis. 'Done is better than perfect' é seu mantra.",
            "leverage": "Use em fases iniciais de produtos/serviços. MVP rápido é sua especialidade."
        })

    if "e" in paei_high:
        strengths.append({
            "area": "Visão Empreendedora (PAEI-E)",
            "description": "Você enxerga oportunidades onde outros veem problemas. Criatividade estratégica.",
            "leverage": "Use para pivotagem e adaptação. Você prospera em mercados voláteis."
        })

    return strengths


def _identify_challenges(
    disc: Dict[str, Any],
    spiral: Dict[str, Any],
    paei: Dict[str, Any],
    enneagram: Dict[str, Any],
    valores: Dict[str, Any]
) -> List[Dict[str, str]]:
    """Identifica desafios e problemas potenciais."""
    challenges = []

    # Desafios de Spiral Dynamics
    spiral_warnings = spiral.get("warnings", [])
    for warning in spiral_warnings:
        if warning.get("type") == "value_conflict":
            challenges.append({
                "area": "Conflito de Valores Internos",
                "description": warning.get("description", ""),
                "impact": "Alto",
                "solution": warning.get("recommendation", "")
            })

    # Desafios de PAEI
    paei_issues = paei.get("issues", [])
    for issue in paei_issues:
        if issue.get("severity") in ["critical", "high"]:
            challenges.append({
                "area": issue.get("type", "").replace("_", " ").title(),
                "description": issue.get("description", ""),
                "impact": issue.get("severity", "medium").capitalize(),
                "solution": issue.get("solution", "")
            })

    # Desafios de Eneagrama
    ennea_type = enneagram.get("type", 3)
    ennea_challenges = {
        1: "Perfeccionismo paralisante - você pode atrasar decisões buscando perfeição inatingível.",
        2: "Dificuldade em cobrar resultados - você pode priorizar ser amado sobre ser eficaz.",
        3: "Identificação com trabalho - seu valor pessoal está muito atrelado a conquistas profissionais.",
        4: "Inconsistência emocional - altos e baixos emocionais podem afetar decisões de negócio.",
        5: "Análise sem ação - você pode acumular conhecimento mas procrastinar execução.",
        6: "Excesso de preparação - você pode gastar energia demais antecipando problemas.",
        7: "Falta de foco - você pode ter dificuldade em completar projetos antes de começar novos.",
        8: "Dificuldade em delegar - sua necessidade de controle pode bloquear crescimento da equipe.",
        9: "Evitar conflitos necessários - você pode deixar problemas crescerem para manter harmonia."
    }

    if ennea_type in ennea_challenges:
        challenges.append({
            "area": f"Padrão de Autossabotagem (Tipo {ennea_type})",
            "description": ennea_challenges[ennea_type],
            "impact": "Alto",
            "solution": "Desenvolva consciência do padrão. Quando perceber o comportamento, pause e escolha resposta diferente."
        })

    return challenges


def _identify_blind_spots(
    disc: Dict[str, Any],
    spiral: Dict[str, Any],
    paei: Dict[str, Any],
    enneagram: Dict[str, Any]
) -> List[Dict[str, str]]:
    """Identifica blind spots (pontos cegos) do empreendedor."""
    blind_spots = []

    # Alto D + Baixo S = Blind spot em paciência
    if disc.get("d", 0) > 70 and disc.get("s", 0) < 30:
        blind_spots.append({
            "blind_spot": "Impaciência com Processos Lentos",
            "description": "Você pode atropelar processos necessários e pessoas mais cuidadosas.",
            "consequence": "Erros evitáveis, retrabalho, turnover de perfis C e S.",
            "awareness": "Nem tudo pode ser feito rápido. Qualidade às vezes exige tempo."
        })

    # Alto E (PAEI) + Baixo A = Blind spot em execução estruturada
    if paei.get("e", 0) > 70 and paei.get("a", 0) < 30:
        blind_spots.append({
            "blind_spot": "Mudanças Sem Consolidação",
            "description": "Você inicia mudanças sem consolidar a anterior. Equipe fica perdida.",
            "consequence": "Nada se completa, retrabalho constante, equipe exausta.",
            "awareness": "Inovação sem execução é apenas distração cara."
        })

    # Alto I (PAEI) + Baixo P = Blind spot em cobrança
    if paei.get("i", 0) > 70 and paei.get("p", 0) < 30:
        blind_spots.append({
            "blind_spot": "Evitar Cobrança de Resultados",
            "description": "Você prioriza harmonia sobre performance. Não cobra quem precisa ser cobrado.",
            "consequence": "Equipe confortável mas improdutiva. Problemas financeiros.",
            "awareness": "Cuidar de pessoas INCLUI cobrar resultados. Baixa performance também prejudica o time."
        })

    # Spiral Verde alto + Vermelho baixo = Blind spot em assertividade
    if spiral.get("green", 0) > 70 and spiral.get("red", 0) < 30:
        blind_spots.append({
            "blind_spot": "Excesso de Consenso",
            "description": "Você busca consenso em decisões que deveriam ser unilaterais.",
            "consequence": "Paralisia decisória, perda de oportunidades, liderança fraca.",
            "awareness": "Nem tudo é democrático. Algumas decisões o líder TEM que tomar sozinho."
        })

    return blind_spots


def _analyze_people_management(
    spiral: Dict[str, Any],
    paei: Dict[str, Any],
    enneagram: Dict[str, Any],
    valores: Dict[str, Any],
    arquetipos: Dict[str, Any]
) -> Dict[str, Any]:
    """Analisa capacidade de gestão de pessoas."""
    analysis = {
        "estilo_lideranca": "",
        "facilidade_delegacao": 0,  # 0-10
        "tendencia_microgestao": 0,  # 0-10
        "capacidade_desenvolver_pessoas": 0,  # 0-10
        "recomendacoes": []
    }

    # Estilo de liderança baseado em Spiral
    spiral_primary = spiral.get("primary", "orange")
    leadership_styles = {
        "red": "Autocrático/Diretivo - Lidera pela força e decisão rápida",
        "blue": "Hierárquico/Tradicional - Lidera por autoridade e regras",
        "orange": "Meritocrático/Resultados - Lidera por metas e performance",
        "green": "Participativo/Colaborativo - Lidera por consenso e inclusão",
        "yellow": "Situacional/Adaptativo - Ajusta estilo ao contexto",
        "turquoise": "Visionário/Inspiracional - Lidera por propósito maior"
    }
    analysis["estilo_lideranca"] = leadership_styles.get(spiral_primary, "Misto")

    # Facilidade de delegação (baseado em PAEI e Eneagrama)
    paei_i = float(paei.get("i", 50))
    paei_p = float(paei.get("p", 50))
    ennea_type = enneagram.get("type", 3)

    # Alto I = boa delegação, Alto P = má delegação, Tipo 8 = má delegação
    delegation_score = (paei_i / 10) - (paei_p / 20)
    if ennea_type == 8:
        delegation_score -= 2
    if ennea_type == 9:
        delegation_score += 1

    analysis["facilidade_delegacao"] = max(0, min(10, 5 + delegation_score))

    # Tendência a microgestão
    paei_a = float(paei.get("a", 50))
    micromanagement_score = (paei_a / 15) + (paei_p / 15)
    if ennea_type in [1, 8]:
        micromanagement_score += 2

    analysis["tendencia_microgestao"] = max(0, min(10, micromanagement_score))

    # Capacidade de desenvolver pessoas
    development_score = (paei_i / 12) + ((100 - paei_p) / 30)
    if spiral.get("green", 0) > 60:
        development_score += 2

    analysis["capacidade_desenvolver_pessoas"] = max(0, min(10, development_score))

    # Recomendações
    if analysis["facilidade_delegacao"] < 5:
        analysis["recomendacoes"].append(
            "Priorize desenvolver delegação. Comece com tarefas pequenas e use framework 'Observar-Explicar-Fazer-Revisar'."
        )

    if analysis["tendencia_microgestao"] > 6:
        analysis["recomendacoes"].append(
            "Cuidado com microgestão. Defina objetivos claros mas deixe equipe escolher o 'como'."
        )

    return analysis


def _analyze_financial_management(
    spiral: Dict[str, Any],
    paei: Dict[str, Any],
    enneagram: Dict[str, Any],
    responses: List[Response],
    questions_data: Dict[str, Any]
) -> Dict[str, Any]:
    """Analisa potenciais problemas com gestão financeira."""
    analysis = {
        "risco_problemas_financeiros": "low",  # low, medium, high
        "padroes_identificados": [],
        "recomendacoes": []
    }

    # Mapeia respostas específicas sobre finanças
    response_map = {str(r.question_id): r for r in responses}

    # q083: Dificuldade em precificar
    # q084: Gastos impulsivos
    # q085: Evita olhar números

    pricing_difficulty = 0
    impulsive_spending = 0
    avoids_numbers = 0

    resp_083 = response_map.get("q083")
    if resp_083 and isinstance(resp_083.answer_value, (int, float)):
        pricing_difficulty = float(resp_083.answer_value)

    resp_084 = response_map.get("q084")
    if resp_084 and isinstance(resp_084.answer_value, (int, float)):
        impulsive_spending = float(resp_084.answer_value)

    resp_085 = response_map.get("q085")
    if resp_085 and isinstance(resp_085.answer_value, (int, float)):
        avoids_numbers = float(resp_085.answer_value)

    # Calcula risco
    risk_score = 0

    # Baixo A (PAEI) = risco financeiro
    if paei.get("a", 50) < 35:
        risk_score += 3
        analysis["padroes_identificados"].append("Baixa organização administrativa aumenta risco de problemas de caixa.")

    # Alto E + Baixo A = gastos impulsivos
    if paei.get("e", 0) > 70 and paei.get("a", 0) < 35:
        risk_score += 2
        analysis["padroes_identificados"].append("Perfil empreendedor sem controle administrativo: risco de gastos não planejados.")

    # Eneagrama 7 = evita dor (números ruins)
    if enneagram.get("type") == 7:
        risk_score += 1
        analysis["padroes_identificados"].append("Tipo 7 tende a evitar olhar para números quando estão ruins.")

    # Respostas diretas
    if pricing_difficulty >= 4:
        risk_score += 2
        analysis["padroes_identificados"].append("Dificuldade em precificar pode resultar em margem insuficiente.")

    if impulsive_spending >= 4:
        risk_score += 2
        analysis["padroes_identificados"].append("Gastos impulsivos comprometem fluxo de caixa.")

    if avoids_numbers >= 4:
        risk_score += 3
        analysis["padroes_identificados"].append("Evitar olhar números é sinal de alerta crítico. Problemas não desaparecem sozinhos.")

    # Define nível de risco
    if risk_score >= 7:
        analysis["risco_problemas_financeiros"] = "high"
        analysis["recomendacoes"].append("CRÍTICO: Implemente dashboards financeiros SEMANAIS. Considere contratar CFO parcial ou contador gerencial.")
    elif risk_score >= 4:
        analysis["risco_problemas_financeiros"] = "medium"
        analysis["recomendacoes"].append("Atenção: Estruture controle financeiro básico. Use ferramentas como Conta Azul ou Omie.")
    else:
        analysis["risco_problemas_financeiros"] = "low"
        analysis["recomendacoes"].append("Gestão financeira aparentemente saudável. Mantenha disciplina.")

    return analysis


def _analyze_growth_potential(
    spiral: Dict[str, Any],
    paei: Dict[str, Any],
    valores: Dict[str, Any]
) -> Dict[str, Any]:
    """Analisa potencial de crescimento da empresa baseado no perfil."""
    analysis = {
        "potencial_escala": 0,  # 0-10
        "velocidade_crescimento_natural": "",  # slow, moderate, fast
        "limitadores_crescimento": [],
        "aceleradores_crescimento": []
    }

    # Potencial de escala
    scale_score = 0

    # Alto E = visão de crescimento
    if paei.get("e", 0) > 65:
        scale_score += 3
        analysis["aceleradores_crescimento"].append("Visão empreendedora forte: você enxerga oportunidades de expansão.")

    # Alto A = capacidade de estruturar crescimento
    if paei.get("a", 0) > 65:
        scale_score += 3
        analysis["aceleradores_crescimento"].append("Capacidade administrativa: você consegue estruturar crescimento.")

    # Amarelo Spiral = pensamento sistêmico
    if spiral.get("yellow", 0) > 60:
        scale_score += 2
        analysis["aceleradores_crescimento"].append("Pensamento sistêmico: você entende complexidade necessária para escalar.")

    # Valor = crescimento
    if valores.get("primary") == "crescimento":
        scale_score += 2
        analysis["aceleradores_crescimento"].append("Crescimento é valor primário: você está disposto a pagar o preço de escalar.")

    # Limitadores
    if paei.get("p", 0) > 75 and paei.get("i", 0) < 35:
        analysis["limitadores_crescimento"].append("Alto P + Baixo I: Você faz tudo sozinho. Esse é o maior bloqueio para escalar.")

    if paei.get("e", 0) > 75 and paei.get("a", 0) < 30:
        analysis["limitadores_crescimento"].append("Alto E + Baixo A: Muitas ideias sem estrutura. Crescimento será caótico.")

    if spiral.get("purple", 0) > 70:
        analysis["limitadores_crescimento"].append("Alto Roxo: Você contrata por lealdade pessoal, não competência. Limita qualidade da equipe.")

    analysis["potencial_escala"] = max(0, min(10, scale_score))

    # Velocidade natural
    if scale_score >= 7:
        analysis["velocidade_crescimento_natural"] = "fast"
    elif scale_score >= 4:
        analysis["velocidade_crescimento_natural"] = "moderate"
    else:
        analysis["velocidade_crescimento_natural"] = "slow"

    return analysis


def _generate_development_recommendations(
    disc: Dict[str, Any],
    spiral: Dict[str, Any],
    paei: Dict[str, Any],
    enneagram: Dict[str, Any],
    valores: Dict[str, Any]
) -> List[Dict[str, str]]:
    """Gera recomendações de desenvolvimento pessoal."""
    recommendations = []

    # Recomendação baseada em nível Spiral
    spiral_primary = spiral.get("primary", "orange")

    if spiral_primary in ["red", "blue"]:
        recommendations.append({
            "area": "Evolução de Consciência",
            "recommendation": f"Você opera primariamente em {spiral_primary.upper()}. Explore níveis superiores (Laranja, Verde) para ampliar perspectivas.",
            "resources": "Livro: 'Spiral Dynamics' de Don Beck. Estude casos de empresas em diferentes níveis."
        })

    if spiral_primary == "orange":
        recommendations.append({
            "area": "Humanização da Liderança",
            "recommendation": "Laranja foca em eficiência. Desenvolva Verde (empatia) para atrair e reter talentos de nova geração.",
            "resources": "Livro: 'Leaders Eat Last' de Simon Sinek."
        })

    # Recomendação baseada em gaps PAEI
    paei_code = paei.get("code", "")
    lowest_paei = min(
        [("P", paei.get("p", 50)), ("A", paei.get("a", 50)), ("E", paei.get("e", 50)), ("I", paei.get("i", 50))],
        key=lambda x: x[1]
    )

    if lowest_paei[1] < 35:
        development_map = {
            "P": ("Execução", "Faça um 'sprint de execução': 30 dias focado APENAS em entregar, sem planejar."),
            "A": ("Organização", "Dedique 2h/semana para criar 1 processo. Em 6 meses você terá 24 processos."),
            "E": ("Inovação", "Bloqueie 1 dia/mês para 'Dia de Inovação': zero operação, só pensar em futuro."),
            "I": ("Integração", "Invista em 1:1s semanais com cada líder. Conexão pessoal gera alinhamento.")
        }

        if lowest_paei[0] in development_map:
            area, action = development_map[lowest_paei[0]]
            recommendations.append({
                "area": f"Desenvolver {area} (PAEI-{lowest_paei[0]})",
                "recommendation": f"Seu {area} é o papel mais fraco. {action}",
                "resources": f"Busque mentoria com alguém forte em {lowest_paei[0]}."
            })

    return recommendations
