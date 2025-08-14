import { AnalyzeResponse } from '../lib/api';
import { ToxicityGauge } from './ToxicityGauge';
import { ResultExplanation } from './ResultExplanation';
import { LoadingSpinner } from './LoadingSpinner';

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
      <div className='card'>
        <LoadingSpinner 
          message="Analizando toxicidad del texto..." 
          size="lg" 
        />
      </div>
    );
  }

  if (error) {
    return (
      <div className='card border-red-200 bg-red-50'>
        <div className='flex items-center space-x-3'>
          <div className='w-8 h-8 text-red-500'>
            <svg fill='currentColor' viewBox='0 0 20 20'>
              <path
                fillRule='evenodd'
                d='M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z'
                clipRule='evenodd'
              />
            </svg>
          </div>
          <div>
            <div className='text-red-800 font-semibold text-lg'>Error en el análisis</div>
            <p className='text-red-700 mt-1'>{error}</p>
          </div>
        </div>
      </div>
    );
  }

  if (!result) {
    return null;
  }

  const isToxic = result.toxic;
  const toxicityPercentage = result.toxicity_percentage;

  return (
    <div className='space-y-6'>
      {/* Gauge principal */}
      <div className='card text-center'>
        <h3 className='text-xl font-bold text-gray-900 mb-6'>
          Resultado del Análisis
        </h3>
        
        <div className='flex justify-center mb-6'>
          <ToxicityGauge 
            percentage={toxicityPercentage} 
            size={220}
            strokeWidth={14}
          />
        </div>

        {/* Estado principal */}
        <div className='mb-6'>
          <div
            className={`inline-flex items-center px-6 py-3 rounded-full text-xl font-bold ${
              isToxic
                ? 'bg-red-100 text-red-800 border-2 border-red-200'
                : 'bg-green-100 text-green-800 border-2 border-green-200'
            }`}
          >
            <div
              className={`w-4 h-4 rounded-full mr-3 ${
                isToxic ? 'bg-red-500' : 'bg-green-500'
              }`}
            ></div>
            {isToxic ? 'CONTENIDO TÓXICO' : 'CONTENIDO SEGURO'}
          </div>
        </div>

        {/* Métricas rápidas */}
        <div className='grid grid-cols-3 gap-4 max-w-md mx-auto'>
          <div className='text-center p-3 bg-gray-50 rounded-lg'>
            <div className='text-lg font-bold text-gray-900'>
              {result.text_length}
            </div>
            <div className='text-xs text-gray-500'>Caracteres</div>
          </div>
          <div className='text-center p-3 bg-gray-50 rounded-lg'>
            <div className='text-lg font-bold text-gray-900'>
              {result.keywords_found}
            </div>
            <div className='text-xs text-gray-500'>Palabras clave</div>
          </div>
          <div className='text-center p-3 bg-gray-50 rounded-lg'>
            <div className='text-lg font-bold text-gray-900'>
              {result.response_time_ms}ms
            </div>
            <div className='text-xs text-gray-500'>Respuesta</div>
          </div>
        </div>
      </div>

      {/* Explicación detallada */}
      <ResultExplanation result={result} />

      {/* Información adicional */}
      <div className='card'>
        <h4 className='text-lg font-semibold text-gray-900 mb-4 text-center'>
          Información Técnica
        </h4>
        
        <div className='grid grid-cols-2 md:grid-cols-4 gap-4'>
          <div className='text-center p-3 bg-blue-50 rounded-lg border border-blue-100'>
            <div className='text-sm font-medium text-blue-900'>Score</div>
            <div className='text-lg font-bold text-blue-700'>
              {result.score.toFixed(3)}
            </div>
          </div>
          
          <div className='text-center p-3 bg-purple-50 rounded-lg border border-purple-100'>
            <div className='text-sm font-medium text-purple-900'>Porcentaje</div>
            <div className='text-lg font-bold text-purple-700'>
              {toxicityPercentage.toFixed(1)}%
            </div>
          </div>
          
          <div className='text-center p-3 bg-indigo-50 rounded-lg border border-indigo-100'>
            <div className='text-sm font-medium text-indigo-900'>Modelo</div>
            <div className='text-sm font-bold text-indigo-700 truncate'>
              {result.model_used}
            </div>
          </div>
          
          <div className='text-center p-3 bg-teal-50 rounded-lg border border-teal-100'>
            <div className='text-sm font-medium text-teal-900'>Timestamp</div>
            <div className='text-xs font-bold text-teal-700'>
              {new Date(result.timestamp).toLocaleTimeString()}
            </div>
          </div>
        </div>

        {/* Etiquetas */}
        {result.labels.length > 0 && (
          <div className='mt-6 text-center'>
            <div className='text-sm text-gray-600 mb-3'>
              Etiquetas de análisis:
            </div>
            <div className='flex flex-wrap justify-center gap-2'>
              {result.labels.map((label, index) => (
                <span
                  key={index}
                  className='inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-indigo-100 text-indigo-800 border border-indigo-200'
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
