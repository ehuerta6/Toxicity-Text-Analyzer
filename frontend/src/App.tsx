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
    <div className='min-h-screen bg-gray-50 py-8'>
      <div className='max-w-4xl mx-auto px-4'>
        {/* Header */}
        <div className='text-center mb-8'>
          <h1 className='text-4xl font-bold text-gray-900 mb-2'>ToxiGuard</h1>
          <p className='text-lg text-gray-600'>
            Detecta comentarios tóxicos en tiempo real
          </p>
        </div>

        {/* Formulario principal */}
        <div className='card mb-6'>
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
                className='input min-h-[120px] resize-none'
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
                    className='btn-secondary disabled:opacity-50 disabled:cursor-not-allowed'
                  >
                    Limpiar
                  </button>
                  <button
                    onClick={handleAnalyze}
                    disabled={isLoading || !text.trim()}
                    className='btn-primary disabled:opacity-50 disabled:cursor-not-allowed'
                  >
                    {isLoading ? (
                      <div className='flex items-center space-x-2'>
                        <div className='w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin'></div>
                        <span>Analizando...</span>
                      </div>
                    ) : (
                      'Analizar'
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
          <div className='card text-center text-gray-500'>
            <div className='w-16 h-16 mx-auto mb-4 text-gray-300'>
              <svg fill='currentColor' viewBox='0 0 20 20'>
                <path
                  fillRule='evenodd'
                  d='M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z'
                  clipRule='evenodd'
                />
              </svg>
            </div>
            <p>Ingresa un texto y haz clic en "Analizar" para comenzar</p>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
