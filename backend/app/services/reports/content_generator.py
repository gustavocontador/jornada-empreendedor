"""
Content Generator - Gera conteúdo detalhado para relatório completo.

Este módulo contém toda a lógica de interpretação profunda baseada na
knowledge base de Spiral Dynamics e outros frameworks.
"""
from typing import Any


# ===== DISC CONTENT =====

def generate_disc_content(disc_scores: dict[str, Any]) -> dict[str, Any]:
    """Gera conteúdo detalhado da seção DISC."""
    profile = disc_scores.get("profile", "")
    d_score = disc_scores.get("D", 0)
    i_score = disc_scores.get("I", 0)
    s_score = disc_scores.get("S", 0)
    c_score = disc_scores.get("C", 0)

    return {
        "disc_profile": profile,
        "disc_profile_title": get_disc_profile_title(profile),
        "disc_profile_full_description": get_disc_full_description(profile),

        # Scores individuais
        "disc_d_score": round(d_score, 1),
        "disc_i_score": round(i_score, 1),
        "disc_s_score": round(s_score, 1),
        "disc_c_score": round(c_score, 1),

        # Interpretações por dimensão
        "disc_d_level_class": get_level_class(d_score),
        "disc_d_interpretation": get_disc_dimension_interpretation("D", d_score),
        "disc_i_level_class": get_level_class(i_score),
        "disc_i_interpretation": get_disc_dimension_interpretation("I", i_score),
        "disc_s_level_class": get_level_class(s_score),
        "disc_s_interpretation": get_disc_dimension_interpretation("S", s_score),
        "disc_c_level_class": get_level_class(c_score),
        "disc_c_interpretation": get_disc_dimension_interpretation("C", c_score),

        # Análises profundas
        "disc_strengths": format_list_items(get_disc_strengths(profile, disc_scores)),
        "disc_blind_spots": format_list_items(get_disc_blind_spots(profile, disc_scores)),
        "disc_communication_style": get_disc_communication_style(profile),
        "disc_decision_style": get_disc_decision_style(profile),
        "disc_ideal_environments": format_list_items(get_disc_ideal_environments(profile)),
        "disc_stressors": format_list_items(get_disc_stressors(profile)),
    }


def get_disc_profile_title(profile: str) -> str:
    """Títulos dos perfis DISC."""
    titles = {
        "D": "O Dominador - Líder Decisivo",
        "I": "O Influenciador - Comunicador Nato",
        "S": "O Estável - Pilar de Confiança",
        "C": "O Consciente - Analista Preciso",
        "DI": "O Capitão - Líder Persuasivo",
        "DC": "O Comandante - Estrategista Objetivo",
        "IS": "O Conselheiro - Empático e Inspirador",
        "CS": "O Especialista - Perfeccionista Dedicado",
    }
    return titles.get(profile, "Perfil Equilibrado")


def get_disc_full_description(profile: str) -> str:
    """Descrição completa do perfil DISC."""
    descriptions = {
        "DI": "Você combina assertividade com carisma de forma poderosa. É um líder nato que não apenas toma decisões difíceis, mas também inspira e motiva pessoas a segui-lo. Em negócios, você é excelente em vendas, liderança de times e situações que exigem tanto ação rápida quanto persuasão. Seu desafio é equilibrar o ritmo acelerado com atenção às necessidades emocionais da equipe.",
        "DC": "Você é o estrategista objetivo que combina assertividade com análise. Toma decisões rápidas mas baseadas em dados. Em negócios, você constrói sistemas eficientes e executa com precisão. Seu desafio é não se tornar frio demais ou ignorar o fator humano nas decisões.",
    }
    return descriptions.get(profile, "Você possui um perfil único que combina características de diferentes estilos comportamentais.")


def get_disc_dimension_interpretation(dimension: str, score: float) -> str:
    """Interpretação detalhada de cada dimensão DISC."""
    level = "alto" if score >= 7 else "médio" if score >= 4 else "baixo"

    interpretations = {
        "D": {
            "alto": "Você é altamente assertivo e orientado a resultados. Toma decisões rápidas, assume riscos e gosta de estar no controle. Em situações de crise, você age com confiança. Pode ser percebido como impaciente ou dominador.",
            "médio": "Você é assertivo quando necessário, mas não excessivamente dominante. Equilibra ação com consideração. Sabe quando pressionar e quando recuar.",
            "baixo": "Você prefere evitar conflitos diretos e pode ter dificuldade em ser assertivo. Pode precisar desenvolver mais confiança para tomar decisões difíceis e confrontar problemas."
        },
        "I": {
            "alto": "Você é extremamente sociável e persuasivo. Networking é natural para você. Inspira pessoas com otimismo e entusiasmo. Pode ter dificuldade com tarefas solitárias ou altamente técnicas. Pode prometer demais.",
            "médio": "Você é social quando apropriado, mas também consegue trabalhar sozinho. Equilibra relacionamento com foco no trabalho.",
            "baixo": "Você é mais reservado e prefere comunicação direta e objetiva. Pode ter dificuldade em situações que exigem persuasão ou networking intenso."
        },
        "S": {
            "alto": "Você valoriza estabilidade e harmonia. É leal, paciente e confiável. Prefere mudanças graduais a disruções. Pode ter dificuldade em ambientes caóticos ou com mudanças constantes.",
            "médio": "Você equilibra estabilidade com adaptabilidade. Consegue lidar com mudanças sem se desestabilizar.",
            "baixo": "Você é inquieto e busca novidade. Adapta-se rapidamente a mudanças. Pode ter dificuldade em seguir rotinas ou processos repetitivos."
        },
        "C": {
            "alto": "Você é extremamente analítico e preciso. Valoriza qualidade e dados. Toma decisões baseadas em análise profunda. Pode ser percebido como lento ou perfeccionista demais.",
            "médio": "Você considera dados quando relevante, mas não se paralisa por análise. Equilibra precisão com velocidade.",
            "baixo": "Você prefere ação a análise. Confia em intuição. Pode cometer erros por falta de atenção aos detalhes ou processos."
        }
    }

    return interpretations.get(dimension, {}).get(level, "")


