import React, { useState, useEffect } from 'react';
import {
  Chart as ChartJS,
  ArcElement,
  Tooltip,
  Legend,
  CategoryScale,
  LinearScale,
  BarElement,
} from 'chart.js';
import { Pie, Bar } from 'react-chartjs-2';

// Register Chart.js components
ChartJS.register(
  ArcElement,
  Tooltip,
  Legend,
  CategoryScale,
  LinearScale,
  BarElement
);

// Simple interface for the response
interface AnalysisResult {
  toxic: boolean;
  score: number;
  toxicity_percentage?: number;
  labels: string[];
  text_length: number;
  keywords_found: number;
  response_time_ms?: number;
  model_used?: string;
}

// Interface for history items
interface HistoryItem {
  id: number;
  text: string;
  toxic: boolean;
  score: number;
  toxicity_percentage?: number;
  category?: string;
  labels: string[];
  text_length: number;
  keywords_found: number;
  response_time_ms?: number;
  model_used?: string;
  timestamp: string;
  created_at: string;
}

// Interface for statistics
interface HistoryStats {
  total_analyses: number;
  toxic_analyses: number;
  safe_analyses: number;
  toxicity_rate: number;
  average_toxicity: number;
  categories: Record<string, number>;
  recent_analyses: number;
}

// Simple API function
async function analyzeText(text: string): Promise<AnalysisResult> {
  const response = await fetch('http://127.0.0.1:8000/analyze', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ text }),
  });

  if (!response.ok) {
    throw new Error(`Error ${response.status}: ${response.statusText}`);
  }

  return response.json();
}

// Function to get history
async function getHistory(limit: number = 50): Promise<HistoryItem[]> {
  const response = await fetch(`http://127.0.0.1:8000/history?limit=${limit}`);
  if (!response.ok) {
    throw new Error(`Error ${response.status}: ${response.statusText}`);
  }
  const data = await response.json();
  return data.history;
}

// Function to get statistics
async function getStats(): Promise<HistoryStats> {
  const response = await fetch('http://127.0.0.1:8000/history/stats');
  if (!response.ok) {
    throw new Error(`Error ${response.status}: ${response.statusText}`);
  }
  return response.json();
}

// Function to delete history item
async function deleteHistoryItem(id: number): Promise<void> {
  const response = await fetch(`http://127.0.0.1:8000/history/${id}`, {
    method: 'DELETE',
  });
  if (!response.ok) {
    throw new Error(`Error ${response.status}: ${response.statusText}`);
  }
}

// Pie Chart Component
function ToxicityPieChart({ stats }: { stats: HistoryStats }) {
  const data = {
    labels: ['Contenido Seguro', 'Contenido Tóxico'],
    datasets: [
      {
        data: [stats.safe_analyses, stats.toxic_analyses],
        backgroundColor: ['#10B981', '#EF4444'],
        borderColor: ['#059669', '#DC2626'],
        borderWidth: 2,
        hoverBackgroundColor: ['#34D399', '#F87171'],
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'bottom' as const,
        labels: {
          padding: 20,
          font: {
            size: 14,
            family: 'system-ui, -apple-system, "Segoe UI", sans-serif',
          },
        },
      },
      tooltip: {
        callbacks: {
          label: function (context: any) {
            // eslint-disable-line @typescript-eslint/no-explicit-any
            const label = context.label || '';
            const value = context.parsed;
            const total = stats.total_analyses;
            const percentage = ((value / total) * 100).toFixed(1);
            return `${label}: ${value} (${percentage}%)`;
          },
        },
      },
    },
  };

  return (
    <div style={{ height: '300px', width: '100%' }}>
      <Pie data={data} options={options} />
    </div>
  );
}

// Bar Chart Component for Toxicity Distribution
function ToxicityDistributionChart({ history }: { history: HistoryItem[] }) {
  // Create distribution ranges
  const ranges = [
    { label: '0-20%', min: 0, max: 20, color: '#10B981' },
    { label: '21-40%', min: 21, max: 40, color: '#84CC16' },
    { label: '41-60%', min: 41, max: 60, color: '#EAB308' },
    { label: '61-80%', min: 61, max: 80, color: '#F97316' },
    { label: '81-100%', min: 81, max: 100, color: '#EF4444' },
  ];

  const distribution = ranges.map((range) => {
    const count = history.filter((item) => {
      const percentage = item.toxicity_percentage || item.score * 100;
      return percentage >= range.min && percentage <= range.max;
    }).length;
    return { ...range, count };
  });

  const data = {
    labels: distribution.map((d) => d.label),
    datasets: [
      {
        label: 'Cantidad de Análisis',
        data: distribution.map((d) => d.count),
        backgroundColor: distribution.map((d) => d.color),
        borderColor: distribution.map((d) => d.color),
        borderWidth: 1,
        borderRadius: 4,
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: false,
      },
      tooltip: {
        callbacks: {
          title: function (context: any) {
            // eslint-disable-line @typescript-eslint/no-explicit-any
            return `Toxicidad ${context[0].label}`;
          },
          label: function (context: any) {
            // eslint-disable-line @typescript-eslint/no-explicit-any
            const value = context.parsed.y;
            const total = history.length;
            const percentage =
              total > 0 ? ((value / total) * 100).toFixed(1) : '0';
            return `${value} análisis (${percentage}%)`;
          },
        },
      },
    },
    scales: {
      y: {
        beginAtZero: true,
        ticks: {
          stepSize: 1,
        },
        title: {
          display: true,
          text: 'Cantidad de Análisis',
        },
      },
      x: {
        title: {
          display: true,
          text: 'Nivel de Toxicidad',
        },
      },
    },
  };

  return (
    <div style={{ height: '300px', width: '100%' }}>
      <Bar data={data} options={options} />
    </div>
  );
}

