import React, { useState, useCallback, useEffect } from 'react';
import { useToxicityAnalysis } from './hooks/useToxicityAnalysis';
import type { ToxicityResult } from './hooks/useToxicityAnalysis';
import { getToxicityColor } from './styles/common';
import SeverityBreakdown from './components/SeverityBreakdown';
import AnalysisDetails from './components/AnalysisDetails';

// Sistema de Estilos Unificado para Consistencia Visual
const DESIGN_SYSTEM = {
  // Tipografía
  typography: {
    h1: {
      fontSize: '28px',
      fontWeight: '700',
      lineHeight: '1.2',
      margin: '0 0 8px 0',
    },
    h2: {
      fontSize: '24px',
      fontWeight: '600',
      lineHeight: '1.3',
      margin: '0 0 20px 0',
    },
    h3: {
      fontSize: '18px',
      fontWeight: '600',
      lineHeight: '1.4',
      margin: '0 0 16px 0',
    },
    h4: {
      fontSize: '16px',
      fontWeight: '600',
      lineHeight: '1.4',
      margin: '0 0 12px 0',
    },
    body: {
      fontSize: '16px',
      fontWeight: '400',
      lineHeight: '1.5',
      margin: '0',
    },
    caption: {
      fontSize: '14px',
      fontWeight: '500',
      lineHeight: '1.4',
      margin: '0',
    },
    small: {
      fontSize: '12px',
      fontWeight: '500',
      lineHeight: '1.3',
      margin: '0',
    },
    tiny: {
      fontSize: '11px',
      fontWeight: '600',
      lineHeight: '1.2',
      margin: '0',
    },
    micro: {
      fontSize: '10px',
      fontWeight: '500',
      lineHeight: '1.2',
      margin: '0',
    },
  },

  // Espaciado
  spacing: {
    xs: '4px',
    sm: '8px',
    md: '12px',
    lg: '16px',
    xl: '20px',
    xxl: '24px',
    xxxl: '32px',
  },

  // Colores consistentes
  colors: {
    primary: 'var(--primary)',
    secondary: 'var(--secondary)',
    destructive: 'var(--destructive)',
    muted: 'var(--muted)',
    background: 'var(--background)',
    card: 'var(--card)',
    border: 'var(--border)',
    foreground: 'var(--foreground)',
    mutedForeground: 'var(--muted-foreground)',
    accent: 'oklch(0.769 0.188 70.08)', // Color amarillo consistente
  },

  // Bordes y sombras
  borders: {
    radius: 'var(--radius)',
    width: '1px',
    shadow: '0 2px 4px rgba(0, 0, 0, 0.05)',
    shadowHover: '0 4px 8px rgba(0, 0, 0, 0.1)',
  },

  // Transiciones
  transitions: {
    fast: 'all 0.2s ease',
    medium: 'all 0.3s ease',
    slow: 'all 0.5s ease',
  },
};

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
        color: DESIGN_SYSTEM.colors.secondary,
        description: 'Content is safe and appropriate',
      };
    } else if (percentage <= 60) {
      return {
        label: 'Moderate',
        color: DESIGN_SYSTEM.colors.accent,
        description: 'Content requires moderate attention',
      };
    } else {
      return {
        label: 'High Risk',
        color: DESIGN_SYSTEM.colors.destructive,
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
          margin: `0 auto ${DESIGN_SYSTEM.spacing.sm}`,
          position: 'relative',
          boxShadow: DESIGN_SYSTEM.borders.shadowHover,
          border: `2px solid ${color}`,
        }}
      >
        <div
          style={{
            width: '56px',
            height: '56px',
            borderRadius: '50%',
            backgroundColor: DESIGN_SYSTEM.colors.background,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            ...DESIGN_SYSTEM.typography.caption,
            fontWeight: '700',
            color: color,
            boxShadow: 'inset 0 1px 4px rgba(0, 0, 0, 0.1)',
          }}
        >
          {roundedPercentage}%
        </div>
      </div>

      <div
        style={{
          ...DESIGN_SYSTEM.typography.small,
          fontWeight: '700',
          color: categoryInfo.color,
          textShadow: '0 1px 2px rgba(0, 0, 0, 0.1)',
          marginBottom: DESIGN_SYSTEM.spacing.xs,
          padding: `${DESIGN_SYSTEM.spacing.xs} ${DESIGN_SYSTEM.spacing.sm}`,
          backgroundColor: `${categoryInfo.color}15`,
          borderRadius: '12px',
          display: 'inline-block',
        }}
      >
        {categoryInfo.label}
      </div>

      <div
        style={{
          ...DESIGN_SYSTEM.typography.micro,
          color: DESIGN_SYSTEM.colors.mutedForeground,
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

const ConfidenceGauge: React.FC<{ confidence: number }> = ({ confidence }) => {
  const getConfidenceColor = (confidence: number): string => {
    if (confidence >= 80) return DESIGN_SYSTEM.colors.secondary; // Verde para alta confianza
    if (confidence >= 60) return DESIGN_SYSTEM.colors.accent; // Amarillo para confianza media
    return DESIGN_SYSTEM.colors.destructive; // Rojo para baja confianza
  };

  const getConfidenceLabel = (confidence: number): string => {
    if (confidence >= 80) return 'Alto';
    if (confidence >= 60) return 'Medio';
    return 'Bajo';
  };

  const color = getConfidenceColor(confidence);
  const roundedConfidence = Math.round(confidence);

  return (
    <div style={{ textAlign: 'center' }}>
      <div
        style={{
          width: '80px',
          height: '80px',
          borderRadius: '50%',
          background: `conic-gradient(${color} ${
            roundedConfidence * 3.6
          }deg, var(--muted) ${roundedConfidence * 3.6}deg)`,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          margin: `0 auto ${DESIGN_SYSTEM.spacing.sm}`,
          position: 'relative',
          boxShadow: DESIGN_SYSTEM.borders.shadowHover,
          border: `2px solid ${color}`,
        }}
      >
        <div
          style={{
            width: '56px',
            height: '56px',
            borderRadius: '50%',
            backgroundColor: DESIGN_SYSTEM.colors.background,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            ...DESIGN_SYSTEM.typography.caption,
            fontWeight: '700',
            color: color,
            boxShadow: 'inset 0 1px 4px rgba(0, 0, 0, 0.1)',
          }}
        >
          {roundedConfidence}%
        </div>
      </div>

      <div
        style={{
          ...DESIGN_SYSTEM.typography.small,
          fontWeight: '700',
          color: color,
          textShadow: '0 1px 2px rgba(0, 0, 0, 0.1)',
          marginBottom: DESIGN_SYSTEM.spacing.xs,
          padding: `${DESIGN_SYSTEM.spacing.xs} ${DESIGN_SYSTEM.spacing.sm}`,
          backgroundColor: `${color}15`,
          borderRadius: '12px',
          display: 'inline-block',
        }}
      >
        {getConfidenceLabel(confidence)}
      </div>

      <div
        style={{
          ...DESIGN_SYSTEM.typography.micro,
          color: DESIGN_SYSTEM.colors.mutedForeground,
          maxWidth: '120px',
          margin: '0 auto',
          lineHeight: '1.2',
        }}
      >
        Model Confidence Level
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
      backgroundColor: DESIGN_SYSTEM.colors.card,
      borderBottom: `${DESIGN_SYSTEM.borders.width} solid ${DESIGN_SYSTEM.colors.border}`,
      padding: `${DESIGN_SYSTEM.spacing.lg} 0`,
      boxShadow: DESIGN_SYSTEM.borders.shadow,
    }}
  >
    <div
      style={{
        maxWidth: '1400px',
        margin: '0 auto',
        padding: `0 ${DESIGN_SYSTEM.spacing.lg}`,
      }}
    >
      <div style={{ textAlign: 'center' }}>
        <div
          style={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            gap: DESIGN_SYSTEM.spacing.sm,
            marginBottom: DESIGN_SYSTEM.spacing.sm,
          }}
        >
          <div style={{ fontSize: '24px' }}>🛡️</div>
          <h1
            style={{
              ...DESIGN_SYSTEM.typography.h1,
              color: DESIGN_SYSTEM.colors.foreground,
            }}
          >
            {title}
          </h1>
        </div>
        <p
          style={{
            ...DESIGN_SYSTEM.typography.caption,
            color: DESIGN_SYSTEM.colors.mutedForeground,
            maxWidth: '400px',
            margin: '0 auto',
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
      backgroundColor: DESIGN_SYSTEM.colors.card,
      borderTop: `${DESIGN_SYSTEM.borders.width} solid ${DESIGN_SYSTEM.colors.border}`,
      marginTop: 'auto',
    }}
  >
    <div
      style={{
        maxWidth: '1400px',
        margin: '0 auto',
        padding: DESIGN_SYSTEM.spacing.lg,
        textAlign: 'center',
        color: DESIGN_SYSTEM.colors.mutedForeground,
        fontSize: DESIGN_SYSTEM.typography.small.fontSize,
        fontWeight: DESIGN_SYSTEM.typography.small.fontWeight,
        lineHeight: DESIGN_SYSTEM.typography.small.lineHeight,
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
  <div style={{ marginBottom: DESIGN_SYSTEM.spacing.xxl }}>
    <textarea
      value={value}
      onChange={(e) => onChange(e.target.value)}
      onKeyDown={onKeyDown}
      placeholder={placeholder}
      style={{
        width: '100%',
        minHeight: `${minHeight}px`,
        padding: DESIGN_SYSTEM.spacing.lg,
        border: `2px solid ${DESIGN_SYSTEM.colors.border}`,
        borderRadius: DESIGN_SYSTEM.borders.radius,
        ...DESIGN_SYSTEM.typography.body,
        fontFamily: 'inherit',
        resize: 'none',
        backgroundColor: 'var(--input)',
        transition: DESIGN_SYSTEM.transitions.fast,
        boxSizing: 'border-box',
      }}
      onFocus={(e) => {
        e.target.style.borderColor = 'var(--ring)';
        e.target.style.backgroundColor = DESIGN_SYSTEM.colors.background;
        e.target.style.boxShadow = '0 0 0 3px var(--ring)';
      }}
      onBlur={(e) => {
        e.target.style.borderColor = value.trim()
          ? 'var(--ring)'
          : DESIGN_SYSTEM.colors.border;
        e.target.style.backgroundColor = value.trim()
          ? DESIGN_SYSTEM.colors.background
          : 'var(--input)';
        e.target.style.boxShadow = value.trim()
          ? '0 0 0 3px var(--ring)'
          : 'none';
      }}
    />
    {showCharCount && value.trim() && (
      <div
        style={{
          marginTop: DESIGN_SYSTEM.spacing.sm,
          ...DESIGN_SYSTEM.typography.caption,
          color: DESIGN_SYSTEM.colors.mutedForeground,
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
    padding: `${DESIGN_SYSTEM.spacing.lg} ${DESIGN_SYSTEM.spacing.xxl}`,
    borderRadius: DESIGN_SYSTEM.borders.radius,
    ...DESIGN_SYSTEM.typography.body,
    fontWeight: '600',
    cursor: disabled ? 'not-allowed' : 'pointer',
    opacity: disabled ? 0.6 : 1,
    transition: DESIGN_SYSTEM.transitions.fast,
    display: 'flex',
    alignItems: 'center',
    gap: DESIGN_SYSTEM.spacing.sm,
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
    (
      text: string,
      toxicityPercentage: number,
      severityBreakdown?: Record<
        string,
        {
          avg_severity: number;
          match_count: number;
          final_score: number;
        }
      >
    ): ToxicityMap => {
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

      // Si tenemos breakdown de severidad, usarlo para asignar toxicidad más precisa
      if (severityBreakdown && Object.keys(severityBreakdown).length > 0) {
        // Palabras tóxicas comunes con sus niveles de severidad
        const toxicKeywords = {
          // Insultos leves
          tonto: 25,
          feo: 20,
          lento: 15,
          aburrido: 15,
          stupid: 25,
          ugly: 20,
          slow: 15,
          boring: 15,

          // Insultos moderados
          idiota: 60,
          estupido: 65,
          imbecil: 70,
          pendejo: 75,
          idiot: 60,
          moron: 70,
          fool: 65,
          gilipollas: 80,

          // Insultos severos
          cabron: 95,
          'hijo de puta': 100,
          puta: 90,
          perra: 85,
          zorra: 85,
          bastardo: 90,
          malparido: 95,
          asshole: 90,
          bitch: 85,
          whore: 90,
          bastard: 90,
          fuck: 80,
          shit: 75,
          damn: 70,
          hell: 70,

          // Acoso y amenazas
          matar: 95,
          morir: 80,
          odio: 85,
          destruir: 90,
          kill: 95,
          die: 80,
          hate: 85,
          destroy: 90,
          muerte: 85,
          asesinar: 95,
          eliminar: 90,

          // Discriminación
          racista: 95,
          xenofobo: 95,
          homofobo: 95,
          machista: 90,
          racist: 95,
          xenophobic: 95,
          homophobic: 95,
          sexist: 90,
          nazi: 95,
          fascista: 95,
          supremacista: 95,
        };

        // Asignar toxicidad basada en palabras conocidas
        cleanWords.forEach((cleanWord) => {
          const lowerWord = cleanWord.toLowerCase();
          let maxToxicity = 0;

          // Buscar coincidencias exactas y parciales
          for (const [keyword, toxicity] of Object.entries(toxicKeywords)) {
            if (lowerWord.includes(keyword) || keyword.includes(lowerWord)) {
              maxToxicity = Math.max(maxToxicity, toxicity);
            }
          }

          // Si no se encontró palabra tóxica conocida, asignar toxicidad basada en el porcentaje general
          if (maxToxicity === 0) {
            if (toxicityPercentage > 70) {
              maxToxicity = Math.round(toxicityPercentage * 0.3); // Palabras no tóxicas en texto tóxico
            } else if (toxicityPercentage > 30) {
              maxToxicity = Math.round(toxicityPercentage * 0.2);
            }
          }

          toxicityMap[cleanWord] = maxToxicity;
        });
      } else {
        // Fallback al método anterior si no hay breakdown de severidad
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
        result.toxicity_percentage,
        result.severity_breakdown
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

      <div
        style={{
          maxWidth: '1400px',
          margin: '0 auto',
          padding: DESIGN_SYSTEM.spacing.lg,
        }}
      >
        {/* Grid de Resultados del Análisis */}
        <div
          style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(350px, 1fr))',
            gap: DESIGN_SYSTEM.spacing.lg,
            marginBottom: DESIGN_SYSTEM.spacing.xxl,
          }}
        >
          {/* Cuadro Combinado: Toxicity Analysis + Confidence Analysis + Analysis Details */}
          <div
            style={{
              backgroundColor: DESIGN_SYSTEM.colors.card,
              borderRadius: DESIGN_SYSTEM.borders.radius,
              padding: DESIGN_SYSTEM.spacing.xl,
              boxShadow: DESIGN_SYSTEM.borders.shadow,
              border: `${DESIGN_SYSTEM.borders.width} solid ${DESIGN_SYSTEM.colors.border}`,
              display: 'flex',
              flexDirection: 'column',
              gap: DESIGN_SYSTEM.spacing.xl,
            }}
          >
            {/* Fila Superior: Toxicity Analysis y Confidence Analysis en disposición horizontal */}
            <div
              style={{
                display: 'grid',
                gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
                gap: DESIGN_SYSTEM.spacing.xl,
              }}
            >
              {/* Toxicity Analysis */}
              <div style={{ textAlign: 'center' }}>
                <h3
                  style={{
                    ...DESIGN_SYSTEM.typography.h4,
                    color: DESIGN_SYSTEM.colors.foreground,
                    textAlign: 'center',
                  }}
                >
                  📊 Toxicity Analysis
                </h3>
                <ToxicityGauge percentage={result?.toxicity_percentage || 0} />
              </div>

              {/* Confidence Analysis */}
              <div style={{ textAlign: 'center' }}>
                <h3
                  style={{
                    ...DESIGN_SYSTEM.typography.h4,
                    color: DESIGN_SYSTEM.colors.foreground,
                    textAlign: 'center',
                  }}
                >
                  🎯 Confidence Analysis
                </h3>
                <ConfidenceGauge confidence={result?.confidence || 0} />
              </div>
            </div>

            {/* Separador visual sutil */}
            <div
              style={{
                height: '1px',
                backgroundColor: DESIGN_SYSTEM.colors.border,
                margin: '0',
              }}
            />

            {/* Analysis Details mejorado */}
            {result && <AnalysisDetails result={result} />}
          </div>

          {/* Cuadro de Toxicity Level */}
          <div
            style={{
              backgroundColor: DESIGN_SYSTEM.colors.card,
              borderRadius: DESIGN_SYSTEM.borders.radius,
              padding: DESIGN_SYSTEM.spacing.xl,
              boxShadow: DESIGN_SYSTEM.borders.shadow,
              border: `${DESIGN_SYSTEM.borders.width} solid ${DESIGN_SYSTEM.colors.border}`,
            }}
          >
            <h3
              style={{
                ...DESIGN_SYSTEM.typography.h4,
                color: DESIGN_SYSTEM.colors.foreground,
                textAlign: 'center',
              }}
            >
              📊 Toxicity Level
            </h3>
            <div style={{ marginBottom: DESIGN_SYSTEM.spacing.md }}>
              <div
                style={{
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'center',
                  marginBottom: DESIGN_SYSTEM.spacing.sm,
                }}
              >
                <span
                  style={{
                    ...DESIGN_SYSTEM.typography.small,
                    color: DESIGN_SYSTEM.colors.mutedForeground,
                    fontWeight: '500',
                  }}
                >
                  Current Level
                </span>
                <span
                  style={{
                    ...DESIGN_SYSTEM.typography.small,
                    color: DESIGN_SYSTEM.colors.foreground,
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
                  backgroundColor: DESIGN_SYSTEM.colors.muted,
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
                      : DESIGN_SYSTEM.colors.muted,
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
                ...DESIGN_SYSTEM.typography.micro,
                color: DESIGN_SYSTEM.colors.mutedForeground,
              }}
            >
              <span>0%</span>
              <span>50%</span>
              <span>100%</span>
            </div>

            <div
              style={{
                marginTop: DESIGN_SYSTEM.spacing.lg,
                padding: DESIGN_SYSTEM.spacing.md,
                backgroundColor: DESIGN_SYSTEM.colors.muted,
                borderRadius: DESIGN_SYSTEM.borders.radius,
                border: `${DESIGN_SYSTEM.borders.width} solid ${DESIGN_SYSTEM.colors.border}`,
              }}
            >
              <div
                style={{
                  ...DESIGN_SYSTEM.typography.tiny,
                  fontWeight: '600',
                  color: DESIGN_SYSTEM.colors.foreground,
                  marginBottom: DESIGN_SYSTEM.spacing.sm,
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
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: DESIGN_SYSTEM.spacing.xs,
                  }}
                >
                  <div
                    style={{
                      width: '10px',
                      height: '10px',
                      backgroundColor: DESIGN_SYSTEM.colors.secondary,
                      borderRadius: '50%',
                      border: `${DESIGN_SYSTEM.borders.width} solid ${DESIGN_SYSTEM.colors.secondary}`,
                    }}
                  />
                  <span
                    style={{
                      ...DESIGN_SYSTEM.typography.micro,
                      color: DESIGN_SYSTEM.colors.secondary,
                      fontWeight: '600',
                    }}
                  >
                    Safe
                  </span>
                </div>
                <div
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: DESIGN_SYSTEM.spacing.xs,
                  }}
                >
                  <div
                    style={{
                      width: '10px',
                      height: '10px',
                      backgroundColor: DESIGN_SYSTEM.colors.accent,
                      borderRadius: '50%',
                      border: `${DESIGN_SYSTEM.borders.width} solid ${DESIGN_SYSTEM.colors.accent}`,
                    }}
                  />
                  <span
                    style={{
                      ...DESIGN_SYSTEM.typography.micro,
                      color: DESIGN_SYSTEM.colors.accent,
                      fontWeight: '600',
                    }}
                  >
                    Moderate
                  </span>
                </div>
                <div
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: DESIGN_SYSTEM.spacing.xs,
                  }}
                >
                  <div
                    style={{
                      width: '10px',
                      height: '10px',
                      backgroundColor: DESIGN_SYSTEM.colors.destructive,
                      borderRadius: '50%',
                      border: `${DESIGN_SYSTEM.borders.width} solid ${DESIGN_SYSTEM.colors.destructive}`,
                    }}
                  />
                  <span
                    style={{
                      ...DESIGN_SYSTEM.typography.micro,
                      color: DESIGN_SYSTEM.colors.destructive,
                      fontWeight: '600',
                    }}
                  >
                    High Risk
                  </span>
                </div>
              </div>
            </div>

            {/* Sección de Confidence Analysis debajo del Toxicity Level */}
            <div
              style={{
                marginTop: DESIGN_SYSTEM.spacing.lg,
                padding: DESIGN_SYSTEM.spacing.lg,
                backgroundColor: DESIGN_SYSTEM.colors.card,
                borderRadius: DESIGN_SYSTEM.borders.radius,
                border: `${DESIGN_SYSTEM.borders.width} solid ${DESIGN_SYSTEM.colors.border}`,
              }}
            >
              <h4
                style={{
                  ...DESIGN_SYSTEM.typography.h4,
                  color: DESIGN_SYSTEM.colors.foreground,
                  textAlign: 'center',
                }}
              >
                🎯 Confidence Analysis
              </h4>

              <div style={{ marginBottom: DESIGN_SYSTEM.spacing.md }}>
                <div
                  style={{
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'center',
                    marginBottom: DESIGN_SYSTEM.spacing.sm,
                  }}
                >
                  <span
                    style={{
                      ...DESIGN_SYSTEM.typography.small,
                      color: DESIGN_SYSTEM.colors.mutedForeground,
                      fontWeight: '500',
                    }}
                  >
                    Confidence Level
                  </span>
                  <span
                    style={{
                      ...DESIGN_SYSTEM.typography.small,
                      color: DESIGN_SYSTEM.colors.foreground,
                      fontWeight: '600',
                    }}
                  >
                    {result ? Math.round(result.confidence) : 0}%
                  </span>
                </div>
                <div
                  style={{
                    width: '100%',
                    height: '12px',
                    backgroundColor: DESIGN_SYSTEM.colors.muted,
                    borderRadius: '6px',
                    overflow: 'hidden',
                    position: 'relative',
                  }}
                >
                  <div
                    style={{
                      width: `${result?.confidence || 0}%`,
                      height: '100%',
                      backgroundColor: result
                        ? (() => {
                            const confidence = result.confidence;
                            if (confidence >= 80)
                              return DESIGN_SYSTEM.colors.secondary;
                            if (confidence >= 60)
                              return DESIGN_SYSTEM.colors.accent;
                            return DESIGN_SYSTEM.colors.destructive;
                          })()
                        : DESIGN_SYSTEM.colors.muted,
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
                  ...DESIGN_SYSTEM.typography.micro,
                  color: DESIGN_SYSTEM.colors.mutedForeground,
                  marginBottom: DESIGN_SYSTEM.spacing.md,
                }}
              >
                <span>0%</span>
                <span>50%</span>
                <span>100%</span>
              </div>

              <div
                style={{
                  padding: DESIGN_SYSTEM.spacing.md,
                  backgroundColor: DESIGN_SYSTEM.colors.muted,
                  borderRadius: DESIGN_SYSTEM.borders.radius,
                  border: `${DESIGN_SYSTEM.borders.width} solid ${DESIGN_SYSTEM.colors.border}`,
                }}
              >
                <div
                  style={{
                    ...DESIGN_SYSTEM.typography.tiny,
                    fontWeight: '600',
                    color: DESIGN_SYSTEM.colors.foreground,
                    marginBottom: DESIGN_SYSTEM.spacing.sm,
                    textAlign: 'center',
                  }}
                >
                  🎨 Confidence Color Legend
                </div>
                <div
                  style={{
                    display: 'flex',
                    justifyContent: 'space-around',
                    alignItems: 'center',
                    gap: DESIGN_SYSTEM.spacing.xs,
                  }}
                >
                  <div
                    style={{
                      display: 'flex',
                      alignItems: 'center',
                      gap: DESIGN_SYSTEM.spacing.xs,
                    }}
                  >
                    <div
                      style={{
                        width: '10px',
                        height: '10px',
                        backgroundColor: DESIGN_SYSTEM.colors.secondary,
                        borderRadius: '50%',
                        border: `${DESIGN_SYSTEM.borders.width} solid ${DESIGN_SYSTEM.colors.secondary}`,
                      }}
                    />
                    <span
                      style={{
                        ...DESIGN_SYSTEM.typography.micro,
                        color: DESIGN_SYSTEM.colors.secondary,
                        fontWeight: '600',
                      }}
                    >
                      Alto
                    </span>
                  </div>
                  <div
                    style={{
                      display: 'flex',
                      alignItems: 'center',
                      gap: DESIGN_SYSTEM.spacing.xs,
                    }}
                  >
                    <div
                      style={{
                        width: '10px',
                        height: '10px',
                        backgroundColor: DESIGN_SYSTEM.colors.accent,
                        borderRadius: '50%',
                        border: `${DESIGN_SYSTEM.borders.width} solid ${DESIGN_SYSTEM.colors.accent}`,
                      }}
                    />
                    <span
                      style={{
                        ...DESIGN_SYSTEM.typography.micro,
                        color: DESIGN_SYSTEM.colors.accent,
                        fontWeight: '600',
                      }}
                    >
                      Medio
                    </span>
                  </div>
                  <div
                    style={{
                      display: 'flex',
                      alignItems: 'center',
                      gap: DESIGN_SYSTEM.spacing.xs,
                    }}
                  >
                    <div
                      style={{
                        width: '10px',
                        height: '10px',
                        backgroundColor: DESIGN_SYSTEM.colors.destructive,
                        borderRadius: '50%',
                        border: `${DESIGN_SYSTEM.borders.width} solid ${DESIGN_SYSTEM.colors.destructive}`,
                      }}
                    />
                    <span
                      style={{
                        ...DESIGN_SYSTEM.typography.micro,
                        color: DESIGN_SYSTEM.colors.destructive,
                        fontWeight: '600',
                      }}
                    >
                      Bajo
                    </span>
                  </div>
                </div>
              </div>
            </div>

            {/* Sección de Categorías Detectadas con Explicaciones */}
            {result &&
              result.detected_categories &&
              result.detected_categories.length > 0 && (
                <div
                  style={{
                    marginTop: DESIGN_SYSTEM.spacing.lg,
                    padding: DESIGN_SYSTEM.spacing.lg,
                    backgroundColor: DESIGN_SYSTEM.colors.card,
                    borderRadius: DESIGN_SYSTEM.borders.radius,
                    border: `${DESIGN_SYSTEM.borders.width} solid ${DESIGN_SYSTEM.colors.border}`,
                  }}
                >
                  <h4
                    style={{
                      ...DESIGN_SYSTEM.typography.h4,
                      color: DESIGN_SYSTEM.colors.foreground,
                      textAlign: 'center',
                    }}
                  >
                    🏷️ Categorías Detectadas
                  </h4>

                  <div
                    style={{
                      display: 'flex',
                      flexDirection: 'column',
                      gap: DESIGN_SYSTEM.spacing.sm,
                    }}
                  >
                    {result.detected_categories.map((category, index) => (
                      <div
                        key={index}
                        style={{
                          padding: `${DESIGN_SYSTEM.spacing.sm} ${DESIGN_SYSTEM.spacing.md}`,
                          backgroundColor: DESIGN_SYSTEM.colors.muted,
                          borderRadius: DESIGN_SYSTEM.borders.radius,
                          border: `${DESIGN_SYSTEM.borders.width} solid ${DESIGN_SYSTEM.colors.border}`,
                        }}
                      >
                        <div
                          style={{
                            ...DESIGN_SYSTEM.typography.small,
                            fontWeight: '600',
                            color: DESIGN_SYSTEM.colors.foreground,
                            marginBottom: DESIGN_SYSTEM.spacing.xs,
                            textTransform: 'capitalize',
                          }}
                        >
                          {category.replace('_', ' ')}
                        </div>

                        {result.explanations &&
                          result.explanations[category] && (
                            <div
                              style={{
                                ...DESIGN_SYSTEM.typography.tiny,
                                color: DESIGN_SYSTEM.colors.mutedForeground,
                                fontStyle: 'italic',
                                lineHeight: '1.4',
                                marginTop: DESIGN_SYSTEM.spacing.xs,
                                padding: `${DESIGN_SYSTEM.spacing.xs} ${DESIGN_SYSTEM.spacing.sm}`,
                                backgroundColor:
                                  DESIGN_SYSTEM.colors.background,
                                borderRadius: '4px',
                                border: `${DESIGN_SYSTEM.borders.width} solid ${DESIGN_SYSTEM.colors.border}`,
                                opacity: 0.8,
                              }}
                            >
                              💡 {result.explanations[category]}
                            </div>
                          )}
                      </div>
                    ))}
                  </div>
                </div>
              )}
          </div>
        </div>

        {/* Texto Analizado con Palabras Resaltadas */}
        <div
          style={{
            backgroundColor: DESIGN_SYSTEM.colors.card,
            borderRadius: DESIGN_SYSTEM.borders.radius,
            padding: DESIGN_SYSTEM.spacing.xl,
            boxShadow: DESIGN_SYSTEM.borders.shadow,
            border: `${DESIGN_SYSTEM.borders.width} solid ${DESIGN_SYSTEM.colors.border}`,
            marginBottom: DESIGN_SYSTEM.spacing.xxl,
          }}
        >
          <h3
            style={{
              ...DESIGN_SYSTEM.typography.h3,
              color: DESIGN_SYSTEM.colors.foreground,
              textAlign: 'center',
            }}
          >
            📝 Analyzed Text with Toxicity Highlighting
          </h3>
          <div
            style={{
              backgroundColor: DESIGN_SYSTEM.colors.muted,
              padding: DESIGN_SYSTEM.spacing.lg,
              borderRadius: DESIGN_SYSTEM.borders.radius,
              border: `${DESIGN_SYSTEM.borders.width} solid ${DESIGN_SYSTEM.colors.border}`,
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

        {/* Análisis de Severidad Ultra-Sensible */}
        {result &&
          result.severity_breakdown &&
          Object.keys(result.severity_breakdown).length > 0 && (
            <SeverityBreakdown
              severityBreakdown={result.severity_breakdown}
              detectedCategories={result.detected_categories}
            />
          )}

        {/* Nueva Caja de Texto para Análisis Adicionales */}
        <div
          style={{
            backgroundColor: DESIGN_SYSTEM.colors.card,
            borderRadius: DESIGN_SYSTEM.borders.radius,
            padding: DESIGN_SYSTEM.spacing.xl,
            boxShadow: DESIGN_SYSTEM.borders.shadow,
            border: `${DESIGN_SYSTEM.borders.width} solid ${DESIGN_SYSTEM.colors.border}`,
          }}
        >
          <h3
            style={{
              ...DESIGN_SYSTEM.typography.h3,
              color: DESIGN_SYSTEM.colors.foreground,
              display: 'flex',
              alignItems: 'center',
              gap: DESIGN_SYSTEM.spacing.xs,
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

          <div
            style={{
              display: 'flex',
              gap: DESIGN_SYSTEM.spacing.sm,
              flexWrap: 'wrap',
            }}
          >
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
                marginTop: DESIGN_SYSTEM.spacing.lg,
                padding: DESIGN_SYSTEM.spacing.md,
                backgroundColor: DESIGN_SYSTEM.colors.destructive,
                color: 'var(--destructive-foreground)',
                borderRadius: DESIGN_SYSTEM.borders.radius,
                border: `${DESIGN_SYSTEM.borders.width} solid ${DESIGN_SYSTEM.colors.destructive}`,
                animation: 'shake 0.5s ease-in-out',
                ...DESIGN_SYSTEM.typography.caption,
              }}
            >
              <div
                style={{
                  marginBottom: DESIGN_SYSTEM.spacing.xs,
                  fontWeight: '600',
                }}
              >
                ❌ {error}
              </div>
              {error.includes('Failed to fetch') && (
                <div
                  style={{
                    ...DESIGN_SYSTEM.typography.small,
                    color: 'var(--destructive-foreground)',
                  }}
                >
                  <strong>🔧 Solution:</strong>
                  <ul
                    style={{
                      marginTop: DESIGN_SYSTEM.spacing.xs,
                      marginLeft: DESIGN_SYSTEM.spacing.lg,
                    }}
                  >
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
