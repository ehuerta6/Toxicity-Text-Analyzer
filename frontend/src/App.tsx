import React, { useState, useCallback, useEffect } from 'react';
import { useToxicityAnalysis } from './hooks/useToxicityAnalysis';
import type { ToxicityResult } from './hooks/useToxicityAnalysis';
import { getToxicityColor } from './styles/common';

interface ToxicityMap {
  [word: string]: number;
}

interface CategoryInfo {
  label: string;
  color: string;
  description: string;
}

const ToxicityGauge: React.FC<{ percentage: number }> = ({ percentage }) => {
  const color = getToxicityColor(percentage);

  const getCategoryInfo = (percentage: number): CategoryInfo => {
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
          width: '80px',
          height: '80px',
          borderRadius: '50%',
          background: `conic-gradient(${color} ${
            roundedPercentage * 3.6
          }deg, var(--muted) ${roundedPercentage * 3.6}deg)`,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          margin: '0 auto 8px',
          position: 'relative',
          boxShadow: '0 2px 8px rgba(0, 0, 0, 0.1)',
          border: `2px solid ${color}`,
        }}
      >
        <div
          style={{
            width: '56px',
            height: '56px',
            borderRadius: '50%',
            backgroundColor: 'var(--background)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            fontSize: '14px',
            fontWeight: 'bold',
            color: color,
            boxShadow: 'inset 0 1px 4px rgba(0, 0, 0, 0.1)',
          }}
        >
          {roundedPercentage}%
        </div>
      </div>

      <div
        style={{
          fontSize: '12px',
          fontWeight: '700',
          color: categoryInfo.color,
          textShadow: '0 1px 2px rgba(0, 0, 0, 0.1)',
          marginBottom: '4px',
          padding: '4px 8px',
          backgroundColor: `${categoryInfo.color}15`,
          borderRadius: '12px',
          display: 'inline-block',
        }}
      >
        {categoryInfo.label}
      </div>

      <div
        style={{
          fontSize: '10px',
          color: 'var(--muted-foreground)',
          maxWidth: '120px',
          margin: '0 auto',
          lineHeight: '1.2',
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
  const getToxicityClass = (percentage: number): string => {
    if (percentage <= 30) return 'text-emerald-600';
    if (percentage <= 60) return 'text-amber-600';
    return 'text-red-600';
  };

  const renderText = () => {
    if (!text || !toxicityMap || Object.keys(toxicityMap).length === 0) {
      return <span className='text-foreground'>{text}</span>;
    }

    const words = text.split(/(\s+)/);

    return words.map((word, index) => {
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
              borderBottom: `2px solid ${color}`,
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
    <div className='text-foreground leading-relaxed text-xs'>
      {renderText()}
    </div>
  );
};

const Header: React.FC<{ title: string }> = ({ title }) => (
  <header
    style={{
      backgroundColor: 'var(--card)',
      borderBottom: '1px solid var(--border)',
      padding: '16px 0',
      boxShadow: '0 1px 3px rgba(0, 0, 0, 0.1)',
    }}
  >
    <div style={{ maxWidth: '1400px', margin: '0 auto', padding: '0 16px' }}>
      <div style={{ textAlign: 'center' }}>
        <div
          style={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            gap: '8px',
            marginBottom: '8px',
          }}
        >
          <div style={{ fontSize: '24px' }}>🛡️</div>
          <h1
            style={{
              fontSize: '28px',
              fontWeight: '700',
              color: 'var(--foreground)',
              margin: '0',
            }}
          >
            {title}
          </h1>
        </div>
        <p
          style={{
            fontSize: '14px',
            color: 'var(--muted-foreground)',
            margin: '0',
            maxWidth: '400px',
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
);

const Footer: React.FC = () => (
  <footer
    style={{
      backgroundColor: 'var(--card)',
      borderTop: '1px solid var(--border)',
      marginTop: 'auto',
    }}
  >
    <div
      style={{
        maxWidth: '1400px',
        margin: '0 auto',
        padding: '16px',
        textAlign: 'center',
        color: 'var(--muted-foreground)',
        fontSize: '12px',
      }}
    >
      <p>&copy; 2024 ToxiGuard. Professional content moderation tools.</p>
    </div>
  </footer>
);

const TextArea: React.FC<{
  value: string;
  onChange: (value: string) => void;
  onKeyDown: (e: React.KeyboardEvent<HTMLTextAreaElement>) => void;
  placeholder: string;
  minHeight?: number;
  showCharCount?: boolean;
}> = ({
  value,
  onChange,
  onKeyDown,
  placeholder,
  minHeight = 150,
  showCharCount = true,
}) => (
  <div style={{ marginBottom: '24px' }}>
    <textarea
      value={value}
      onChange={(e) => onChange(e.target.value)}
      onKeyDown={onKeyDown}
      placeholder={placeholder}
      style={{
        width: '100%',
        minHeight: `${minHeight}px`,
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
        e.target.style.borderColor = value.trim()
          ? 'var(--ring)'
          : 'var(--border)';
        e.target.style.backgroundColor = value.trim()
          ? 'var(--background)'
          : 'var(--input)';
        e.target.style.boxShadow = value.trim()
          ? '0 0 0 3px var(--ring)'
          : 'none';
      }}
    />
    {showCharCount && value.trim() && (
      <div
        style={{
          marginTop: '8px',
          fontSize: '14px',
          color: 'var(--muted-foreground)',
          textAlign: 'right',
        }}
      >
        {value.length} characters
      </div>
    )}
  </div>
);

const Button: React.FC<{
  onClick: () => void;
  disabled?: boolean;
  variant?: 'primary' | 'secondary';
  children: React.ReactNode;
  ariaLabel?: string;
}> = ({
  onClick,
  disabled = false,
  variant = 'primary',
  children,
  ariaLabel,
}) => {
  const baseStyles = {
    border: 'none',
    padding: '14px 28px',
    borderRadius: 'var(--radius)',
    fontSize: '16px',
    fontWeight: '600',
    cursor: disabled ? 'not-allowed' : 'pointer',
    opacity: disabled ? 0.6 : 1,
    transition: 'all 0.2s ease',
    display: 'flex',
    alignItems: 'center',
    gap: '8px',
  };

  const variantStyles =
    variant === 'primary'
      ? {
          backgroundColor: 'var(--primary)',
          color: 'var(--primary-foreground)',
        }
      : {
          backgroundColor: 'var(--muted)',
          color: 'var(--muted-foreground)',
          border: '1px solid var(--border)',
        };

  return (
    <button
      onClick={onClick}
      disabled={disabled}
      aria-label={ariaLabel}
      style={{ ...baseStyles, ...variantStyles }}
      onMouseEnter={(e) => {
        if (!disabled) {
          if (variant === 'primary') {
            e.currentTarget.style.backgroundColor =
              'oklch(0.548 0.15 197.137 / 0.9)';
          } else {
            e.currentTarget.style.backgroundColor = 'var(--border)';
          }
          e.currentTarget.style.transform = 'translateY(-1px)';
        }
      }}
      onMouseLeave={(e) => {
        if (!disabled) {
          if (variant === 'primary') {
            e.currentTarget.style.backgroundColor = 'var(--primary)';
          } else {
            e.currentTarget.style.backgroundColor = 'var(--muted)';
          }
          e.currentTarget.style.transform = 'translateY(0)';
        }
      }}
    >
      {children}
    </button>
  );
};

const App: React.FC = () => {
  const [text, setText] = useState('');
  const [toxicityMap, setToxicityMap] = useState<Record<string, number>>({});
  const [hasAnalyzed, setHasAnalyzed] = useState(false);
  const [showExplanations, setShowExplanations] = useState(false);
  const [lastAnalysis, setLastAnalysis] = useState<{
    text: string;
    result: ToxicityResult;
    toxicityMap: Record<string, number>;
    timestamp: string;
  } | null>(() => {
    const saved = localStorage.getItem('toxiguard_last_analysis');
    return saved ? JSON.parse(saved) : null;
  });

  const { result, loading, error, analyzeText, clearResult } =
    useToxicityAnalysis();

  const generateToxicityMap = useCallback(
    (text: string, toxicityPercentage: number): ToxicityMap => {
      if (!text || toxicityPercentage === 0) return {};

      const words = text
        .toLowerCase()
        .split(/\s+/)
        .filter((word) => word.length > 2);
      if (words.length === 0) return {};

      const toxicityMap: ToxicityMap = {};
      const cleanWords = new Map();

      words.forEach((word) => {
        const cleanWord = word.replace(/[^\wáéíóúñ]/g, '');
        if (cleanWord.length > 0) {
          cleanWords.set(word, cleanWord);
        }
      });

      if (toxicityPercentage <= 30) {
        const toxicWords = Math.max(1, Math.floor(words.length * 0.3));
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
      setHasAnalyzed(true);
    } catch (error) {
      console.error('Error al analizar texto:', error);
    }
  }, [text, analyzeText]);

  useEffect(() => {
    if (result && text.trim()) {
      const wordToxicityMap = generateToxicityMap(
        text,
        result.toxicity_percentage
      );
      setToxicityMap(wordToxicityMap);

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
    setHasAnalyzed(false);
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleAnalyze();
    }
  };

  if (!hasAnalyzed) {
    return (
      <div
        style={{
          minHeight: '100vh',
          backgroundColor: 'var(--background)',
          fontFamily:
            'DM Sans, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
        }}
      >
        <Header title='ToxiGuard' />

        <div
          style={{
            maxWidth: '800px',
            margin: '0 auto',
            padding: '40px 16px',
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            justifyContent: 'center',
            minHeight: 'calc(100vh - 200px)',
          }}
        >
          <div
            style={{
              backgroundColor: 'var(--card)',
              borderRadius: 'var(--radius)',
              padding: '32px',
              boxShadow: '0 4px 12px rgba(0, 0, 0, 0.1)',
              border: '1px solid var(--border)',
              width: '100%',
              maxWidth: '600px',
            }}
          >
            <h2
              style={{
                fontSize: '24px',
                fontWeight: '600',
                color: 'var(--foreground)',
                margin: '0 0 24px 0',
                textAlign: 'center',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                gap: '8px',
              }}
            >
              ⚡ Analyze Your First Text
            </h2>

            <TextArea
              value={text}
              onChange={setText}
              onKeyDown={handleKeyDown}
              placeholder='Enter or paste the text you want to analyze for toxicity... (Press Enter to analyze, Shift+Enter for new line)'
            />

            <div
              style={{
                display: 'flex',
                gap: '12px',
                justifyContent: 'center',
                alignItems: 'center',
              }}
            >
              <Button
                onClick={handleAnalyze}
                disabled={loading || !text.trim()}
                ariaLabel='Analyze text for toxicity detection'
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
                    <span>Analyze Text</span>
                  </>
                )}
              </Button>

              <Button
                onClick={handleClear}
                variant='secondary'
                ariaLabel='Clear text'
              >
                🗑️ Clear
              </Button>

              <div
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '8px',
                  padding: '8px 12px',
                  backgroundColor: 'var(--muted)',
                  borderRadius: 'var(--radius)',
                  border: '1px solid var(--border)',
                }}
              >
                <input
                  type='checkbox'
                  id='show-explanations'
                  checked={showExplanations}
                  onChange={(e) => setShowExplanations(e.target.checked)}
                  style={{ cursor: 'pointer' }}
                />
                <label
                  htmlFor='show-explanations'
                  style={{
                    fontSize: '14px',
                    color: 'var(--foreground)',
                    cursor: 'pointer',
                    userSelect: 'none',
                  }}
                >
                  💡 Mostrar explicaciones
                </label>
              </div>
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
                  fontSize: '14px',
                }}
              >
                <div style={{ marginBottom: '8px', fontWeight: '600' }}>
                  ❌ {error}
                </div>
                {error.includes('Failed to fetch') && (
                  <div
                    style={{
                      fontSize: '13px',
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
        </div>

        <Footer />
      </div>
    );
  }

  return (
    <div
      style={{
        minHeight: '100vh',
        backgroundColor: 'var(--background)',
        fontFamily:
          'DM Sans, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
      }}
    >
      <Header title='ToxiGuard Dashboard' />

      <div style={{ maxWidth: '1400px', margin: '0 auto', padding: '16px' }}>
        {/* Grid de Resultados del Análisis */}
        <div
          style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
            gap: '16px',
            marginBottom: '24px',
          }}
        >
          {/* Tarjeta de Gauge Principal */}
          <div
            style={{
              backgroundColor: 'var(--card)',
              borderRadius: 'var(--radius)',
              padding: '20px',
              boxShadow: '0 2px 4px rgba(0, 0, 0, 0.05)',
              border: '1px solid var(--border)',
              textAlign: 'center',
            }}
          >
            <h3
              style={{
                fontSize: '16px',
                fontWeight: '600',
                color: 'var(--foreground)',
                margin: '0 0 16px 0',
              }}
            >
              📊 Toxicity Analysis
            </h3>
            <ToxicityGauge percentage={result?.toxicity_percentage || 0} />
          </div>

          {/* Tarjeta de Estadísticas */}
          <div
            style={{
              backgroundColor: 'var(--card)',
              borderRadius: 'var(--radius)',
              padding: '20px',
              boxShadow: '0 2px 4px rgba(0, 0, 0, 0.05)',
              border: '1px solid var(--border)',
            }}
          >
            <h3
              style={{
                fontSize: '16px',
                fontWeight: '600',
                color: 'var(--foreground)',
                margin: '0 0 16px 0',
                textAlign: 'center',
              }}
            >
              📈 Analysis Details
            </h3>
            <div
              style={{
                display: 'grid',
                gridTemplateColumns: 'repeat(2, 1fr)',
                gap: '12px',
              }}
            >
              <div style={{ textAlign: 'center' }}>
                <div
                  style={{
                    fontSize: '10px',
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
                  {result ? Math.round(result.toxicity_percentage) : 0}%
                </div>
              </div>

              <div style={{ textAlign: 'center' }}>
                <div
                  style={{
                    fontSize: '10px',
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
                  {result
                    ? (() => {
                        const percentage = result.toxicity_percentage;
                        if (percentage <= 30) return 'Safe';
                        if (percentage <= 60) return 'Moderate';
                        return 'High Risk';
                      })()
                    : 'N/A'}
                </div>
              </div>

              <div style={{ textAlign: 'center' }}>
                <div
                  style={{
                    fontSize: '10px',
                    color: 'var(--muted-foreground)',
                    marginBottom: '4px',
                  }}
                >
                  Técnica
                </div>
                <div
                  style={{
                    fontSize: '14px',
                    fontWeight: '600',
                    color: 'var(--foreground)',
                  }}
                >
                  {result?.classification_technique || 'N/A'}
                </div>
              </div>

              <div style={{ textAlign: 'center' }}>
                <div
                  style={{
                    fontSize: '10px',
                    color: 'var(--muted-foreground)',
                    marginBottom: '4px',
                  }}
                >
                  Time
                </div>
                <div
                  style={{
                    fontSize: '14px',
                    fontWeight: '600',
                    color: 'var(--foreground)',
                  }}
                >
                  {result?.response_time_ms || 0}ms
                </div>
              </div>
            </div>

            <div
              style={{
                marginTop: '16px',
                fontSize: '11px',
                color: 'var(--muted-foreground)',
                textAlign: 'center',
                padding: '8px',
                backgroundColor: 'var(--muted)',
                borderRadius: 'var(--radius)',
                border: '1px solid var(--border)',
              }}
            >
              Analyzed on{' '}
              {result ? new Date(result.timestamp).toLocaleString() : 'N/A'}
            </div>
          </div>

          {/* Tarjeta de Barra de Progreso */}
          <div
            style={{
              backgroundColor: 'var(--card)',
              borderRadius: 'var(--radius)',
              padding: '20px',
              boxShadow: '0 2px 4px rgba(0, 0, 0, 0.05)',
              border: '1px solid var(--border)',
            }}
          >
            <h3
              style={{
                fontSize: '16px',
                fontWeight: '600',
                color: 'var(--foreground)',
                margin: '0 0 16px 0',
                textAlign: 'center',
              }}
            >
              📊 Toxicity Level
            </h3>
            <div style={{ marginBottom: '12px' }}>
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
                    fontSize: '12px',
                    color: 'var(--muted-foreground)',
                    fontWeight: '500',
                  }}
                >
                  Current Level
                </span>
                <span
                  style={{
                    fontSize: '12px',
                    color: 'var(--foreground)',
                    fontWeight: '600',
                  }}
                >
                  {result ? Math.round(result.toxicity_percentage) : 0}%
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
                    width: `${result?.toxicity_percentage || 0}%`,
                    height: '100%',
                    backgroundColor: result
                      ? getToxicityColor(result.toxicity_percentage)
                      : 'var(--muted)',
                    borderRadius: '6px',
                    transition: 'width 1s ease-out',
                  }}
                />
              </div>
            </div>

            <div
              style={{
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
                fontSize: '10px',
                color: 'var(--muted-foreground)',
              }}
            >
              <span>0%</span>
              <span>50%</span>
              <span>100%</span>
            </div>

            <div
              style={{
                marginTop: '16px',
                padding: '12px',
                backgroundColor: 'var(--muted)',
                borderRadius: 'var(--radius)',
                border: '1px solid var(--border)',
              }}
            >
              <div
                style={{
                  fontSize: '11px',
                  fontWeight: '600',
                  color: 'var(--foreground)',
                  marginBottom: '8px',
                  textAlign: 'center',
                }}
              >
                🎨 Color Legend
              </div>
              <div
                style={{
                  display: 'flex',
                  justifyContent: 'space-around',
                  alignItems: 'center',
                  gap: '4px',
                }}
              >
                <div
                  style={{ display: 'flex', alignItems: 'center', gap: '3px' }}
                >
                  <div
                    style={{
                      width: '10px',
                      height: '10px',
                      backgroundColor: 'var(--secondary)',
                      borderRadius: '50%',
                      border: '1px solid var(--secondary)',
                    }}
                  />
                  <span
                    style={{
                      fontSize: '9px',
                      color: 'var(--secondary)',
                      fontWeight: '600',
                    }}
                  >
                    Safe
                  </span>
                </div>
                <div
                  style={{ display: 'flex', alignItems: 'center', gap: '3px' }}
                >
                  <div
                    style={{
                      width: '10px',
                      height: '10px',
                      backgroundColor: 'oklch(0.769 0.188 70.08)',
                      borderRadius: '50%',
                      border: '1px solid oklch(0.769 0.188 70.08)',
                    }}
                  />
                  <span
                    style={{
                      fontSize: '9px',
                      color: 'oklch(0.769 0.188 70.08)',
                      fontWeight: '600',
                    }}
                  >
                    Moderate
                  </span>
                </div>
                <div
                  style={{ display: 'flex', alignItems: 'center', gap: '3px' }}
                >
                  <div
                    style={{
                      width: '10px',
                      height: '10px',
                      backgroundColor: 'var(--destructive)',
                      borderRadius: '50%',
                      border: '1px solid var(--destructive)',
                    }}
                  />
                  <span
                    style={{
                      fontSize: '9px',
                      color: 'var(--destructive)',
                      fontWeight: '600',
                    }}
                  >
                    High Risk
                  </span>
                </div>
              </div>
            </div>

            {/* Sección de Categorías Detectadas con Explicaciones */}
            {result &&
              result.detected_categories &&
              result.detected_categories.length > 0 && (
                <div
                  style={{
                    marginTop: '16px',
                    padding: '16px',
                    backgroundColor: 'var(--card)',
                    borderRadius: 'var(--radius)',
                    border: '1px solid var(--border)',
                  }}
                >
                  <h4
                    style={{
                      fontSize: '14px',
                      fontWeight: '600',
                      color: 'var(--foreground)',
                      margin: '0 0 12px 0',
                      textAlign: 'center',
                    }}
                  >
                    🏷️ Categorías Detectadas
                  </h4>

                  <div
                    style={{
                      display: 'flex',
                      flexDirection: 'column',
                      gap: '8px',
                    }}
                  >
                    {result.detected_categories.map((category, index) => (
                      <div
                        key={index}
                        style={{
                          padding: '8px 12px',
                          backgroundColor: 'var(--muted)',
                          borderRadius: 'var(--radius)',
                          border: '1px solid var(--border)',
                        }}
                      >
                        <div
                          style={{
                            fontSize: '12px',
                            fontWeight: '600',
                            color: 'var(--foreground)',
                            marginBottom: '4px',
                            textTransform: 'capitalize',
                          }}
                        >
                          {category.replace('_', ' ')}
                        </div>

                        {showExplanations &&
                          result.explanations &&
                          result.explanations[category] && (
                            <div
                              style={{
                                fontSize: '11px',
                                color: 'var(--muted-foreground)',
                                fontStyle: 'italic',
                                lineHeight: '1.4',
                              }}
                            >
                              💡 {result.explanations[category]}
                            </div>
                          )}
                      </div>
                    ))}
                  </div>

                  {!showExplanations && (
                    <div
                      style={{
                        marginTop: '12px',
                        fontSize: '11px',
                        color: 'var(--muted-foreground)',
                        textAlign: 'center',
                        fontStyle: 'italic',
                      }}
                    >
                      💡 Activa "Mostrar explicaciones" para ver por qué se
                      detectó cada categoría
                    </div>
                  )}
                </div>
              )}
          </div>
        </div>

        {/* Texto Analizado con Palabras Resaltadas */}
        <div
          style={{
            backgroundColor: 'var(--card)',
            borderRadius: 'var(--radius)',
            padding: '20px',
            boxShadow: '0 2px 4px rgba(0, 0, 0, 0.05)',
            border: '1px solid var(--border)',
            marginBottom: '24px',
          }}
        >
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
              padding: '16px',
              borderRadius: 'var(--radius)',
              border: '1px solid var(--border)',
              maxHeight: '200px',
              overflowY: 'auto',
            }}
          >
            <ColoredText
              text={lastAnalysis?.text || ''}
              toxicityMap={toxicityMap}
            />
          </div>
        </div>

        {/* Nueva Caja de Texto para Análisis Adicionales */}
        <div
          style={{
            backgroundColor: 'var(--card)',
            borderRadius: 'var(--radius)',
            padding: '20px',
            boxShadow: '0 2px 4px rgba(0, 0, 0, 0.05)',
            border: '1px solid var(--border)',
          }}
        >
          <h3
            style={{
              fontSize: '18px',
              fontWeight: '600',
              color: 'var(--foreground)',
              margin: '0 0 16px 0',
              display: 'flex',
              alignItems: 'center',
              gap: '6px',
            }}
          >
            ⚡ Analyze New Text
          </h3>

          <TextArea
            value={text}
            onChange={setText}
            onKeyDown={handleKeyDown}
            placeholder='Enter or paste new text to analyze... (Press Enter to analyze, Shift+Enter for new line)'
            minHeight={100}
            showCharCount={true}
          />

          <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
            <Button
              onClick={handleAnalyze}
              disabled={loading || !text.trim()}
              ariaLabel='Analyze new text for toxicity detection'
            >
              {loading ? (
                <>
                  <div
                    style={{
                      width: '14px',
                      height: '14px',
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
            </Button>

            <Button
              onClick={handleClear}
              variant='secondary'
              ariaLabel='Clear text and reset analysis'
            >
              🗑️ Clear & Reset
            </Button>

            {result && (
              <Button
                onClick={() => {
                  navigator.clipboard.writeText(text);
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
                variant='secondary'
                ariaLabel='Copy text to clipboard'
              >
                📋 Copy Text
              </Button>
            )}
          </div>

          {error && (
            <div
              style={{
                marginTop: '16px',
                padding: '12px',
                backgroundColor: 'var(--destructive)',
                color: 'var(--destructive-foreground)',
                borderRadius: 'var(--radius)',
                border: '1px solid var(--destructive)',
                animation: 'shake 0.5s ease-in-out',
                fontSize: '13px',
              }}
            >
              <div style={{ marginBottom: '6px', fontWeight: '600' }}>
                ❌ {error}
              </div>
              {error.includes('Failed to fetch') && (
                <div
                  style={{
                    fontSize: '12px',
                    color: 'var(--destructive-foreground)',
                  }}
                >
                  <strong>🔧 Solution:</strong>
                  <ul style={{ marginTop: '6px', marginLeft: '16px' }}>
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
      </div>

      <Footer />
    </div>
  );
};

export default App;
