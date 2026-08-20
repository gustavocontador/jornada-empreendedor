interface LoadingStateProps {
  label?: string;
}

/** Indicador de carregamento acessível. */
export function LoadingState({ label = "Carregando…" }: LoadingStateProps) {
  return (
    <div className="loading-state" role="status">
      <span className="loading-state__spinner" aria-hidden="true" />
      <span>{label}</span>
    </div>
  );
}
