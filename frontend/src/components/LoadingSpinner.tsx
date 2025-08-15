interface LoadingSpinnerProps {
  message?: string;
  size?: 'sm' | 'md' | 'lg';
}

export function LoadingSpinner({ 
  message = "Analizando texto...", 
  size = 'md' 
}: LoadingSpinnerProps) {
  const sizeClasses = {
    sm: 'w-6 h-6',
    md: 'w-8 h-8',
    lg: 'w-12 h-12'
  };

  const textSizes = {
    sm: 'text-sm',
    md: 'text-base',
    lg: 'text-lg'
  };

  return (
    <div className="flex flex-col items-center justify-center p-8 space-y-4">
      {/* Spinner principal */}
      <div className="relative">
        <div className={`${sizeClasses[size]} border-4 border-gray-200 rounded-full animate-pulse`}></div>
        <div 
          className={`${sizeClasses[size]} border-4 border-blue-500 border-t-transparent rounded-full absolute top-0 left-0 animate-spin`}
        ></div>
        
        {/* Punto central */}
        <div className={`${sizeClasses[size]} bg-blue-500 rounded-full absolute top-0 left-0 flex items-center justify-center`}>
          <div className="w-1 h-1 bg-white rounded-full animate-ping"></div>
        </div>
      </div>

      {/* Mensaje de carga */}
      <div className="text-center space-y-2">
        <p className={`${textSizes[size]} font-medium text-gray-700`}>
          {message}
        </p>
        <p className="text-sm text-gray-500">
          Esto puede tomar unos segundos...
        </p>
      </div>

      {/* Indicador de progreso animado */}
      <div className="flex space-x-1">
        <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
        <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
        <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
      </div>

              {/* Additional information */}
      <div className="text-xs text-gray-400 text-center max-w-xs">
        <p>Analyzing content with advanced AI</p>
        <p>Detecting toxicity patterns</p>
      </div>
    </div>
  );
}
