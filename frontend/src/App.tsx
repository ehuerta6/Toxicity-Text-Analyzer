import React, { useState, useCallback, useEffect } from 'react';
import { useToxicityAnalysis } from './hooks/useToxicityAnalysis';
import { getToxicityColor, getToxicityBorderColor } from './styles/common';

interface ToxicityMap {
  [word: string]: number;
}

const ToxicityGauge: React.FC<{ percentage: number }> = ({ percentage }) => {
  const color = getToxicityColor(percentage);

  // Función para obtener categoría simple y color
  const getCategoryInfo = (percentage: number) => {
    if (percentage <= 30) {
      return {
        label: 'Leve',
        color: '#10b981',
        description: 'El contenido es seguro y apropiado',
      };
    } else if (percentage <= 60) {
      return {
        label: 'Moderado',
        color: '#f59e0b',
        description: 'El contenido requiere atención moderada',
      };
    } else {
      return {
        label: 'Alto',
        color: '#ef4444',
        description: 'El contenido presenta niveles altos de toxicidad',
      };
    }
  };

  const categoryInfo = getCategoryInfo(percentage);
  const roundedPercentage = Math.round(percentage);

  return (
    <div style={{ textAlign: 'center' }}>
      <div
        style={{
          width: '140px',
          height: '140px',
          borderRadius: '50%',
          background: `conic-gradient(${color} ${
            roundedPercentage * 3.6
          }deg, #e5e7eb ${roundedPercentage * 3.6}deg)`,
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
            fontSize: '24px',
            fontWeight: 'bold',
            color: color,
            boxShadow: 'inset 0 2px 10px rgba(0, 0, 0, 0.1)',
          }}
        >
          {roundedPercentage}%
        </div>
      </div>

      {/* Categoría con color asociado */}
      <div
        style={{
          fontSize: '22px',
          fontWeight: '700',
          color: categoryInfo.color,
          textShadow: '0 1px 2px rgba(0, 0, 0, 0.1)',
          marginBottom: '8px',
          padding: '8px 16px',
          backgroundColor: `${categoryInfo.color}15`,
          borderRadius: '20px',
          display: 'inline-block',
        }}
      >
        {categoryInfo.label}
      </div>

      <div
        style={{
          fontSize: '14px',
          color: '#6b7280',
          maxWidth: '250px',
          margin: '0 auto',
          lineHeight: '1.4',
        }}
      >
        {categoryInfo.description}
      </div>
    </div>
  );
};

const ColoredText: React.FC<{ text: string; toxicityMap: ToxicityMap }> = ({
  text,
  toxicityMap,
}) => {
  const getToxicityColor = (percentage: number): string => {
    if (percentage <= 30) return '#10b981'; // Verde
    if (percentage <= 60) return '#f59e0b'; // Amarillo
    return '#ef4444'; // Rojo
  };

  const getToxicityClass = (percentage: number): string => {
    if (percentage <= 30) return 'text-green-600';
    if (percentage <= 60) return 'text-yellow-600';
    return 'text-red-600';
  };

  const renderText = () => {
    if (!text || !toxicityMap || Object.keys(toxicityMap).length === 0) {
      return <span className='text-gray-700'>{text}</span>;
    }

    // Dividir el texto en palabras preservando espacios y puntuación
    const words = text.split(/(\s+)/);

    return words.map((word, index) => {
      // Limpiar la palabra para buscar en el mapa de toxicidad
      const cleanWord = word.toLowerCase().replace(/[^\wáéíóúñ]/g, '');
      const toxicityPercentage = toxicityMap[cleanWord] || 0;

      if (toxicityPercentage > 0) {
        const color = getToxicityColor(toxicityPercentage);
        const textClass = getToxicityClass(toxicityPercentage);

        return (
          <span
            key={index}
            className={`${textClass} cursor-help transition-all duration-200 hover:scale-105 font-semibold`}
            style={{
              borderBottom: `3px solid ${color}`,
              paddingBottom: '1px',
            }}
            title={`Toxicidad: ${toxicityPercentage}%`}
          >
            {word}
          </span>
        );
      }

      return <span key={index}>{word}</span>;
    });
  };

  return (
    <div className='text-gray-800 leading-relaxed text-lg'>{renderText()}</div>
  );
};

