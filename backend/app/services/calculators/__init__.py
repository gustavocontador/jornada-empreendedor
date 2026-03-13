"""
Calculators - Algoritmos de cálculo de scores psicométricos.

Este módulo contém os algoritmos para calcular scores de todos os frameworks:
- DISC: Dominância, Influência, Estabilidade, Conformidade
- Spiral Dynamics: 8 níveis de desenvolvimento de valores
- PAEI: Producer, Administrator, Entrepreneur, Integrator
- Enneagram: 9 tipos de personalidade e motivações
- Valores: 10 valores empresariais prioritários
- Arquetipos: Perfis de contratação preferidos
"""
from app.services.calculators.scoring_engine import ScoringEngine
from app.services.calculators.disc_calculator import calculate_disc
from app.services.calculators.spiral_calculator import calculate_spiral
from app.services.calculators.paei_calculator import calculate_paei
from app.services.calculators.enneagram_calculator import calculate_enneagram
from app.services.calculators.valores_calculator import calculate_valores
from app.services.calculators.arquetipos_calculator import calculate_arquetipos
from app.services.calculators.interpretations_generator import generate_interpretations

__all__ = [
    "ScoringEngine",
    "calculate_disc",
    "calculate_spiral",
    "calculate_paei",
    "calculate_enneagram",
    "calculate_valores",
    "calculate_arquetipos",
    "generate_interpretations",
]
