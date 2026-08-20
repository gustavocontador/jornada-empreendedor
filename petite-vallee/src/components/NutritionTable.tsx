import type { NutritionFacts } from "@/data/products";

interface NutritionTableProps {
  nutrition: NutritionFacts;
}

function formatNumber(value: number): string {
  return value.toLocaleString("pt-BR", {
    minimumFractionDigits: 0,
    maximumFractionDigits: 1,
  });
}

/**
 * Tabela nutricional montada em HTML no estilo de rótulo
 * brasileiro, com os valores oficiais fornecidos pela marca.
 * Exibe somente os campos fornecidos — sem %VD calculado nem
 * valores inventados.
 */
export function NutritionTable({ nutrition }: NutritionTableProps) {
  const rows: Array<[string, string]> = [
    ["Valor energético", `${formatNumber(nutrition.energyKcal)} kcal`],
    ["Carboidratos", `${formatNumber(nutrition.carbsG)} g`],
    ["Proteínas", `${formatNumber(nutrition.proteinG)} g`],
    ["Gorduras totais", `${formatNumber(nutrition.totalFatG)} g`],
    ["Fibra alimentar", `${formatNumber(nutrition.fiberG)} g`],
  ];

  return (
    <table className="nutrition-table">
      <caption className="nutrition-table__caption">
        Informação Nutricional
        <span className="nutrition-table__portion">
          Porção de {nutrition.portionLabel}
        </span>
      </caption>
      <thead className="visually-hidden">
        <tr>
          <th scope="col">Item</th>
          <th scope="col">Quantidade por porção</th>
        </tr>
      </thead>
      <tbody>
        {rows.map(([label, value]) => (
          <tr key={label}>
            <th scope="row">{label}</th>
            <td>{value}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