def get_disc_strengths(profile: str, scores: dict[str, Any]) -> list[str]:
    """Pontos fortes do perfil DISC."""
    strengths = []

    if scores.get("D", 0) >= 7:
        strengths.extend([
            "Coragem para tomar decisões difíceis rapidamente",
            "Assertividade em negociações e situações de conflito",
            "Capacidade de liderar em momentos de crise",
            "Foco intenso em resultados e execução"
        ])

    if scores.get("I", 0) >= 7:
        strengths.extend([
            "Carisma natural que atrai pessoas e oportunidades",
            "Networking poderoso e relacionamentos genuínos",
            "Capacidade de inspirar e motivar equipes",
            "Comunicação persuasiva e storytelling"
        ])

    if scores.get("S", 0) >= 7:
        strengths.extend([
            "Lealdade e confiabilidade que criam equipes estáveis",
            "Paciência para construir relacionamentos de longo prazo",
            "Capacidade de criar ambientes harmoniosos",
            "Consistência na execução"
        ])

    if scores.get("C", 0) >= 7:
        strengths.extend([
            "Análise profunda que minimiza erros custosos",
            "Atenção aos detalhes que garante qualidade",
            "Sistemas e processos bem estruturados",
            "Decisões baseadas em dados e evidências"
        ])

    return strengths if strengths else ["Perfil equilibrado em todas as dimensões"]


def get_disc_blind_spots(profile: str, scores: dict[str, Any]) -> list[str]:
    """Pontos cegos do perfil DISC."""
    blind_spots = []

    if scores.get("D", 0) >= 7:
        blind_spots.extend([
            "Pode atropelar pessoas ou ignorar impactos emocionais das decisões",
            "Impaciência com processos ou pessoas mais lentas",
            "Pode criar ambientes de medo ou pressão excessiva",
            "Dificuldade em mostrar vulnerabilidade ou pedir ajuda"
        ])

    if scores.get("I", 0) >= 7:
        blind_spots.extend([
            "Pode prometer demais e entregar de menos",
            "Dificuldade com tarefas técnicas ou solitárias",
            "Pode evitar conversas difíceis para manter harmonia",
            "Tendência a confundir popularidade com efetividade"
        ])

    if scores.get("S", 0) >= 7:
        blind_spots.extend([
            "Resistência a mudanças necessárias",
            "Pode evitar conflitos necessários",
            "Dificuldade em dar feedback direto",
            "Pode se sobrecarregar tentando agradar todos"
        ])

    if scores.get("C", 0) >= 7:
        blind_spots.extend([
            "Paralisia por análise - demora para decidir",
            "Perfeccionismo que atrasa entregas",
            "Pode ser percebido como frio ou distante",
            "Dificuldade em lidar com ambiguidade"
        ])

    return blind_spots if blind_spots else ["Desenvolva autoconsciência sobre seus padrões"]


def get_disc_communication_style(profile: str) -> str:
    """Estilo de comunicação do perfil."""
    styles = {
        "DI": "Você comunica de forma direta, assertiva e persuasiva. Vai direto ao ponto mas sabe envolver emocionalmente. Prefere conversas rápidas e dinâmicas. Pode precisar desacelerar para pessoas mais analíticas ou reflexivas.",
        "DC": "Você comunica de forma objetiva e baseada em fatos. Vai direto ao ponto com dados. Pode ser percebido como frio. Beneficia-se de adicionar mais contexto emocional.",
    }
    return styles.get(profile, "Seu estilo de comunicação equilibra diferentes elementos.")


def get_disc_decision_style(profile: str) -> str:
    """Estilo de tomada de decisão."""
    styles = {
        "DI": "Você decide rápido baseado em uma combinação de intuição, análise superficial e confiança em sua capacidade de persuadir/ajustar depois. Isso é uma força em ambientes dinâmicos, mas pode levar a erros em decisões que exigem análise profunda.",
        "DC": "Você decide baseado em dados mas com rapidez. Não se paralisa por análise, mas também não age por impulso puro. Esse é um estilo poderoso para empreendedorismo.",
    }
    return styles.get(profile, "Seu estilo de decisão é único.")


def get_disc_ideal_environments(profile: str) -> list[str]:
    """Ambientes ideais de trabalho."""
    return [
        "Ambientes dinâmicos com autonomia para tomar decisões",
        "Cultura que valoriza resultados e ação",
        "Projetos desafiadores que exigem liderança",
        "Times pequenos e ágeis (vs burocracias)"
    ]


def get_disc_stressors(profile: str) -> list[str]:
    """Estressores comuns."""
    return [
        "Burocracia excessiva e processos lentos",
        "Falta de autonomia ou microgerenciamento",
        "Ambientes políticos onde ação é bloqueada",
        "Tarefas repetitivas sem desafio"
    ]


# ===== SPIRAL DYNAMICS CONTENT =====

