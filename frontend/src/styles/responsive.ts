// 📱 ToxiGuard Responsive Design System
// Consistent breakpoints, utilities, and responsive patterns

import { designSystem } from './common';

// Responsive breakpoints
export const breakpoints = {
  xs: '320px',
  sm: '640px',
  md: '768px',
  lg: '1024px',
  xl: '1280px',
  '2xl': '1536px',
} as const;

// Media query utilities
export const media = {
  xs: `@media (min-width: ${breakpoints.xs})`,
  sm: `@media (min-width: ${breakpoints.sm})`,
  md: `@media (min-width: ${breakpoints.md})`,
  lg: `@media (min-width: ${breakpoints.lg})`,
  xl: `@media (min-width: ${breakpoints.xl})`,
  '2xl': `@media (min-width: ${breakpoints['2xl']})`,

  // Max-width queries
  maxXs: `@media (max-width: ${breakpoints.xs})`,
  maxSm: `@media (max-width: ${breakpoints.sm})`,
  maxMd: `@media (max-width: ${breakpoints.md})`,
  maxLg: `@media (max-width: ${breakpoints.lg})`,
  maxXl: `@media (max-width: ${breakpoints.xl})`,

  // Range queries
  smOnly: `@media (min-width: ${breakpoints.sm}) and (max-width: ${breakpoints.md})`,
  mdOnly: `@media (min-width: ${breakpoints.md}) and (max-width: ${breakpoints.lg})`,
  lgOnly: `@media (min-width: ${breakpoints.lg}) and (max-width: ${breakpoints.xl})`,

  // Orientation
  portrait: '@media (orientation: portrait)',
  landscape: '@media (orientation: landscape)',

  // Device types
  mobile: `@media (max-width: ${breakpoints.md})`,
  tablet: `@media (min-width: ${breakpoints.md}) and (max-width: ${breakpoints.lg})`,
  desktop: `@media (min-width: ${breakpoints.lg})`,

  // Touch devices
  touch: '@media (hover: none) and (pointer: coarse)',
  noTouch: '@media (hover: hover) and (pointer: fine)',

  // Reduced motion
  reducedMotion: '@media (prefers-reduced-motion: reduce)',

  // Dark mode
  darkMode: '@media (prefers-color-scheme: dark)',
  lightMode: '@media (prefers-color-scheme: light)',

  // High contrast
  highContrast: '@media (prefers-contrast: high)',

  // Print
  print: '@media print',
} as const;

// Responsive spacing utilities
export const responsiveSpacing = {
  // Container padding
  container: {
    xs: designSystem.spacing[3],
    sm: designSystem.spacing[4],
    md: designSystem.spacing[6],
    lg: designSystem.spacing[8],
    xl: designSystem.spacing[10],
  },

  // Section margins
  section: {
    xs: designSystem.spacing[6],
    sm: designSystem.spacing[8],
    md: designSystem.spacing[12],
    lg: designSystem.spacing[16],
    xl: designSystem.spacing[20],
  },

  // Grid gaps
  grid: {
    xs: designSystem.spacing[3],
    sm: designSystem.spacing[4],
    md: designSystem.spacing[6],
    lg: designSystem.spacing[8],
    xl: designSystem.spacing[10],
  },
} as const;

// Responsive typography
export const responsiveTypography = {
  h1: {
    xs: { fontSize: '1.5rem', lineHeight: '1.3' },
    sm: { fontSize: '1.875rem', lineHeight: '1.2' },
    md: { fontSize: '2.25rem', lineHeight: '1.2' },
    lg: { fontSize: '2.5rem', lineHeight: '1.1' },
    xl: { fontSize: '3rem', lineHeight: '1.1' },
  },
  h2: {
    xs: { fontSize: '1.25rem', lineHeight: '1.4' },
    sm: { fontSize: '1.5rem', lineHeight: '1.3' },
    md: { fontSize: '1.875rem', lineHeight: '1.3' },
    lg: { fontSize: '2rem', lineHeight: '1.2' },
    xl: { fontSize: '2.25rem', lineHeight: '1.2' },
  },
  h3: {
    xs: { fontSize: '1.125rem', lineHeight: '1.4' },
    sm: { fontSize: '1.25rem', lineHeight: '1.4' },
    md: { fontSize: '1.5rem', lineHeight: '1.4' },
    lg: { fontSize: '1.625rem', lineHeight: '1.3' },
    xl: { fontSize: '1.75rem', lineHeight: '1.3' },
  },
  body: {
    xs: { fontSize: '0.875rem', lineHeight: '1.5' },
    sm: { fontSize: '0.875rem', lineHeight: '1.6' },
    md: { fontSize: '1rem', lineHeight: '1.6' },
    lg: { fontSize: '1.125rem', lineHeight: '1.6' },
    xl: { fontSize: '1.125rem', lineHeight: '1.6' },
  },
} as const;

// Responsive layout patterns
export const responsiveLayouts = {
  // Grid columns
  grid: {
    xs: { columns: 1, gap: responsiveSpacing.grid.xs },
    sm: { columns: 2, gap: responsiveSpacing.grid.sm },
    md: { columns: 3, gap: responsiveSpacing.grid.md },
    lg: { columns: 4, gap: responsiveSpacing.grid.lg },
    xl: { columns: 5, gap: responsiveSpacing.grid.xl },
  },

  // Sidebar layouts
  sidebar: {
    xs: { sidebar: 'none', main: 'full' },
    sm: { sidebar: 'none', main: 'full' },
    md: { sidebar: '250px', main: 'calc(100% - 250px)' },
    lg: { sidebar: '280px', main: 'calc(100% - 280px)' },
    xl: { sidebar: '320px', main: 'calc(100% - 320px)' },
  },

  // Container max-widths
  container: {
    xs: '100%',
    sm: '640px',
    md: '768px',
    lg: '1024px',
    xl: '1280px',
    '2xl': '1536px',
  },
} as const;

