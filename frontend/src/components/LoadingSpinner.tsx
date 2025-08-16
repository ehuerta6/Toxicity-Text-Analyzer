import React, { useMemo } from 'react';
import { designSystem } from '../styles/common';

interface LoadingSpinnerProps {
  size?: 'xs' | 'sm' | 'md' | 'lg' | 'xl';
  variant?:
    | 'default'
    | 'primary'
    | 'secondary'
    | 'success'
    | 'warning'
    | 'error';
  text?: string;
  className?: string;
  fullScreen?: boolean;
  overlay?: boolean;
}

const LoadingSpinner: React.FC<LoadingSpinnerProps> = ({
  size = 'md',
  variant = 'default',
  text,
  className = '',
  fullScreen = false,
  overlay = false,
}) => {
  // Size configurations
  const sizeConfig = useMemo(() => {
    switch (size) {
      case 'xs':
        return { spinner: 16, border: 2, text: 12 };
      case 'sm':
        return { spinner: 20, border: 2, text: 14 };
      case 'md':
        return { spinner: 32, border: 3, text: 16 };
      case 'lg':
        return { spinner: 48, border: 4, text: 18 };
      case 'xl':
        return { spinner: 64, border: 5, text: 20 };
      default:
        return { spinner: 32, border: 3, text: 16 };
    }
  }, [size]);

  // Color configurations
  const colorConfig = useMemo(() => {
    switch (variant) {
      case 'primary':
        return designSystem.colors.primary[500];
      case 'secondary':
        return designSystem.colors.secondary[500];
      case 'success':
        return designSystem.colors.success;
      case 'warning':
        return designSystem.colors.warning;
      case 'error':
        return designSystem.colors.error;
      default:
        return designSystem.colors.neutral[400];
    }
  }, [variant]);

  // Spinner styles
  const spinnerStyles = useMemo(
    () => ({
      width: `${sizeConfig.spinner}px`,
      height: `${sizeConfig.spinner}px`,
      border: `${sizeConfig.border}px solid ${designSystem.colors.neutral[200]}`,
      borderTop: `${sizeConfig.border}px solid ${colorConfig}`,
      borderRadius: '50%',
      animation: 'spin 1s linear infinite',
    }),
    [sizeConfig, colorConfig]
  );

  // Text styles
  const textStyles = useMemo(
    () => ({
      fontSize: `${sizeConfig.text}px`,
      fontWeight: designSystem.typography.fontWeight.medium,
      color: designSystem.colors.neutral[600],
      marginTop: designSystem.spacing[3],
      textAlign: 'center' as const,
      lineHeight: designSystem.typography.lineHeight.normal,
    }),
    [sizeConfig]
  );

  // Container styles
  const containerStyles = useMemo(
    () => ({
      display: 'flex',
      flexDirection: 'column' as const,
      alignItems: 'center',
      justifyContent: 'center',
      gap: designSystem.spacing[2],
      padding: fullScreen ? designSystem.spacing[8] : designSystem.spacing[4],
      ...(fullScreen && {
        position: 'fixed' as const,
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        backgroundColor: 'rgba(255, 255, 255, 0.95)',
        backdropFilter: 'blur(4px)',
        zIndex: designSystem.zIndex.overlay,
      }),
      ...(overlay && {
        position: 'absolute' as const,
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        backgroundColor: 'rgba(255, 255, 255, 0.9)',
        zIndex: designSystem.zIndex.overlay,
      }),
    }),
    [fullScreen, overlay]
  );

  // Pulse dots styles
  const pulseDotsStyles = useMemo(
    () => ({
      display: 'flex',
      gap: designSystem.spacing[1],
      marginTop: designSystem.spacing[2],
    }),
    []
  );

  const pulseDotStyles = useMemo(
    () => ({
      width: '6px',
      height: '6px',
      backgroundColor: colorConfig,
      borderRadius: '50%',
      animation: 'pulse 1.5s ease-in-out infinite',
    }),
    [colorConfig]
  );

  // Progress bar styles (for larger sizes)
  const progressBarStyles = useMemo(
    () => ({
      width: `${sizeConfig.spinner * 2}px`,
      height: '4px',
      backgroundColor: designSystem.colors.neutral[200],
      borderRadius: designSystem.borderRadius.full,
      overflow: 'hidden',
      marginTop: designSystem.spacing[3],
    }),
    [sizeConfig]
  );

  const progressFillStyles = useMemo(
    () => ({
      height: '100%',
      backgroundColor: colorConfig,
      borderRadius: designSystem.borderRadius.full,
      animation: 'progress 2s ease-in-out infinite',
    }),
    [colorConfig]
  );

  // If fullScreen, render as full screen overlay
  if (fullScreen) {
    return (
      <div style={containerStyles} className={className}>
        <div style={spinnerStyles} />
        {text && <div style={textStyles}>{text}</div>}
        {size === 'lg' || size === 'xl' ? (
          <div style={pulseDotsStyles}>
            <div style={{ ...pulseDotStyles, animationDelay: '0ms' }} />
            <div style={{ ...pulseDotStyles, animationDelay: '150ms' }} />
            <div style={{ ...pulseDotStyles, animationDelay: '300ms' }} />
          </div>
        ) : null}
      </div>
    );
  }

  // If overlay, render as overlay
  if (overlay) {
    return (
      <div style={containerStyles} className={className}>
        <div style={spinnerStyles} />
        {text && <div style={textStyles}>{text}</div>}
      </div>
    );
  }

  // Default inline spinner
  return (
    <div style={containerStyles} className={className}>
      <div style={spinnerStyles} />
      {text && <div style={textStyles}>{text}</div>}
      {size === 'lg' || size === 'xl' ? (
        <div style={pulseDotsStyles}>
          <div style={{ ...pulseDotStyles, animationDelay: '0ms' }} />
          <div style={{ ...pulseDotStyles, animationDelay: '150ms' }} />
          <div style={{ ...pulseDotStyles, animationDelay: '300ms' }} />
        </div>
      ) : null}
    </div>
  );
};

export default LoadingSpinner;