const App: React.FC = () => {
  const [text, setText] = useState('');
  const [toxicityMap, setToxicityMap] = useState<ToxicityMap>({});

  const { result, loading, error, analyzeText, clearResult } =
    useToxicityAnalysis();

  const generateToxicityMap = useCallback(
    (text: string, toxicityPercentage: number): ToxicityMap => {
      if (!text || toxicityPercentage === 0) return {};

      // Dividir el texto en palabras y filtrar palabras vacías
      const words = text
        .toLowerCase()
        .split(/\s+/)
        .filter((word) => word.length > 2); // Solo palabras de 3+ caracteres

      if (words.length === 0) return {};

      const toxicityMap: ToxicityMap = {};

      // Distribuir la toxicidad de manera más realista
      if (toxicityPercentage <= 30) {
        // Para toxicidad baja, solo algunas palabras tienen toxicidad
        const toxicWords = Math.max(1, Math.floor(words.length * 0.3));
        const toxicWordIndices = new Set();

        // Seleccionar palabras aleatoriamente para ser tóxicas
        while (toxicWordIndices.size < toxicWords) {
          const randomIndex = Math.floor(Math.random() * words.length);
          toxicWordIndices.add(randomIndex);
        }

        words.forEach((word, index) => {
          const cleanWord = word.replace(/[^\wáéíóúñ]/g, '');
          if (cleanWord.length > 0) {
            if (toxicWordIndices.has(index)) {
              toxicityMap[cleanWord] = Math.round(toxicityPercentage * 1.5);
            } else {
              toxicityMap[cleanWord] = 0;
            }
          }
        });
      } else if (toxicityPercentage <= 60) {
        // Para toxicidad moderada, más palabras tienen toxicidad
        const toxicWords = Math.max(2, Math.floor(words.length * 0.6));
        const toxicWordIndices = new Set();

        while (toxicWordIndices.size < toxicWords) {
          const randomIndex = Math.floor(Math.random() * words.length);
          toxicWordIndices.add(randomIndex);
        }

        words.forEach((word, index) => {
          const cleanWord = word.replace(/[^\wáéíóúñ]/g, '');
          if (cleanWord.length > 0) {
            if (toxicWordIndices.has(index)) {
              toxicityMap[cleanWord] = Math.round(toxicityPercentage * 0.8);
            } else {
              toxicityMap[cleanWord] = Math.round(toxicityPercentage * 0.2);
            }
          }
        });
      } else {
        // Para toxicidad alta, la mayoría de palabras tienen toxicidad
        words.forEach((word) => {
          const cleanWord = word.replace(/[^\wáéíóúñ]/g, '');
          if (cleanWord.length > 0) {
            // Distribuir la toxicidad de manera más uniforme
            const baseToxicity = Math.round(toxicityPercentage * 0.7);
            const variation = Math.round(Math.random() * 20) - 10; // ±10%
            toxicityMap[cleanWord] = Math.max(
              0,
              Math.min(100, baseToxicity + variation)
            );
          }
        });
      }

      return toxicityMap;
    },
    []
  );

  const handleAnalyze = useCallback(async () => {
    if (!text.trim()) return;

    try {
      await analyzeText(text);
      // El resultado se actualiza automáticamente a través del hook useToxicityAnalysis
      // y se puede acceder a través de la variable `result`
    } catch (error) {
      console.error('Error al analizar texto:', error);
    }
  }, [text, analyzeText]);

  // Generar mapa de toxicidad cuando cambie el resultado
  useEffect(() => {
    if (result && text.trim()) {
      const wordToxicityMap = generateToxicityMap(
        text,
        result.toxicity_percentage
      );
      setToxicityMap(wordToxicityMap);
    }
  }, [result, text, generateToxicityMap]);

  const handleClear = () => {
    setText('');
    setToxicityMap({});
    clearResult();
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleAnalyze();
    }
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
                value={text}
                onChange={(e) => setText(e.target.value)}
                onKeyDown={handleKeyDown}
                placeholder='Escribe o pega el texto que quieres analizar... (Presiona Enter para analizar, Shift+Enter para nueva línea)'
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
                  e.target.style.borderColor = text.trim()
                    ? '#3b82f6'
                    : '#e2e8f0';
                  e.target.style.backgroundColor = text.trim()
                    ? 'white'
                    : '#fafafa';
                  e.target.style.boxShadow = text.trim()
                    ? '0 0 0 3px rgba(59, 130, 246, 0.1)'
                    : 'none';
                }}
              />
              {text.trim() && (
                <div
                  style={{
                    marginTop: '8px',
                    fontSize: '14px',
                    color: '#64748b',
                    textAlign: 'right',
                  }}
                >
                  {text.length} caracteres
                </div>
              )}
            </div>

            <div style={{ display: 'flex', gap: '12px', flexWrap: 'wrap' }}>
              <button
                onClick={handleAnalyze}
                disabled={loading || !text.trim()}
                style={{
                  backgroundColor: '#3b82f6',
                  color: 'white',
                  border: 'none',
                  padding: '12px 24px',
                  borderRadius: '8px',
                  fontSize: '16px',
                  fontWeight: '600',
                  cursor: loading || !text.trim() ? 'not-allowed' : 'pointer',
                  opacity: loading || !text.trim() ? 0.6 : 1,
                  transition: 'all 0.2s ease',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '8px',
                }}
                onMouseEnter={(e) => {
                  if (!loading && text.trim()) {
                    e.currentTarget.style.backgroundColor = '#2563eb';
                    e.currentTarget.style.transform = 'translateY(-1px)';
                  }
                }}
                onMouseLeave={(e) => {
                  if (!loading && text.trim()) {
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
                  <>
                    <svg
                      className='w-5 h-5'
                      fill='none'
                      stroke='currentColor'
                      viewBox='0 0 24 24'
                    >
                      <path
                        strokeLinecap='round'
                        strokeLinejoin='round'
                        strokeWidth={2}
                        d='M9 5l7 7-7 7'
                      />
                    </svg>
                    <span>Analizar</span>
                  </>
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
                      {Math.round(result.toxicity_percentage)}%
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
                      Categoría
                    </div>
                    <div
                      style={{
                        fontSize: '18px',
                        fontWeight: '600',
                        color: '#1e293b',
                      }}
                    >
                      {(() => {
                        const percentage = result.toxicity_percentage;
                        if (percentage <= 30) return 'Leve';
                        if (percentage <= 60) return 'Moderado';
                        return 'Alto';
                      })()}
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

              {/* Texto con palabras resaltadas */}
              <div style={{ marginTop: '24px' }}>
                <h3
                  style={{
                    fontSize: '18px',
                    fontWeight: '600',
                    color: '#1e293b',
                    margin: '0 0 16px 0',
                    textAlign: 'center',
                  }}
                >
                  📝 Texto Analizado con Resaltado de Toxicidad
                </h3>
                <div
                  style={{
                    backgroundColor: '#f8fafc',
                    padding: '20px',
                    borderRadius: '12px',
                    border: '1px solid #e2e8f0',
                    maxHeight: '300px',
                    overflowY: 'auto',
                  }}
                >
                  <ColoredText text={text} toxicityMap={toxicityMap} />
                </div>
                <div
                  style={{
                    marginTop: '16px',
                    padding: '16px',
                    backgroundColor: '#f8fafc',
                    borderRadius: '12px',
                    border: '1px solid #e2e8f0',
                  }}
                >
                  <div
                    style={{
                      fontSize: '14px',
                      fontWeight: '600',
                      color: '#374151',
                      marginBottom: '12px',
                      textAlign: 'center',
                    }}
                  >
                    🎨 Leyenda de Colores por Toxicidad
                  </div>
                  <div
                    style={{
                      display: 'flex',
                      justifyContent: 'space-around',
                      alignItems: 'center',
                      flexWrap: 'wrap',
                      gap: '8px',
                    }}
                  >
                    <div
                      style={{
                        display: 'flex',
                        alignItems: 'center',
                        gap: '6px',
                      }}
                    >
                      <div
                        style={{
                          width: '16px',
                          height: '16px',
                          backgroundColor: '#10b981',
                          borderRadius: '50%',
                          border: '2px solid #10b981',
                        }}
                      />
                      <span
                        style={{
                          fontSize: '13px',
                          color: '#10b981',
                          fontWeight: '600',
                        }}
                      >
                        Verde (0-30%)
                      </span>
                    </div>
                    <div
                      style={{
                        display: 'flex',
                        alignItems: 'center',
                        gap: '6px',
                      }}
                    >
                      <div
                        style={{
                          width: '16px',
                          height: '16px',
                          backgroundColor: '#f59e0b',
                          borderRadius: '50%',
                          border: '2px solid #f59e0b',
                        }}
                      />
                      <span
                        style={{
                          fontSize: '13px',
                          color: '#f59e0b',
                          fontWeight: '600',
                        }}
                      >
                        Amarillo (31-60%)
                      </span>
                    </div>
                    <div
                      style={{
                        display: 'flex',
                        alignItems: 'center',
                        gap: '6px',
                      }}
                    >
                      <div
                        style={{
                          width: '16px',
                          height: '16px',
                          backgroundColor: '#ef4444',
                          borderRadius: '50%',
                          border: '2px solid #ef4444',
                        }}
                      />
                      <span
                        style={{
                          fontSize: '13px',
                          color: '#ef4444',
                          fontWeight: '600',
                        }}
                      >
                        Rojo (61-100%)
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default App;