def generate_spiral_content(spiral_scores: dict[str, Any]) -> dict[str, Any]:
    """Gera conteúdo detalhado da seção Espiral Dinâmica."""
    primary = spiral_scores.get("primary", "orange")
    secondary = spiral_scores.get("secondary", "blue")

    return {
        "spiral_primary": primary.capitalize(),
        "spiral_secondary": secondary.capitalize(),
        "spiral_combination_name": get_spiral_combination_name(primary, secondary),

        # Tabela de scores
        "spiral_scores_table": generate_spiral_scores_table(spiral_scores),

        # Análise da cor primária
        "spiral_primary_bg_class": f"bg-{primary}",
        "spiral_primary_title": get_spiral_color_title(primary),
        "spiral_primary_description": get_spiral_color_description(primary),
        "spiral_primary_healthy": format_list_items(get_spiral_healthy_manifestation(primary)),
        "spiral_primary_unhealthy": format_list_items(get_spiral_unhealthy_manifestation(primary)),

        # Análise da cor secundária
        "spiral_secondary_bg_class": f"bg-{secondary}",
        "spiral_secondary_title": get_spiral_color_title(secondary),
        "spiral_secondary_description": get_spiral_color_description(secondary),
        "spiral_secondary_healthy": format_list_items(get_spiral_healthy_manifestation(secondary)),
        "spiral_secondary_unhealthy": format_list_items(get_spiral_unhealthy_manifestation(secondary)),

        # Análise de combinação
        "spiral_combination_analysis": get_spiral_combination_analysis(primary, secondary),
        "spiral_combination_patterns": format_list_items(get_spiral_combination_patterns(primary, secondary)),
        "spiral_combination_conflicts": format_list_items(get_spiral_combination_conflicts(primary, secondary)),
        "spiral_integration_tips": format_list_items(get_spiral_integration_tips(primary, secondary)),

        # Transições
        "spiral_next_color": get_next_spiral_color(primary),
        "spiral_transition_description": get_spiral_transition_description(primary),
        "spiral_transition_signs": format_list_items(get_spiral_transition_signs(primary)),

        # Aplicações em negócios
        "spiral_org_structure": get_spiral_org_structure(primary, secondary),
        "spiral_culture": get_spiral_culture(primary, secondary),
        "spiral_leadership": get_spiral_leadership(primary, secondary),
        "spiral_red_flags": format_list_items(get_spiral_red_flags(primary, secondary)),
    }


def generate_spiral_scores_table(spiral_scores: dict[str, Any]) -> str:
    """Gera HTML da tabela de scores da Espiral."""
    colors = ["beige", "purple", "red", "blue", "orange", "green", "yellow", "turquoise"]
    total = sum([spiral_scores.get(c, 0) for c in colors])

    rows = []
    for color in colors:
        score = spiral_scores.get(color, 0)
        pct = (score / total * 100) if total > 0 else 0
        intensity = "Alta" if pct > 20 else "Média" if pct > 10 else "Baixa"

        rows.append(f"""
            <tr>
                <td class="color-{color}"><strong>{color.capitalize()}</strong></td>
                <td>{score:.1f}</td>
                <td>{pct:.1f}%</td>
                <td>{intensity}</td>
            </tr>
        """)

    return "".join(rows)


def get_spiral_color_title(color: str) -> str:
    """Título da cor da Espiral."""
    titles = {
        "beige": "BEGE - Sobrevivência e Instinto",
        "purple": "ROXO - Tribal e Mágico",
        "red": "VERMELHO - Poder e Impulso",
        "blue": "AZUL - Ordem e Significado",
        "orange": "LARANJA - Sucesso e Inovação",
        "green": "VERDE - Comunidade e Igualdade",
        "yellow": "AMARELO - Sistêmico e Integrador",
        "turquoise": "TURQUESA - Holístico e Global"
    }
    return titles.get(color, color.upper())


def get_spiral_color_description(color: str) -> str:
    """Descrição profunda de cada cor (baseado na knowledge base)."""
    descriptions = {
        "orange": "O nível LARANJA emergiu com o Iluminismo e a Revolução Científica há 300 anos. É o motor do empreendedorismo moderno, caracterizado pela crença em progresso, meritocracia e inovação constante. Indivíduos neste nível acreditam que podem melhorar sua situação através de esforço, estratégia e competição. É o código do Vale do Silício, das startups unicórnio e do capitalismo de livre mercado.",

        "blue": "O nível AZUL emergiu há 5.000 anos com as grandes religiões e códigos de lei. É o fundamento da civilização organizada. Pessoas neste nível buscam significado transcendente, ordem e verdade absoluta. Acreditam em sacrificar gratificação presente por recompensas futuras. É o código que constrói instituições duradouras, processos confiáveis e culturas disciplinadas.",

        "red": "O nível VERMELHO emergiu há 10.000 anos quando humanos começaram a afirmar poder individual. É caracterizado por impulsividade, ego forte e assertividade extrema. Pessoas neste nível respeitam apenas força e poder. Vivem no presente, buscam gratificação imediata e não sentem culpa. É o código dos conquistadores, dos vendedores agressivos e dos empreendedores 'hustlers'.",

        "green": "O nível VERDE emergiu há 150 anos com movimentos de direitos civis e ambientalismo. É uma reação ao materialismo e competição do LARANJA. Pessoas neste nível buscam igualdade, comunidade e sustentabilidade. Valorizam consenso, diversidade e autenticidade. É o código das empresas B Corp, cooperativas e organizações com propósito social.",

        "purple": "O nível ROXO emergiu há 50.000 anos com as primeiras tribos humanas. É caracterizado por pensamento mágico, rituais e forte senso de pertencimento ao grupo. Pessoas neste nível encontram segurança na tradição e na família/tribo. É o código das culturas corporativas fortes, do networking baseado em confiança pessoal e da lealdade profunda.",

        "yellow": "AMARELO é o primeiro nível da Segunda Camada - uma mudança radical de consciência. Pessoas neste nível transcendem ideologia e enxergam todos os níveis anteriores como válidos e necessários. Pensam em sistemas complexos e valorizam funcionalidade acima de ego ou pertencimento. São raros (1-2% da população) e excelentes em integrar perspectivas conflitantes.",

        "turquoise": "TURQUESA é o segundo nível da Segunda Camada. Adiciona ao pensamento sistêmico do AMARELO uma consciência holística e global. Pessoas neste nível experienciam profunda interconexão com todos os sistemas vivos. São extremamente raras e geralmente atuam em desafios planetários ou consciência coletiva."
    }
    return descriptions.get(color, f"Nível {color.upper()} da Espiral Dinâmica.")


