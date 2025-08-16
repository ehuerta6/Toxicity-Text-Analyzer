// 🎨 ToxiGuard Design System - Comprehensive UI/UX Standards
// Consistent typography, spacing, colors, and responsive design

export const designSystem = {
  // Typography Scale - Consistent across all components
  typography: {
    fontFamily: {
      primary:
        "'DM Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif",
      mono: "'JetBrains Mono', 'Fira Code', Consolas, monospace",
    },

    fontSize: {
      xs: '0.75rem', // 12px
      sm: '0.875rem', // 14px
      base: '1rem', // 16px
      lg: '1.125rem', // 18px
      xl: '1.25rem', // 20px
      '2xl': '1.5rem', // 24px
      '3xl': '1.875rem', // 30px
      '4xl': '2.25rem', // 36px
    },

    fontWeight: {
      normal: '400',
      medium: '500',
      semibold: '600',
      bold: '700',
    },

    lineHeight: {
      tight: '1.25',
      normal: '1.5',
      relaxed: '1.75',
    },

    // Predefined text styles for consistency
    styles: {
      h1: {
        fontSize: '2.25rem', // 36px
        fontWeight: '700',
        lineHeight: '1.2',
        letterSpacing: '-0.025em',
      },
      h2: {
        fontSize: '1.875rem', // 30px
        fontWeight: '600',
        lineHeight: '1.3',
        letterSpacing: '-0.025em',
      },
      h3: {
        fontSize: '1.5rem', // 24px
        fontWeight: '600',
        lineHeight: '1.4',
      },
      h4: {
        fontSize: '1.25rem', // 20px
        fontWeight: '600',
        lineHeight: '1.4',
      },
      body: {
        fontSize: '1rem', // 16px
        fontWeight: '400',
        lineHeight: '1.6',
      },
      bodyLarge: {
        fontSize: '1.125rem', // 18px
        fontWeight: '400',
        lineHeight: '1.6',
      },
      bodySmall: {
        fontSize: '0.875rem', // 14px
        fontWeight: '400',
        lineHeight: '1.5',
      },
      caption: {
        fontSize: '0.75rem', // 12px
        fontWeight: '500',
        lineHeight: '1.4',
        textTransform: 'uppercase',
        letterSpacing: '0.05em',
      },
    },
  },

  // Spacing Scale - Consistent spacing throughout the app
  spacing: {
    px: '1px',
    0: '0',
    0.5: '0.125rem', // 2px
    1: '0.25rem', // 4px
    1.5: '0.375rem', // 6px
    2: '0.5rem', // 8px
    2.5: '0.625rem', // 10px
    3: '0.75rem', // 12px
    3.5: '0.875rem', // 14px
    4: '1rem', // 16px
    5: '1.25rem', // 20px
    6: '1.5rem', // 24px
    7: '1.75rem', // 28px
    8: '2rem', // 32px
    9: '2.25rem', // 36px
    10: '2.5rem', // 40px
    11: '2.75rem', // 44px
    12: '3rem', // 48px
    14: '3.5rem', // 56px
    16: '4rem', // 64px
    20: '5rem', // 80px
    24: '6rem', // 96px
    28: '7rem', // 112px
    32: '8rem', // 128px
  },

  // Color Palette - Consistent colors across all components
  colors: {
    // Primary colors
    primary: {
      50: 'oklch(0.98 0.015 197.137)',
      100: 'oklch(0.95 0.03 197.137)',
      200: 'oklch(0.9 0.06 197.137)',
      300: 'oklch(0.8 0.12 197.137)',
      400: 'oklch(0.7 0.15 197.137)',
      500: 'oklch(0.548 0.15 197.137)', // Main primary
      600: 'oklch(0.45 0.15 197.137)',
      700: 'oklch(0.35 0.15 197.137)',
      800: 'oklch(0.25 0.15 197.137)',
      900: 'oklch(0.15 0.15 197.137)',
    },

    // Secondary colors
    secondary: {
      50: 'oklch(0.98 0.022 162.015)',
      100: 'oklch(0.95 0.044 162.015)',
      200: 'oklch(0.9 0.088 162.015)',
      300: 'oklch(0.8 0.133 162.015)',
      400: 'oklch(0.7 0.177 162.015)',
      500: 'oklch(0.646 0.222 162.015)', // Main secondary
      600: 'oklch(0.55 0.222 162.015)',
      700: 'oklch(0.45 0.222 162.015)',
      800: 'oklch(0.35 0.222 162.015)',
      900: 'oklch(0.25 0.222 162.015)',
    },

    // Neutral colors
    neutral: {
      50: 'oklch(0.98 0 0)',
      100: 'oklch(0.96 0 0)',
      200: 'oklch(0.92 0 0)',
      300: 'oklch(0.88 0 0)',
      400: 'oklch(0.8 0 0)',
      500: 'oklch(0.7 0 0)',
      600: 'oklch(0.6 0 0)',
      700: 'oklch(0.5 0 0)',
      800: 'oklch(0.4 0 0)',
      900: 'oklch(0.3 0 0)',
    },

    // Semantic colors
    success: 'oklch(0.646 0.222 162.015)', // Green
    warning: 'oklch(0.769 0.188 70.08)', // Amber
    error: 'oklch(0.577 0.245 27.325)', // Red
    info: 'oklch(0.548 0.15 197.137)', // Blue

    // Toxicity-specific colors
    toxicity: {
      safe: 'oklch(0.646 0.222 162.015)', // Green
      moderate: 'oklch(0.769 0.188 70.08)', // Amber
      high: 'oklch(0.577 0.245 27.325)', // Red
      critical: 'oklch(0.4 0.3 27.325)', // Dark red
    },
  },

  // Border Radius - Consistent rounded corners
  borderRadius: {
    none: '0',
    sm: '0.125rem', // 2px
    base: '0.25rem', // 4px
    md: '0.375rem', // 6px
    lg: '0.5rem', // 8px
    xl: '0.75rem', // 12px
    '2xl': '1rem', // 16px
    '3xl': '1.5rem', // 24px
    full: '9999px',
  },

  // Shadows - Consistent depth and elevation
  shadows: {
    sm: '0 1px 2px 0 rgb(0 0 0 / 0.05)',
    base: '0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1)',
    md: '0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1)',
    lg: '0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1)',
    xl: '0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1)',
    '2xl': '0 25px 50px -12px rgb(0 0 0 / 0.25)',
    inner: 'inset 0 2px 4px 0 rgb(0 0 0 / 0.05)',
    none: '0 0 #0000',
  },

  // Transitions - Consistent animation timing
  transitions: {
    duration: {
      fast: '150ms',
      normal: '200ms',
      slow: '300ms',
      slower: '500ms',
    },
    easing: {
      linear: 'linear',
      in: 'cubic-bezier(0.4, 0, 1, 1)',
      out: 'cubic-bezier(0, 0, 0.2, 1)',
      inOut: 'cubic-bezier(0.4, 0, 0.2, 1)',
    },
  },

  // Breakpoints - Responsive design system
  breakpoints: {
    xs: '320px',
    sm: '640px',
    md: '768px',
    lg: '1024px',
    xl: '1280px',
    '2xl': '1536px',
  },

  // Z-index scale - Consistent layering
  zIndex: {
    hide: -1,
    auto: 'auto',
    base: 0,
    docked: 10,
    dropdown: 1000,
    sticky: 1100,
    banner: 1200,
    overlay: 1300,
    modal: 1400,
    popover: 1500,
    skipLink: 1600,
    toast: 1700,
    tooltip: 1800,
  },
};

