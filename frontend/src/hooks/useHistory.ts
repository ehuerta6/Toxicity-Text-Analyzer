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
      console.log('Cargando historial desde:', 'http://127.0.0.1:8000/history');

      const response = await fetch('http://127.0.0.1:8000/history');
      console.log(
        'Respuesta del historial:',
        response.status,
        response.statusText
      );

      if (!response.ok) {
        throw new Error(`Error cargando historial: ${response.status}`);
      }

      const data = await response.json();
      console.log('Historial recibido:', data);
      setHistory(data.history || []);
    } catch (err) {
      console.error('Error cargando historial:', err);

      if (err instanceof Error) {
        if (err.message.includes('Failed to fetch')) {
          setError('No se pudo conectar al servidor para cargar el historial');
        } else {
          setError(err.message);
        }
      } else {
        setError('Error desconocido cargando historial');
      }
    } finally {
      setLoading(false);
    }
  }, []);

  const loadStats = useCallback(async () => {
    try {
      console.log(
        'Cargando estadísticas desde:',
        'http://127.0.0.1:8000/history/stats'
      );

      const response = await fetch('http://127.0.0.1:8000/history/stats');
      console.log(
        'Respuesta de estadísticas:',
        response.status,
        response.statusText
      );

      if (!response.ok) {
        console.warn('Error cargando estadísticas:', response.status);
        return;
      }

      const data = await response.json();
      console.log('Estadísticas recibidas:', data);
      setStats(data);
    } catch (err) {
      console.error('Error cargando estadísticas:', err);
      // No establecemos error aquí para no bloquear la UI
    }
  }, []);

  const deleteItem = useCallback(
    async (id: number) => {
      try {
        console.log('Eliminando elemento:', id);

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
        console.error('Error eliminando elemento:', err);
        setError(err instanceof Error ? err.message : 'Error desconocido');
      }
    },
    [loadHistory, loadStats]
  );

  const clearHistory = useCallback(async () => {
    try {
      console.log('Limpiando historial completo');

      const response = await fetch('http://127.0.0.1:8000/history', {
        method: 'DELETE',
      });

      if (!response.ok) {
        throw new Error('Error limpiando historial');
      }

      setHistory([]);
      setStats(null);
    } catch (err) {
      console.error('Error limpiando historial:', err);
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
