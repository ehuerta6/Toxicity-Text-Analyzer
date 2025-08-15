// Estilos comunes para la aplicación ToxiGuard - Diseño V0

export const commonStyles = {
  // Contenedores principales
  container: {
    maxWidth: '1400px',
    margin: '0 auto',
    padding: '32px 24px',
  },

  // Tarjetas
  card: {
    backgroundColor: 'var(--card)',
    borderRadius: 'var(--radius)',
    boxShadow: '0 4px 6px rgba(0, 0, 0, 0.05)',
    border: '1px solid var(--border)',
    padding: '32px',
    transition: 'all 0.2s ease-in-out',
  },

  // Botones
  button: {
    primary: {
      backgroundColor: 'var(--primary)',
      color: 'var(--primary-foreground)',
      border: 'none',
      borderRadius: 'var(--radius)',
      padding: '12px 24px',
      fontSize: '16px',
      fontWeight: '600',
      cursor: 'pointer',
      transition: 'all 0.2s ease-in-out',
      ':hover': {
        backgroundColor: 'oklch(0.548 0.15 197.137 / 0.9)',
        transform: 'translateY(-1px)',
        boxShadow: '0 4px 12px rgba(8, 145, 178, 0.4)',
      },
    },
    secondary: {
      backgroundColor: 'var(--muted)',
      color: 'var(--muted-foreground)',
      border: '1px solid var(--border)',
      borderRadius: 'var(--radius)',
      padding: '12px 24px',
      fontSize: '16px',
      fontWeight: '600',
      cursor: 'pointer',
      transition: 'all 0.2s ease-in-out',
      ':hover': {
        backgroundColor: 'var(--border)',
        transform: 'translateY(-1px)',
        boxShadow: '0 4px 12px rgba(0, 0, 0, 0.1)',
      },
    },
    danger: {
      backgroundColor: 'var(--destructive)',
      color: 'var(--destructive-foreground)',
      border: 'none',
      borderRadius: 'var(--radius)',
      padding: '8px 16px',
      fontSize: '14px',
      fontWeight: '500',
      cursor: 'pointer',
      transition: 'all 0.2s ease-in-out',
      ':hover': {
        backgroundColor: 'oklch(0.577 0.245 27.325 / 0.9)',
        transform: 'translateY(-1px)',
        boxShadow: '0 4px 12px rgba(227, 52, 47, 0.4)',
      },
    },
  },

  // Inputs
  input: {
    width: '100%',
    padding: '12px 16px',
    border: '2px solid var(--border)',
    borderRadius: 'var(--radius)',
    fontSize: '16px',
    transition: 'all 0.2s ease-in-out',
    ':focus': {
      outline: 'none',
      borderColor: 'var(--ring)',
      boxShadow: '0 0 0 3px var(--ring)',
    },
  },

  // Texto
  text: {
    heading: {
      fontSize: '28px',
      fontWeight: '700',
      color: 'var(--foreground)',
      marginBottom: '16px',
    },
    subheading: {
      fontSize: '20px',
      fontWeight: '600',
      color: 'var(--foreground)',
      marginBottom: '12px',
    },
    body: {
      fontSize: '16px',
      color: 'var(--foreground)',
      lineHeight: '1.6',
    },
    small: {
      fontSize: '14px',
      color: 'var(--muted-foreground)',
    },
  },

  // Colores de toxicidad
  toxicity: {
    safe: 'var(--secondary)',
    warning: 'oklch(0.769 0.188 70.08)', // Amber
    toxic: 'var(--destructive)',
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
  if (percentage <= 30) return 'var(--secondary)'; // Verde/Emerald
  if (percentage <= 60) return 'oklch(0.769 0.188 70.08)'; // Amarillo/Amber
  return 'var(--destructive)'; // Rojo
};

export const getToxicityLabel = (percentage: number): string => {
  if (percentage <= 30) return 'Safe';
  if (percentage <= 60) return 'Moderate';
  return 'High Risk';
};

// Función para obtener color de fondo basado en toxicidad
export const getToxicityBackgroundColor = (percentage: number): string => {
  if (percentage <= 30) return 'var(--secondary)';
  if (percentage <= 60) return 'oklch(0.769 0.188 70.08)';
  return 'var(--destructive)';
};

// Función para obtener color de borde basado en toxicidad
export const getToxicityBorderColor = (percentage: number): string => {
  if (percentage <= 30) return 'var(--secondary)';
  if (percentage <= 60) return 'oklch(0.769 0.188 70.08)';
  return 'var(--destructive)';
};
