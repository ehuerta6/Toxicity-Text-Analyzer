import { useState, useCallback } from 'react';

export interface ToxicityResult {
  text: string;
  is_toxic: boolean;
  toxicity_percentage: number;
  toxicity_category: string;
  confidence: number;
  detected_categories: string[];
  word_count: number;
  response_time_ms: number;
  timestamp: string;
  model_used: string;
  classification_technique: string;
  explanations: Record<string, string>;
  severity_breakdown?: Record<
    string,
    {
      avg_severity: number;
      match_count: number;
      final_score: number;
    }
  >;
  ultra_sensitive_analysis?: boolean;
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
      const response = await fetch('http://127.0.0.1:8000/analyze', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: text.trim() }),
      });

      if (!response.ok) {
        const errorData = await response
          .json()
          .catch(() => ({ detail: 'Error desconocido del servidor' }));
        throw new Error(
          errorData.detail || `Error del servidor: ${response.status}`
        );
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      if (err instanceof Error) {
        const errorMessage = err.message;

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