// Utility functions for responsive design
export const responsiveUtils = {
  // Get responsive value based on breakpoint
  getValue: <T>(
    values: Partial<Record<keyof typeof breakpoints, T>>,
    defaultValue: T
  ): T => {
    // This would be implemented with a hook in actual usage
    return defaultValue;
  },

  // Create responsive object
  create: <T>(values: Partial<Record<keyof typeof breakpoints, T>>) => values,

  // Responsive array (mobile-first)
  array: <T>(values: T[]) => values,

  // Responsive object (mobile-first)
  object: <T>(values: Partial<Record<keyof typeof breakpoints, T>>) => values,
} as const;

// CSS-in-JS responsive helpers
export const responsiveCSS = {
  // Responsive padding
  padding: (
    values: Partial<Record<keyof typeof breakpoints, string | number>>
  ) => ({
    padding:
      values.xs ||
      values.sm ||
      values.md ||
      values.lg ||
      values.xl ||
      values['2xl'],
    [media.sm]: values.sm && { padding: values.sm },
    [media.md]: values.md && { padding: values.md },
    [media.lg]: values.lg && { padding: values.lg },
    [media.xl]: values.xl && { padding: values.xl },
    [media['2xl']]: values['2xl'] && { padding: values['2xl'] },
  }),

  // Responsive margin
  margin: (
    values: Partial<Record<keyof typeof breakpoints, string | number>>
  ) => ({
    margin:
      values.xs ||
      values.sm ||
      values.md ||
      values.lg ||
      values.xl ||
      values['2xl'],
    [media.sm]: values.sm && { margin: values.sm },
    [media.md]: values.md && { margin: values.md },
    [media.lg]: values.lg && { margin: values.lg },
    [media.xl]: values.xl && { margin: values.xl },
    [media['2xl']]: values['2xl'] && { margin: values['2xl'] },
  }),

  // Responsive fontSize
  fontSize: (
    values: Partial<Record<keyof typeof breakpoints, string | number>>
  ) => ({
    fontSize:
      values.xs ||
      values.sm ||
      values.md ||
      values.lg ||
      values.xl ||
      values['2xl'],
    [media.sm]: values.sm && { fontSize: values.sm },
    [media.md]: values.md && { fontSize: values.md },
    [media.lg]: values.lg && { fontSize: values.lg },
    [media.xl]: values.xl && { fontSize: values.xl },
    [media['2xl']]: values['2xl'] && { fontSize: values['2xl'] },
  }),

  // Responsive display
  display: (values: Partial<Record<keyof typeof breakpoints, string>>) => ({
    display:
      values.xs ||
      values.sm ||
      values.md ||
      values.lg ||
      values.xl ||
      values['2xl'],
    [media.sm]: values.sm && { display: values.sm },
    [media.md]: values.md && { display: values.md },
    [media.lg]: values.lg && { display: values.lg },
    [media.xl]: values.xl && { display: values.xl },
    [media['2xl']]: values['2xl'] && { display: values['2xl'] },
  }),
} as const;

// Common responsive patterns
export const responsivePatterns = {
  // Hide on specific breakpoints
  hide: {
    xs: { [media.xs]: { display: 'none' } },
    sm: { [media.sm]: { display: 'none' } },
    md: { [media.md]: { display: 'none' } },
    lg: { [media.lg]: { display: 'none' } },
    xl: { [media.xl]: { display: 'none' } },
    '2xl': { [media['2xl']]: { display: 'none' } },
  },

  // Show on specific breakpoints
  show: {
    xs: { display: 'none', [media.xs]: { display: 'block' } },
    sm: { display: 'none', [media.sm]: { display: 'block' } },
    md: { display: 'none', [media.md]: { display: 'block' } },
    lg: { display: 'none', [media.lg]: { display: 'block' } },
    xl: { display: 'none', [media.xl]: { display: 'block' } },
    '2xl': { display: 'none', [media['2xl']]: { display: 'block' } },
  },

  // Responsive text alignment
  textAlign: {
    left: { textAlign: 'left' as const },
    center: { textAlign: 'center' as const },
    right: { textAlign: 'right' as const },
    justify: { textAlign: 'justify' as const },
  },

  // Responsive flexbox
  flex: {
    row: { display: 'flex', flexDirection: 'row' as const },
    column: { display: 'flex', flexDirection: 'column' as const },
    wrap: { flexWrap: 'wrap' as const },
    nowrap: { flexWrap: 'nowrap' as const },
    center: { alignItems: 'center', justifyContent: 'center' },
    start: { alignItems: 'flex-start', justifyContent: 'flex-start' },
    end: { alignItems: 'flex-end', justifyContent: 'flex-end' },
    between: { justifyContent: 'space-between' },
    around: { justifyContent: 'space-around' },
    evenly: { justifyContent: 'space-evenly' },
  },
} as const;

// Export everything
export default {
  breakpoints,
  media,
  responsiveSpacing,
  responsiveTypography,
  responsiveLayouts,
  responsiveUtils,
  responsiveCSS,
  responsivePatterns,
};