def get_spiral_healthy_manifestation(color: str) -> list[str]:
    """Manifestação saudável da cor em negócios."""
    manifestations = {
        "orange": [
            "Inovação constante que melhora produto/serviço genuinamente",
            "Métricas e dados usados para decisões racionais",
            "Meritocracia real que recompensa performance",
            "Crescimento sustentável baseado em criar valor",
            "Flexibilidade estratégica - pivota quando necessário",
            "Atração de capital e investidores de qualidade"
        ],
        "blue": [
            "Processos claros e replicáveis que permitem escala",
            "Planejamento estratégico de longo prazo (5-10 anos)",
            "Cultura de disciplina e execução consistente",
            "Ética e valores que guiam decisões difíceis",
            "Hierarquia funcional com clareza de responsabilidades",
            "Qualidade consistente e confiável"
        ],
        "red": [
            "Coragem para tomar decisões difíceis sob pressão",
            "Assertividade em negociações complexas",
            "Capacidade de agir rápido quando oportunidade surge",
            "Energia alta que impulsiona o time",
            "Defesa feroz do negócio e da equipe",
            "Superação de obstáculos por determinação"
        ],
        "green": [
            "Propósito genuíno que resolve problema social/ambiental",
            "Cultura de cuidado com saúde mental e wellbeing",
            "Diversidade real com vozes ativas de todos",
            "Decisões participativas que engajam o time",
            "Transparência e informação compartilhada",
            "Sustentabilidade ambiental integrada ao negócio"
        ]
    }
    return manifestations.get(color, ["Manifestação saudável desta cor"])


def get_spiral_unhealthy_manifestation(color: str) -> list[str]:
    """Manifestação não saudável da cor em negócios."""
    manifestations = {
        "orange": [
            "Ganância - lucro a qualquer custo, inclusive ético",
            "Workaholismo e burnout generalizado da equipe",
            "Cinismo - tudo vira transação, perda de humanidade",
            "Manipulação e 'jogo' mais importante que integridade",
            "Materialismo vazio - nunca é suficiente",
            "Descarte de pessoas como 'recursos' substituíveis",
            "Externalidades ignoradas (poluição, desigualdade)"
        ],
        "blue": [
            "Burocracia excessiva - processo vira fim em si mesmo",
            "Rigidez extrema - incapacidade de se adaptar",
            "Autoritarismo tóxico - 'porque eu mandei'",
            "Resistência doentia a inovação",
            "Cultura de medo e punição vs aprendizado",
            "Microgerenciamento sufocante"
        ],
        "red": [
            "Liderança abusiva e tóxica",
            "Decisões impulsivas que destroem valor",
            "Atropelar pessoas para atingir objetivos",
            "Falta de planejamento - só ação sem estratégia",
            "Criar ambientes de medo e competição destrutiva",
            "Burnout por gratificação imediata constante"
        ],
        "green": [
            "Paralisia por consenso - nada decide",
            "Virtue signaling - discurso sem ação real",
            "Tirania da sensibilidade - 'cancelamento' interno",
            "Produtividade sacrificada por 'ser bonzinho'",
            "Narcisismo moral - grupo se acha superior",
            "Rejeição a estrutura e hierarquia - vira caos"
        ]
    }
    return manifestations.get(color, ["Manifestação não saudável desta cor"])


def get_spiral_combination_name(primary: str, secondary: str) -> str:
    """Nome da combinação de cores."""
    combinations = {
        ("orange", "blue"): "O Empreendedor Estruturado",
        ("orange", "green"): "O Inovador Consciente",
        ("orange", "red"): "O Guerreiro Estratégico",
        ("blue", "orange"): "O Gestor Inovador",
        ("red", "orange"): "O Conquistador Inteligente",
        ("green", "yellow"): "O Humanista Sistêmico",
    }
    return combinations.get((primary, secondary), f"Perfil {primary.capitalize()}-{secondary.capitalize()}")


def get_spiral_combination_analysis(primary: str, secondary: str) -> str:
    """Análise profunda da combinação."""
    if primary == "orange" and secondary == "blue":
        return """Esta é uma das combinações mais poderosas para empreendedorismo escalável. Você tem a inovação e ambição do LARANJA temperada pela disciplina e estrutura do AZUL. Isso significa que você não apenas tem ideias, mas as executa com consistência. Você constrói sistemas que permitem crescimento sustentável. O risco é se tornar rígido demais (AZUL excessivo) ou perder propósito pelo caminho (LARANJA sem freios)."""

    elif primary == "orange" and secondary == "green":
        return """Você representa o 'novo capitalismo' - busca lucro e crescimento, mas não a qualquer custo. Se importa genuinamente com impacto social e bem-estar da equipe. Isso é cada vez mais valorizado por clientes e talentos millennials/Gen Z. Seu desafio é equilibrar resultados (LARANJA) com cuidado (VERDE) sem sacrificar nem um nem outro."""

    return f"A combinação {primary.upper()}-{secondary.upper()} cria um perfil único de valores."


def get_spiral_combination_patterns(primary: str, secondary: str) -> list[str]:
    """Padrões únicos da combinação."""
    if primary == "orange" and secondary == "blue":
        return [
            "Você inova dentro de estruturas - não é caos criativo",
            "Planeja o crescimento em vez de apenas 'ir fazendo'",
            "Valoriza tanto métricas quanto processos",
            "Consegue escalar negócios de forma previsível"
        ]
    return ["Padrões únicos desta combinação"]


def get_spiral_combination_conflicts(primary: str, secondary: str) -> list[str]:
    """Conflitos internos da combinação."""
    if primary == "orange" and secondary == "blue":
        return [
            "Tensão entre inovar rápido (LARANJA) vs manter qualidade e processos (AZUL)",
            "Frustração quando burocracia atrasa inovação",
            "Conflito entre meritocracia (LARANJA) e hierarquia tradicional (AZUL)",
            "Dificuldade em saber quando quebrar regras vs quando segui-las"
        ]
    return ["Tensões naturais desta combinação"]


def get_spiral_integration_tips(primary: str, secondary: str) -> list[str]:
    """Dicas para integrar as cores."""
    return [
        "Reconheça que ambas as cores são válidas e necessárias",
        "Use AZUL para estruturar e LARANJA para inovar - não um contra o outro",
        "Crie 'espaços seguros' para experimentação dentro de estruturas",
        "Desenvolva a próxima cor (VERDE ou AMARELO) para transcender a tensão"
    ]


