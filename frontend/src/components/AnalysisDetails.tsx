import React from 'react';
import type { ToxicityResult } from '../hooks/useToxicityAnalysis';

interface AnalysisDetailsProps {
  result: ToxicityResult;
}

const AnalysisDetails: React.FC<AnalysisDetailsProps> = ({ result }) => {
  const getCategoryColor = (category: string): string => {
    switch (category.toLowerCase()) {
      case 'safe':
        return 'oklch(0.8 0.15 120)'; // Green
      case 'moderate':
        return 'oklch(0.7 0.2 60)'; // Yellow
      case 'high_risk':
      case 'high risk':
        return 'oklch(0.6 0.2 30)'; // Orange
      case 'critical_risk':
      case 'critical risk':
        return 'var(--destructive)'; // Red
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
    if (technique.length > 25) {
      return technique.substring(0, 25) + '...';
    }
    return technique;
  };

  const formatTimestamp = (timestamp: string): string => {
    const date = new Date(timestamp);
    const now = new Date();
    const diffMs = now.getTime() - date.getTime();
    const diffMins = Math.floor(diffMs / (1000 * 60));

    if (diffMins < 1) return 'Just now';
    if (diffMins < 60) return `${diffMins}m ago`;
    if (diffMins < 1440) return `${Math.floor(diffMins / 60)}h ago`;
    return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
  };

  return (
    <div
      style={{
        backgroundColor: 'var(--background)',
        borderRadius: '8px',
        border: '1px solid var(--border)',
        overflow: 'hidden',
        animation: 'fadeInUp 0.4s ease-out',
      }}
    >
      {/* Compact Header */}
      <div
        style={{
          backgroundColor: 'var(--muted)',
          padding: '12px 16px',
          borderBottom: '1px solid var(--border)',
          display: 'flex',
          alignItems: 'center',
          gap: '8px',
        }}
      >
        <div style={{ fontSize: '16px' }}>📊</div>
        <h4
          style={{
            fontSize: '14px',
            fontWeight: '600',
            color: 'var(--foreground)',
            margin: 0,
            textTransform: 'uppercase',
            letterSpacing: '0.5px',
          }}
        >
          Analysis Details
        </h4>
      </div>

      {/* Compact Information Grid */}
      <div style={{ padding: '16px' }}>
        {/* Key Metrics Row */}
        <div
          style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(3, 1fr)',
            gap: '12px',
            marginBottom: '16px',
          }}
        >
          {/* Score */}
          <div
            style={{
              textAlign: 'center',
              padding: '8px',
              backgroundColor: 'var(--muted)',
              borderRadius: '6px',
              border: '1px solid var(--border)',
            }}
          >
            <div
              style={{
                fontSize: '18px',
                fontWeight: '700',
                color: 'var(--foreground)',
                marginBottom: '2px',
              }}
            >
              {Math.round(result.toxicity_percentage)}%
            </div>
            <div
              style={{
                fontSize: '10px',
                color: 'var(--muted-foreground)',
                fontWeight: '500',
                textTransform: 'uppercase',
                letterSpacing: '0.3px',
              }}
            >
              Score
            </div>
          </div>

          {/* Category */}
          <div
            style={{
              textAlign: 'center',
              padding: '8px',
              backgroundColor: 'var(--muted)',
              borderRadius: '6px',
              border: '1px solid var(--border)',
            }}
          >
            <div
              style={{
                fontSize: '14px',
                marginBottom: '2px',
              }}
            >
              {getCategoryIcon(result.toxicity_category)}
            </div>
            <div
              style={{
                fontSize: '10px',
                color: getCategoryColor(result.toxicity_category),
                fontWeight: '600',
                textTransform: 'capitalize',
              }}
            >
              {result.toxicity_category.replace('_', ' ')}
            </div>
          </div>

          {/* Response Time */}
          <div
            style={{
              textAlign: 'center',
              padding: '8px',
              backgroundColor: 'var(--muted)',
              borderRadius: '6px',
              border: '1px solid var(--border)',
            }}
          >
            <div
              style={{
                fontSize: '16px',
                fontWeight: '600',
                color: 'var(--foreground)',
                marginBottom: '2px',
              }}
            >
              {result.response_time_ms}ms
            </div>
            <div
              style={{
                fontSize: '10px',
                color: 'var(--muted-foreground)',
                fontWeight: '500',
                textTransform: 'uppercase',
                letterSpacing: '0.3px',
              }}
            >
              Time
            </div>
          </div>
        </div>

        {/* Technical Details Table */}
        <div
          style={{
            backgroundColor: 'var(--card)',
            borderRadius: '6px',
            border: '1px solid var(--border)',
            overflow: 'hidden',
          }}
        >
          {/* Table Header */}
          <div
            style={{
              backgroundColor: 'var(--muted)',
              padding: '8px 12px',
              borderBottom: '1px solid var(--border)',
              fontSize: '11px',
              fontWeight: '600',
              color: 'var(--muted-foreground)',
              textTransform: 'uppercase',
              letterSpacing: '0.3px',
            }}
          >
            Technical Information
          </div>

          {/* Table Rows */}
          <div style={{ fontSize: '12px' }}>
            {/* Model Used */}
            <div
              style={{
                display: 'flex',
                alignItems: 'center',
                padding: '8px 12px',
                borderBottom: '1px solid var(--border)',
                gap: '8px',
              }}
            >
              <div style={{ fontSize: '12px', opacity: 0.7 }}>🤖</div>
              <div
                style={{
                  color: 'var(--muted-foreground)',
                  fontWeight: '500',
                  minWidth: '60px',
                }}
              >
                Model:
              </div>
              <div
                style={{
                  color: 'var(--foreground)',
                  fontWeight: '600',
                  flex: 1,
                }}
                title={result.model_used || 'N/A'}
              >
                {result.model_used || 'N/A'}
              </div>
            </div>

            {/* Classification Technique */}
            <div
              style={{
                display: 'flex',
                alignItems: 'center',
                padding: '8px 12px',
                borderBottom: '1px solid var(--border)',
                gap: '8px',
              }}
            >
              <div style={{ fontSize: '12px', opacity: 0.7 }}>⚙️</div>
              <div
                style={{
                  color: 'var(--muted-foreground)',
                  fontWeight: '500',
                  minWidth: '60px',
                }}
              >
                Method:
              </div>
              <div
                style={{
                  color: 'var(--foreground)',
                  fontWeight: '600',
                  flex: 1,
                }}
                title={result.classification_technique}
              >
                {formatTechnique(result.classification_technique)}
              </div>
            </div>

            {/* Timestamp */}
            <div
              style={{
                display: 'flex',
                alignItems: 'center',
                padding: '8px 12px',
                gap: '8px',
              }}
            >
              <div style={{ fontSize: '12px', opacity: 0.7 }}>📅</div>
              <div
                style={{
                  color: 'var(--muted-foreground)',
                  fontWeight: '500',
                  minWidth: '60px',
                }}
              >
                Analyzed:
              </div>
              <div
                style={{
                  color: 'var(--foreground)',
                  fontWeight: '600',
                  flex: 1,
                }}
                title={new Date(result.timestamp).toLocaleString()}
              >
                {formatTimestamp(result.timestamp)}
              </div>
            </div>
          </div>
        </div>

        {/* Additional Stats Row */}
        <div
          style={{
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            marginTop: '12px',
            padding: '8px 12px',
            backgroundColor: 'var(--muted)',
            borderRadius: '6px',
            border: '1px solid var(--border)',
            fontSize: '11px',
          }}
        >
          <span style={{ color: 'var(--muted-foreground)' }}>
            📝 {result.word_count} words
          </span>
          <span style={{ color: 'var(--muted-foreground)' }}>
            🏷️ {result.detected_categories.length} categories
          </span>
          {result.ultra_sensitive_analysis && (
            <span
              style={{
                color: 'var(--primary)',
                fontWeight: '600',
              }}
            >
              🚨 Ultra-Sensitive
            </span>
          )}
        </div>
      </div>

      {/* CSS styles for animations */}
      <style>
        {`
          @keyframes fadeInUp {
            from {
              opacity: 0;
              transform: translateY(10px);
            }
            to {
              opacity: 1;
              transform: translateY(0);
            }
          }
        `}
      </style>
    </div>
  );
};

export default AnalysisDetails;
