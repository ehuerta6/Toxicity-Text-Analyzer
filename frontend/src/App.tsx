import React, { useState } from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
} from 'chart.js';
import { Bar, Pie, Doughnut } from 'react-chartjs-2';
import { useToxicityAnalysis } from './hooks/useToxicityAnalysis';
import { useHistory } from './hooks/useHistory';
import {
  commonStyles,
  getToxicityColor,
  getToxicityLabel,
  getToxicityBorderColor,
} from './styles/common';

// Register Chart.js components
ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement
);

const ToxicityGauge: React.FC<{ percentage: number }> = ({ percentage }) => {
  const color = getToxicityColor(percentage);
  const label = getToxicityLabel(percentage);

  return (
    <div style={{ textAlign: 'center' }}>
      <div
        style={{
          width: '140px',
          height: '140px',
          borderRadius: '50%',
          background: `conic-gradient(${color} ${
            percentage * 3.6
          }deg, #e5e7eb ${percentage * 3.6}deg)`,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          margin: '0 auto 20px',
          position: 'relative',
          boxShadow: '0 8px 25px rgba(0, 0, 0, 0.15)',
          border: `4px solid ${color}`,
        }}
      >
        <div
          style={{
            width: '100px',
            height: '100px',
            borderRadius: '50%',
            backgroundColor: 'white',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            fontSize: '20px',
            fontWeight: 'bold',
            color: color,
            boxShadow: 'inset 0 2px 10px rgba(0, 0, 0, 0.1)',
          }}
        >
          {percentage}%
        </div>
      </div>
      <div
        style={{
          fontSize: '20px',
          fontWeight: '700',
          color: color,
          textShadow: '0 1px 2px rgba(0, 0, 0, 0.1)',
          marginBottom: '8px',
        }}
      >
        {label}
      </div>
      <div
        style={{
          fontSize: '14px',
          color: '#6b7280',
          maxWidth: '200px',
          margin: '0 auto',
        }}
      >
        {percentage < 30
          ? 'El contenido es seguro y apropiado'
          : percentage < 70
          ? 'El contenido requiere atención moderada'
          : 'El contenido presenta niveles altos de toxicidad'}
      </div>
    </div>
  );
};

const ToxicityPieChart: React.FC<{
  stats: { safe_count: number; toxic_count: number };
}> = ({ stats }) => {
  const data = {
    labels: ['Seguro', 'Tóxico'],
    datasets: [
      {
        data: [stats.safe_count, stats.toxic_count],
        backgroundColor: [
          commonStyles.toxicity.safe,
          commonStyles.toxicity.toxic,
        ],
        borderWidth: 2,
        borderColor: 'white',
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'bottom' as const,
      },
      title: {
        display: true,
        text: 'Distribución de Toxicidad',
      },
    },
  };

  return <Pie data={data} options={options} />;
};

const ToxicityDistributionChart: React.FC<{
  history: Array<{ result: { toxicity_percentage: number } }>;
}> = ({ history }) => {
  const scoreRanges = {
    '0-20%': 0,
    '21-40%': 0,
    '41-60%': 0,
    '61-80%': 0,
    '81-100%': 0,
  };

  history.forEach((item) => {
    const percentage = item.result.toxicity_percentage;
    if (percentage <= 20) scoreRanges['0-20%']++;
    else if (percentage <= 40) scoreRanges['21-40%']++;
    else if (percentage <= 60) scoreRanges['41-60%']++;
    else if (percentage <= 80) scoreRanges['61-80%']++;
    else scoreRanges['81-100%']++;
  });

  const data = {
    labels: Object.keys(scoreRanges),
    datasets: [
      {
        label: 'Número de Análisis',
        data: Object.values(scoreRanges),
        backgroundColor: [
          commonStyles.toxicity.safe,
          '#fbbf24',
          '#f59e0b',
          '#f97316',
          commonStyles.toxicity.toxic,
        ],
        borderWidth: 1,
        borderColor: 'white',
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'bottom' as const,
      },
      title: {
        display: true,
        text: 'Distribución de Scores de Toxicidad',
      },
    },
    scales: {
      y: {
        beginAtZero: true,
        ticks: {
          stepSize: 1,
        },
      },
    },
  };

  return <Bar data={data} options={options} />;
};