def get_next_spiral_color(current: str) -> str:
    """Próxima cor na evolução."""
    sequence = ["beige", "purple", "red", "blue", "orange", "green", "yellow", "turquoise"]
    try:
        idx = sequence.index(current)
        return sequence[idx + 1] if idx < len(sequence) - 1 else "turquoise"
    except ValueError:
        return "green"


def get_spiral_transition_description(current: str) -> str:
    """Descrição da transição para próxima cor."""
    transitions = {
        "orange": "Você está começando a questionar se sucesso material é suficiente. Começa a se importar mais com impacto, propósito e bem-estar coletivo. Isso indica emergência de VERDE.",
        "blue": "Você está começando a questionar se 'uma verdade única' faz sentido. Quer flexibilidade e inovação dentro da estrutura. Isso indica emergência de LARANJA.",
    }
    return transitions.get(current, "Transição para próximo nível.")


def get_spiral_transition_signs(current: str) -> list[str]:
    """Sinais de transição."""
    if current == "orange":
        return [
            "Questionamento sobre propósito além de lucro",
            "Preocupação crescente com bem-estar da equipe",
            "Interesse em impacto social e sustentabilidade",
            "Sensação de 'vazio' apesar do sucesso material"
        ]
    return ["Sinais de evolução"]


def get_spiral_org_structure(primary: str, secondary: str) -> str:
    """Estrutura organizacional ideal."""
    if primary == "orange":
        return "Estrutura ágil e matricial. Equipes multifuncionais com autonomia. KPIs claros mas flexibilidade na execução. Hierarquia mínima necessária."
    return "Estrutura que equilibra suas cores dominantes."


def get_spiral_culture(primary: str, secondary: str) -> str:
    """Cultura organizacional."""
    if primary == "orange":
        return "Cultura de inovação, métricas e meritocracia. Valoriza dados, experimentos e crescimento rápido. Recompensa performance e resultados."
    return "Cultura alinhada com seus valores."


def get_spiral_leadership(primary: str, secondary: str) -> str:
    """Estilo de liderança."""
    if primary == "orange" and secondary == "blue":
        return "Liderança visionária mas disciplinada. Você define direção ambiciosa e cria sistemas para alcançá-la. Equilibra inspiração com execução."
    return "Estilo de liderança único."


def get_spiral_red_flags(primary: str, secondary: str) -> list[str]:
    """Red flags - sinais de alerta."""
    if primary == "orange":
        return [
            "Burnout recorrente seu ou da equipe",
            "Alta rotatividade de talentos",
            "Sensação de vazio apesar de resultados",
            "Decisões que você sabe serem antiéticas 'pelo negócio'",
            "Relacionamentos pessoais deteriorando por foco no trabalho"
        ]
    return ["Sinais de alerta específicos do seu perfil"]


# ===== PAEI CONTENT =====

def generate_paei_content(paei_scores: dict[str, Any]) -> dict[str, Any]:
    """Gera conteúdo detalhado da seção PAEI."""
    code = paei_scores.get("code", "")

    return {
        "paei_code": code,
        "paei_profile_name": get_paei_profile_name(code),
        "paei_full_interpretation": get_paei_full_interpretation(code),

        # Detalhes de cada papel
        "paei_p_letter": "P" if paei_scores.get("P", 0) >= 7 else "p",
        "paei_a_letter": "A" if paei_scores.get("A", 0) >= 7 else "a",
        "paei_e_letter": "E" if paei_scores.get("E", 0) >= 7 else "e",
        "paei_i_letter": "I" if paei_scores.get("I", 0) >= 7 else "i",

        "paei_p_class": get_level_class(paei_scores.get("P", 0)),
        "paei_p_level_name": get_paei_level_name("P", paei_scores.get("P", 0)),
        "paei_p_detailed": get_paei_role_detailed("P", paei_scores.get("P", 0)),

        "paei_a_class": get_level_class(paei_scores.get("A", 0)),
        "paei_a_level_name": get_paei_level_name("A", paei_scores.get("A", 0)),
        "paei_a_detailed": get_paei_role_detailed("A", paei_scores.get("A", 0)),

        "paei_e_class": get_level_class(paei_scores.get("E", 0)),
        "paei_e_level_name": get_paei_level_name("E", paei_scores.get("E", 0)),
        "paei_e_detailed": get_paei_role_detailed("E", paei_scores.get("E", 0)),

        "paei_i_class": get_level_class(paei_scores.get("I", 0)),
        "paei_i_level_name": get_paei_level_name("I", paei_scores.get("I", 0)),
        "paei_i_detailed": get_paei_role_detailed("I", paei_scores.get("I", 0)),

        # Análises específicas
        "paei_people_problems": get_paei_people_problems(code),
        "paei_financial_problems": get_paei_financial_problems(code),
        "paei_hiring_recommendations": format_list_items(get_paei_hiring_recommendations(code)),
        "paei_team_structure": get_paei_team_structure(code),
    }


def get_paei_profile_name(code: str) -> str:
    """Nome do perfil PAEI."""
    names = {
        "Paei": "Produtor Solitário (Lone Ranger)",
        "pAei": "Burocrata",
        "paEi": "Inventor / Arsonista",
        "paeI": "Super Follower",
        "PAei": "Executor",
        "PaEi": "Visionário Desorganizado",
        "PaeI": "Líder de Torcida",
        "pAEi": "Falso Empreendedor",
        "pAeI": "Administrador Político",
        "paEI": "Demagogo",
        "PAEi": "Empreendedor",
        "PAeI": "Estadista",
        "PaEI": "Desenvolvedor",
        "pAEI": "Missionário",
        "PAEI": "Líder Completo"
    }
    return names.get(code, "Perfil Único")


