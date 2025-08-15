import { useState, useCallback } from 'react';

interface ToxicityResult {
  toxic: boolean;
  score: number;
  toxicity_percentage: number;
  category: string | null;
  labels: string[];
  text_length: number;
  keywords_found: number;
  response_time_ms: number;
  timestamp: string;
  model_used: string;
}

interface UseToxicityAnalysisReturn {
  result: ToxicityResult | null;
  loading: boolean;
  error: string | null;
  analyzeText: (text: string) => Promise<void>;
  clearResult: () => void;
}

export const useToxicityAnalysis = (): UseToxicityAnalysisReturn => {
  const [result, setResult] = useState<ToxicityResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const analyzeText = useCallback(async (text: string) => {
    if (!text.trim()) {
      setError('Por favor ingresa un texto para analizar');
      return;
    }

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      console.log('🚀 Enviando solicitud a:', 'http://127.0.0.1:8000/analyze');
      console.log('📝 Texto a analizar:', text.trim());

      const response = await fetch('http://127.0.0.1:8000/analyze', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: text.trim() }),
      });

      console.log(
        '📡 Respuesta recibida:',
        response.status,
        response.statusText
      );
      console.log(
        '📋 Headers de respuesta:',
        Object.fromEntries(response.headers.entries())
      );

      if (!response.ok) {
        const errorData = await response
          .json()
          .catch(() => ({ detail: 'Error desconocido del servidor' }));
        console.error('❌ Error del servidor:', errorData);
        throw new Error(
          errorData.detail || `Error del servidor: ${response.status}`
        );
      }

      const data = await response.json();
      console.log('✅ Datos recibidos exitosamente:', data);
      setResult(data);
    } catch (err) {
      console.error('💥 Error en análisis:', err);

      if (err instanceof Error) {
        const errorMessage = err.message;
        console.log('🔍 Tipo de error:', errorMessage);

        if (errorMessage.includes('Failed to fetch')) {
          setError(
            '❌ No se pudo conectar al servidor. Verifica que el backend esté ejecutándose en http://127.0.0.1:8000'
          );
        } else if (errorMessage.includes('NetworkError')) {
          setError('🌐 Error de red. Verifica tu conexión a internet.');
        } else if (errorMessage.includes('TypeError')) {
          setError('🔌 Error de conexión. El servidor no está respondiendo.');
        } else {
          setError(`⚠️ ${errorMessage}`);
        }
      } else {
        console.error('❓ Error desconocido:', err);
        setError('❓ Error desconocido durante el análisis');
      }
    } finally {
      setLoading(false);
    }
  }, []);

  const clearResult = useCallback(() => {
    setResult(null);
    setError(null);
  }, []);

  return {
    result,
    loading,
    error,
    analyzeText,
    clearResult,
  };
};