// Categories Distribution Chart
function CategoriesChart({ stats }: { stats: HistoryStats }) {
  const categories = Object.entries(stats.categories || {});

  if (categories.length === 0) {
    return (
      <div style={{ textAlign: 'center', padding: '2rem', color: '#6B7280' }}>
        <p>No hay categorías para mostrar</p>
      </div>
    );
  }

  const colors = ['#3B82F6', '#EF4444', '#F59E0B', '#10B981', '#8B5CF6'];

  const data = {
    labels: categories.map(
      ([category]) => category.charAt(0).toUpperCase() + category.slice(1)
    ),
    datasets: [
      {
        label: 'Detecciones por Categoría',
        data: categories.map(([, count]) => count),
        backgroundColor: categories.map(
          (_, index) => colors[index % colors.length]
        ),
        borderColor: categories.map(
          (_, index) => colors[index % colors.length]
        ),
        borderWidth: 1,
        borderRadius: 4,
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: false,
      },
      tooltip: {
        callbacks: {
          label: function (context: any) {
            // eslint-disable-line @typescript-eslint/no-explicit-any
            const value = context.parsed.y;
            const total = categories.reduce((sum, [, count]) => sum + count, 0);
            const percentage = ((value / total) * 100).toFixed(1);
            return `${value} detecciones (${percentage}%)`;
          },
        },
      },
    },
    scales: {
      y: {
        beginAtZero: true,
        ticks: {
          stepSize: 1,
        },
        title: {
          display: true,
          text: 'Cantidad de Detecciones',
        },
      },
      x: {
        title: {
          display: true,
          text: 'Categorías de Toxicidad',
        },
      },
    },
  };

  return (
    <div style={{ height: '300px', width: '100%' }}>
      <Bar data={data} options={options} />
    </div>
  );
}

// Simple circular gauge component
function ToxicityGauge({ percentage }: { percentage: number }) {
  const radius = 80;
  const circumference = radius * 2 * Math.PI;
  const strokeDashoffset = circumference - (percentage / 100) * circumference;

  const getColor = (percent: number) => {
    if (percent < 30) return '#10B981'; // Green
    if (percent < 70) return '#F59E0B'; // Yellow
    return '#EF4444'; // Red
  };

  const color = getColor(percentage);

  return (
    <div style={{ position: 'relative', width: '200px', height: '200px' }}>
      <svg width='200' height='200' style={{ transform: 'rotate(-90deg)' }}>
        <circle
          cx='100'
          cy='100'
          r={radius}
          stroke='#E5E7EB'
          strokeWidth='12'
          fill='transparent'
        />
        <circle
          cx='100'
          cy='100'
          r={radius}
          stroke={color}
          strokeWidth='12'
          fill='transparent'
          strokeDasharray={circumference}
          strokeDashoffset={strokeDashoffset}
          strokeLinecap='round'
          style={{
            transition: 'stroke-dashoffset 1s ease-out',
          }}
        />
      </svg>
      <div
        style={{
          position: 'absolute',
          top: '50%',
          left: '50%',
          transform: 'translate(-50%, -50%)',
          textAlign: 'center',
        }}
      >
        <div style={{ fontSize: '2rem', fontWeight: 'bold', color }}>
          {Math.round(percentage)}%
        </div>
        <div style={{ fontSize: '0.875rem', color: '#6B7280' }}>
          {percentage < 30 ? 'Seguro' : percentage < 70 ? 'Cuidado' : 'Tóxico'}
        </div>
      </div>
    </div>
  );
}

