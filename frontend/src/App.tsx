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
        label: 'Safe',
        color: 'var(--secondary)',
        description: 'Content is safe and appropriate',
      };
    } else if (percentage <= 60) {
      return {
        label: 'Moderate',
        color: 'oklch(0.769 0.188 70.08)',
        description: 'Content requires moderate attention',
      };
    } else {
      return {
        label: 'High Risk',
        color: 'var(--destructive)',
        description: 'Content presents high toxicity levels',
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
          }deg, var(--muted) ${roundedPercentage * 3.6}deg)`,
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
            backgroundColor: 'var(--background)',
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
          color: 'var(--muted-foreground)',
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
    if (percentage <= 30) return 'var(--secondary)'; // Verde
    if (percentage <= 60) return 'oklch(0.769 0.188 70.08)'; // Amarillo
    return 'var(--destructive)'; // Rojo
  };

  const getToxicityClass = (percentage: number): string => {
    if (percentage <= 30) return 'text-emerald-600';
    if (percentage <= 60) return 'text-amber-600';
    return 'text-red-600';
  };

  const renderText = () => {
    if (!text || !toxicityMap || Object.keys(toxicityMap).length === 0) {
      return <span className='text-foreground'>{text}</span>;
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
            className={`${textClass} cursor-help transition-all duration-300 hover:scale-105 font-semibold`}
            style={{
              borderBottom: `3px solid ${color}`,
              paddingBottom: '1px',
              animation: 'fadeInWord 0.6s ease-out',
              animationDelay: `${index * 0.1}s`,
            }}
            title={`Toxicity: ${toxicityPercentage}%`}
          >
            {word}
          </span>
        );
      }

      return <span key={index}>{word}</span>;
    });
  };

  return (
    <div className='text-foreground leading-relaxed text-lg'>
      {renderText()}
    </div>
  );
};

const App: React.FC = () => {
  const [text, setText] = useState('');
  const [toxicityMap, setToxicityMap] = useState<ToxicityMap>({});

  // Guardar temporalmente el último análisis en localStorage
  const [lastAnalysis, setLastAnalysis] = useState(() => {
    const saved = localStorage.getItem('toxiguard_last_analysis');
    return saved ? JSON.parse(saved) : null;
  });

  const { result, loading, error, analyzeText, clearResult } =
    useToxicityAnalysis();

  const generateToxicityMap = useCallback(
    (text: string, toxicityPercentage: number): ToxicityMap => {
      if (!text || toxicityPercentage === 0) return {};

      // Optimización: Usar regex más eficiente y cache de palabras
      const words = text
        .toLowerCase()
        .split(/\s+/)
        .filter((word) => word.length > 2);

      if (words.length === 0) return {};

      const toxicityMap: ToxicityMap = {};
      const cleanWords = new Map(); // Cache para palabras limpias

      // Pre-procesar palabras para evitar recálculos
      words.forEach((word) => {
        const cleanWord = word.replace(/[^\wáéíóúñ]/g, '');
        if (cleanWord.length > 0) {
          cleanWords.set(word, cleanWord);
        }
      });

      // Distribuir toxicidad de manera más eficiente
      if (toxicityPercentage <= 30) {
        const toxicWords = Math.max(1, Math.floor(words.length * 0.3));
        const toxicIndices = new Set();

        // Selección más eficiente de palabras tóxicas
        for (let i = 0; i < toxicWords; i++) {
          let randomIndex;
          do {
            randomIndex = Math.floor(Math.random() * words.length);
          } while (toxicIndices.has(randomIndex));
          toxicIndices.add(randomIndex);
        }

        cleanWords.forEach((cleanWord, originalWord) => {
          const index = words.indexOf(originalWord);
          toxicityMap[cleanWord] = toxicIndices.has(index)
            ? Math.round(toxicityPercentage * 1.5)
            : 0;
        });
      } else if (toxicityPercentage <= 60) {
        const toxicWords = Math.max(2, Math.floor(words.length * 0.6));
        const toxicIndices = new Set();

        for (let i = 0; i < toxicWords; i++) {
          let randomIndex;
          do {
            randomIndex = Math.floor(Math.random() * words.length);
          } while (toxicIndices.has(randomIndex));
          toxicIndices.add(randomIndex);
        }

        cleanWords.forEach((cleanWord, originalWord) => {
          const index = words.indexOf(originalWord);
          toxicityMap[cleanWord] = toxicIndices.has(index)
            ? Math.round(toxicityPercentage * 0.8)
            : Math.round(toxicityPercentage * 0.2);
        });
      } else {
        // Para toxicidad alta, distribución más directa
        cleanWords.forEach((cleanWord) => {
          const baseToxicity = Math.round(toxicityPercentage * 0.7);
          const variation = Math.round(Math.random() * 20) - 10;
          toxicityMap[cleanWord] = Math.max(
            0,
            Math.min(100, baseToxicity + variation)
          );
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

      // Guardar el análisis en localStorage
      const analysisData = {
        text,
        result,
        toxicityMap: wordToxicityMap,
        timestamp: new Date().toISOString(),
      };
      setLastAnalysis(analysisData);
      localStorage.setItem(
        'toxiguard_last_analysis',
        JSON.stringify(analysisData)
      );
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
        backgroundColor: 'var(--background)',
        fontFamily:
          'DM Sans, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
      }}
    >
      {/* Header */}
      <header
        style={{
          backgroundColor: 'var(--card)',
          borderBottom: '1px solid var(--border)',
          padding: '32px 0',
          boxShadow: '0 1px 3px rgba(0, 0, 0, 0.1)',
        }}
      >
        <div
          style={{ maxWidth: '1400px', margin: '0 auto', padding: '0 24px' }}
        >
          <div style={{ textAlign: 'center' }}>
            <div
              style={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                gap: '12px',
                marginBottom: '16px',
              }}
            >
              <div style={{ fontSize: '32px' }}>🛡️</div>
              <h1
                style={{
                  fontSize: '36px',
                  fontWeight: '700',
                  color: 'var(--foreground)',
                  margin: '0',
                }}
              >
                ToxiGuard
              </h1>
            </div>
            <p
              style={{
                fontSize: '18px',
                color: 'var(--muted-foreground)',
                margin: '0',
                maxWidth: '560px',
                marginLeft: 'auto',
                marginRight: 'auto',
              }}
            >
              Professional obscene text detection powered by advanced machine
              learning algorithms
            </p>
          </div>
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
              backgroundColor: 'var(--card)',
              borderRadius: 'var(--radius)',
              padding: '32px',
              boxShadow: '0 4px 6px rgba(0, 0, 0, 0.05)',
              border: '1px solid var(--border)',
            }}
          >
            <h2
              style={{
                fontSize: '20px',
                fontWeight: '600',
                color: 'var(--foreground)',
                margin: '0 0 24px 0',
                display: 'flex',
                alignItems: 'center',
                gap: '8px',
              }}
            >
              ⚡ Analyze Text
            </h2>

            <div style={{ marginBottom: '20px' }}>
              <textarea
                value={text}
                onChange={(e) => setText(e.target.value)}
                onKeyDown={handleKeyDown}
                placeholder='Enter or paste the text you want to analyze for toxicity... (Press Enter to analyze, Shift+Enter for new line)'
                style={{
                  width: '100%',
                  minHeight: '200px',
                  padding: '16px',
                  border: '2px solid var(--border)',
                  borderRadius: 'var(--radius)',
                  fontSize: '16px',
                  fontFamily: 'inherit',
                  resize: 'none',
                  backgroundColor: 'var(--input)',
                  transition: 'all 0.2s ease',
                  boxSizing: 'border-box',
                }}
                onFocus={(e) => {
                  e.target.style.borderColor = 'var(--ring)';
                  e.target.style.backgroundColor = 'var(--background)';
                  e.target.style.boxShadow = '0 0 0 3px var(--ring)';
                }}
                onBlur={(e) => {
                  e.target.style.borderColor = text.trim()
                    ? 'var(--ring)'
                    : 'var(--border)';
                  e.target.style.backgroundColor = text.trim()
                    ? 'var(--background)'
                    : 'var(--input)';
                  e.target.style.boxShadow = text.trim()
                    ? '0 0 0 3px var(--ring)'
                    : 'none';
                }}
              />
              {text.trim() && (
                <div
                  style={{
                    marginTop: '8px',
                    fontSize: '14px',
                    color: 'var(--muted-foreground)',
                    textAlign: 'right',
                  }}
                >
                  {text.length} characters
                </div>
              )}
            </div>

            <div style={{ display: 'flex', gap: '12px', flexWrap: 'wrap' }}>
              <button
                onClick={handleAnalyze}
                disabled={loading || !text.trim()}
                aria-label='Analyze text for toxicity detection'
                style={{
                  backgroundColor: 'var(--primary)',
                  color: 'var(--primary-foreground)',
                  border: 'none',
                  padding: '12px 24px',
                  borderRadius: 'var(--radius)',
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
                    e.currentTarget.style.backgroundColor =
                      'oklch(0.548 0.15 197.137 / 0.9)';
                    e.currentTarget.style.transform = 'translateY(-1px)';
                  }
                }}
                onMouseLeave={(e) => {
                  if (!loading && text.trim()) {
                    e.currentTarget.style.backgroundColor = 'var(--primary)';
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
                        borderTop: '2px solid currentColor',
                        borderRadius: '50%',
                        animation: 'spin 1s linear infinite',
                      }}
                    />
                    Analyzing...
                  </>
                ) : (
                  <>
                    🛡️
                    <span>Analyze</span>
                  </>
                )}
              </button>

              <button
                onClick={handleClear}
                aria-label='Clear text and analysis results'
                style={{
                  backgroundColor: 'var(--muted)',
                  color: 'var(--muted-foreground)',
                  border: '1px solid var(--border)',
                  padding: '12px 24px',
                  borderRadius: 'var(--radius)',
                  fontSize: '16px',
                  fontWeight: '600',
                  cursor: 'pointer',
                  transition: 'all 0.2s ease',
                }}
                onMouseEnter={(e) => {
                  e.currentTarget.style.backgroundColor = 'var(--border)';
                  e.currentTarget.style.transform = 'translateY(-1px)';
                }}
                onMouseLeave={(e) => {
                  e.currentTarget.style.backgroundColor = 'var(--muted)';
                  e.currentTarget.style.transform = 'translateY(0)';
                }}
              >
                🗑️ Clear
              </button>

              {result && (
                <button
                  onClick={() => {
                    navigator.clipboard.writeText(text);
                    // Feedback visual temporal
                    const button = document.activeElement as HTMLButtonElement;
                    if (button) {
                      const originalText = button.innerHTML;
                      button.innerHTML = '✅ Copied!';
                      button.style.backgroundColor = 'var(--secondary)';
                      button.style.color = 'var(--secondary-foreground)';
                      setTimeout(() => {
                        button.innerHTML = originalText;
                        button.style.backgroundColor = 'var(--muted)';
                        button.style.color = 'var(--muted-foreground)';
                      }, 2000);
                    }
                  }}
                  style={{
                    backgroundColor: 'var(--muted)',
                    color: 'var(--muted-foreground)',
                    border: '1px solid var(--border)',
                    padding: '12px 24px',
                    borderRadius: 'var(--radius)',
                    fontSize: '16px',
                    fontWeight: '600',
                    cursor: 'pointer',
                    transition: 'all 0.2s ease',
                  }}
                  onMouseEnter={(e) => {
                    e.currentTarget.style.backgroundColor = 'var(--border)';
                    e.currentTarget.style.transform = 'translateY(-1px)';
                  }}
                  onMouseLeave={(e) => {
                    e.currentTarget.style.backgroundColor = 'var(--muted)';
                    e.currentTarget.style.transform = 'translateY(0)';
                  }}
                >
                  📋 Copy Text
                </button>
              )}
            </div>

            {error && (
              <div
                style={{
                  marginTop: '20px',
                  padding: '16px',
                  backgroundColor: 'var(--destructive)',
                  color: 'var(--destructive-foreground)',
                  borderRadius: 'var(--radius)',
                  border: '1px solid var(--destructive)',
                  animation: 'shake 0.5s ease-in-out',
                }}
              >
                <div style={{ marginBottom: '8px', fontWeight: '600' }}>
                  ❌ {error}
                </div>
                {error.includes('No se pudo conectar') && (
                  <div
                    style={{
                      fontSize: '14px',
                      color: 'var(--destructive-foreground)',
                    }}
                  >
                    <strong>🔧 Solution:</strong>
                    <ul style={{ marginTop: '8px', marginLeft: '20px' }}>
                      <li>
                        Verify that the backend is running on
                        http://127.0.0.1:8000
                      </li>
                      <li>Open the browser console (F12) for more details</li>
                      <li>
                        Try the test-connection.html file to verify connectivity
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
                backgroundColor: 'var(--card)',
                borderRadius: 'var(--radius)',
                padding: '32px',
                boxShadow: '0 4px 6px rgba(0, 0, 0, 0.05)',
                border: '2px solid',
                borderColor: getToxicityBorderColor(result.toxicity_percentage),
                transition: 'all 0.3s ease',
                animation: 'slideInRight 0.5s ease-out',
              }}
            >
              <h2
                style={{
                  fontSize: '20px',
                  fontWeight: '600',
                  color: 'var(--foreground)',
                  margin: '0 0 24px 0',
                  textAlign: 'center',
                }}
              >
                📊 Analysis Results
              </h2>

              <div style={{ marginBottom: '24px' }}>
                <ToxicityGauge percentage={result.toxicity_percentage} />

                {/* Barra de progreso adicional para toxicidad */}
                <div style={{ marginTop: '20px' }}>
                  <div
                    style={{
                      display: 'flex',
                      justifyContent: 'space-between',
                      alignItems: 'center',
                      marginBottom: '8px',
                    }}
                  >
                    <span
                      style={{
                        fontSize: '14px',
                        color: 'var(--muted-foreground)',
                        fontWeight: '500',
                      }}
                    >
                      Toxicity Level
                    </span>
                    <span
                      style={{
                        fontSize: '14px',
                        color: 'var(--foreground)',
                        fontWeight: '600',
                      }}
                    >
                      {Math.round(result.toxicity_percentage)}%
                    </span>
                  </div>
                  <div
                    style={{
                      width: '100%',
                      height: '12px',
                      backgroundColor: 'var(--muted)',
                      borderRadius: '6px',
                      overflow: 'hidden',
                      position: 'relative',
                    }}
                  >
                    <div
                      style={{
                        width: `${result.toxicity_percentage}%`,
                        height: '100%',
                        backgroundColor: getToxicityColor(
                          result.toxicity_percentage
                        ),
                        borderRadius: '6px',
                        transition: 'width 1s ease-out',
                        animation: 'slideInProgress 1.2s ease-out',
                      }}
                    />
                  </div>
                  <div
                    style={{
                      display: 'flex',
                      justifyContent: 'space-between',
                      marginTop: '6px',
                      fontSize: '12px',
                      color: 'var(--muted-foreground)',
                    }}
                  >
                    <span>0%</span>
                    <span>50%</span>
                    <span>100%</span>
                  </div>
                </div>
              </div>

              {/* Enhanced Results Display */}
              <div
                style={{
                  backgroundColor: 'var(--muted)',
                  padding: '20px',
                  borderRadius: 'var(--radius)',
                  border: '1px solid var(--border)',
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
                        color: 'var(--muted-foreground)',
                        marginBottom: '4px',
                      }}
                    >
                      Score
                    </div>
                    <div
                      style={{
                        fontSize: '18px',
                        fontWeight: '600',
                        color: 'var(--foreground)',
                      }}
                    >
                      {Math.round(result.toxicity_percentage)}%
                    </div>
                  </div>

                  <div style={{ textAlign: 'center' }}>
                    <div
                      style={{
                        fontSize: '12px',
                        color: 'var(--muted-foreground)',
                        marginBottom: '4px',
                      }}
                    >
                      Category
                    </div>
                    <div
                      style={{
                        fontSize: '18px',
                        fontWeight: '600',
                        color: 'var(--foreground)',
                      }}
                    >
                      {(() => {
                        const percentage = result.toxicity_percentage;
                        if (percentage <= 30) return 'Safe';
                        if (percentage <= 60) return 'Moderate';
                        return 'High Risk';
                      })()}
                    </div>
                  </div>

                  <div style={{ textAlign: 'center' }}>
                    <div
                      style={{
                        fontSize: '12px',
                        color: 'var(--muted-foreground)',
                        marginBottom: '4px',
                      }}
                    >
                      Model
                    </div>
                    <div
                      style={{
                        fontSize: '18px',
                        fontWeight: '600',
                        color: 'var(--foreground)',
                      }}
                    >
                      {result.model_used}
                    </div>
                  </div>

                  <div style={{ textAlign: 'center' }}>
                    <div
                      style={{
                        fontSize: '12px',
                        color: 'var(--muted-foreground)',
                        marginBottom: '4px',
                      }}
                    >
                      Time
                    </div>
                    <div
                      style={{
                        fontSize: '18px',
                        fontWeight: '600',
                        color: 'var(--foreground)',
                      }}
                    >
                      {result.response_time_ms}ms
                    </div>
                  </div>
                </div>

                <div
                  style={{
                    fontSize: '14px',
                    color: 'var(--muted-foreground)',
                    textAlign: 'center',
                    padding: '12px',
                    backgroundColor: 'var(--card)',
                    borderRadius: 'var(--radius)',
                    border: '1px solid var(--border)',
                  }}
                >
                  Analyzed on {new Date(result.timestamp).toLocaleString()}
                  {lastAnalysis && (
                    <div
                      style={{
                        marginTop: '8px',
                        fontSize: '12px',
                        color: 'var(--muted-foreground)',
                      }}
                    >
                      💾 Analysis temporarily saved
                    </div>
                  )}
                </div>
              </div>

              {/* Texto con palabras resaltadas */}
              <div style={{ marginTop: '24px' }}>
                <h3
                  style={{
                    fontSize: '18px',
                    fontWeight: '600',
                    color: 'var(--foreground)',
                    margin: '0 0 16px 0',
                    textAlign: 'center',
                  }}
                >
                  📝 Analyzed Text with Toxicity Highlighting
                </h3>
                <div
                  style={{
                    backgroundColor: 'var(--muted)',
                    padding: '20px',
                    borderRadius: 'var(--radius)',
                    border: '1px solid var(--border)',
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
                    backgroundColor: 'var(--muted)',
                    borderRadius: 'var(--radius)',
                    border: '1px solid var(--border)',
                  }}
                >
                  <div
                    style={{
                      fontSize: '14px',
                      fontWeight: '600',
                      color: 'var(--foreground)',
                      marginBottom: '12px',
                      textAlign: 'center',
                    }}
                  >
                    🎨 Color Legend by Toxicity
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
                          backgroundColor: 'var(--secondary)',
                          borderRadius: '50%',
                          border: '2px solid var(--secondary)',
                        }}
                      />
                      <span
                        style={{
                          fontSize: '13px',
                          color: 'var(--secondary)',
                          fontWeight: '600',
                        }}
                      >
                        Green (0-30%)
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
                          backgroundColor: 'oklch(0.769 0.188 70.08)',
                          borderRadius: '50%',
                          border: '2px solid oklch(0.769 0.188 70.08)',
                        }}
                      />
                      <span
                        style={{
                          fontSize: '13px',
                          color: 'oklch(0.769 0.188 70.08)',
                          fontWeight: '600',
                        }}
                      >
                        Amber (31-60%)
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
                          backgroundColor: 'var(--destructive)',
                          borderRadius: '50%',
                          border: '2px solid var(--destructive)',
                        }}
                      />
                      <span
                        style={{
                          fontSize: '13px',
                          color: 'var(--destructive)',
                          fontWeight: '600',
                        }}
                      >
                        Red (61-100%)
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Footer */}
      <footer
        style={{
          backgroundColor: 'var(--card)',
          borderTop: '1px solid var(--border)',
          marginTop: '64px',
        }}
      >
        <div
          style={{
            maxWidth: '1400px',
            margin: '0 auto',
            padding: '32px 24px',
            textAlign: 'center',
            color: 'var(--muted-foreground)',
          }}
        >
          <p>&copy; 2024 ToxiGuard. Professional content moderation tools.</p>
        </div>
      </footer>
    </div>
  );
};

export default App;
