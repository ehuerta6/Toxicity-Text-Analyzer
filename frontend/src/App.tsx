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
  getToxicityBackgroundColor,
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
    <div style={{ minHeight: '100vh', backgroundColor: '#f9fafb' }}>
      <div style={commonStyles.container}>
        {/* Header */}
        <header style={{ textAlign: 'center', marginBottom: '32px' }}>
          <h1 style={commonStyles.text.heading}>🛡️ ToxiGuard</h1>
          <p style={commonStyles.text.body}>
            Detección inteligente de contenido tóxico usando Machine Learning
          </p>
        </header>

        {/* Main Content Grid */}
        <div
          style={{
            display: 'grid',
            gridTemplateColumns: result ? '1fr 1fr' : '1fr',
            gap: '24px',
            marginBottom: '32px',
          }}
        >
          {/* Input Form */}
          <div style={commonStyles.card}>
            <h2 style={commonStyles.text.subheading}>📝 Analizar Texto</h2>
            <div style={{ marginBottom: '16px' }}>
              <textarea
                value={inputText}
                onChange={(e) => setInputText(e.target.value)}
                placeholder='Ingresa el texto que quieres analizar...'
                style={{
                  ...commonStyles.input,
                  minHeight: '120px',
                  resize: 'vertical',
                  fontFamily: 'inherit',
                  backgroundColor: '#fafafa',
                  borderColor: inputText.trim() ? '#3b82f6' : '#e5e7eb',
                  boxShadow: inputText.trim()
                    ? '0 0 0 3px rgba(59, 130, 246, 0.1)'
                    : 'none',
                }}
                onFocus={(e) => {
                  e.target.style.borderColor = '#3b82f6';
                  e.target.style.boxShadow =
                    '0 0 0 3px rgba(59, 130, 246, 0.1)';
                  e.target.style.backgroundColor = 'white';
                }}
                onBlur={(e) => {
                  e.target.style.borderColor = inputText.trim()
                    ? '#3b82f6'
                    : '#e5e7eb';
                  e.target.style.boxShadow = inputText.trim()
                    ? '0 0 0 3px rgba(59, 130, 246, 0.1)'
                    : 'none';
                  e.target.style.backgroundColor = inputText.trim()
                    ? 'white'
                    : '#fafafa';
                }}
              />
              {inputText.trim() && (
                <div
                  style={{
                    marginTop: '8px',
                    fontSize: '12px',
                    color: '#6b7280',
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
                  ...commonStyles.button.primary,
                  opacity: loading || !inputText.trim() ? 0.6 : 1,
                  position: 'relative',
                  transform:
                    loading || !inputText.trim() ? 'none' : 'translateY(0)',
                  boxShadow:
                    loading || !inputText.trim()
                      ? 'none'
                      : '0 4px 6px rgba(0, 0, 0, 0.1)',
                }}
                onMouseEnter={(e) => {
                  if (!loading && inputText.trim()) {
                    e.currentTarget.style.transform = 'translateY(-2px)';
                    e.currentTarget.style.boxShadow =
                      '0 6px 20px rgba(59, 130, 246, 0.3)';
                  }
                }}
                onMouseLeave={(e) => {
                  if (!loading && inputText.trim()) {
                    e.currentTarget.style.transform = 'translateY(0)';
                    e.currentTarget.style.boxShadow =
                      '0 4px 6px rgba(0, 0, 0, 0.1)';
                  }
                }}
              >
                {loading ? (
                  <>
                    <div
                      style={{
                        display: 'inline-block',
                        width: '16px',
                        height: '16px',
                        border: '2px solid transparent',
                        borderTop: '2px solid white',
                        borderRadius: '50%',
                        animation: 'spin 1s linear infinite',
                        marginRight: '8px',
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
                  ...commonStyles.button.secondary,
                  transform: 'translateY(0)',
                  boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)',
                }}
                onMouseEnter={(e) => {
                  e.currentTarget.style.transform = 'translateY(-2px)';
                  e.currentTarget.style.boxShadow =
                    '0 6px 20px rgba(107, 114, 128, 0.3)';
                }}
                onMouseLeave={(e) => {
                  e.currentTarget.style.transform = 'translateY(0)';
                  e.currentTarget.style.boxShadow =
                    '0 4px 6px rgba(0, 0, 0, 0.1)';
                }}
              >
                🗑️ Limpiar
              </button>
            </div>
            {error && (
              <div
                style={{
                  marginTop: '16px',
                  color: commonStyles.toxicity.toxic,
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

          {/* Results */}
          {result && (
            <div
              style={{
                ...commonStyles.card,
                backgroundColor: getToxicityBackgroundColor(
                  result.toxicity_percentage
                ),
                borderColor: getToxicityBorderColor(result.toxicity_percentage),
                borderWidth: '2px',
              }}
            >
              <h2 style={commonStyles.text.subheading}>
                📊 Resultados del Análisis
              </h2>
              <div style={{ marginBottom: '24px' }}>
                <ToxicityGauge percentage={result.toxicity_percentage} />
              </div>

              {/* Enhanced Results Display */}
              <div
                style={{
                  backgroundColor: 'white',
                  padding: '16px',
                  borderRadius: '8px',
                  border: '1px solid #e2e8f0',
                  boxShadow: '0 2px 4px rgba(0, 0, 0, 0.05)',
                }}
              >
                <div
                  style={{
                    display: 'grid',
                    gridTemplateColumns: 'repeat(auto-fit, minmax(120px, 1fr))',
                    gap: '12px',
                    marginBottom: '16px',
                  }}
                >
                  <div style={{ textAlign: 'center' }}>
                    <div
                      style={{
                        fontSize: '12px',
                        color: '#6b7280',
                        marginBottom: '4px',
                      }}
                    >
                      Score
                    </div>
                    <div
                      style={{
                        fontSize: '18px',
                        fontWeight: '600',
                        color: '#1f2937',
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
                          color: '#6b7280',
                          marginBottom: '4px',
                        }}
                      >
                        Categoría
                      </div>
                      <div
                        style={{
                          fontSize: '18px',
                          fontWeight: '600',
                          color: '#1f2937',
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
                        color: '#6b7280',
                        marginBottom: '4px',
                      }}
                    >
                      Modelo
                    </div>
                    <div
                      style={{
                        fontSize: '18px',
                        fontWeight: '600',
                        color: '#1f2937',
                      }}
                    >
                      {result.model_used}
                    </div>
                  </div>
                  <div style={{ textAlign: 'center' }}>
                    <div
                      style={{
                        fontSize: '12px',
                        color: '#6b7280',
                        marginBottom: '4px',
                      }}
                    >
                      Tiempo
                    </div>
                    <div
                      style={{
                        fontSize: '18px',
                        fontWeight: '600',
                        color: '#1f2937',
                      }}
                    >
                      {result.response_time_ms}ms
                    </div>
                  </div>
                </div>

                <div
                  style={{
                    fontSize: '14px',
                    color: '#6b7280',
                    textAlign: 'center',
                    padding: '8px',
                    backgroundColor: '#f8fafc',
                    borderRadius: '6px',
                    border: '1px solid #e5e7eb',
                  }}
                >
                  Analizado el {new Date(result.timestamp).toLocaleString()}
                </div>
              </div>
            </div>
          )}
        </div>

        {/* History and Charts Toggle */}
        <div style={{ textAlign: 'center', marginBottom: '24px' }}>
          <button
            onClick={() => setShowHistory(!showHistory)}
            style={{
              ...commonStyles.button.secondary,
              marginRight: '12px',
              transform: 'translateY(0)',
              boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)',
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.transform = 'translateY(-2px)';
              e.currentTarget.style.boxShadow =
                '0 6px 20px rgba(107, 114, 128, 0.3)';
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.transform = 'translateY(0)';
              e.currentTarget.style.boxShadow = '0 4px 6px rgba(0, 0, 0, 0.1)';
            }}
          >
            {showHistory ? '📊 Ocultar Historial' : '📚 Mostrar Historial'}
          </button>
          <button
            onClick={() => setShowCharts(!showCharts)}
            style={{
              ...commonStyles.button.secondary,
              transform: 'translateY(0)',
              boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)',
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.transform = 'translateY(-2px)';
              e.currentTarget.style.boxShadow =
                '0 6px 20px rgba(107, 114, 128, 0.3)';
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.transform = 'translateY(0)';
              e.currentTarget.style.boxShadow = '0 4px 6px rgba(0, 0, 0, 0.1)';
            }}
          >
            {showCharts ? '📈 Ocultar Gráficos' : '📈 Mostrar Gráficos'}
          </button>
        </div>

        {/* History Section */}
        {showHistory && (
          <div style={commonStyles.card}>
            <div
              style={{
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
                marginBottom: '24px',
              }}
            >
              <h2 style={commonStyles.text.subheading}>
                📚 Historial de Análisis
              </h2>
              <button
                onClick={clearHistory}
                style={{
                  ...commonStyles.button.danger,
                  transform: 'translateY(0)',
                  boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)',
                }}
                onMouseEnter={(e) => {
                  e.currentTarget.style.transform = 'translateY(-2px)';
                  e.currentTarget.style.boxShadow =
                    '0 6px 20px rgba(239, 68, 68, 0.3)';
                }}
                onMouseLeave={(e) => {
                  e.currentTarget.style.transform = 'translateY(0)';
                  e.currentTarget.style.boxShadow =
                    '0 4px 6px rgba(0, 0, 0, 0.1)';
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
                  gap: '16px',
                  marginBottom: '24px',
                }}
              >
                <div
                  style={{
                    textAlign: 'center',
                    padding: '16px',
                    backgroundColor: '#f3f4f6',
                    borderRadius: '8px',
                  }}
                >
                  <div
                    style={{
                      fontSize: '24px',
                      fontWeight: 'bold',
                      color: '#3b82f6',
                    }}
                  >
                    {stats.total_analyses}
                  </div>
                  <div style={{ fontSize: '14px', color: '#6b7280' }}>
                    Total
                  </div>
                </div>
                <div
                  style={{
                    textAlign: 'center',
                    padding: '16px',
                    backgroundColor: '#f3f4f6',
                    borderRadius: '8px',
                  }}
                >
                  <div
                    style={{
                      fontSize: '24px',
                      fontWeight: 'bold',
                      color: commonStyles.toxicity.safe,
                    }}
                  >
                    {stats.safe_count}
                  </div>
                  <div style={{ fontSize: '14px', color: '#6b7280' }}>
                    Seguros
                  </div>
                </div>
                <div
                  style={{
                    textAlign: 'center',
                    padding: '16px',
                    backgroundColor: '#f3f4f6',
                    borderRadius: '8px',
                  }}
                >
                  <div
                    style={{
                      fontSize: '24px',
                      fontWeight: 'bold',
                      color: commonStyles.toxicity.toxic,
                    }}
                  >
                    {stats.toxic_count}
                  </div>
                  <div style={{ fontSize: '14px', color: '#6b7280' }}>
                    Tóxicos
                  </div>
                </div>
                <div
                  style={{
                    textAlign: 'center',
                    padding: '16px',
                    backgroundColor: '#f3f4f6',
                    borderRadius: '8px',
                  }}
                >
                  <div
                    style={{
                      fontSize: '24px',
                      fontWeight: 'bold',
                      color: '#8b5cf6',
                    }}
                  >
                    {stats.average_score?.toFixed(2) || '0.00'}
                  </div>
                  <div style={{ fontSize: '14px', color: '#6b7280' }}>
                    Score Promedio
                  </div>
                </div>
              </div>
            )}

            {historyLoading ? (
              <div style={{ textAlign: 'center', padding: '40px' }}>
                ⏳ Cargando historial...
              </div>
            ) : history.length > 0 ? (
              <div style={{ overflowX: 'auto' }}>
                <table style={{ width: '100%', borderCollapse: 'collapse' }}>
                  <thead>
                    <tr style={{ backgroundColor: '#f9fafb' }}>
                      <th
                        style={{
                          padding: '12px',
                          textAlign: 'left',
                          borderBottom: '1px solid #e5e7eb',
                        }}
                      >
                        Texto
                      </th>
                      <th
                        style={{
                          padding: '12px',
                          textAlign: 'center',
                          borderBottom: '1px solid #e5e7eb',
                        }}
                      >
                        Tóxico
                      </th>
                      <th
                        style={{
                          padding: '12px',
                          textAlign: 'center',
                          borderBottom: '1px solid #e5e7eb',
                        }}
                      >
                        Score
                      </th>
                      <th
                        style={{
                          padding: '12px',
                          textAlign: 'center',
                          borderBottom: '1px solid #e5e7eb',
                        }}
                      >
                        Fecha
                      </th>
                      <th
                        style={{
                          padding: '12px',
                          textAlign: 'center',
                          borderBottom: '1px solid #e5e7eb',
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
                        style={{ borderBottom: '1px solid #f3f4f6' }}
                      >
                        <td style={{ padding: '12px', maxWidth: '300px' }}>
                          <div
                            style={{
                              overflow: 'hidden',
                              textOverflow: 'ellipsis',
                              whiteSpace: 'nowrap',
                            }}
                          >
                            {item.text}
                          </div>
                        </td>
                        <td style={{ padding: '12px', textAlign: 'center' }}>
                          <span
                            style={{
                              padding: '4px 8px',
                              borderRadius: '4px',
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
                        <td style={{ padding: '12px', textAlign: 'center' }}>
                          {item.result.toxicity_percentage}%
                        </td>
                        <td
                          style={{
                            padding: '12px',
                            textAlign: 'center',
                            fontSize: '14px',
                          }}
                        >
                          {new Date(item.timestamp).toLocaleDateString()}
                        </td>
                        <td style={{ padding: '12px', textAlign: 'center' }}>
                          <button
                            onClick={() => deleteItem(item.id)}
                            style={{
                              ...commonStyles.button.danger,
                              padding: '6px 12px',
                              fontSize: '12px',
                              transform: 'translateY(0)',
                              boxShadow: '0 2px 4px rgba(0, 0, 0, 0.1)',
                            }}
                            onMouseEnter={(e) => {
                              e.currentTarget.style.transform =
                                'translateY(-1px)';
                              e.currentTarget.style.boxShadow =
                                '0 4px 12px rgba(239, 68, 68, 0.3)';
                            }}
                            onMouseLeave={(e) => {
                              e.currentTarget.style.transform = 'translateY(0)';
                              e.currentTarget.style.boxShadow =
                                '0 2px 4px rgba(0, 0, 0, 0.1)';
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
                  color: '#6b7280',
                }}
              >
                📝 No hay análisis en el historial
              </div>
            )}
          </div>
        )}

        {/* Charts Section */}
        {showCharts && (
          <div style={commonStyles.card}>
            <h2 style={commonStyles.text.subheading}>📊 Visualizaciones</h2>
            <div
              style={{
                display: 'grid',
                gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
                gap: '24px',
                marginTop: '24px',
              }}
            >
              {stats && (
                <div>
                  <h3
                    style={{
                      ...commonStyles.text.subheading,
                      fontSize: '18px',
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
                        ...commonStyles.text.subheading,
                        fontSize: '18px',
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
                        ...commonStyles.text.subheading,
                        fontSize: '18px',
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
