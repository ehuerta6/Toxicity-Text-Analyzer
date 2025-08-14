import { AnalyzeResponse } from '../lib/api';

interface ToxicityResultProps {
  result: AnalyzeResponse | null;
  isLoading: boolean;
  error: string | null;
}

export function ToxicityResult({
  result,
  isLoading,
  error,
}: ToxicityResultProps) {
  if (isLoading) {
    return (
      <div className='card animate-pulse'>
        <div className='flex items-center space-x-2'>
          <div className='w-4 h-4 bg-gray-300 rounded-full animate-pulse'></div>
          <div className='text-gray-500'>Analizando texto...</div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className='card border-toxic-200 bg-toxic-50'>
        <div className='flex items-center space-x-2'>
          <div className='w-5 h-5 text-toxic-500'>
            <svg fill='currentColor' viewBox='0 0 20 20'>
              <path
                fillRule='evenodd'
                d='M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z'
                clipRule='evenodd'
              />
            </svg>
          </div>
          <div className='text-toxic-800 font-medium'>Error</div>
        </div>
        <p className='text-toxic-700 mt-2'>{error}</p>
      </div>
    );
  }

  if (!result) {
    return null;
  }

  const scorePercentage = Math.round(result.score * 100);
  const isToxic = result.toxic;

  return (
    <div className='card animate-fade-in'>
      <div className='space-y-4'>
        {/* Estado principal */}
        <div className='text-center'>
          <div
            className={`inline-flex items-center px-4 py-2 rounded-full text-lg font-semibold ${
              isToxic
                ? 'bg-toxic-100 text-toxic-800 border border-toxic-200'
                : 'bg-safe-100 text-safe-800 border border-safe-200'
            }`}
          >
            <div
              className={`w-3 h-3 rounded-full mr-2 ${
                isToxic ? 'bg-toxic-500' : 'bg-safe-500'
              }`}
            ></div>
            {isToxic ? 'TÓXICO' : 'NO TÓXICO'}
          </div>
        </div>

        {/* Score de toxicidad */}
        <div className='text-center'>
          <div className='text-2xl font-bold text-gray-900'>
            {scorePercentage}%
          </div>
          <div className='text-sm text-gray-500'>Score de toxicidad</div>

          {/* Barra de progreso */}
          <div className='mt-2 w-full bg-gray-200 rounded-full h-2'>
            <div
              className={`h-2 rounded-full transition-all duration-500 ${
                isToxic ? 'bg-toxic-500' : 'bg-safe-500'
              }`}
              style={{ width: `${scorePercentage}%` }}
            ></div>
          </div>
        </div>

        {/* Detalles adicionales */}
        <div className='grid grid-cols-2 gap-4 text-sm'>
          <div className='text-center p-3 bg-gray-50 rounded-lg'>
            <div className='font-semibold text-gray-900'>
              {result.text_length}
            </div>
            <div className='text-gray-500'>Caracteres</div>
          </div>
          <div className='text-center p-3 bg-gray-50 rounded-lg'>
            <div className='font-semibold text-gray-900'>
              {result.keywords_found}
            </div>
            <div className='text-gray-500'>Palabras clave</div>
          </div>
        </div>

        {/* Etiquetas */}
        {result.labels.length > 0 && (
          <div className='text-center'>
            <div className='text-sm text-gray-500 mb-2'>
              Categorías detectadas
            </div>
            <div className='flex flex-wrap justify-center gap-2'>
              {result.labels.map((label, index) => (
                <span
                  key={index}
                  className='badge-toxic px-3 py-1 text-xs font-medium'
                >
                  {label}
                </span>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