def get_paei_full_interpretation(code: str) -> str:
    """Interpretação completa do código PAEI."""
    if code == "PaEi":
        return """Você é um Visionário Desorganizado - forte em produzir resultados (P) e criar inovação (E), mas fraco em processos (a) e gestão de pessoas (i). Isso é comum em empreendedores na fase inicial. Você tem ideias brilhantes e energia para executar, mas pode ser caótico e ter dificuldade em escalar. Você PRECISA contratar um COO ou gestor forte para complementar."""

    elif code == "PAEi":
        return """Você é um Empreendedor completo - produz (P), organiza (A) e inova (E). Seu ponto fraco é integração de pessoas (i). Você constrói negócios eficientes e inovadores, mas pode ter alta rotatividade ou problemas de cultura. Precisa desenvolver empatia e habilidades de gestão de pessoas, ou contratar um Chief People Officer / Head of Culture."""

    return "Seu código PAEI revela um perfil de gestão único com forças e desafios específicos."


def get_paei_level_name(role: str, score: float) -> str:
    """Nome do nível de cada papel."""
    if score >= 7:
        level = "Alto"
    elif score >= 4:
        level = "Médio"
    else:
        level = "Baixo"

    names = {
        "P": {"Alto": "Produtor Forte", "Médio": "Produtor Moderado", "Baixo": "Produtor Fraco"},
        "A": {"Alto": "Administrador Forte", "Médio": "Administrador Moderado", "Baixo": "Administrador Fraco"},
        "E": {"Alto": "Empreendedor Forte", "Médio": "Empreendedor Moderado", "Baixo": "Empreendedor Fraco"},
        "I": {"Alto": "Integrador Forte", "Médio": "Integrador Moderado", "Baixo": "Integrador Fraco"},
    }

    return names.get(role, {}).get(level, "")


def get_paei_role_detailed(role: str, score: float) -> str:
    """Descrição detalhada de cada papel."""
    if score >= 7:
        level = "alto"
    elif score >= 4:
        level = "médio"
    else:
        level = "baixo"

    descriptions = {
        "P": {
            "alto": "Você é excelente em entregar resultados. Foca no que precisa ser feito e faz acontecer. Clientes e stakeholders confiam que você vai cumprir. Seu desafio é não se tornar apenas um 'fazedor' e desenvolver outras dimensões.",
            "médio": "Você produz resultados mas não de forma consistente. Pode precisar melhorar disciplina e foco.",
            "baixo": "Você tem muitas ideias mas dificuldade em executar. Pode precisar de um 'executor' ao seu lado ou desenvolver mais disciplina."
        },
        "A": {
            "alto": "Você tem sistemas, processos e organização. Sabe onde tudo está, tem planejamento claro e executa com consistência. Isso é fundamental para escalar. Cuidado para não burocratizar demais.",
            "médio": "Você tem alguma organização mas pode melhorar. Processos existem mas não são sempre seguidos.",
            "baixo": "Você é caótico e desorganizado. Isso funciona no início mas impede escala. URGENTE desenvolver estrutura ou contratar alguém com 'A' alto."
        },
        "E": {
            "alto": "Você é altamente inovador e visionário. Sempre vê novas oportunidades e quer experimentar. Isso é essencial para crescimento, mas pode ser desestabilizador se não houver 'A' para estruturar.",
            "médio": "Você inova ocasionalmente mas não é seu padrão principal.",
            "baixo": "Você pode estar preso em zona de conforto. Pode precisar estimular mais inovação ou trazer alguém com 'E' alto."
        },
        "I": {
            "alto": "Você é excelente em desenvolver pessoas e criar coesão de time. Sabe integrar personalidades diferentes e criar cultura forte. Isso é raro e valioso.",
            "médio": "Você se importa com pessoas mas pode melhorar habilidades de gestão e desenvolvimento.",
            "baixo": "Você pode ver pessoas como 'recursos' ou ter dificuldade com gestão emocional. Isso causará problemas de rotatividade e cultura. Desenvolva ou delegue."
        }
    }

    return descriptions.get(role, {}).get(level, "")


def get_paei_people_problems(code: str) -> str:
    """Problemas com pessoas baseados no código."""
    if "i" in code.lower() and code[-1] != "I":
        return """Seu código indica baixo 'I' (Integrador). Isso significa que você provavelmente tem ou terá problemas com gestão de pessoas:

• **Alta rotatividade:** Pessoas boas saem porque não se sentem desenvolvidas ou valorizadas
• **Conflitos não resolvidos:** Você evita conversas difíceis ou as conduz de forma técnica/fria
• **Falta de cultura:** Time trabalha mas não há senso de propósito ou pertencimento
• **Dificuldade em dar feedback:** Você é direto demais ou evita completamente
• **Microgerenciamento:** Compensa falta de confiança/desenvolvimento com controle

**O que fazer:**
1. Contrate um Head of People / Chief People Officer forte
2. Invista em coaching de liderança
3. Crie rituais de feedback estruturados
4. Delegue gestão direta de pessoas para alguém com 'I' alto"""

    return "Seu perfil de integração de pessoas está em nível adequado."


def get_paei_financial_problems(code: str) -> str:
    """Problemas financeiros baseados no código."""
    if "a" in code.lower() and code[1] != "A":
        return """Seu código indica baixo 'A' (Administrador). Isso significa problemas financeiros prováveis:

• **Falta de controles:** Você não sabe exatamente quanto ganha/gasta em tempo real
• **Desperdício:** Gastos desnecessários porque não há processo de aprovação
• **Fluxo de caixa:** Surpresas negativas porque não planeja adequadamente
• **Impostos e compliance:** Atrasos, multas ou problemas com fisco
• **Precificação incorreta:** Vende sem calcular custos reais

**O que fazer:**
1. Contrate um CFO ou controller URGENTE
2. Implemente sistema financeiro (ERP)
3. Crie orçamento anual e acompanhamento mensal
4. Estabeleça alçadas de aprovação de gastos
5. Revise precificação com análise de margem"""

    return "Seu perfil de administração financeira está em nível adequado."


