import { useState, useCallback, useEffect } from 'react';

interface HistoryItem {
  id: number;
  text: string;
  result: any;
  timestamp: string;
}

interface HistoryStats {
  total_analyses: number;
  toxic_count: number;
  safe_count: number;
  average_score: number;
}

interface UseHistoryReturn {
  history: HistoryItem[];
  stats: HistoryStats | null;
  loading: boolean;
  error: string | null;
  loadHistory: () => Promise<void>;
  loadStats: () => Promise<void>;
  deleteItem: (id: number) => Promise<void>;
  clearHistory: () => Promise<void>;
}

export const useHistory = (): UseHistoryReturn => {
  const [history, setHistory] = useState<HistoryItem[]>([]);
  const [stats, setStats] = useState<HistoryStats | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const loadHistory = useCallback(async () => {
    setLoading(true);
    setError(null);

    try {
      const response = await fetch('http://127.0.0.1:8000/history');
      if (!response.ok) {
        throw new Error('Error cargando historial');
      }
      const data = await response.json();
      setHistory(data.history || []);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Error desconocido');
    } finally {
      setLoading(false);
    }
  }, []);

  const loadStats = useCallback(async () => {
    try {
      const response = await fetch('http://127.0.0.1:8000/history/stats');
      if (!response.ok) {
        throw new Error('Error cargando estadísticas');
      }
      const data = await response.json();
      setStats(data);
    } catch (err) {
      console.error('Error cargando estadísticas:', err);
    }
  }, []);

  const deleteItem = useCallback(async (id: number) => {
    try {
      const response = await fetch(`http://127.0.0.1:8000/history/${id}`, {
        method: 'DELETE',
      });
      if (!response.ok) {
        throw new Error('Error eliminando elemento');
      }
      // Recargar historial después de eliminar
      await loadHistory();
      await loadStats();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Error desconocido');
    }
  }, [loadHistory, loadStats]);

  const clearHistory = useCallback(async () => {
    try {
      const response = await fetch('http://127.0.0.1:8000/history', {
        method: 'DELETE',
      });
      if (!response.ok) {
        throw new Error('Error limpiando historial');
      }
      setHistory([]);
      setStats(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Error desconocido');
    }
  }, []);

  // Cargar historial al montar el componente
  useEffect(() => {
    loadHistory();
    loadStats();
  }, [loadHistory, loadStats]);

  return {
    history,
    stats,
    loading,
    error,
    loadHistory,
    loadStats,
    deleteItem,
    clearHistory,
  };
};
