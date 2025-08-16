import React, { forwardRef, useMemo } from 'react';
import { designSystem, componentStyles } from '../styles/common';

interface CardProps {
  children: React.ReactNode;
  className?: string;
  variant?: 'default' | 'elevated' | 'outlined' | 'filled';
  padding?: 'none' | 'sm' | 'md' | 'lg' | 'xl';
  hover?: boolean;
  onClick?: () => void;
  disabled?: boolean;
  fullWidth?: boolean;
  header?: React.ReactNode;
  footer?: React.ReactNode;
  divider?: boolean;
}

const Card = forwardRef<HTMLDivElement, CardProps>(
  (
    {
      children,
      className = '',
      variant = 'default',
      padding = 'md',
      hover = false,
      onClick,
      disabled = false,
      fullWidth = false,
      header,
      footer,
      divider = false,
      ...props
    },
    ref
  ) => {
    // Padding configurations
    const paddingConfig = useMemo(() => {
      switch (padding) {
        case 'none':
          return 0;
        case 'sm':
          return designSystem.spacing[3];
        case 'md':
          return designSystem.spacing[4];
        case 'lg':
          return designSystem.spacing[6];
        case 'xl':
          return designSystem.spacing[8];
        default:
          return designSystem.spacing[4];
      }
    }, [padding]);

    // Variant styles
    const variantStyles = useMemo(() => {
      switch (variant) {
        case 'elevated':
          return {
            backgroundColor: 'white',
            border: 'none',
            boxShadow: designSystem.shadows.md,
            ...(hover && {
              '&:hover': {
                boxShadow: designSystem.shadows.lg,
                transform: 'translateY(-2px)',
              },
            }),
          };
        case 'outlined':
          return {
            backgroundColor: 'white',
            border: `1px solid ${designSystem.colors.neutral[300]}`,
            boxShadow: 'none',
            ...(hover && {
              '&:hover': {
                borderColor: designSystem.colors.neutral[400],
                boxShadow: designSystem.shadows.sm,
              },
            }),
          };
        case 'filled':
          return {
            backgroundColor: designSystem.colors.neutral[50],
            border: `1px solid ${designSystem.colors.neutral[200]}`,
            boxShadow: 'none',
            ...(hover && {
              '&:hover': {
                backgroundColor: designSystem.colors.neutral[100],
                borderColor: designSystem.colors.neutral[300],
              },
            }),
          };
        default:
          return {
            backgroundColor: 'white',
            border: `1px solid ${designSystem.colors.neutral[200]}`,
            boxShadow: designSystem.shadows.sm,
            ...(hover && {
              '&:hover': {
                boxShadow: designSystem.shadows.md,
                transform: 'translateY(-1px)',
              },
            }),
          };
      }
    }, [variant, hover]);

    // Base card styles
    const cardStyles = useMemo(
      () => ({
        ...componentStyles.card.base,
        ...variantStyles,
        width: fullWidth ? '100%' : 'auto',
        cursor: onClick && !disabled ? 'pointer' : 'default',
        transition: `all ${designSystem.transitions.duration.normal} ${designSystem.transitions.easing.out}`,
        ...(disabled && {
          opacity: 0.6,
          cursor: 'not-allowed',
          pointerEvents: 'none',
        }),
      }),
      [variantStyles, fullWidth, onClick, disabled]
    );

    // Header styles
    const headerStyles = useMemo(
      () => ({
        padding: `${designSystem.spacing[4]} ${paddingConfig}px`,
        paddingBottom: divider
          ? designSystem.spacing[3]
          : designSystem.spacing[4],
        borderBottom: divider
          ? `1px solid ${designSystem.colors.neutral[200]}`
          : 'none',
        backgroundColor: designSystem.colors.neutral[50],
        borderTopLeftRadius: designSystem.borderRadius.xl,
        borderTopRightRadius: designSystem.borderRadius.xl,
      }),
      [paddingConfig, divider]
    );

    // Content styles
    const contentStyles = useMemo(
      () => ({
        padding: `${paddingConfig}px`,
        ...(header && { paddingTop: designSystem.spacing[4] }),
        ...(footer && { paddingBottom: designSystem.spacing[4] }),
      }),
      [paddingConfig, header, footer]
    );

    // Footer styles
    const footerStyles = useMemo(
      () => ({
        padding: `${designSystem.spacing[4]} ${paddingConfig}px`,
        paddingTop: divider ? designSystem.spacing[3] : designSystem.spacing[4],
        borderTop: divider
          ? `1px solid ${designSystem.colors.neutral[200]}`
          : 'none',
        backgroundColor: designSystem.colors.neutral[50],
        borderBottomLeftRadius: designSystem.borderRadius.xl,
        borderBottomRightRadius: designSystem.borderRadius.xl,
      }),
      [paddingConfig, divider]
    );

    const handleClick = () => {
      if (onClick && !disabled) {
        onClick();
      }
    };

    return (
      <div
        ref={ref}
        className={className}
        style={cardStyles}
        onClick={handleClick}
        {...props}
      >
        {/* Header */}
        {header && <div style={headerStyles}>{header}</div>}

        {/* Content */}
        <div style={contentStyles}>{children}</div>

        {/* Footer */}
        {footer && <div style={footerStyles}>{footer}</div>}
      </div>
    );
  }
);

Card.displayName = 'Card';

export default Card;