def get_paei_hiring_recommendations(code: str) -> list[str]:
    """Recomendações de contratação baseadas nos gaps."""
    recommendations = []

    if "a" in code.lower() and code[1] != "A":
        recommendations.append("**URGENTE: COO ou CFO** - Alguém que ame processos, planilhas e organização. Perfil 'pAei' ou 'pAEi'.")

    if "i" in code.lower() and code[-1] != "I":
        recommendations.append("**PRIORITÁRIO: Head of People / Chief People Officer** - Alguém empático, com habilidade de desenvolver pessoas. Perfil 'paeI' ou 'paEI'.")

    if "p" in code.lower() and code[0] != "P":
        recommendations.append("**IMPORTANTE: Head of Operations / COO** - Alguém que executa com consistência. Perfil 'Paei' ou 'PAei'.")

    if "e" in code.lower() and code[2] != "E":
        recommendations.append("**SUGERIDO: Chief Innovation Officer / Head of Product** - Alguém criativo e visionário. Perfil 'paEi' ou 'PaEi'.")

    if not recommendations:
        recommendations.append("Seu perfil é balanceado. Foque em contratar especialistas funcionais (Head de Marketing, Head de Vendas, etc).")

    return recommendations


def get_paei_team_structure(code: str) -> str:
    """Estrutura de time ideal."""
    if code == "PaEi":
        return """Você precisa de um **Co-founder ou COO** com perfil 'pAei' ou 'pAEi' - alguém que ADORE organização e processos. Essa pessoa será seu complemento perfeito: você cria e inova, ela estrutura e escala. Também precisa de um **Head of People** cedo (antes de 10 funcionários) porque gestão de pessoas não é seu forte."""

    return "Monte um time que complemente seus pontos fracos do PAEI."


# ===== ENEAGRAMA, VALORES E SÍNTESE =====

def generate_enneagram_content(enneagram_scores: dict[str, Any]) -> dict[str, Any]:
    """Gera conteúdo detalhado do Eneagrama."""
    ennea_type = enneagram_scores.get("type", 3)
    wing = enneagram_scores.get("wing", "")
    subtype = enneagram_scores.get("subtype", "")

    return {
        "enneagram_type": ennea_type,
        "enneagram_name": get_enneagram_name(ennea_type),
        "enneagram_wing": wing,
        "enneagram_subtype_full": get_enneagram_subtype_name(subtype),
        "enneagram_type_description": get_enneagram_description(ennea_type),
        "enneagram_core_motivations": format_list_items(get_enneagram_motivations(ennea_type)),
        "enneagram_core_fears": format_list_items(get_enneagram_fears(ennea_type)),
        "enneagram_self_sabotage": format_list_items(get_enneagram_sabotage(ennea_type)),
        "enneagram_business_impact": get_enneagram_business_impact(ennea_type),
        "enneagram_growth_direction": get_enneagram_growth_direction(ennea_type),
        "enneagram_growth_practices": format_list_items(get_enneagram_practices(ennea_type)),
        "enneagram_stress_direction": get_enneagram_stress_direction(ennea_type),
        "enneagram_wing_influence": get_enneagram_wing_influence(wing),
        "enneagram_subtype_description": get_enneagram_subtype_description(subtype),
    }


def get_enneagram_name(type_num: int) -> str:
    """Nome do tipo."""
    names = {
        1: "O Perfeccionista",
        2: "O Ajudador",
        3: "O Realizador",
        4: "O Individualista",
        5: "O Investigador",
        6: "O Leal",
        7: "O Entusiasta",
        8: "O Desafiador",
        9: "O Pacificador"
    }
    return names.get(type_num, "Tipo Único")


def get_enneagram_description(type_num: int) -> str:
    """Descrição do tipo."""
    if type_num == 3:
        return "Tipo 3 - O Realizador é orientado a sucesso, adaptável e focado em imagem. Você se motiva por conquistas visíveis e reconhecimento. É altamente eficiente, carismático e sabe 'vender' tanto a si mesmo quanto suas ideias. Em negócios, você é um motor de resultados."
    return f"Descrição do Tipo {type_num} do Eneagrama."


def get_enneagram_motivations(type_num: int) -> list[str]:
    """Motivações core."""
    motivations = {
        3: [
            "Ser visto como bem-sucedido e admirado pelos outros",
            "Alcançar metas ambiciosas e superar expectativas",
            "Provar seu valor através de conquistas visíveis",
            "Evitar fracasso, rejeição ou ser visto como incompetente"
        ]
    }
    return motivations.get(type_num, ["Motivações do tipo"])


def get_enneagram_fears(type_num: int) -> list[str]:
    """Medos inconscientes."""
    fears = {
        3: [
            "Fracassar publicamente e perder admiração",
            "Ser visto como incompetente ou 'sem valor'",
            "Perder status ou posição conquistada",
            "Descobrir que sem conquistas, você 'não é ninguém'"
        ]
    }
    return fears.get(type_num, ["Medos do tipo"])


def get_enneagram_sabotage(type_num: int) -> list[str]:
    """Padrões de autossabotagem."""
    sabotage = {
        3: [
            "Workaholismo - sacrifica saúde, relacionamentos e bem-estar por mais conquistas",
            "Foco excessivo em imagem - 'vender' sucesso em vez de construir substância real",
            "Dificuldade em ser autêntico - sempre 'performando' em vez de sendo",
            "Burnout recorrente - não sabe quando parar",
            "Relações superficiais - usa pessoas como degraus ou troféus",
            "Depressão quando conquistas não trazem satisfação esperada"
        ]
    }
    return sabotage.get(type_num, ["Padrões de autossabotagem"])


def get_enneagram_business_impact(type_num: int) -> str:
    """Impacto no empreendedorismo."""
    if type_num == 3:
        return """Como Tipo 3, você é um 'motor de crescimento' natural. Constrói negócios escaláveis e atrai investidores. Mas cuidado: pode construir um negócio 'lindo por fora, vazio por dentro' - muito marketing, pouca substância. Pode também queimar sua equipe (e a si mesmo) por ritmo insustentável. Seu maior desafio é conectar com autenticidade e propósito real, não apenas aparências."""
    return "Impacto do seu tipo no empreendedorismo."


