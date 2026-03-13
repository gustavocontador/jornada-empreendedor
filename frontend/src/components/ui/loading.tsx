export function Loading({ message = 'Carregando...' }: { message?: string }) {
  return (
    <div className="min-h-screen flex items-center justify-center">
      <div className="text-center space-y-4">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto"></div>
        <p className="text-muted-foreground">{message}</p>
      </div>
    </div>
  )
}

export function LoadingSpinner({ size = 'default' }: { size?: 'small' | 'default' | 'large' }) {
  const sizeClasses = {
    small: 'h-4 w-4 border',
    default: 'h-8 w-8 border-2',
    large: 'h-12 w-12 border-2',
  }

  return <div className={`animate-spin rounded-full border-b-primary ${sizeClasses[size]}`}></div>
}
