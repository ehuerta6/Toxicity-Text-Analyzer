import React, { forwardRef, useMemo } from 'react';
import { designSystem } from '../styles/common';

interface BadgeProps {
  children: React.ReactNode;
  variant?:
    | 'default'
    | 'primary'
    | 'secondary'
    | 'success'
    | 'warning'
    | 'error'
    | 'info';
  size?: 'sm' | 'md' | 'lg';
  className?: string;
  icon?: React.ReactNode;
  iconPosition?: 'left' | 'right';
  removable?: boolean;
  onRemove?: () => void;
  fullWidth?: boolean;
  rounded?: boolean;
}

const Badge = forwardRef<HTMLDivElement, BadgeProps>(
  (
    {
      children,
      variant = 'default',
      size = 'md',
      className = '',
      icon,
      iconPosition = 'left',
      removable = false,
      onRemove,
      fullWidth = false,
      rounded = false,
      ...props
    },
    ref
  ) => {
    // Size configurations
    const sizeConfig = useMemo(() => {
      switch (size) {
        case 'sm':
          return {
            padding: `${designSystem.spacing[1]} ${designSystem.spacing[2]}`,
            fontSize: designSystem.typography.fontSize.xs,
            borderRadius: rounded
              ? designSystem.borderRadius.full
              : designSystem.borderRadius.sm,
            iconSize: '12px',
          };
        case 'md':
          return {
            padding: `${designSystem.spacing[2]} ${designSystem.spacing[3]}`,
            fontSize: designSystem.typography.fontSize.sm,
            borderRadius: rounded
              ? designSystem.borderRadius.full
              : designSystem.borderRadius.md,
            iconSize: '14px',
          };
        case 'lg':
          return {
            padding: `${designSystem.spacing[3]} ${designSystem.spacing[4]}`,
            fontSize: designSystem.typography.fontSize.base,
            borderRadius: rounded
              ? designSystem.borderRadius.full
              : designSystem.borderRadius.lg,
            iconSize: '16px',
          };
        default:
          return {
            padding: `${designSystem.spacing[2]} ${designSystem.spacing[3]}`,
            fontSize: designSystem.typography.fontSize.sm,
            borderRadius: rounded
              ? designSystem.borderRadius.full
              : designSystem.borderRadius.md,
            iconSize: '14px',
          };
      }
    }, [size, rounded]);

    // Variant configurations
    const variantConfig = useMemo(() => {
      switch (variant) {
        case 'primary':
          return {
            backgroundColor: designSystem.colors.primary[100],
            color: designSystem.colors.primary[700],
            border: `1px solid ${designSystem.colors.primary[200]}`,
          };
        case 'secondary':
          return {
            backgroundColor: designSystem.colors.secondary[100],
            color: designSystem.colors.secondary[700],
            border: `1px solid ${designSystem.colors.secondary[200]}`,
          };
        case 'success':
          return {
            backgroundColor: designSystem.colors.success + '20',
            color: designSystem.colors.success,
            border: `1px solid ${designSystem.colors.success + '40'}`,
          };
        case 'warning':
          return {
            backgroundColor: designSystem.colors.warning + '20',
            color: designSystem.colors.warning,
            border: `1px solid ${designSystem.colors.warning + '40'}`,
          };
        case 'error':
          return {
            backgroundColor: designSystem.colors.error + '20',
            color: designSystem.colors.error,
            border: `1px solid ${designSystem.colors.error + '40'}`,
          };
        case 'info':
          return {
            backgroundColor: designSystem.colors.primary[100],
            color: designSystem.colors.primary[700],
            border: `1px solid ${designSystem.colors.primary[200]}`,
          };
        default:
          return {
            backgroundColor: designSystem.colors.neutral[100],
            color: designSystem.colors.neutral[700],
            border: `1px solid ${designSystem.colors.neutral[200]}`,
          };
      }
    }, [variant]);

    // Base badge styles
    const badgeStyles = useMemo(
      () => ({
        display: 'inline-flex',
        alignItems: 'center',
        justifyContent: 'center',
        gap: designSystem.spacing[1],
        padding: sizeConfig.padding,
        fontSize: sizeConfig.fontSize,
        fontWeight: designSystem.typography.fontWeight.medium,
        borderRadius: sizeConfig.borderRadius,
        border: variantConfig.border,
        backgroundColor: variantConfig.backgroundColor,
        color: variantConfig.color,
        width: fullWidth ? '100%' : 'auto',
        transition: `all ${designSystem.transitions.duration.normal} ${designSystem.transitions.easing.out}`,
        cursor: 'default',
        userSelect: 'none' as const,
        whiteSpace: 'nowrap' as const,
        overflow: 'hidden',
        textOverflow: 'ellipsis',
      }),
      [sizeConfig, variantConfig, fullWidth]
    );

    // Icon styles
    const iconStyles = useMemo(
      () => ({
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        fontSize: sizeConfig.iconSize,
        flexShrink: 0,
      }),
      [sizeConfig.iconSize]
    );

    // Remove button styles
    const removeButtonStyles = useMemo(
      () => ({
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        width: sizeConfig.iconSize,
        height: sizeConfig.iconSize,
        borderRadius: '50%',
        border: 'none',
        backgroundColor: 'transparent',
        color: 'inherit',
        cursor: 'pointer',
        padding: 0,
        marginLeft: designSystem.spacing[1],
        transition: `all ${designSystem.transitions.duration.fast} ${designSystem.transitions.easing.out}`,
        '&:hover': {
          backgroundColor: 'rgba(0, 0, 0, 0.1)',
        },
        '&:focus-visible': {
          outline: `2px solid ${designSystem.colors.primary[500]}`,
          outlineOffset: '2px',
        },
      }),
      [sizeConfig.iconSize]
    );

    const handleRemove = (e: React.MouseEvent) => {
      e.stopPropagation();
      if (onRemove) {
        onRemove();
      }
    };

    return (
      <div ref={ref} className={className} style={badgeStyles} {...props}>
        {/* Left icon */}
        {icon && iconPosition === 'left' && (
          <span style={iconStyles}>{icon}</span>
        )}

        {/* Badge content */}
        <span style={{ overflow: 'hidden', textOverflow: 'ellipsis' }}>
          {children}
        </span>

        {/* Right icon */}
        {icon && iconPosition === 'right' && (
          <span style={iconStyles}>{icon}</span>
        )}

        {/* Remove button */}
        {removable && (
          <button
            type='button'
            onClick={handleRemove}
            style={removeButtonStyles}
            aria-label='Remove badge'
          >
            <span style={{ fontSize: sizeConfig.iconSize }}>×</span>
          </button>
        )}
      </div>
    );
  }
);

Badge.displayName = 'Badge';

export default Badge;