const CategoriesChart: React.FC<{
  history: Array<{ result: { category: string | null } }>;
}> = ({ history }) => {
  const categories: { [key: string]: number } = {};

  history.forEach((item) => {
    const category = item.result.category;
    if (category) {
      categories[category] = (categories[category] || 0) + 1;
    }
  });

  const data = {
    labels: Object.keys(categories),
    datasets: [
      {
        label: 'Análisis por Categoría',
        data: Object.values(categories),
        backgroundColor: [
          '#ef4444',
          '#f97316',
          '#eab308',
          '#84cc16',
          '#22c55e',
          '#06b6d4',
          '#8b5cf6',
          '#ec4899',
        ],
        borderWidth: 1,
        borderColor: 'white',
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'bottom' as const,
      },
      title: {
        display: true,
        text: 'Análisis por Categoría de Toxicidad',
      },
    },
  };

  return <Doughnut data={data} options={options} />;
};

const App: React.FC = () => {
  const [inputText, setInputText] = useState('');
  const [showHistory, setShowHistory] = useState(false);
  const [showCharts, setShowCharts] = useState(false);

  const { result, loading, error, analyzeText, clearResult } =
    useToxicityAnalysis();
  const {
    history,
    stats,
    loading: historyLoading,
    deleteItem,
    clearHistory,
  } = useHistory();

  const handleAnalyze = async () => {
    if (inputText.trim()) {
      console.log('🔄 Iniciando análisis de texto:', inputText.trim());
      try {
        await analyzeText(inputText);
        console.log('✅ Análisis completado exitosamente');
      } catch (error) {
        console.error('❌ Error en handleAnalyze:', error);
      }
    }
  };

  const handleClear = () => {
    setInputText('');
    clearResult();
  };

  return (
    <div
      style={{
        minHeight: '100vh',
        backgroundColor: '#f8fafc',
        fontFamily:
          'Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
      }}
    >
      {/* Header */}
      <header
        style={{
          backgroundColor: 'white',
          borderBottom: '1px solid #e2e8f0',
          padding: '24px 0',
          boxShadow: '0 1px 3px rgba(0, 0, 0, 0.1)',
        }}
      >
        <div
          style={{ maxWidth: '1400px', margin: '0 auto', padding: '0 24px' }}
        >
          <h1
            style={{
              fontSize: '28px',
              fontWeight: '700',
              color: '#1e293b',
              textAlign: 'center',
              margin: '0',
            }}
          >
            🛡️ ToxiGuard – Analiza texto
          </h1>
          <p
            style={{
              fontSize: '16px',
              color: '#64748b',
              textAlign: 'center',
              margin: '8px 0 0 0',
            }}
          >
            Detección inteligente de contenido tóxico usando Machine Learning
          </p>
        </div>
      </header>

      {/* Main Content Container */}
      <div
        style={{
          maxWidth: '1400px',
          margin: '0 auto',
          padding: '32px 24px',
          display: 'grid',
          gridTemplateColumns: '1fr',
          gap: '32px',
        }}
      >
        {/* Main Grid Layout */}
        <div
          style={{
            display: 'grid',
            gridTemplateColumns: result ? '1fr 1fr' : '1fr',
            gap: '32px',
            alignItems: 'start',
          }}
        >
          {/* Input Form - Left Column */}
          <div
            style={{
              backgroundColor: 'white',
              borderRadius: '16px',
              padding: '32px',
              boxShadow: '0 4px 6px rgba(0, 0, 0, 0.05)',
              border: '1px solid #e2e8f0',
            }}
          >
            <h2
              style={{
                fontSize: '20px',
                fontWeight: '600',
                color: '#1e293b',
                margin: '0 0 24px 0',
              }}
            >
              📝 Analizar Texto
            </h2>

            <div style={{ marginBottom: '20px' }}>
              <textarea
                value={inputText}
                onChange={(e) => setInputText(e.target.value)}
                placeholder='Ingresa el texto que quieres analizar...'
                style={{
                  width: '100%',
                  minHeight: '160px',
                  padding: '16px',
                  border: '2px solid #e2e8f0',
                  borderRadius: '12px',
                  fontSize: '16px',
                  fontFamily: 'inherit',
                  resize: 'vertical',
                  backgroundColor: '#fafafa',
                  transition: 'all 0.2s ease',
                  boxSizing: 'border-box',
                }}
                onFocus={(e) => {
                  e.target.style.borderColor = '#3b82f6';
                  e.target.style.backgroundColor = 'white';
                  e.target.style.boxShadow =
                    '0 0 0 3px rgba(59, 130, 246, 0.1)';
                }}
                onBlur={(e) => {
                  e.target.style.borderColor = inputText.trim()
                    ? '#3b82f6'
                    : '#e2e8f0';
                  e.target.style.backgroundColor = inputText.trim()
                    ? 'white'
                    : '#fafafa';
                  e.target.style.boxShadow = inputText.trim()
                    ? '0 0 0 3px rgba(59, 130, 246, 0.1)'
                    : 'none';
                }}
              />
              {inputText.trim() && (
                <div
                  style={{
                    marginTop: '8px',
                    fontSize: '14px',
                    color: '#64748b',
                    textAlign: 'right',
                  }}
                >
                  {inputText.length} caracteres
                </div>
              )}
            </div>

            <div style={{ display: 'flex', gap: '12px', flexWrap: 'wrap' }}>
              <button
                onClick={handleAnalyze}
                disabled={loading || !inputText.trim()}
                style={{
                  backgroundColor: '#3b82f6',
                  color: 'white',
                  border: 'none',
                  padding: '12px 24px',
                  borderRadius: '8px',
                  fontSize: '16px',
                  fontWeight: '600',
                  cursor:
                    loading || !inputText.trim() ? 'not-allowed' : 'pointer',
                  opacity: loading || !inputText.trim() ? 0.6 : 1,
                  transition: 'all 0.2s ease',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '8px',
                }}
                onMouseEnter={(e) => {
                  if (!loading && inputText.trim()) {
                    e.currentTarget.style.backgroundColor = '#2563eb';
                    e.currentTarget.style.transform = 'translateY(-1px)';
                  }
                }}
                onMouseLeave={(e) => {
                  if (!loading && inputText.trim()) {
                    e.currentTarget.style.backgroundColor = '#3b82f6';
                    e.currentTarget.style.transform = 'translateY(0)';
                  }
                }}
              >
                {loading ? (
                  <>
                    <div
                      style={{
                        width: '16px',
                        height: '16px',
                        border: '2px solid transparent',
                        borderTop: '2px solid white',
                        borderRadius: '50%',
                        animation: 'spin 1s linear infinite',
                      }}
                    />
                    Analizando...
                  </>
                ) : (
                  '🔍 Analizar'
                )}
              </button>

              <button
                onClick={handleClear}
                style={{
                  backgroundColor: '#f1f5f9',
                  color: '#475569',
                  border: '1px solid #cbd5e1',
                  padding: '12px 24px',
                  borderRadius: '8px',
                  fontSize: '16px',
                  fontWeight: '600',
                  cursor: 'pointer',
                  transition: 'all 0.2s ease',
                }}
                onMouseEnter={(e) => {
                  e.currentTarget.style.backgroundColor = '#e2e8f0';
                  e.currentTarget.style.transform = 'translateY(-1px)';
                }}
                onMouseLeave={(e) => {
                  e.currentTarget.style.backgroundColor = '#f1f5f9';
                  e.currentTarget.style.transform = 'translateY(0)';
                }}
              >
                🗑️ Limpiar
              </button>
            </div>

            {error && (
              <div
                style={{
                  marginTop: '20px',
                  color: '#dc2626',
                  padding: '16px',
                  backgroundColor: '#fef2f2',
                  borderRadius: '8px',
                  border: '1px solid #fecaca',
                  animation: 'shake 0.5s ease-in-out',
                }}
              >
                <div style={{ marginBottom: '8px', fontWeight: '600' }}>
                  ❌ {error}
                </div>
                {error.includes('No se pudo conectar') && (
                  <div style={{ fontSize: '14px', color: '#dc2626' }}>
                    <strong>🔧 Solución:</strong>
                    <ul style={{ marginTop: '8px', marginLeft: '20px' }}>
                      <li>
                        Verifica que el backend esté ejecutándose en
                        http://127.0.0.1:8000
                      </li>
                      <li>
                        Abre la consola del navegador (F12) para ver más
                        detalles
                      </li>
                      <li>
                        Prueba el archivo test-connection.html para verificar la
                        conectividad
                      </li>
                    </ul>
                  </div>
                )}
              </div>
            )}
          </div>

          {/* Results - Right Column */}
          {result && (
            <div
              style={{
                backgroundColor: 'white',
                borderRadius: '16px',
                padding: '32px',
                boxShadow: '0 4px 6px rgba(0, 0, 0, 0.05)',
                border: '2px solid',
                borderColor: getToxicityBorderColor(result.toxicity_percentage),
                transition: 'all 0.3s ease',
              }}
            >
              <h2
                style={{
                  fontSize: '20px',
                  fontWeight: '600',
                  color: '#1e293b',
                  margin: '0 0 24px 0',
                  textAlign: 'center',
                }}
              >
                📊 Resultados del Análisis
              </h2>

              <div style={{ marginBottom: '24px' }}>
                <ToxicityGauge percentage={result.toxicity_percentage} />
              </div>

              {/* Enhanced Results Display */}
              <div
                style={{
                  backgroundColor: '#f8fafc',
                  padding: '20px',
                  borderRadius: '12px',
                  border: '1px solid #e2e8f0',
                }}
              >
                <div
                  style={{
                    display: 'grid',
                    gridTemplateColumns: 'repeat(auto-fit, minmax(120px, 1fr))',
                    gap: '16px',
                    marginBottom: '20px',
                  }}
                >
                  <div style={{ textAlign: 'center' }}>
                    <div
                      style={{
                        fontSize: '12px',
                        color: '#64748b',
                        marginBottom: '4px',
                      }}
                    >
                      Score
                    </div>
                    <div
                      style={{
                        fontSize: '18px',
                        fontWeight: '600',
                        color: '#1e293b',
                      }}
                    >
                      {result.score.toFixed(3)}
                    </div>
                  </div>

                  {result.category && (
                    <div style={{ textAlign: 'center' }}>
                      <div
                        style={{
                          fontSize: '12px',
                          color: '#64748b',
                          marginBottom: '4px',
                        }}
                      >
                        Categoría
                      </div>
                      <div
                        style={{
                          fontSize: '18px',
                          fontWeight: '600',
                          color: '#1e293b',
                        }}
                      >
                        {result.category}
                      </div>
                    </div>
                  )}

                  <div style={{ textAlign: 'center' }}>
                    <div
                      style={{
                        fontSize: '12px',
                        color: '#64748b',
                        marginBottom: '4px',
                      }}
                    >
                      Modelo
                    </div>
                    <div
                      style={{
                        fontSize: '18px',
                        fontWeight: '600',
                        color: '#1e293b',
                      }}
                    >
                      {result.model_used}
                    </div>
                  </div>

                  <div style={{ textAlign: 'center' }}>
                    <div
                      style={{
                        fontSize: '12px',
                        color: '#64748b',
                        marginBottom: '4px',
                      }}
                    >
                      Tiempo
                    </div>
                    <div
                      style={{
                        fontSize: '18px',
                        fontWeight: '600',
                        color: '#1e293b',
                      }}
                    >
                      {result.response_time_ms}ms
                    </div>
                  </div>
                </div>

                <div
                  style={{
                    fontSize: '14px',
                    color: '#64748b',
                    textAlign: 'center',
                    padding: '12px',
                    backgroundColor: '#f1f5f9',
                    borderRadius: '8px',
                    border: '1px solid #e2e8f0',
                  }}
                >
                  Analizado el {new Date(result.timestamp).toLocaleString()}
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Control Buttons */}
        <div style={{ textAlign: 'center' }}>
          <button
            onClick={() => setShowHistory(!showHistory)}
            style={{
              backgroundColor: '#f1f5f9',
              color: '#475569',
              border: '1px solid #cbd5e1',
              padding: '12px 24px',
              borderRadius: '8px',
              fontSize: '16px',
              fontWeight: '600',
              cursor: 'pointer',
              marginRight: '12px',
              transition: 'all 0.2s ease',
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.backgroundColor = '#e2e8f0';
              e.currentTarget.style.transform = 'translateY(-1px)';
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.backgroundColor = '#f1f5f9';
              e.currentTarget.style.transform = 'translateY(0)';
            }}
          >
            {showHistory ? '📊 Ocultar Historial' : '📚 Mostrar Historial'}
          </button>

          <button
            onClick={() => setShowCharts(!showCharts)}
            style={{
              backgroundColor: '#f1f5f9',
              color: '#475569',
              border: '1px solid #cbd5e1',
              padding: '12px 24px',
              borderRadius: '8px',
              fontSize: '16px',
              fontWeight: '600',
              cursor: 'pointer',
              transition: 'all 0.2s ease',
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.backgroundColor = '#e2e8f0';
              e.currentTarget.style.transform = 'translateY(-1px)';
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.backgroundColor = '#f1f5f9';
              e.currentTarget.style.transform = 'translateY(0)';
            }}
          >
            {showCharts ? '📈 Ocultar Gráficos' : '📈 Mostrar Gráficos'}
          </button>
        </div>

        {/* History Section */}
        {showHistory && (
          <div
            style={{
              backgroundColor: 'white',
              borderRadius: '16px',
              padding: '32px',
              boxShadow: '0 4px 6px rgba(0, 0, 0, 0.05)',
              border: '1px solid #e2e8f0',
            }}
          >
            <div
              style={{
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
                marginBottom: '24px',
              }}
            >
              <h2
                style={{
                  fontSize: '20px',
                  fontWeight: '600',
                  color: '#1e293b',
                  margin: '0',
                }}
              >
                📚 Historial de Análisis
              </h2>
              <button
                onClick={clearHistory}
                style={{
                  backgroundColor: '#fef2f2',
                  color: '#dc2626',
                  border: '1px solid #fecaca',
                  padding: '8px 16px',
                  borderRadius: '6px',
                  fontSize: '14px',
                  fontWeight: '600',
                  cursor: 'pointer',
                  transition: 'all 0.2s ease',
                }}
                onMouseEnter={(e) => {
                  e.currentTarget.style.backgroundColor = '#fee2e2';
                  e.currentTarget.style.transform = 'translateY(-1px)';
                }}
                onMouseLeave={(e) => {
                  e.currentTarget.style.backgroundColor = '#fef2f2';
                  e.currentTarget.style.transform = 'translateY(0)';
                }}
              >
                🗑️ Limpiar Todo
              </button>
            </div>

            {stats && (
              <div
                style={{
                  display: 'grid',
                  gridTemplateColumns: 'repeat(auto-fit, minmax(150px, 1fr))',
                  gap: '20px',
                  marginBottom: '24px',
                }}
              >
                <div
                  style={{
                    textAlign: 'center',
                    padding: '20px',
                    backgroundColor: '#f0f9ff',
                    borderRadius: '12px',
                    border: '1px solid #bae6fd',
                  }}
                >
                  <div
                    style={{
                      fontSize: '24px',
                      fontWeight: 'bold',
                      color: '#0369a1',
                      marginBottom: '8px',
                    }}
                  >
                    {stats.total_analyses}
                  </div>
                  <div style={{ fontSize: '14px', color: '#64748b' }}>
                    Total
                  </div>
                </div>

                <div
                  style={{
                    textAlign: 'center',
                    padding: '20px',
                    backgroundColor: '#f0fdf4',
                    borderRadius: '12px',
                    border: '1px solid #bbf7d0',
                  }}
                >
                  <div
                    style={{
                      fontSize: '24px',
                      fontWeight: 'bold',
                      color: '#16a34a',
                      marginBottom: '8px',
                    }}
                  >
                    {stats.safe_count}
                  </div>
                  <div style={{ fontSize: '14px', color: '#64748b' }}>
                    Seguros
                  </div>
                </div>

                <div
                  style={{
                    textAlign: 'center',
                    padding: '20px',
                    backgroundColor: '#fef2f2',
                    borderRadius: '12px',
                    border: '1px solid #fecaca',
                  }}
                >
                  <div
                    style={{
                      fontSize: '24px',
                      fontWeight: 'bold',
                      color: '#dc2626',
                      marginBottom: '8px',
                    }}
                  >
                    {stats.toxic_count}
                  </div>
                  <div style={{ fontSize: '14px', color: '#64748b' }}>
                    Tóxicos
                  </div>
                </div>

                <div
                  style={{
                    textAlign: 'center',
                    padding: '20px',
                    backgroundColor: '#faf5ff',
                    borderRadius: '12px',
                    border: '1px solid #ddd6fe',
                  }}
                >
                  <div
                    style={{
                      fontSize: '24px',
                      fontWeight: 'bold',
                      color: '#7c3aed',
                      marginBottom: '8px',
                    }}
                  >
                    {stats.average_score?.toFixed(2) || '0.00'}
                  </div>
                  <div style={{ fontSize: '14px', color: '#64748b' }}>
                    Score Promedio
                  </div>
                </div>
              </div>
            )}

            {historyLoading ? (
              <div style={{ textAlign: 'center', padding: '40px' }}>
                <div
                  style={{
                    display: 'inline-block',
                    width: '32px',
                    height: '32px',
                    border: '3px solid #e2e8f0',
                    borderTop: '3px solid #3b82f6',
                    borderRadius: '50%',
                    animation: 'spin 1s linear infinite',
                  }}
                />
                <div style={{ marginTop: '16px', color: '#64748b' }}>
                  ⏳ Cargando historial...
                </div>
              </div>
            ) : history.length > 0 ? (
              <div style={{ overflowX: 'auto' }}>
                <table style={{ width: '100%', borderCollapse: 'collapse' }}>
                  <thead>
                    <tr style={{ backgroundColor: '#f8fafc' }}>
                      <th
                        style={{
                          padding: '16px',
                          textAlign: 'left',
                          borderBottom: '1px solid #e2e8f0',
                          fontSize: '14px',
                          fontWeight: '600',
                          color: '#475569',
                        }}
                      >
                        Texto
                      </th>
                      <th
                        style={{
                          padding: '16px',
                          textAlign: 'center',
                          borderBottom: '1px solid #e2e8f0',
                          fontSize: '14px',
                          fontWeight: '600',
                          color: '#475569',
                        }}
                      >
                        Tóxico
                      </th>
                      <th
                        style={{
                          padding: '16px',
                          textAlign: 'center',
                          borderBottom: '1px solid #e2e8f0',
                          fontSize: '14px',
                          fontWeight: '600',
                          color: '#475569',
                        }}
                      >
                        Score
                      </th>
                      <th
                        style={{
                          padding: '16px',
                          textAlign: 'center',
                          borderBottom: '1px solid #e2e8f0',
                          fontSize: '14px',
                          fontWeight: '600',
                          color: '#475569',
                        }}
                      >
                        Fecha
                      </th>
                      <th
                        style={{
                          padding: '16px',
                          textAlign: 'center',
                          borderBottom: '1px solid #e2e8f0',
                          fontSize: '14px',
                          fontWeight: '600',
                          color: '#475569',
                        }}
                      >
                        Acciones
                      </th>
                    </tr>
                  </thead>
                  <tbody>
                    {history.map((item) => (
                      <tr
                        key={item.id}
                        style={{ borderBottom: '1px solid #f1f5f9' }}
                      >
                        <td style={{ padding: '16px', maxWidth: '300px' }}>
                          <div
                            style={{
                              overflow: 'hidden',
                              textOverflow: 'ellipsis',
                              whiteSpace: 'nowrap',
                              fontSize: '14px',
                              color: '#1e293b',
                            }}
                          >
                            {item.text}
                          </div>
                        </td>
                        <td style={{ padding: '16px', textAlign: 'center' }}>
                          <span
                            style={{
                              padding: '6px 12px',
                              borderRadius: '6px',
                              fontSize: '12px',
                              fontWeight: '600',
                              backgroundColor: item.result.toxic
                                ? '#fef2f2'
                                : '#f0fdf4',
                              color: item.result.toxic ? '#dc2626' : '#16a34a',
                            }}
                          >
                            {item.result.toxic ? '🚨 Tóxico' : '✅ Seguro'}
                          </span>
                        </td>
                        <td
                          style={{
                            padding: '16px',
                            textAlign: 'center',
                            fontSize: '14px',
                            color: '#1e293b',
                            fontWeight: '500',
                          }}
                        >
                          {item.result.toxicity_percentage}%
                        </td>
                        <td
                          style={{
                            padding: '16px',
                            textAlign: 'center',
                            fontSize: '14px',
                            color: '#64748b',
                          }}
                        >
                          {new Date(item.timestamp).toLocaleDateString()}
                        </td>
                        <td style={{ padding: '16px', textAlign: 'center' }}>
                          <button
                            onClick={() => deleteItem(item.id)}
                            style={{
                              backgroundColor: '#fef2f2',
                              color: '#dc2626',
                              border: '1px solid #fecaca',
                              padding: '8px 12px',
                              borderRadius: '6px',
                              fontSize: '12px',
                              fontWeight: '600',
                              cursor: 'pointer',
                              transition: 'all 0.2s ease',
                            }}
                            onMouseEnter={(e) => {
                              e.currentTarget.style.backgroundColor = '#fee2e2';
                              e.currentTarget.style.transform =
                                'translateY(-1px)';
                            }}
                            onMouseLeave={(e) => {
                              e.currentTarget.style.backgroundColor = '#fef2f2';
                              e.currentTarget.style.transform = 'translateY(0)';
                            }}
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
                  padding: '40px',
                  color: '#64748b',
                }}
              >
                📝 No hay análisis en el historial
              </div>
            )}
          </div>
        )}

        {/* Charts Section */}
        {showCharts && (
          <div
            style={{
              backgroundColor: 'white',
              borderRadius: '16px',
              padding: '32px',
              boxShadow: '0 4px 6px rgba(0, 0, 0, 0.05)',
              border: '1px solid #e2e8f0',
            }}
          >
            <h2
              style={{
                fontSize: '20px',
                fontWeight: '600',
                color: '#1e293b',
                margin: '0 0 24px 0',
              }}
            >
              📊 Visualizaciones
            </h2>

            <div
              style={{
                display: 'grid',
                gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
                gap: '32px',
                marginTop: '24px',
              }}
            >
              {stats && (
                <div>
                  <h3
                    style={{
                      fontSize: '18px',
                      fontWeight: '600',
                      color: '#1e293b',
                      marginBottom: '16px',
                    }}
                  >
                    Distribución General
                  </h3>
                  <div style={{ height: '250px' }}>
                    <ToxicityPieChart stats={stats} />
                  </div>
                </div>
              )}

              {history.length > 0 && (
                <>
                  <div>
                    <h3
                      style={{
                        fontSize: '18px',
                        fontWeight: '600',
                        color: '#1e293b',
                        marginBottom: '16px',
                      }}
                    >
                      Distribución de Scores
                    </h3>
                    <div style={{ height: '250px' }}>
                      <ToxicityDistributionChart history={history} />
                    </div>
                  </div>

                  <div>
                    <h3
                      style={{
                        fontSize: '18px',
                        fontWeight: '600',
                        color: '#1e293b',
                        marginBottom: '16px',
                      }}
                    >
                      Análisis por Categoría
                    </h3>
                    <div style={{ height: '250px' }}>
                      <CategoriesChart history={history} />
                    </div>
                  </div>
                </>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default App;