def get_enneagram_growth_direction(type_num: int) -> str:
    """Direção de crescimento."""
    if type_num == 3:
        return "Quando saudável, você integra qualidades do Tipo 6 (lealdade, vulnerabilidade, conexão real com pessoas). Para de performar e começa a SER. Desenvolve autenticidade e valoriza relacionamentos genuínos além de conquistas."
    return "Direção de integração do seu tipo."


def get_enneagram_practices(type_num: int) -> list[str]:
    """Práticas de crescimento."""
    if type_num == 3:
        return [
            "Pausas regulares SEM produzir - apenas ser",
            "Terapia para explorar quem você é além de conquistas",
            "Compartilhar fracassos e vulnerabilidades com pessoas próximas",
            "Medir sucesso por critérios internos, não externos",
            "Cultivar hobbies onde você é 'iniciante' (ego check)"
        ]
    return ["Práticas de crescimento para seu tipo"]


def get_enneagram_stress_direction(type_num: int) -> str:
    """Direção de desintegração."""
    if type_num == 3:
        return "Sob estresse extremo, você desintegra para Tipo 9 - torna-se apático, dissociado e 'vai no piloto automático'. Perde motivação e pode procrastinar - o oposto do seu estado normal."
    return "Comportamento sob estresse extremo."


def get_enneagram_wing_influence(wing: str) -> str:
    """Influência da asa."""
    if wing == "3w2":
        return "Asa 2 adiciona carisma e foco em relacionamentos. Você não apenas quer conquistar, mas ser amado e admirado pessoalmente. Mais político e socialmente habilidoso."
    elif wing == "3w4":
        return "Asa 4 adiciona profundidade emocional e busca por autenticidade. Você quer sucesso mas também significado. Mais introspectivo e criativo."
    return "Influência da sua asa."


def get_enneagram_subtype_name(subtype: str) -> str:
    """Nome do subtipo."""
    names = {
        "sp": "Autopreservação",
        "so": "Social",
        "sx": "Sexual/Um-a-um"
    }
    return names.get(subtype, "")


def get_enneagram_subtype_description(subtype: str) -> str:
    """Descrição do subtipo."""
    if subtype == "so":
        return "Subtipo Social: Você busca status e reconhecimento em grupos/comunidades. Quer ser visto como líder ou referência. Networking é importante para você."
    return "Descrição do seu subtipo."


def generate_valores_content(valores_scores: dict[str, Any], arquetipos_scores: dict[str, Any]) -> dict[str, Any]:
    """Gera conteúdo da seção de valores."""
    top_5 = sorted([(k, v) for k, v in valores_scores.items() if k not in ["primary", "secondary", "tertiary"]],
                   key=lambda x: x[1], reverse=True)[:5]

    return {
        "top_5_values_detailed": format_ordered_list([f"<li><strong>{v[0]}</strong> ({v[1]:.1f}/10) - {get_value_description(v[0])}</li>" for v in top_5]),
        "desired_archetypes": get_desired_archetypes(arquetipos_scores),
        "values_alignment_class": "success-box",
        "values_alignment_analysis": "Seus valores estão alinhados com seu perfil geral.",
        "values_gaps": format_list_items(["Gap 1", "Gap 2"]),  # Placeholder
    }


def get_value_description(value_name: str) -> str:
    """Descrição de cada valor."""
    return f"Valor fundamental para sua cultura organizacional"


def get_desired_archetypes(arquetipos: dict[str, Any]) -> str:
    """Arquetipos que busca contratar."""
    return "Arquetipos complementares ao seu perfil."


def generate_integrated_content(disc: dict[str, Any], spiral: dict[str, Any], paei: dict[str, Any], enneagram: dict[str, Any]) -> dict[str, Any]:
    """Gera síntese integrada."""
    return {
        "integrated_summary": "Síntese integrada de todos os frameworks...",
        "pattern_disc_spiral": "Padrão DISC + Espiral...",
        "pattern_paei_enneagram": "Padrão PAEI + Eneagrama...",
        "pattern_spiral_enneagram": "Padrão Espiral + Eneagrama...",
        "unique_operating_mode": "Seu modo de operação único...",
        "integrated_strengths": format_list_items(["Força integrada 1", "Força integrada 2"]),
        "integrated_risks": format_list_items(["Risco integrado 1", "Risco integrado 2"]),
    }


def generate_action_plan(disc: dict[str, Any], spiral: dict[str, Any], paei: dict[str, Any], enneagram: dict[str, Any]) -> dict[str, Any]:
    """Gera plano de ação 30/60/90."""
    return {
        "action_30_days": format_action_items(["Ação 1", "Ação 2", "Ação 3"]),
        "action_60_days": format_action_items(["Ação 1", "Ação 2", "Ação 3"]),
        "action_90_days": format_action_items(["Ação 1", "Ação 2", "Ação 3"]),
        "hiring_priorities": format_ordered_list(["Contratação 1", "Contratação 2"]),
        "recommended_books": format_list_items(["Livro 1", "Livro 2"]),
        "recommended_practices": format_list_items(["Prática 1", "Prática 2"]),
        "recommended_tools": format_list_items(["Ferramenta 1", "Ferramenta 2"]),
    }


def format_action_items(items: list[str]) -> str:
    """Formata items de ação."""
    return "".join([f'<div class="action-item">{item}</div>' for item in items])


# ===== UTILITIES =====

def get_level_class(score: float) -> str:
    """Retorna classe CSS baseada no nível do score."""
    if score >= 7:
        return "success-box"
    elif score >= 4:
        return "info-box"
    else:
        return "warning-box"


def format_list_items(items: list[str]) -> str:
    """Formata lista de items como HTML <li>."""
    return "\n".join([f"<li>{item}</li>" for item in items])


def format_ordered_list(items: list[str]) -> str:
    """Formata lista ordenada."""
    return "\n".join([f"<li>{item}</li>" for item in items])
