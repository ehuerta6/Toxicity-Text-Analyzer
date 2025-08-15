// Estilos comunes para la aplicación ToxiGuard

export const commonStyles = {
  // Contenedores principales
  container: {
    maxWidth: '1200px',
    margin: '0 auto',
    padding: '20px',
  },
  
  // Tarjetas
  card: {
    backgroundColor: 'white',
    borderRadius: '12px',
    boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)',
    border: '1px solid #e5e7eb',
    padding: '24px',
  },
  
  // Botones
  button: {
    primary: {
      backgroundColor: '#3b82f6',
      color: 'white',
      border: 'none',
      borderRadius: '8px',
      padding: '12px 24px',
      fontSize: '16px',
      fontWeight: '600',
      cursor: 'pointer',
      transition: 'background-color 0.2s',
    },
    secondary: {
      backgroundColor: '#6b7280',
      color: 'white',
      border: 'none',
      borderRadius: '8px',
      padding: '12px 24px',
      fontSize: '16px',
      fontWeight: '600',
      cursor: 'pointer',
      transition: 'background-color 0.2s',
    },
    danger: {
      backgroundColor: '#ef4444',
      color: 'white',
      border: 'none',
      borderRadius: '8px',
      padding: '8px 16px',
      fontSize: '14px',
      fontWeight: '500',
      cursor: 'pointer',
      transition: 'background-color 0.2s',
    },
  },
  
  // Inputs
  input: {
    width: '100%',
    padding: '12px 16px',
    border: '2px solid #e5e7eb',
    borderRadius: '8px',
    fontSize: '16px',
    transition: 'border-color 0.2s',
  },
  
  // Texto
  text: {
    heading: {
      fontSize: '28px',
      fontWeight: '700',
      color: '#1f2937',
      marginBottom: '16px',
    },
    subheading: {
      fontSize: '20px',
      fontWeight: '600',
      color: '#374151',
      marginBottom: '12px',
    },
    body: {
      fontSize: '16px',
      color: '#4b5563',
      lineHeight: '1.6',
    },
    small: {
      fontSize: '14px',
      color: '#6b7280',
    },
  },
  
  // Colores de toxicidad
  toxicity: {
    safe: '#10b981',
    warning: '#f59e0b',
    toxic: '#ef4444',
  },
  
  // Espaciado
  spacing: {
    xs: '4px',
    sm: '8px',
    md: '16px',
    lg: '24px',
    xl: '32px',
  },
  
  // Bordes
  borders: {
    radius: {
      sm: '4px',
      md: '8px',
      lg: '12px',
      xl: '16px',
    },
  },
  
  // Sombras
  shadows: {
    sm: '0 1px 2px rgba(0, 0, 0, 0.05)',
    md: '0 4px 6px rgba(0, 0, 0, 0.1)',
    lg: '0 10px 15px rgba(0, 0, 0, 0.1)',
  },
  
  // Transiciones
  transitions: {
    fast: '0.15s ease-in-out',
    normal: '0.2s ease-in-out',
    slow: '0.3s ease-in-out',
  },
};

// Funciones de utilidad para estilos
export const getToxicityColor = (percentage: number): string => {
  if (percentage < 30) return commonStyles.toxicity.safe;
  if (percentage < 70) return commonStyles.toxicity.warning;
  return commonStyles.toxicity.toxic;
};

export const getToxicityLabel = (percentage: number): string => {
  if (percentage < 30) return 'Seguro';
  if (percentage < 70) return 'Advertencia';
  return 'Tóxico';
};
