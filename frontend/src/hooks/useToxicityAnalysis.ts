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
      const response = await fetch('http://127.0.0.1:8000/analyze', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: text.trim() }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Error en el análisis');
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Error desconocido');
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
