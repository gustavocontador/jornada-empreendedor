"""
Exemplo de uso da engine de relatórios.

Este script demonstra como gerar relatórios simplificados e completos.
"""
import os
import sys
from pathlib import Path

# Adicionar o diretório raiz ao path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.services.reports.report_generator import ReportGenerator


def example_generate_simplified_report():
    """Exemplo de geração de relatório simplificado."""
    db: Session = SessionLocal()

    try:
        generator = ReportGenerator(db)

        # IDs de exemplo - substitua pelos IDs reais do seu banco
        result_id = "seu-result-uuid-aqui"
        user_id = "seu-user-uuid-aqui"

        print("Gerando relatório simplificado...")
        pdf_path = generator.generate_simplified_report(result_id, user_id)
        print(f"✓ Relatório simplificado gerado: {pdf_path}")

        return pdf_path

    except Exception as e:
        print(f"✗ Erro ao gerar relatório: {e}")
        raise
    finally:
        db.close()


def example_generate_complete_report():
    """Exemplo de geração de relatório completo."""
    db: Session = SessionLocal()

    try:
        generator = ReportGenerator(db)

        # IDs de exemplo - substitua pelos IDs reais do seu banco
        result_id = "seu-result-uuid-aqui"
        user_id = "seu-user-uuid-aqui"

        print("Gerando relatório completo...")
        pdf_path = generator.generate_complete_report(result_id, user_id)
        print(f"✓ Relatório completo gerado: {pdf_path}")

        return pdf_path

    except Exception as e:
        print(f"✗ Erro ao gerar relatório: {e}")
        raise
    finally:
        db.close()


def example_with_mock_data():
    """
    Exemplo usando dados mockados (sem banco de dados).
    Útil para testar a engine sem precisar de dados reais.
    """
    from app.services.reports.chart_generator import (
        generate_disc_chart,
        generate_spiral_chart,
        generate_paei_chart,
        generate_enneagram_diagram,
        generate_valores_chart
    )

    print("\n=== TESTE DE GERAÇÃO DE GRÁFICOS ===\n")

    # Dados mockados
    disc_scores = {"D": 7.5, "I": 8.2, "S": 4.1, "C": 5.8}
    spiral_scores = {
        "beige": 2.1,
        "purple": 3.5,
        "red": 5.8,
        "blue": 6.2,
        "orange": 8.5,
        "green": 5.5,
        "yellow": 3.2,
        "turquoise": 1.5
    }
    paei_scores = {"P": 8.1, "A": 3.2, "E": 7.5, "I": 4.1}
    enneagram_type = 3
    valores_scores = {
        "Inovação": 8.5,
        "Resultado": 8.2,
        "Crescimento": 7.8,
        "Qualidade": 6.5,
        "Ética": 6.2
    }

    # Gerar gráficos
    print("1. Gerando gráfico DISC...")
    disc_chart = generate_disc_chart(disc_scores)
    print(f"   ✓ DISC chart: {len(disc_chart)} bytes (base64)")

    print("\n2. Gerando gráfico Espiral Dinâmica...")
    spiral_chart = generate_spiral_chart(spiral_scores)
    print(f"   ✓ Spiral chart: {len(spiral_chart)} bytes (base64)")

    print("\n3. Gerando gráfico PAEI...")
    paei_chart = generate_paei_chart(paei_scores)
    print(f"   ✓ PAEI chart: {len(paei_chart)} bytes (base64)")

    print("\n4. Gerando diagrama Eneagrama...")
    enneagram_chart = generate_enneagram_diagram(enneagram_type)
    print(f"   ✓ Enneagram chart: {len(enneagram_chart)} bytes (base64)")

    print("\n5. Gerando gráfico de Valores...")
    valores_chart = generate_valores_chart(valores_scores, top_n=5)
    print(f"   ✓ Valores chart: {len(valores_chart)} bytes (base64)")

    print("\n✓ Todos os gráficos foram gerados com sucesso!")
    print("\nDica: Os gráficos estão em formato base64. Para visualizar:")
    print("  1. Copie o conteúdo base64")
    print("  2. Cole em um arquivo HTML dentro de <img src='...' />")
    print("  3. Abra o HTML no navegador")


def main():
    """Função principal."""
    print("=" * 60)
    print("  ENGINE DE RELATÓRIOS - JORNADA DO EMPREENDEDOR")
    print("=" * 60)

    while True:
        print("\n\nOpções:")
        print("1. Gerar relatório simplificado (com banco de dados)")
        print("2. Gerar relatório completo (com banco de dados)")
        print("3. Testar geração de gráficos (mock)")
        print("4. Sair")

        choice = input("\nEscolha uma opção: ").strip()

        if choice == "1":
            example_generate_simplified_report()
        elif choice == "2":
            example_generate_complete_report()
        elif choice == "3":
            example_with_mock_data()
        elif choice == "4":
            print("\nAté logo!")
            break
        else:
            print("\n✗ Opção inválida. Tente novamente.")


if __name__ == "__main__":
    # Se quiser testar apenas os gráficos sem banco:
    example_with_mock_data()

    # Para usar o menu interativo:
    # main()
