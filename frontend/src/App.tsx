import { useState } from 'react';
import { analyze, type AnalyzeResponse } from './lib/api';
import { ToxicityResult } from './components/ToxicityResult';

function App() {
  const [text, setText] = useState('');
  const [result, setResult] = useState<AnalyzeResponse | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleAnalyze = async () => {
    if (!text.trim()) {
      setError('Por favor, ingresa algún texto para analizar');
      return;
    }

    setIsLoading(true);
    setError(null);
    setResult(null);

    try {
      const analysisResult = await analyze(text);
      setResult(analysisResult);
    } catch (err) {
      const errorMessage =
        err instanceof Error ? err.message : 'Error desconocido';
      setError(errorMessage);
    } finally {
      setIsLoading(false);
    }
  };

  const handleClear = () => {
    setText('');
    setResult(null);
    setError(null);
  };

  return (
    <div className='min-h-screen bg-gradient-to-br from-gray-50 to-blue-50 py-8'>
      <div className='max-w-4xl mx-auto px-4'>
        {/* Header */}
        <div className='text-center mb-8'>
          <h1 className='text-5xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent mb-3'>
            ToxiGuard
          </h1>
          <p className='text-xl text-gray-600'>
            Detecta comentarios tóxicos en tiempo real con IA avanzada
          </p>
          <p className='text-sm text-gray-500 mt-2'>
            Fase 3 - Enhanced API & Visual Results
          </p>
        </div>

        {/* Formulario principal */}
        <div className='card mb-6 shadow-lg border-0 bg-white/80 backdrop-blur-sm'>
          <div className='space-y-4'>
            <div>
              <label
                htmlFor='text-input'
                className='block text-sm font-medium text-gray-700 mb-2'
              >
                Ingresa el texto a analizar:
              </label>
              <textarea
                id='text-input'
                value={text}
                onChange={(e) => setText(e.target.value)}
                placeholder='Escribe aquí el comentario o texto que quieres analizar...'
                className='input min-h-[120px] resize-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500'
                disabled={isLoading}
              />
              <div className='flex justify-between items-center mt-2'>
                <span className='text-sm text-gray-500'>
                  {text.length} caracteres
                </span>
                <div className='space-x-2'>
                  <button
                    onClick={handleClear}
                    disabled={isLoading || !text}
                    className='btn-secondary disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-100'
                  >
                    Limpiar
                  </button>
                  <button
                    onClick={handleAnalyze}
                    disabled={isLoading || !text.trim()}
                    className='btn-primary disabled:opacity-50 disabled:cursor-not-allowed hover:bg-blue-600 transform hover:scale-105 transition-all duration-200'
                  >
                    {isLoading ? (
                      <div className='flex items-center space-x-2'>
                        <div className='w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin'></div>
                        <span>Analizando...</span>
                      </div>
                    ) : (
                      'Analizar Toxicidad'
                    )}
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Resultados */}
        <ToxicityResult result={result} isLoading={isLoading} error={error} />

        {/* Información adicional */}
        {!result && !isLoading && !error && (
          <div className='card text-center text-gray-500 bg-white/60 backdrop-blur-sm border-0 shadow-lg'>
            <div className='w-20 h-20 mx-auto mb-4 text-gray-300'>
              <svg fill='currentColor' viewBox='0 0 20 20'>
                <path
                  fillRule='evenodd'
                  d='M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z'
                  clipRule='evenodd'
                />
              </svg>
            </div>
            <p className='text-lg font-medium mb-2'>¿Listo para analizar?</p>
            <p className='text-gray-600'>
              Ingresa un texto y haz clic en "Analizar Toxicidad" para comenzar
            </p>
            <div className='mt-4 text-xs text-gray-400 space-y-1'>
              <p>✨ Análisis con IA avanzada</p>
              <p>🎯 Detección precisa de toxicidad</p>
              <p>📊 Resultados visuales detallados</p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
