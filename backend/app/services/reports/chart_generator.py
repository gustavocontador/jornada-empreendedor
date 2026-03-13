"""
Gerador de gráficos para relatórios PDF.
Usa Plotly para criar visualizações profissionais e converte para base64.
"""
import plotly.graph_objects as go
import plotly.express as px
from typing import Dict
import base64
from io import BytesIO

# Cores oficiais dos frameworks
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

DISC_COLORS = {
    'D': '#FF4444',
    'I': '#FFD700',
    'S': '#4CAF50',
    'C': '#2196F3'
}

PAEI_COLORS = {
    'P': '#8B4513',
    'A': '#2F4F4F',
    'E': '#FF6347',
    'I': '#4682B4'
}


def generate_disc_chart(disc_scores: Dict[str, float]) -> str:
    """
    Gera gráfico DISC em formato de barras horizontais.
    Retorna imagem em base64 para embedding no HTML.
    """
    dimensions = ['D', 'I', 'S', 'C']
    values = [disc_scores.get(dim, 0) for dim in dimensions]
    colors = [DISC_COLORS[dim] for dim in dimensions]

    labels = {
        'D': 'Dominância',
        'I': 'Influência',
        'S': 'Estabilidade',
        'C': 'Conformidade'
    }

    fig = go.Figure()

    fig.add_trace(go.Bar(
        y=[labels[dim] for dim in dimensions],
        x=values,
        orientation='h',
        marker=dict(
            color=colors,
            line=dict(color='rgba(0,0,0,0.5)', width=1)
        ),
        text=[f'{v:.1f}' for v in values],
        textposition='outside',
        textfont=dict(size=14, color='#333'),
        hovertemplate='<b>%{y}</b><br>Score: %{x:.1f}<extra></extra>'
    ))

    fig.update_layout(
        title={
            'text': 'Perfil DISC',
            'font': {'size': 24, 'color': '#1a1a1a', 'family': 'Arial Black'},
            'x': 0.5,
            'xanchor': 'center'
        },
        xaxis=dict(
            title='Score',
            range=[0, 10],
            gridcolor='#e0e0e0',
            showgrid=True,
            zeroline=True,
            zerolinecolor='#999',
            tickfont=dict(size=12)
        ),
        yaxis=dict(
            tickfont=dict(size=14, color='#333')
        ),
        plot_bgcolor='white',
        paper_bgcolor='white',
        height=400,
        margin=dict(l=150, r=50, t=80, b=60),
        font=dict(family='Arial, sans-serif')
    )

    # Converter para base64
    img_bytes = fig.to_image(format="png", width=800, height=400, scale=2)
    img_base64 = base64.b64encode(img_bytes).decode('utf-8')

    return f"data:image/png;base64,{img_base64}"


def generate_spiral_chart(spiral_scores: Dict[str, float]) -> str:
    """
    Gera gráfico radar da Espiral Dinâmica com cores corretas.
    Retorna imagem em base64.
    """
    colors_order = ['beige', 'purple', 'red', 'blue', 'orange', 'green', 'yellow', 'turquoise']

    labels = {
        'beige': 'Beige<br>Sobrevivência',
        'purple': 'Roxo<br>Tribal',
        'red': 'Vermelho<br>Poder',
        'blue': 'Azul<br>Ordem',
        'orange': 'Laranja<br>Sucesso',
        'green': 'Verde<br>Comunidade',
        'yellow': 'Amarelo<br>Sistêmico',
        'turquoise': 'Turquesa<br>Holístico'
    }

    values = [spiral_scores.get(color, 0) for color in colors_order]

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=[labels[c] for c in colors_order],
        fill='toself',
        fillcolor='rgba(100, 149, 237, 0.3)',
        line=dict(color='#6495ED', width=3),
        marker=dict(size=10, color=[SPIRAL_COLORS[c] for c in colors_order]),
        hovertemplate='<b>%{theta}</b><br>Score: %{r:.1f}<extra></extra>'
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 10],
                showline=True,
                linecolor='#ccc',
                gridcolor='#e0e0e0',
                tickfont=dict(size=12)
            ),
            angularaxis=dict(
                tickfont=dict(size=13, color='#333')
            ),
            bgcolor='white'
        ),
        title={
            'text': 'Espiral Dinâmica',
            'font': {'size': 24, 'color': '#1a1a1a', 'family': 'Arial Black'},
            'x': 0.5,
            'xanchor': 'center'
        },
        showlegend=False,
        height=500,
        paper_bgcolor='white',
        font=dict(family='Arial, sans-serif')
    )

    # Converter para base64
    img_bytes = fig.to_image(format="png", width=700, height=500, scale=2)
    img_base64 = base64.b64encode(img_bytes).decode('utf-8')

    return f"data:image/png;base64,{img_base64}"