// 🎯 Component-specific style presets
export const componentStyles = {
  // Button variants with consistent styling
  button: {
    base: {
      display: 'inline-flex',
      alignItems: 'center',
      justifyContent: 'center',
      gap: designSystem.spacing[2],
      fontWeight: designSystem.typography.fontWeight.semibold,
      borderRadius: designSystem.borderRadius.lg,
      transition: `all ${designSystem.transitions.duration.normal} ${designSystem.transitions.easing.out}`,
      cursor: 'pointer',
      border: 'none',
      outline: 'none',
      '&:focus-visible': {
        outline: `2px solid ${designSystem.colors.primary[500]}`,
        outlineOffset: '2px',
      },
      '&:disabled': {
        opacity: 0.6,
        cursor: 'not-allowed',
        pointerEvents: 'none',
      },
    },

    sizes: {
      sm: {
        padding: `${designSystem.spacing[2]} ${designSystem.spacing[3]}`,
        fontSize: designSystem.typography.fontSize.sm,
        minHeight: '32px',
      },
      md: {
        padding: `${designSystem.spacing[3]} ${designSystem.spacing[4]}`,
        fontSize: designSystem.typography.fontSize.base,
        minHeight: '40px',
      },
      lg: {
        padding: `${designSystem.spacing[4]} ${designSystem.spacing[6]}`,
        fontSize: designSystem.typography.fontSize.lg,
        minHeight: '48px',
      },
    },

    variants: {
      primary: {
        backgroundColor: designSystem.colors.primary[500],
        color: 'white',
        '&:hover': {
          backgroundColor: designSystem.colors.primary[600],
          transform: 'translateY(-1px)',
          boxShadow: designSystem.shadows.md,
        },
        '&:active': {
          transform: 'translateY(0)',
        },
      },
      secondary: {
        backgroundColor: designSystem.colors.neutral[100],
        color: designSystem.colors.neutral[700],
        border: `1px solid ${designSystem.colors.neutral[300]}`,
        '&:hover': {
          backgroundColor: designSystem.colors.neutral[200],
          borderColor: designSystem.colors.neutral[400],
        },
      },
      outline: {
        backgroundColor: 'transparent',
        color: designSystem.colors.primary[500],
        border: `1px solid ${designSystem.colors.primary[500]}`,
        '&:hover': {
          backgroundColor: designSystem.colors.primary[50],
        },
      },
      ghost: {
        backgroundColor: 'transparent',
        color: designSystem.colors.neutral[700],
        '&:hover': {
          backgroundColor: designSystem.colors.neutral[100],
        },
      },
      destructive: {
        backgroundColor: designSystem.colors.error,
        color: 'white',
        '&:hover': {
          backgroundColor: 'oklch(0.5 0.25 27.325)',
        },
      },
    },
  },

  // Input field styles
  input: {
    base: {
      width: '100%',
      padding: `${designSystem.spacing[3]} ${designSystem.spacing[4]}`,
      fontSize: designSystem.typography.fontSize.base,
      lineHeight: designSystem.typography.lineHeight.normal,
      color: designSystem.colors.neutral[900],
      backgroundColor: 'white',
      border: `1px solid ${designSystem.colors.neutral[300]}`,
      borderRadius: designSystem.borderRadius.lg,
      transition: `all ${designSystem.transitions.duration.normal} ${designSystem.transitions.easing.out}`,
      '&:focus': {
        outline: 'none',
        borderColor: designSystem.colors.primary[500],
        boxShadow: `0 0 0 3px ${designSystem.colors.primary[100]}`,
      },
      '&:disabled': {
        backgroundColor: designSystem.colors.neutral[50],
        color: designSystem.colors.neutral[500],
        cursor: 'not-allowed',
      },
      '&::placeholder': {
        color: designSystem.colors.neutral[400],
      },
    },
  },

  // Card styles
  card: {
    base: {
      backgroundColor: 'white',
      borderRadius: designSystem.borderRadius.xl,
      border: `1px solid ${designSystem.colors.neutral[200]}`,
      boxShadow: designSystem.shadows.sm,
      transition: `all ${designSystem.transitions.duration.normal} ${designSystem.transitions.easing.out}`,
    },
    hover: {
      transform: 'translateY(-2px)',
      boxShadow: designSystem.shadows.lg,
      borderColor: designSystem.colors.neutral[300],
    },
  },
};

