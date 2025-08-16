import React, { forwardRef, useCallback } from 'react';
import { designSystem, componentStyles } from '../styles/common';

interface ButtonProps {
  onClick?: () => void;
  disabled?: boolean;
  variant?: 'primary' | 'secondary' | 'outline' | 'ghost' | 'destructive';
  size?: 'sm' | 'md' | 'lg';
  children: React.ReactNode;
  ariaLabel?: string;
  className?: string;
  type?: 'button' | 'submit' | 'reset';
  fullWidth?: boolean;
  loading?: boolean;
  icon?: React.ReactNode;
  iconPosition?: 'left' | 'right';
}

const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  (
    {
      onClick,
      disabled = false,
      variant = 'primary',
      size = 'md',
      children,
      ariaLabel,
      className = '',
      type = 'button',
      fullWidth = false,
      loading = false,
      icon,
      iconPosition = 'left',
      ...props
    },
    ref
  ) => {
    const handleClick = useCallback(
      (e: React.MouseEvent<HTMLButtonElement>) => {
        if (!disabled && !loading && onClick) {
          onClick();
        }
      },
      [onClick, disabled, loading]
    );

    const isDisabled = disabled || loading;

    // Base button styles
    const baseStyles = {
      ...componentStyles.button.base,
      ...componentStyles.button.sizes[size],
      ...componentStyles.button.variants[variant],
      width: fullWidth ? '100%' : 'auto',
      position: 'relative' as const,
      overflow: 'hidden',
    };

    // Loading spinner styles
    const loadingSpinnerStyles = {
      position: 'absolute' as const,
      top: '50%',
      left: '50%',
      transform: 'translate(-50%, -50%)',
      width: size === 'sm' ? '14px' : size === 'md' ? '16px' : '18px',
      height: size === 'sm' ? '14px' : size === 'md' ? '16px' : '18px',
      border: '2px solid transparent',
      borderTop: `2px solid currentColor`,
      borderRadius: '50%',
      animation: 'spin 1s linear infinite',
    };

    // Content wrapper for proper centering with icon
    const contentStyles = {
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      gap: designSystem.spacing[2],
      opacity: loading ? 0 : 1,
      transition: `opacity ${designSystem.transitions.duration.normal} ${designSystem.transitions.easing.out}`,
    };

    return (
      <button
        ref={ref}
        onClick={handleClick}
        disabled={isDisabled}
        aria-label={ariaLabel}
        type={type}
        className={className}
        style={baseStyles}
        {...props}
      >
        {/* Loading spinner */}
        {loading && <div style={loadingSpinnerStyles} />}

        {/* Button content */}
        <div style={contentStyles}>
          {/* Left icon */}
          {icon && iconPosition === 'left' && (
            <span style={{ display: 'flex', alignItems: 'center' }}>
              {icon}
            </span>
          )}

          {/* Button text */}
          <span>{children}</span>

          {/* Right icon */}
          {icon && iconPosition === 'right' && (
            <span style={{ display: 'flex', alignItems: 'center' }}>
              {icon}
            </span>
          )}
        </div>
      </button>
    );
  }
);

Button.displayName = 'Button';

export default Button;