def generate_paei_chart(paei_scores: Dict[str, float]) -> str:
    """
    Gera gráfico radar PAEI (4 papéis organizacionais).
    Retorna imagem em base64.
    """
    dimensions = ['P', 'A', 'E', 'I']

    labels = {
        'P': 'Produtor<br>(Resultados)',
        'A': 'Administrador<br>(Processos)',
        'E': 'Empreendedor<br>(Inovação)',
        'I': 'Integrador<br>(Pessoas)'
    }

    values = [paei_scores.get(dim, 0) for dim in dimensions]

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=[labels[dim] for dim in dimensions],
        fill='toself',
        fillcolor='rgba(255, 140, 0, 0.3)',
        line=dict(color='#FF8C00', width=3),
        marker=dict(size=12, color=[PAEI_COLORS[dim] for dim in dimensions]),
        hovertemplate='<b>%{theta}</b><br>Score: %{r:.1f}<extra></extra>'
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 10],
                showline=True,
                linecolor='#ccc',
                gridcolor='#e0e0e0',
                tickfont=dict(size=12)
            ),
            angularaxis=dict(
                tickfont=dict(size=13, color='#333')
            ),
            bgcolor='white'
        ),
        title={
            'text': 'PAEI - Papéis de Gestão',
            'font': {'size': 24, 'color': '#1a1a1a', 'family': 'Arial Black'},
            'x': 0.5,
            'xanchor': 'center'
        },
        showlegend=False,
        height=450,
        paper_bgcolor='white',
        font=dict(family='Arial, sans-serif')
    )

    # Converter para base64
    img_bytes = fig.to_image(format="png", width=700, height=450, scale=2)
    img_base64 = base64.b64encode(img_bytes).decode('utf-8')

    return f"data:image/png;base64,{img_base64}"