// 🎨 Utility functions for consistent styling
export const getToxicityColor = (percentage: number): string => {
  if (percentage <= 30) return designSystem.colors.toxicity.safe;
  if (percentage <= 60) return designSystem.colors.toxicity.moderate;
  if (percentage <= 80) return designSystem.colors.toxicity.high;
  return designSystem.colors.toxicity.critical;
};

export const getToxicityLabel = (percentage: number): string => {
  if (percentage <= 30) return 'Safe';
  if (percentage <= 60) return 'Moderate';
  if (percentage <= 80) return 'High Risk';
  return 'Critical';
};

export const getToxicityBackgroundColor = (percentage: number): string => {
  if (percentage <= 30) return `${designSystem.colors.toxicity.safe}15`;
  if (percentage <= 60) return `${designSystem.colors.toxicity.moderate}15`;
  if (percentage <= 80) return `${designSystem.colors.toxicity.high}15`;
  return `${designSystem.colors.toxicity.critical}15`;
};

// 📱 Responsive utility functions
export const responsive = {
  xs: `@media (min-width: ${designSystem.breakpoints.xs})`,
  sm: `@media (min-width: ${designSystem.breakpoints.sm})`,
  md: `@media (min-width: ${designSystem.breakpoints.md})`,
  lg: `@media (min-width: ${designSystem.breakpoints.lg})`,
  xl: `@media (min-width: ${designSystem.breakpoints.xl})`,
  '2xl': `@media (min-width: ${designSystem.breakpoints['2xl']})`,
};

// 🔧 Common style combinations
export const commonStyles = {
  container: {
    maxWidth: '1400px',
    margin: '0 auto',
    padding: `${designSystem.spacing[4]} ${designSystem.spacing[4]}`,
    [responsive.md]: {
      padding: `${designSystem.spacing[6]} ${designSystem.spacing[6]}`,
    },
    [responsive.lg]: {
      padding: `${designSystem.spacing[8]} ${designSystem.spacing[8]}`,
    },
  },

  section: {
    marginBottom: designSystem.spacing[12],
    [responsive.md]: {
      marginBottom: designSystem.spacing[16],
    },
  },

  grid: {
    display: 'grid',
    gap: designSystem.spacing[6],
    [responsive.md]: {
      gap: designSystem.spacing[8],
    },
  },

  flexCenter: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
  },

  textCenter: {
    textAlign: 'center',
  },

  fullWidth: {
    width: '100%',
  },

  fullHeight: {
    height: '100%',
  },
};

// Legacy exports for backward compatibility
export { designSystem as DESIGN_SYSTEM };
export { componentStyles as COMPONENT_STYLES };
export { commonStyles as COMMON_STYLES };
