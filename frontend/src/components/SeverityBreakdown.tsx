import React from 'react';

interface SeverityBreakdownProps {
  severityBreakdown: Record<
    string,
    {
      avg_severity: number;
      match_count: number;
      final_score: number;
    }
  >;
  detectedCategories: string[];
}

const SeverityBreakdown: React.FC<SeverityBreakdownProps> = ({
  severityBreakdown,
  detectedCategories,
}) => {
  if (!severityBreakdown || Object.keys(severityBreakdown).length === 0) {
    return null;
  }

  const getSeverityColor = (severity: number): string => {
    if (severity >= 0.9) return 'var(--destructive)'; // Red for critical severity
    if (severity >= 0.7) return 'oklch(0.6 0.2 30)'; // Orange for high severity
    if (severity >= 0.5) return 'oklch(0.7 0.2 60)'; // Yellow for moderate severity
    return 'oklch(0.8 0.15 120)'; // Green for low severity
  };

  const getSeverityLabel = (severity: number): string => {
    if (severity >= 0.9) return 'CRITICAL';
    if (severity >= 0.7) return 'HIGH';
    if (severity >= 0.5) return 'MODERATE';
    return 'LOW';
  };

  const getCategoryName = (category: string): string => {
    const categoryNames: Record<string, string> = {
      insulto_leve: 'Mild Insult',
      insulto_moderado: 'Moderate Insult',
      insulto_severo: 'Severe Insult',
      acoso_directo: 'Direct Harassment',
      discriminacion: 'Discrimination',
      amenazas: 'Threats',
      spam_toxico: 'Toxic Spam',
    };
    return categoryNames[category] || category.replace('_', ' ');
  };

  return (
    <div
      style={{
        backgroundColor: 'var(--card)',
        borderRadius: 'var(--radius)',
        padding: '20px',
        border: '1px solid var(--border)',
        marginTop: '16px',
      }}
    >
      <h4
        style={{
          fontSize: '18px',
          fontWeight: '600',
          color: 'var(--foreground)',
          margin: '0 0 16px 0',
          textAlign: 'center',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          gap: '8px',
        }}
      >
        🚨 Ultra-Sensitive Severity Analysis
      </h4>

      <div
        style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))',
          gap: '16px',
        }}
      >
        {detectedCategories.map((category) => {
          const breakdown = severityBreakdown[category];
          if (!breakdown) return null;

          const severityColor = getSeverityColor(breakdown.avg_severity);
          const severityLabel = getSeverityLabel(breakdown.avg_severity);

          return (
            <div
              key={category}
              style={{
                backgroundColor: 'var(--muted)',
                borderRadius: '8px',
                padding: '16px',
                border: `2px solid ${severityColor}`,
                position: 'relative',
              }}
            >
              {/* Severity badge */}
              <div
                style={{
                  position: 'absolute',
                  top: '-8px',
                  right: '12px',
                  backgroundColor: severityColor,
                  color: 'white',
                  padding: '4px 8px',
                  borderRadius: '12px',
                  fontSize: '11px',
                  fontWeight: '700',
                  textTransform: 'uppercase',
                }}
              >
                {severityLabel}
              </div>

              {/* Category name */}
              <h5
                style={{
                  fontSize: '16px',
                  fontWeight: '600',
                  color: 'var(--foreground)',
                  margin: '0 0 12px 0',
                  textTransform: 'capitalize',
                }}
              >
                {getCategoryName(category)}
              </h5>

              {/* Severity metrics */}
              <div
                style={{
                  display: 'grid',
                  gridTemplateColumns: '1fr 1fr',
                  gap: '12px',
                }}
              >
                <div style={{ textAlign: 'center' }}>
                  <div
                    style={{
                      fontSize: '12px',
                      color: 'var(--muted-foreground)',
                      marginBottom: '4px',
                      fontWeight: '500',
                    }}
                  >
                    Severity
                  </div>
                  <div
                    style={{
                      fontSize: '20px',
                      fontWeight: '700',
                      color: severityColor,
                    }}
                  >
                    {(breakdown.avg_severity * 100).toFixed(0)}%
                  </div>
                </div>

                <div style={{ textAlign: 'center' }}>
                  <div
                    style={{
                      fontSize: '12px',
                      color: 'var(--muted-foreground)',
                      marginBottom: '4px',
                      fontWeight: '500',
                    }}
                  >
                    Matches
                  </div>
                  <div
                    style={{
                      fontSize: '20px',
                      fontWeight: '700',
                      color: 'var(--foreground)',
                    }}
                  >
                    {breakdown.match_count}
                  </div>
                </div>
              </div>

              {/* Final score */}
              <div
                style={{
                  marginTop: '12px',
                  textAlign: 'center',
                  padding: '8px',
                  backgroundColor: 'var(--background)',
                  borderRadius: '6px',
                  border: '1px solid var(--border)',
                }}
              >
                <div
                  style={{
                    fontSize: '12px',
                    color: 'var(--muted-foreground)',
                    marginBottom: '4px',
                    fontWeight: '500',
                  }}
                >
                  Final Score
                </div>
                <div
                  style={{
                    fontSize: '18px',
                    fontWeight: '700',
                    color: severityColor,
                  }}
                >
                  {breakdown.final_score.toFixed(3)}
                </div>
              </div>

              {/* Severity progress bar */}
              <div
                style={{
                  marginTop: '12px',
                }}
              >
                <div
                  style={{
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'center',
                    marginBottom: '6px',
                  }}
                >
                  <span
                    style={{
                      fontSize: '11px',
                      color: 'var(--muted-foreground)',
                      fontWeight: '500',
                    }}
                  >
                    Risk Level
                  </span>
                  <span
                    style={{
                      fontSize: '11px',
                      color: severityColor,
                      fontWeight: '600',
                    }}
                  >
                    {severityLabel}
                  </span>
                </div>
                <div
                  style={{
                    width: '100%',
                    height: '8px',
                    backgroundColor: 'var(--border)',
                    borderRadius: '4px',
                    overflow: 'hidden',
                  }}
                >
                  <div
                    style={{
                      width: `${breakdown.avg_severity * 100}%`,
                      height: '100%',
                      backgroundColor: severityColor,
                      borderRadius: '4px',
                      transition: 'width 0.8s ease-out',
                    }}
                  />
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* Additional information */}
      <div
        style={{
          marginTop: '20px',
          padding: '16px',
          backgroundColor: 'var(--muted)',
          borderRadius: '8px',
          border: '1px solid var(--border)',
          textAlign: 'center',
        }}
      >
        <div
          style={{
            fontSize: '14px',
            color: 'var(--muted-foreground)',
            fontWeight: '500',
          }}
        >
          🔍 This analysis uses ultra-sensitive thresholds to detect even low
          levels of toxicity
        </div>
        <div
          style={{
            fontSize: '12px',
            color: 'var(--muted-foreground)',
            marginTop: '8px',
            opacity: 0.8,
          }}
        >
          Each word has a severity weight that influences the global result
        </div>
      </div>
    </div>
  );
};

export default SeverityBreakdown;
