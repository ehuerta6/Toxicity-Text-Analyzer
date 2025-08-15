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
          width: '120px',
          height: '120px',
          borderRadius: '50%',
          background: `conic-gradient(${color} ${
            percentage * 3.6
          }deg, #e5e7eb ${percentage * 3.6}deg)`,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          margin: '0 auto 16px',
          position: 'relative',
        }}
      >
        <div
          style={{
            width: '80px',
            height: '80px',
            borderRadius: '50%',
            backgroundColor: 'white',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            fontSize: '18px',
            fontWeight: 'bold',
            color: color,
          }}
        >
          {percentage}%
        </div>
      </div>
      <div style={{ fontSize: '18px', fontWeight: '600', color: color }}>
        {label}
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
      await analyzeText(inputText);
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
                }}
              />
            </div>
            <div style={{ display: 'flex', gap: '12px', flexWrap: 'wrap' }}>
              <button
                onClick={handleAnalyze}
                disabled={loading || !inputText.trim()}
                style={{
                  ...commonStyles.button.primary,
                  opacity: loading || !inputText.trim() ? 0.6 : 1,
                }}
              >
                {loading ? '⏳ Analizando...' : '🔍 Analizar'}
              </button>
              <button
                onClick={handleClear}
                style={commonStyles.button.secondary}
              >
                🗑️ Limpiar
              </button>
            </div>
            {error && (
              <div
                style={{
                  marginTop: '16px',
                  color: commonStyles.toxicity.toxic,
                }}
              >
                ❌ {error}
              </div>
            )}
          </div>

          {/* Results */}
          {result && (
            <div style={commonStyles.card}>
              <h2 style={commonStyles.text.subheading}>
                📊 Resultados del Análisis
              </h2>
              <div style={{ marginBottom: '24px' }}>
                <ToxicityGauge percentage={result.toxicity_percentage} />
              </div>
              <div style={{ marginBottom: '16px' }}>
                <strong>Score:</strong> {result.score.toFixed(3)}
              </div>
              {result.category && (
                <div style={{ marginBottom: '16px' }}>
                  <strong>Categoría:</strong> {result.category}
                </div>
              )}
              <div style={{ marginBottom: '16px' }}>
                <strong>Modelo usado:</strong> {result.model_used}
              </div>
              <div style={{ marginBottom: '16px' }}>
                <strong>Tiempo de respuesta:</strong> {result.response_time_ms}
                ms
              </div>
              <div style={{ fontSize: '14px', color: '#6b7280' }}>
                Analizado el {new Date(result.timestamp).toLocaleString()}
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
            }}
          >
            {showHistory ? '📊 Ocultar Historial' : '📚 Mostrar Historial'}
          </button>
          <button
            onClick={() => setShowCharts(!showCharts)}
            style={commonStyles.button.secondary}
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
              <button onClick={clearHistory} style={commonStyles.button.danger}>
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
                            style={commonStyles.button.danger}
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