function App() {
  const [text, setText] = useState('');
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // History state
  const [history, setHistory] = useState<HistoryItem[]>([]);
  const [stats, setStats] = useState<HistoryStats | null>(null);
  const [showHistory, setShowHistory] = useState(false);
  const [showCharts, setShowCharts] = useState(false);
  const [historyLoading, setHistoryLoading] = useState(false);

  const handleAnalyze = async () => {
    if (!text.trim()) {
      setError('Por favor, ingresa algún texto para analizar');
      return;
    }

    setIsLoading(true);
    setError(null);
    setResult(null);

    try {
      const analysisResult = await analyzeText(text);
      setResult(analysisResult);
      // Refresh history after analysis
      await loadHistory();
    } catch (err) {
      const errorMessage =
        err instanceof Error ? err.message : 'Error desconocido';
      setError(errorMessage);
    } finally {
      setIsLoading(false);
    }
  };

  const loadHistory = async () => {
    try {
      setHistoryLoading(true);
      const [historyData, statsData] = await Promise.all([
        getHistory(20),
        getStats(),
      ]);
      setHistory(historyData);
      setStats(statsData);
    } catch (err) {
      console.error('Error loading history:', err);
    } finally {
      setHistoryLoading(false);
    }
  };

  const handleDeleteHistoryItem = async (id: number) => {
    try {
      await deleteHistoryItem(id);
      await loadHistory(); // Refresh history
    } catch (err) {
      console.error('Error deleting history item:', err);
    }
  };

  // Load history on component mount
  useEffect(() => {
    loadHistory();
  }, []);

  const handleClear = () => {
    setText('');
    setResult(null);
    setError(null);
  };

  const containerStyle: React.CSSProperties = {
    minHeight: '100vh',
    background: 'linear-gradient(135deg, #F9FAFB 0%, #EBF4FF 100%)',
    padding: '2rem',
    fontFamily: 'system-ui, -apple-system, sans-serif',
  };

  const cardStyle: React.CSSProperties = {
    backgroundColor: 'white',
    borderRadius: '12px',
    boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
    padding: '2rem',
    marginBottom: '1.5rem',
  };

  const buttonStyle: React.CSSProperties = {
    padding: '0.75rem 1.5rem',
    borderRadius: '8px',
    border: 'none',
    fontWeight: '500',
    cursor: 'pointer',
    transition: 'all 0.2s',
  };

  const primaryButtonStyle: React.CSSProperties = {
    ...buttonStyle,
    backgroundColor: '#3B82F6',
    color: 'white',
  };

  const secondaryButtonStyle: React.CSSProperties = {
    ...buttonStyle,
    backgroundColor: '#F3F4F6',
    color: '#374151',
  };

  const textareaStyle: React.CSSProperties = {
    width: '100%',
    padding: '0.75rem',
    border: '1px solid #D1D5DB',
    borderRadius: '8px',
    minHeight: '120px',
    resize: 'none',
    fontSize: '1rem',
    fontFamily: 'inherit',
  };

  const toxicityPercentage =
    result?.toxicity_percentage ||
    (result ? Math.round(result.score * 100) : 0);

  return (
    <div style={containerStyle}>
      <div style={{ maxWidth: '800px', margin: '0 auto' }}>
        {/* Header */}
        <div style={{ textAlign: 'center', marginBottom: '2rem' }}>
          <h1
            style={{
              fontSize: '3rem',
              fontWeight: 'bold',
              background: 'linear-gradient(135deg, #3B82F6 0%, #8B5CF6 100%)',
              WebkitBackgroundClip: 'text',
              WebkitTextFillColor: 'transparent',
              margin: '0 0 1rem 0',
            }}
          >
            ToxiGuard
          </h1>
          <p
            style={{
              fontSize: '1.25rem',
              color: '#6B7280',
              margin: '0 0 1rem 0',
            }}
          >
            Detecta comentarios tóxicos en tiempo real con IA avanzada
          </p>

          {/* History Toggle */}
          <div
            style={{ display: 'flex', justifyContent: 'center', gap: '1rem' }}
          >
            <button
              style={{
                padding: '0.5rem 1rem',
                borderRadius: '8px',
                border: '1px solid #D1D5DB',
                backgroundColor: showHistory ? '#3B82F6' : 'white',
                color: showHistory ? 'white' : '#374151',
                fontWeight: '500',
                cursor: 'pointer',
                transition: 'all 0.2s',
                display: 'flex',
                alignItems: 'center',
                gap: '0.5rem',
              }}
              onClick={() => setShowHistory(!showHistory)}
            >
              <span>📊</span>
              {showHistory ? 'Ocultar Historial' : 'Ver Historial'}
              {stats && (
                <span
                  style={{
                    backgroundColor: showHistory
                      ? 'rgba(255,255,255,0.2)'
                      : '#EBF4FF',
                    color: showHistory ? 'white' : '#1E40AF',
                    padding: '0.125rem 0.5rem',
                    borderRadius: '12px',
                    fontSize: '0.75rem',
                    fontWeight: 'bold',
                  }}
                >
                  {stats.total_analyses}
                </span>
              )}
            </button>

            {showHistory && (
              <button
                style={{
                  padding: '0.5rem 1rem',
                  borderRadius: '8px',
                  border: '1px solid #D1D5DB',
                  backgroundColor: showCharts ? '#8B5CF6' : 'white',
                  color: showCharts ? 'white' : '#374151',
                  fontWeight: '500',
                  cursor: 'pointer',
                  transition: 'all 0.2s',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '0.5rem',
                }}
                onClick={() => setShowCharts(!showCharts)}
              >
                <span>📈</span>
                {showCharts ? 'Ocultar Gráficos' : 'Ver Gráficos'}
              </button>
            )}
          </div>
        </div>

        {/* Input Form */}
        <div style={cardStyle}>
          <label
            style={{
              display: 'block',
              fontSize: '0.875rem',
              fontWeight: '500',
              color: '#374151',
              marginBottom: '0.5rem',
            }}
          >
            Ingresa el texto a analizar:
          </label>
          <textarea
            style={textareaStyle}
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder='Escribe aquí el comentario o texto que quieres analizar...'
            disabled={isLoading}
          />
          <div
            style={{
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center',
              marginTop: '1rem',
            }}
          >
            <span style={{ fontSize: '0.875rem', color: '#6B7280' }}>
              {text.length} caracteres
            </span>
            <div style={{ display: 'flex', gap: '0.5rem' }}>
              <button
                style={{
                  ...secondaryButtonStyle,
                  opacity: isLoading || !text ? 0.5 : 1,
                  cursor: isLoading || !text ? 'not-allowed' : 'pointer',
                }}
                onClick={handleClear}
                disabled={isLoading || !text}
              >
                Limpiar
              </button>
              <button
                style={{
                  ...primaryButtonStyle,
                  opacity: isLoading || !text.trim() ? 0.5 : 1,
                  cursor: isLoading || !text.trim() ? 'not-allowed' : 'pointer',
                }}
                onClick={handleAnalyze}
                disabled={isLoading || !text.trim()}
              >
                {isLoading ? (
                  <span
                    style={{
                      display: 'flex',
                      alignItems: 'center',
                      gap: '0.5rem',
                    }}
                  >
                    <div
                      style={{
                        width: '16px',
                        height: '16px',
                        border: '2px solid white',
                        borderTop: '2px solid transparent',
                        borderRadius: '50%',
                        animation: 'spin 1s linear infinite',
                      }}
                    ></div>
                    Analizando...
                  </span>
                ) : (
                  'Analizar Toxicidad'
                )}
              </button>
            </div>
          </div>
        </div>

        {/* Loading */}
        {isLoading && (
          <div style={{ ...cardStyle, textAlign: 'center' }}>
            <div
              style={{
                width: '48px',
                height: '48px',
                border: '4px solid #3B82F6',
                borderTop: '4px solid transparent',
                borderRadius: '50%',
                animation: 'spin 1s linear infinite',
                margin: '0 auto 1rem auto',
              }}
            ></div>
            <p style={{ color: '#374151', fontWeight: '500' }}>
              Analizando toxicidad del texto...
            </p>
            <p style={{ color: '#6B7280', fontSize: '0.875rem' }}>
              Esto puede tomar unos segundos...
            </p>
          </div>
        )}

        {/* Error */}
        {error && (
          <div
            style={{
              ...cardStyle,
              backgroundColor: '#FEF2F2',
              border: '1px solid #FECACA',
            }}
          >
            <div
              style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}
            >
              <div style={{ color: '#EF4444', fontSize: '1.5rem' }}>⚠️</div>
              <div>
                <div
                  style={{
                    color: '#991B1B',
                    fontWeight: '600',
                    fontSize: '1.125rem',
                  }}
                >
                  Error en el análisis
                </div>
                <p style={{ color: '#B91C1C', margin: '0.25rem 0 0 0' }}>
                  {error}
                </p>
              </div>
            </div>
          </div>
        )}

        {/* Results */}
        {result && (
          <div style={cardStyle}>
            <h3
              style={{
                textAlign: 'center',
                fontSize: '1.5rem',
                fontWeight: 'bold',
                color: '#111827',
                marginBottom: '2rem',
              }}
            >
              Resultado del Análisis
            </h3>

            {/* Gauge */}
            <div
              style={{
                display: 'flex',
                justifyContent: 'center',
                marginBottom: '2rem',
              }}
            >
              <ToxicityGauge percentage={toxicityPercentage} />
            </div>

            {/* Status */}
            <div style={{ textAlign: 'center', marginBottom: '2rem' }}>
              <div
                style={{
                  display: 'inline-flex',
                  alignItems: 'center',
                  gap: '0.75rem',
                  padding: '1rem 1.5rem',
                  borderRadius: '2rem',
                  fontSize: '1.25rem',
                  fontWeight: 'bold',
                  backgroundColor: result.toxic ? '#FEF2F2' : '#F0FDF4',
                  color: result.toxic ? '#991B1B' : '#166534',
                  border: result.toxic
                    ? '2px solid #FECACA'
                    : '2px solid #BBF7D0',
                }}
              >
                <div
                  style={{
                    width: '16px',
                    height: '16px',
                    borderRadius: '50%',
                    backgroundColor: result.toxic ? '#EF4444' : '#10B981',
                  }}
                ></div>
                {result.toxic ? 'CONTENIDO TÓXICO' : 'CONTENIDO SEGURO'}
              </div>
            </div>

            {/* Metrics */}
            <div
              style={{
                display: 'grid',
                gridTemplateColumns: 'repeat(3, 1fr)',
                gap: '1rem',
                maxWidth: '400px',
                margin: '0 auto 2rem auto',
              }}
            >
              <div
                style={{
                  textAlign: 'center',
                  padding: '1rem',
                  backgroundColor: '#F9FAFB',
                  borderRadius: '8px',
                }}
              >
                <div
                  style={{
                    fontSize: '1.125rem',
                    fontWeight: 'bold',
                    color: '#111827',
                  }}
                >
                  {result.text_length}
                </div>
                <div style={{ fontSize: '0.75rem', color: '#6B7280' }}>
                  Caracteres
                </div>
              </div>
              <div
                style={{
                  textAlign: 'center',
                  padding: '1rem',
                  backgroundColor: '#F9FAFB',
                  borderRadius: '8px',
                }}
              >
                <div
                  style={{
                    fontSize: '1.125rem',
                    fontWeight: 'bold',
                    color: '#111827',
                  }}
                >
                  {result.keywords_found}
                </div>
                <div style={{ fontSize: '0.75rem', color: '#6B7280' }}>
                  Palabras clave
                </div>
              </div>
              <div
                style={{
                  textAlign: 'center',
                  padding: '1rem',
                  backgroundColor: '#F9FAFB',
                  borderRadius: '8px',
                }}
              >
                <div
                  style={{
                    fontSize: '1.125rem',
                    fontWeight: 'bold',
                    color: '#111827',
                  }}
                >
                  {result.response_time_ms
                    ? `${result.response_time_ms}ms`
                    : 'N/A'}
                </div>
                <div style={{ fontSize: '0.75rem', color: '#6B7280' }}>
                  Respuesta
                </div>
              </div>
            </div>

            {/* Technical Info */}
            <div>
              <h4
                style={{
                  textAlign: 'center',
                  fontSize: '1.125rem',
                  fontWeight: '600',
                  color: '#111827',
                  marginBottom: '1rem',
                }}
              >
                Información Técnica
              </h4>
              <div
                style={{
                  display: 'grid',
                  gridTemplateColumns: 'repeat(auto-fit, minmax(150px, 1fr))',
                  gap: '1rem',
                }}
              >
                <div
                  style={{
                    textAlign: 'center',
                    padding: '0.75rem',
                    backgroundColor: '#EBF8FF',
                    borderRadius: '8px',
                    border: '1px solid #93C5FD',
                  }}
                >
                  <div
                    style={{
                      fontSize: '0.875rem',
                      fontWeight: '500',
                      color: '#1E40AF',
                    }}
                  >
                    Score
                  </div>
                  <div
                    style={{
                      fontSize: '1.125rem',
                      fontWeight: 'bold',
                      color: '#1D4ED8',
                    }}
                  >
                    {result.score.toFixed(3)}
                  </div>
                </div>
                <div
                  style={{
                    textAlign: 'center',
                    padding: '0.75rem',
                    backgroundColor: '#FAF5FF',
                    borderRadius: '8px',
                    border: '1px solid #C4B5FD',
                  }}
                >
                  <div
                    style={{
                      fontSize: '0.875rem',
                      fontWeight: '500',
                      color: '#7C3AED',
                    }}
                  >
                    Porcentaje
                  </div>
                  <div
                    style={{
                      fontSize: '1.125rem',
                      fontWeight: 'bold',
                      color: '#6D28D9',
                    }}
                  >
                    {toxicityPercentage.toFixed(1)}%
                  </div>
                </div>
                <div
                  style={{
                    textAlign: 'center',
                    padding: '0.75rem',
                    backgroundColor: '#F0F9FF',
                    borderRadius: '8px',
                    border: '1px solid #7DD3FC',
                  }}
                >
                  <div
                    style={{
                      fontSize: '0.875rem',
                      fontWeight: '500',
                      color: '#0369A1',
                    }}
                  >
                    Modelo
                  </div>
                  <div
                    style={{
                      fontSize: '0.875rem',
                      fontWeight: 'bold',
                      color: '#0284C7',
                    }}
                  >
                    {result.model_used || 'N/A'}
                  </div>
                </div>
              </div>

              {/* Labels */}
              {result.labels && result.labels.length > 0 && (
                <div style={{ marginTop: '1.5rem', textAlign: 'center' }}>
                  <div
                    style={{
                      fontSize: '0.875rem',
                      color: '#6B7280',
                      marginBottom: '0.75rem',
                    }}
                  >
                    Etiquetas de análisis:
                  </div>
                  <div
                    style={{
                      display: 'flex',
                      flexWrap: 'wrap',
                      justifyContent: 'center',
                      gap: '0.5rem',
                    }}
                  >
                    {result.labels.map((label, index) => (
                      <span
                        key={index}
                        style={{
                          display: 'inline-flex',
                          alignItems: 'center',
                          padding: '0.25rem 0.75rem',
                          borderRadius: '9999px',
                          fontSize: '0.75rem',
                          fontWeight: '500',
                          backgroundColor: '#EBF4FF',
                          color: '#1E40AF',
                          border: '1px solid #93C5FD',
                        }}
                      >
                        {label}
                      </span>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </div>
        )}

        {/* History Section */}
        {showHistory && (
          <div style={cardStyle}>
            <div
              style={{
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
                marginBottom: '1.5rem',
              }}
            >
              <h3
                style={{
                  fontSize: '1.5rem',
                  fontWeight: 'bold',
                  color: '#111827',
                  margin: '0',
                }}
              >
                📊 Historial de Análisis
              </h3>
              <button
                style={{
                  padding: '0.5rem 1rem',
                  borderRadius: '8px',
                  border: '1px solid #D1D5DB',
                  backgroundColor: '#F9FAFB',
                  color: '#374151',
                  fontSize: '0.875rem',
                  fontWeight: '500',
                  cursor: 'pointer',
                  transition: 'all 0.2s',
                }}
                onClick={loadHistory}
                disabled={historyLoading}
              >
                {historyLoading ? '🔄 Cargando...' : '🔄 Actualizar'}
              </button>
            </div>

            {/* Statistics */}
            {stats && (
              <div
                style={{
                  display: 'grid',
                  gridTemplateColumns: 'repeat(auto-fit, minmax(120px, 1fr))',
                  gap: '1rem',
                  marginBottom: '1.5rem',
                }}
              >
                <div
                  style={{
                    textAlign: 'center',
                    padding: '1rem',
                    backgroundColor: '#EBF8FF',
                    borderRadius: '8px',
                    border: '1px solid #93C5FD',
                  }}
                >
                  <div
                    style={{
                      fontSize: '1.5rem',
                      fontWeight: 'bold',
                      color: '#1D4ED8',
                    }}
                  >
                    {stats.total_analyses}
                  </div>
                  <div style={{ fontSize: '0.75rem', color: '#1E40AF' }}>
                    Total
                  </div>
                </div>
                <div
                  style={{
                    textAlign: 'center',
                    padding: '1rem',
                    backgroundColor: '#F0FDF4',
                    borderRadius: '8px',
                    border: '1px solid #BBF7D0',
                  }}
                >
                  <div
                    style={{
                      fontSize: '1.5rem',
                      fontWeight: 'bold',
                      color: '#166534',
                    }}
                  >
                    {stats.safe_analyses}
                  </div>
                  <div style={{ fontSize: '0.75rem', color: '#166534' }}>
                    Seguros
                  </div>
                </div>
                <div
                  style={{
                    textAlign: 'center',
                    padding: '1rem',
                    backgroundColor: '#FEF2F2',
                    borderRadius: '8px',
                    border: '1px solid #FECACA',
                  }}
                >
                  <div
                    style={{
                      fontSize: '1.5rem',
                      fontWeight: 'bold',
                      color: '#991B1B',
                    }}
                  >
                    {stats.toxic_analyses}
                  </div>
                  <div style={{ fontSize: '0.75rem', color: '#991B1B' }}>
                    Tóxicos
                  </div>
                </div>
                <div
                  style={{
                    textAlign: 'center',
                    padding: '1rem',
                    backgroundColor: '#FAF5FF',
                    borderRadius: '8px',
                    border: '1px solid #C4B5FD',
                  }}
                >
                  <div
                    style={{
                      fontSize: '1.5rem',
                      fontWeight: 'bold',
                      color: '#7C3AED',
                    }}
                  >
                    {stats.toxicity_rate.toFixed(1)}%
                  </div>
                  <div style={{ fontSize: '0.75rem', color: '#7C3AED' }}>
                    Tasa tóxica
                  </div>
                </div>
              </div>
            )}

            {/* Charts Section */}
            {showCharts && stats && (
              <div style={{ marginBottom: '2rem' }}>
                <h4
                  style={{
                    fontSize: '1.25rem',
                    fontWeight: 'bold',
                    color: '#111827',
                    marginBottom: '1.5rem',
                    textAlign: 'center',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    gap: '0.5rem',
                  }}
                >
                  <span>📈</span>
                  Análisis Visual
                </h4>

                <div
                  style={{
                    display: 'grid',
                    gridTemplateColumns: 'repeat(auto-fit, minmax(350px, 1fr))',
                    gap: '2rem',
                    marginBottom: '1.5rem',
                  }}
                >
                  {/* Pie Chart */}
                  <div
                    style={{
                      backgroundColor: '#F9FAFB',
                      borderRadius: '12px',
                      padding: '1.5rem',
                      border: '1px solid #E5E7EB',
                    }}
                  >
                    <h5
                      style={{
                        fontSize: '1rem',
                        fontWeight: '600',
                        color: '#374151',
                        marginBottom: '1rem',
                        textAlign: 'center',
                      }}
                    >
                      🥧 Distribución General
                    </h5>
                    <ToxicityPieChart stats={stats} />
                    <div
                      style={{
                        marginTop: '1rem',
                        fontSize: '0.875rem',
                        color: '#6B7280',
                        textAlign: 'center',
                      }}
                    >
                      Total de {stats.total_analyses} análisis realizados
                    </div>
                  </div>

                  {/* Distribution Chart */}
                  {history.length > 0 && (
                    <div
                      style={{
                        backgroundColor: '#F9FAFB',
                        borderRadius: '12px',
                        padding: '1.5rem',
                        border: '1px solid #E5E7EB',
                      }}
                    >
                      <h5
                        style={{
                          fontSize: '1rem',
                          fontWeight: '600',
                          color: '#374151',
                          marginBottom: '1rem',
                          textAlign: 'center',
                        }}
                      >
                        📊 Distribución por Niveles
                      </h5>
                      <ToxicityDistributionChart history={history} />
                      <div
                        style={{
                          marginTop: '1rem',
                          fontSize: '0.875rem',
                          color: '#6B7280',
                          textAlign: 'center',
                        }}
                      >
                        Análisis agrupados por rango de toxicidad
                      </div>
                    </div>
                  )}
                </div>

                {/* Categories Chart */}
                {stats.categories &&
                  Object.keys(stats.categories).length > 0 && (
                    <div
                      style={{
                        backgroundColor: '#F9FAFB',
                        borderRadius: '12px',
                        padding: '1.5rem',
                        border: '1px solid #E5E7EB',
                        marginBottom: '1.5rem',
                      }}
                    >
                      <h5
                        style={{
                          fontSize: '1rem',
                          fontWeight: '600',
                          color: '#374151',
                          marginBottom: '1rem',
                          textAlign: 'center',
                        }}
                      >
                        🏷️ Detecciones por Categoría
                      </h5>
                      <CategoriesChart stats={stats} />
                      <div
                        style={{
                          marginTop: '1rem',
                          fontSize: '0.875rem',
                          color: '#6B7280',
                          textAlign: 'center',
                        }}
                      >
                        Tipos de toxicidad más frecuentes
                      </div>
                    </div>
                  )}

                {/* Charts Info */}
                {(!stats.categories ||
                  Object.keys(stats.categories).length === 0) &&
                  history.length === 0 && (
                    <div
                      style={{
                        textAlign: 'center',
                        padding: '2rem',
                        color: '#6B7280',
                        backgroundColor: '#F9FAFB',
                        borderRadius: '12px',
                        border: '1px solid #E5E7EB',
                      }}
                    >
                      <div style={{ fontSize: '3rem', marginBottom: '1rem' }}>
                        📈
                      </div>
                      <p
                        style={{
                          fontSize: '1.125rem',
                          fontWeight: '500',
                          marginBottom: '0.5rem',
                        }}
                      >
                        Gráficos en construcción
                      </p>
                      <p style={{ fontSize: '0.875rem' }}>
                        Realiza algunos análisis para generar visualizaciones
                        detalladas
                      </p>
                    </div>
                  )}
              </div>
            )}

            {/* History Table */}
            {historyLoading ? (
              <div style={{ textAlign: 'center', padding: '2rem' }}>
                <div
                  style={{
                    width: '48px',
                    height: '48px',
                    border: '4px solid #3B82F6',
                    borderTop: '4px solid transparent',
                    borderRadius: '50%',
                    animation: 'spin 1s linear infinite',
                    margin: '0 auto 1rem auto',
                  }}
                ></div>
                <p style={{ color: '#6B7280' }}>Cargando historial...</p>
              </div>
            ) : history.length > 0 ? (
              <div style={{ overflowX: 'auto' }}>
                <table
                  style={{
                    width: '100%',
                    borderCollapse: 'collapse',
                    fontSize: '0.875rem',
                  }}
                >
                  <thead>
                    <tr
                      style={{
                        backgroundColor: '#F9FAFB',
                        borderBottom: '2px solid #E5E7EB',
                      }}
                    >
                      <th
                        style={{
                          padding: '0.75rem',
                          textAlign: 'left',
                          fontWeight: '600',
                          color: '#374151',
                        }}
                      >
                        Texto
                      </th>
                      <th
                        style={{
                          padding: '0.75rem',
                          textAlign: 'center',
                          fontWeight: '600',
                          color: '#374151',
                        }}
                      >
                        Estado
                      </th>
                      <th
                        style={{
                          padding: '0.75rem',
                          textAlign: 'center',
                          fontWeight: '600',
                          color: '#374151',
                        }}
                      >
                        %
                      </th>
                      <th
                        style={{
                          padding: '0.75rem',
                          textAlign: 'center',
                          fontWeight: '600',
                          color: '#374151',
                        }}
                      >
                        Categoría
                      </th>
                      <th
                        style={{
                          padding: '0.75rem',
                          textAlign: 'center',
                          fontWeight: '600',
                          color: '#374151',
                        }}
                      >
                        Fecha
                      </th>
                      <th
                        style={{
                          padding: '0.75rem',
                          textAlign: 'center',
                          fontWeight: '600',
                          color: '#374151',
                        }}
                      >
                        Acción
                      </th>
                    </tr>
                  </thead>
                  <tbody>
                    {history.map((item, index) => (
                      <tr
                        key={item.id}
                        style={{
                          borderBottom: '1px solid #E5E7EB',
                          backgroundColor:
                            index % 2 === 0 ? 'white' : '#F9FAFB',
                        }}
                      >
                        <td style={{ padding: '0.75rem', maxWidth: '200px' }}>
                          <div
                            style={{
                              overflow: 'hidden',
                              textOverflow: 'ellipsis',
                              whiteSpace: 'nowrap',
                              color: '#374151',
                            }}
                          >
                            {item.text}
                          </div>
                        </td>
                        <td style={{ padding: '0.75rem', textAlign: 'center' }}>
                          <span
                            style={{
                              display: 'inline-flex',
                              alignItems: 'center',
                              gap: '0.25rem',
                              padding: '0.25rem 0.5rem',
                              borderRadius: '12px',
                              fontSize: '0.75rem',
                              fontWeight: '500',
                              backgroundColor: item.toxic
                                ? '#FEF2F2'
                                : '#F0FDF4',
                              color: item.toxic ? '#991B1B' : '#166534',
                              border: item.toxic
                                ? '1px solid #FECACA'
                                : '1px solid #BBF7D0',
                            }}
                          >
                            <div
                              style={{
                                width: '8px',
                                height: '8px',
                                borderRadius: '50%',
                                backgroundColor: item.toxic
                                  ? '#EF4444'
                                  : '#10B981',
                              }}
                            ></div>
                            {item.toxic ? 'Tóxico' : 'Seguro'}
                          </span>
                        </td>
                        <td
                          style={{
                            padding: '0.75rem',
                            textAlign: 'center',
                            fontWeight: '600',
                          }}
                        >
                          <span
                            style={{
                              color: item.toxic ? '#991B1B' : '#166534',
                            }}
                          >
                            {item.toxicity_percentage
                              ? `${item.toxicity_percentage.toFixed(1)}%`
                              : `${(item.score * 100).toFixed(1)}%`}
                          </span>
                        </td>
                        <td
                          style={{
                            padding: '0.75rem',
                            textAlign: 'center',
                            fontSize: '0.75rem',
                            color: '#6B7280',
                          }}
                        >
                          {item.category || '-'}
                        </td>
                        <td
                          style={{
                            padding: '0.75rem',
                            textAlign: 'center',
                            fontSize: '0.75rem',
                            color: '#6B7280',
                          }}
                        >
                          {new Date(item.created_at).toLocaleDateString(
                            'es-ES',
                            {
                              day: '2-digit',
                              month: '2-digit',
                              hour: '2-digit',
                              minute: '2-digit',
                            }
                          )}
                        </td>
                        <td style={{ padding: '0.75rem', textAlign: 'center' }}>
                          <button
                            style={{
                              padding: '0.25rem 0.5rem',
                              borderRadius: '4px',
                              border: '1px solid #F87171',
                              backgroundColor: '#FEF2F2',
                              color: '#991B1B',
                              fontSize: '0.75rem',
                              cursor: 'pointer',
                              transition: 'all 0.2s',
                            }}
                            onClick={() => handleDeleteHistoryItem(item.id)}
                            title='Eliminar análisis'
                          >
                            🗑️
                          </button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            ) : (
              <div
                style={{
                  textAlign: 'center',
                  padding: '2rem',
                  color: '#6B7280',
                }}
              >
                <div style={{ fontSize: '3rem', marginBottom: '1rem' }}>📊</div>
                <p
                  style={{
                    fontSize: '1.125rem',
                    fontWeight: '500',
                    marginBottom: '0.5rem',
                  }}
                >
                  No hay análisis en el historial
                </p>
                <p style={{ fontSize: '0.875rem' }}>
                  Realiza tu primer análisis para empezar a construir el
                  historial
                </p>
              </div>
            )}
          </div>
        )}

        {/* Info Card */}
        {!result && !isLoading && !error && !showHistory && (
          <div style={{ ...cardStyle, textAlign: 'center', color: '#6B7280' }}>
            <div
              style={{
                width: '80px',
                height: '80px',
                margin: '0 auto 1rem auto',
                color: '#D1D5DB',
                fontSize: '3rem',
              }}
            >
              ℹ️
            </div>
            <p
              style={{
                fontSize: '1.125rem',
                fontWeight: '500',
                marginBottom: '0.5rem',
                color: '#374151',
              }}
            >
              ¿Listo para analizar?
            </p>
            <p style={{ color: '#6B7280', marginBottom: '1rem' }}>
              Ingresa un texto y haz clic en "Analizar Toxicidad" para comenzar
            </p>
            <div style={{ fontSize: '0.75rem', color: '#9CA3AF' }}>
              <p>✨ Análisis con IA avanzada</p>
              <p>🎯 Detección precisa de toxicidad</p>
              <p>📊 Resultados visuales detallados</p>
            </div>
          </div>
        )}
      </div>

      <style>{`
        @keyframes spin {
          0% { transform: rotate(0deg); }
          100% { transform: rotate(360deg); }
        }
      `}</style>
    </div>
  );
}

export default App;