def generate_enneagram_diagram(enneagram_type: int, wing: str = None) -> str:
    """
    Gera diagrama do Eneagrama destacando o tipo do usuário.
    Retorna imagem em base64.
    """
    import numpy as np

    # Posições dos 9 tipos no círculo (começando do topo, sentido horário)
    angles = np.linspace(0, 2 * np.pi, 10)[:-1] + np.pi/2  # Começa em cima

    types_positions = {}
    for i in range(1, 10):
        x = np.cos(angles[i-1])
        y = np.sin(angles[i-1])
        types_positions[i] = (x, y)

    fig = go.Figure()

    # Desenhar o círculo
    circle_angles = np.linspace(0, 2 * np.pi, 100)
    circle_x = np.cos(circle_angles)
    circle_y = np.sin(circle_angles)

    fig.add_trace(go.Scatter(
        x=circle_x,
        y=circle_y,
        mode='lines',
        line=dict(color='#ccc', width=2),
        showlegend=False,
        hoverinfo='skip'
    ))

    # Desenhar as linhas de conexão (triângulo e hexágono interno)
    # Triângulo: 3-6-9
    triangle_types = [3, 6, 9, 3]
    triangle_x = [types_positions[t][0] for t in triangle_types]
    triangle_y = [types_positions[t][1] for t in triangle_types]

    fig.add_trace(go.Scatter(
        x=triangle_x,
        y=triangle_y,
        mode='lines',
        line=dict(color='#ddd', width=1.5),
        showlegend=False,
        hoverinfo='skip'
    ))

    # Hexágono: 1-4-2-8-5-7
    hexagon_types = [1, 4, 2, 8, 5, 7, 1]
    hexagon_x = [types_positions[t][0] for t in hexagon_types]
    hexagon_y = [types_positions[t][1] for t in hexagon_types]

    fig.add_trace(go.Scatter(
        x=hexagon_x,
        y=hexagon_y,
        mode='lines',
        line=dict(color='#ddd', width=1.5),
        showlegend=False,
        hoverinfo='skip'
    ))

    # Desenhar os pontos (tipos)
    type_names = {
        1: 'O Perfeccionista',
        2: 'O Ajudador',
        3: 'O Realizador',
        4: 'O Individualista',
        5: 'O Investigador',
        6: 'O Leal',
        7: 'O Entusiasta',
        8: 'O Desafiador',
        9: 'O Pacificador'
    }

    for t in range(1, 10):
        x, y = types_positions[t]
        is_user_type = (t == enneagram_type)

        fig.add_trace(go.Scatter(
            x=[x],
            y=[y],
            mode='markers+text',
            marker=dict(
                size=40 if is_user_type else 30,
                color='#FF6347' if is_user_type else '#6495ED',
                line=dict(color='#333' if is_user_type else '#888', width=2 if is_user_type else 1)
            ),
            text=str(t),
            textfont=dict(size=18 if is_user_type else 14, color='white', family='Arial Black'),
            textposition='middle center',
            name=type_names[t],
            hovertemplate=f'<b>Tipo {t}</b><br>{type_names[t]}<extra></extra>',
            showlegend=False
        ))

    fig.update_layout(
        title={
            'text': f'Eneagrama - Tipo {enneagram_type}<br><sub>{type_names[enneagram_type]}</sub>',
            'font': {'size': 24, 'color': '#1a1a1a', 'family': 'Arial Black'},
            'x': 0.5,
            'xanchor': 'center'
        },
        xaxis=dict(
            showgrid=False,
            showticklabels=False,
            zeroline=False,
            range=[-1.3, 1.3]
        ),
        yaxis=dict(
            showgrid=False,
            showticklabels=False,
            zeroline=False,
            scaleanchor='x',
            scaleratio=1,
            range=[-1.3, 1.3]
        ),
        plot_bgcolor='white',
        paper_bgcolor='white',
        height=500,
        width=500,
        font=dict(family='Arial, sans-serif')
    )

    # Converter para base64
    img_bytes = fig.to_image(format="png", width=500, height=500, scale=2)
    img_base64 = base64.b64encode(img_bytes).decode('utf-8')

    return f"data:image/png;base64,{img_base64}"


def generate_valores_chart(valores_scores: Dict[str, float], top_n: int = 5) -> str:
    """
    Gera gráfico de barras dos valores empresariais principais.
    Retorna imagem em base64.
    """
    # Ordenar valores por score
    sorted_valores = sorted(valores_scores.items(), key=lambda x: x[1], reverse=True)[:top_n]

    labels = [v[0] for v in sorted_valores]
    values = [v[1] for v in sorted_valores]

    # Gradiente de cores (do mais importante para menos)
    colors = ['#1a5490', '#2874a6', '#5499c7', '#7fb3d5', '#a9cce3'][:len(labels)]

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=labels,
        y=values,
        marker=dict(
            color=colors,
            line=dict(color='rgba(0,0,0,0.3)', width=1)
        ),
        text=[f'{v:.1f}' for v in values],
        textposition='outside',
        textfont=dict(size=14, color='#333'),
        hovertemplate='<b>%{x}</b><br>Score: %{y:.1f}<extra></extra>'
    ))

    fig.update_layout(
        title={
            'text': 'Valores Empresariais',
            'font': {'size': 24, 'color': '#1a1a1a', 'family': 'Arial Black'},
            'x': 0.5,
            'xanchor': 'center'
        },
        xaxis=dict(
            tickfont=dict(size=12, color='#333'),
            tickangle=-45
        ),
        yaxis=dict(
            title='Importância',
            range=[0, 10],
            gridcolor='#e0e0e0',
            showgrid=True,
            tickfont=dict(size=12)
        ),
        plot_bgcolor='white',
        paper_bgcolor='white',
        height=400,
        margin=dict(l=60, r=40, t=80, b=120),
        font=dict(family='Arial, sans-serif')
    )

    # Converter para base64
    img_bytes = fig.to_image(format="png", width=700, height=400, scale=2)
    img_base64 = base64.b64encode(img_bytes).decode('utf-8')

    return f"data:image/png;base64,{img_base64}"
