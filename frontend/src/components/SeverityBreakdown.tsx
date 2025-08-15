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
    if (severity >= 0.9) return 'var(--destructive)'; // Rojo para severidad crítica
    if (severity >= 0.7) return 'oklch(0.6 0.2 30)'; // Naranja para severidad alta
    if (severity >= 0.5) return 'oklch(0.7 0.2 60)'; // Amarillo para severidad moderada
    return 'oklch(0.8 0.15 120)'; // Verde para severidad baja
  };

  const getSeverityLabel = (severity: number): string => {
    if (severity >= 0.9) return 'CRÍTICO';
    if (severity >= 0.7) return 'ALTO';
    if (severity >= 0.5) return 'MODERADO';
    return 'BAJO';
  };

  const getCategoryName = (category: string): string => {
    const categoryNames: Record<string, string> = {
      insulto_leve: 'Insulto Leve',
      insulto_moderado: 'Insulto Moderado',
      insulto_severo: 'Insulto Severo',
      acoso_directo: 'Acoso Directo',
      discriminacion: 'Discriminación',
      amenazas: 'Amenazas',
      spam_toxico: 'Spam Tóxico',
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
        🚨 Análisis de Severidad Ultra-Sensible
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
              {/* Badge de severidad */}
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

              {/* Nombre de la categoría */}
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

              {/* Métricas de severidad */}
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
                    Severidad
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
                    Coincidencias
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

              {/* Score final */}
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
                  Score Final
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

              {/* Barra de progreso de severidad */}
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
                    Nivel de Riesgo
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

      {/* Información adicional */}
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
          🔍 Este análisis utiliza umbrales ultra-sensibles para detectar
          incluso niveles bajos de toxicidad
        </div>
        <div
          style={{
            fontSize: '12px',
            color: 'var(--muted-foreground)',
            marginTop: '8px',
            opacity: 0.8,
          }}
        >
          Cada palabra tiene un peso de severidad que influye en el resultado
          global
        </div>
      </div>
    </div>
  );
};

export default SeverityBreakdown;
