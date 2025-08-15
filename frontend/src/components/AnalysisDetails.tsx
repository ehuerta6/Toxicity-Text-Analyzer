import React from 'react';
import type { ToxicityResult } from '../hooks/useToxicityAnalysis';

interface AnalysisDetailsProps {
  result: ToxicityResult;
}

const AnalysisDetails: React.FC<AnalysisDetailsProps> = ({ result }) => {
  const getCategoryColor = (category: string): string => {
    switch (category.toLowerCase()) {
      case 'safe':
        return 'oklch(0.8 0.15 120)'; // Verde
      case 'moderate':
        return 'oklch(0.7 0.2 60)'; // Amarillo
      case 'high_risk':
      case 'high risk':
        return 'oklch(0.6 0.2 30)'; // Naranja
      case 'critical_risk':
      case 'critical risk':
        return 'var(--destructive)'; // Rojo
      default:
        return 'var(--foreground)';
    }
  };

  const getCategoryIcon = (category: string): string => {
    switch (category.toLowerCase()) {
      case 'safe':
        return '🟢';
      case 'moderate':
        return '🟡';
      case 'high_risk':
      case 'high risk':
        return '🟠';
      case 'critical_risk':
      case 'critical risk':
        return '🔴';
      default:
        return '⚪';
    }
  };

  const formatTechnique = (technique: string): string => {
    if (technique.length > 40) {
      return technique.substring(0, 40) + '...';
    }
    return technique;
  };

  return (
    <div
      style={{
        backgroundColor: 'var(--card)',
        borderRadius: 'var(--radius)',
        padding: '24px',
        border: '1px solid var(--border)',
        boxShadow: '0 2px 8px rgba(0, 0, 0, 0.04)',
        marginTop: '16px',
        animation: 'fadeInUp 0.6s ease-out',
      }}
    >
      {/* Header con icono y título */}
      <div
        style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          gap: '12px',
          marginBottom: '24px',
          paddingBottom: '16px',
          borderBottom: '1px solid var(--border)',
        }}
      >
        <div
          style={{
            fontSize: '24px',
            animation: 'pulse 2s infinite',
          }}
        >
          📊
        </div>
        <h3
          style={{
            fontSize: '20px',
            fontWeight: '600',
            color: 'var(--foreground)',
            margin: 0,
          }}
        >
          Analysis Details
        </h3>
      </div>

      {/* Grid de métricas principales */}
      <div
        style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(160px, 1fr))',
          gap: '20px',
          marginBottom: '24px',
        }}
      >
        {/* Score */}
        <div
          style={{
            backgroundColor: 'var(--muted)',
            borderRadius: '12px',
            padding: '16px',
            textAlign: 'center',
            border: '2px solid transparent',
            transition: 'all 0.3s ease',
            cursor: 'default',
            animation: 'slideInLeft 0.5s ease-out',
          }}
          onMouseEnter={(e) => {
            e.currentTarget.style.borderColor = 'var(--primary)';
            e.currentTarget.style.transform = 'translateY(-2px)';
          }}
          onMouseLeave={(e) => {
            e.currentTarget.style.borderColor = 'transparent';
            e.currentTarget.style.transform = 'translateY(0)';
          }}
        >
          <div
            style={{
              fontSize: '32px',
              marginBottom: '8px',
              animation: 'bounceIn 0.8s ease-out',
            }}
          >
            🎯
          </div>
          <div
            style={{
              fontSize: '14px',
              color: 'var(--muted-foreground)',
              marginBottom: '8px',
              fontWeight: '500',
              textTransform: 'uppercase',
              letterSpacing: '0.5px',
            }}
          >
            Toxicity Score
          </div>
          <div
            style={{
              fontSize: '28px',
              fontWeight: '700',
              color: 'var(--foreground)',
            }}
          >
            {Math.round(result.toxicity_percentage)}%
          </div>
        </div>

        {/* Category */}
        <div
          style={{
            backgroundColor: 'var(--muted)',
            borderRadius: '12px',
            padding: '16px',
            textAlign: 'center',
            border: '2px solid transparent',
            transition: 'all 0.3s ease',
            cursor: 'default',
            animation: 'slideInLeft 0.5s ease-out 0.1s both',
          }}
          onMouseEnter={(e) => {
            e.currentTarget.style.borderColor = 'var(--primary)';
            e.currentTarget.style.transform = 'translateY(-2px)';
          }}
          onMouseLeave={(e) => {
            e.currentTarget.style.borderColor = 'transparent';
            e.currentTarget.style.transform = 'translateY(0)';
          }}
        >
          <div
            style={{
              fontSize: '32px',
              marginBottom: '8px',
              animation: 'bounceIn 0.8s ease-out 0.1s both',
            }}
          >
            {getCategoryIcon(result.toxicity_category)}
          </div>
          <div
            style={{
              fontSize: '14px',
              color: 'var(--muted-foreground)',
              marginBottom: '8px',
              fontWeight: '500',
              textTransform: 'uppercase',
              letterSpacing: '0.5px',
            }}
          >
            Risk Level
          </div>
          <div
            style={{
              fontSize: '20px',
              fontWeight: '600',
              color: getCategoryColor(result.toxicity_category),
              textTransform: 'capitalize',
            }}
          >
            {result.toxicity_category.replace('_', ' ')}
          </div>
        </div>

        {/* Response Time */}
        <div
          style={{
            backgroundColor: 'var(--muted)',
            borderRadius: '12px',
            padding: '16px',
            textAlign: 'center',
            border: '2px solid transparent',
            transition: 'all 0.3s ease',
            cursor: 'default',
            animation: 'slideInLeft 0.5s ease-out 0.2s both',
          }}
          onMouseEnter={(e) => {
            e.currentTarget.style.borderColor = 'var(--primary)';
            e.currentTarget.style.transform = 'translateY(-2px)';
          }}
          onMouseLeave={(e) => {
            e.currentTarget.style.borderColor = 'transparent';
            e.currentTarget.style.transform = 'translateY(0)';
          }}
        >
          <div
            style={{
              fontSize: '32px',
              marginBottom: '8px',
              animation: 'bounceIn 0.8s ease-out 0.2s both',
            }}
          >
            ⏱️
          </div>
          <div
            style={{
              fontSize: '14px',
              color: 'var(--muted-foreground)',
              marginBottom: '8px',
              fontWeight: '500',
              textTransform: 'uppercase',
              letterSpacing: '0.5px',
            }}
          >
            Response Time
          </div>
          <div
            style={{
              fontSize: '20px',
              fontWeight: '600',
              color: 'var(--foreground)',
            }}
          >
            {result.response_time_ms}ms
          </div>
        </div>
      </div>

      {/* Información técnica en tarjetas horizontales */}
      <div
        style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))',
          gap: '16px',
          marginBottom: '24px',
        }}
      >
        {/* Model Used */}
        <div
          style={{
            backgroundColor: 'var(--background)',
            borderRadius: '8px',
            padding: '16px',
            border: '1px solid var(--border)',
            transition: 'all 0.2s ease',
            animation: 'slideInUp 0.6s ease-out 0.3s both',
          }}
          onMouseEnter={(e) => {
            e.currentTarget.style.backgroundColor = 'var(--muted)';
            e.currentTarget.style.transform = 'scale(1.02)';
          }}
          onMouseLeave={(e) => {
            e.currentTarget.style.backgroundColor = 'var(--background)';
            e.currentTarget.style.transform = 'scale(1)';
          }}
        >
          <div
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '12px',
              marginBottom: '8px',
            }}
          >
            <div style={{ fontSize: '20px' }}>🤖</div>
            <div
              style={{
                fontSize: '14px',
                color: 'var(--muted-foreground)',
                fontWeight: '500',
                textTransform: 'uppercase',
                letterSpacing: '0.5px',
              }}
            >
              Model Used
            </div>
          </div>
          <div
            style={{
              fontSize: '16px',
              fontWeight: '600',
              color: 'var(--foreground)',
              wordBreak: 'break-word',
            }}
          >
            {result.model_used || 'N/A'}
          </div>
        </div>

        {/* Classification Technique */}
        <div
          style={{
            backgroundColor: 'var(--background)',
            borderRadius: '8px',
            padding: '16px',
            border: '1px solid var(--border)',
            transition: 'all 0.2s ease',
            animation: 'slideInUp 0.6s ease-out 0.4s both',
          }}
          onMouseEnter={(e) => {
            e.currentTarget.style.backgroundColor = 'var(--muted)';
            e.currentTarget.style.transform = 'scale(1.02)';
          }}
          onMouseLeave={(e) => {
            e.currentTarget.style.backgroundColor = 'var(--background)';
            e.currentTarget.style.transform = 'scale(1)';
          }}
        >
          <div
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '12px',
              marginBottom: '8px',
            }}
          >
            <div style={{ fontSize: '20px' }}>⚙️</div>
            <div
              style={{
                fontSize: '14px',
                color: 'var(--muted-foreground)',
                fontWeight: '500',
                textTransform: 'uppercase',
                letterSpacing: '0.5px',
              }}
            >
              Technique
            </div>
          </div>
          <div
            style={{
              fontSize: '16px',
              fontWeight: '600',
              color: 'var(--foreground)',
              wordBreak: 'break-word',
            }}
            title={result.classification_technique}
          >
            {formatTechnique(result.classification_technique)}
          </div>
        </div>
      </div>

      {/* Información adicional */}
      <div
        style={{
          backgroundColor: 'var(--muted)',
          borderRadius: '8px',
          padding: '16px',
          textAlign: 'center',
          border: '1px solid var(--border)',
          animation: 'slideInUp 0.6s ease-out 0.5s both',
        }}
      >
        <div
          style={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            gap: '8px',
            marginBottom: '8px',
          }}
        >
          <div style={{ fontSize: '16px' }}>📅</div>
          <div
            style={{
              fontSize: '14px',
              color: 'var(--muted-foreground)',
              fontWeight: '500',
            }}
          >
            Analyzed on{' '}
            {new Date(result.timestamp).toLocaleString('en-US', {
              year: 'numeric',
              month: 'short',
              day: 'numeric',
              hour: '2-digit',
              minute: '2-digit',
            })}
          </div>
        </div>

        {/* Información adicional */}
        <div
          style={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            gap: '16px',
            marginTop: '12px',
            fontSize: '13px',
            color: 'var(--muted-foreground)',
          }}
        >
          <span>📝 {result.word_count} words</span>
          <span>🏷️ {result.detected_categories.length} categories</span>
          {result.ultra_sensitive_analysis && (
            <span style={{ color: 'var(--primary)' }}>🚨 Ultra-Sensitive</span>
          )}
        </div>
      </div>

      {/* Estilos CSS para animaciones */}
      <style>
        {`
          @keyframes fadeInUp {
            from {
              opacity: 0;
              transform: translateY(20px);
            }
            to {
              opacity: 1;
              transform: translateY(0);
            }
          }
          
          @keyframes slideInLeft {
            from {
              opacity: 0;
              transform: translateX(-20px);
            }
            to {
              opacity: 1;
              transform: translateX(0);
            }
          }
          
          @keyframes slideInUp {
            from {
              opacity: 0;
              transform: translateY(30px);
            }
            to {
              opacity: 1;
              transform: translateY(0);
            }
          }
          
          @keyframes bounceIn {
            0% {
              opacity: 0;
              transform: scale(0.3);
            }
            50% {
              opacity: 1;
              transform: scale(1.05);
            }
            70% {
              transform: scale(0.9);
            }
            100% {
              opacity: 1;
              transform: scale(1);
            }
          }
          
          @keyframes pulse {
            0%, 100% {
              opacity: 1;
            }
            50% {
              opacity: 0.7;
            }
          }
        `}
      </style>
    </div>
  );
};

export default AnalysisDetails;
