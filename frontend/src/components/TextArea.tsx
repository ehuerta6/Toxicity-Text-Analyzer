import React, { forwardRef, useCallback, useMemo } from 'react';
import { designSystem, componentStyles } from '../styles/common';

interface TextAreaProps {
  value: string;
  onChange: (value: string) => void;
  onKeyDown?: (e: React.KeyboardEvent<HTMLTextAreaElement>) => void;
  placeholder?: string;
  minHeight?: number;
  maxHeight?: number;
  showCharCount?: boolean;
  maxLength?: number;
  disabled?: boolean;
  className?: string;
  label?: string;
  error?: string;
  required?: boolean;
  autoResize?: boolean;
  rows?: number;
}

const TextArea = forwardRef<HTMLTextAreaElement, TextAreaProps>(
  (
    {
      value,
      onChange,
      onKeyDown,
      placeholder = 'Enter text...',
      minHeight = 120,
      maxHeight = 400,
      showCharCount = true,
      maxLength,
      disabled = false,
      className = '',
      label,
      error,
      required = false,
      autoResize = true,
      rows = 4,
      ...props
    },
    ref
  ) => {
    const handleChange = useCallback(
      (e: React.ChangeEvent<HTMLTextAreaElement>) => {
        onChange(e.target.value);
      },
      [onChange]
    );

    const handleKeyDown = useCallback(
      (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
        if (onKeyDown) {
          onKeyDown(e);
        }
      },
      [onKeyDown]
    );

    // Character count calculations
    const charCount = useMemo(() => value.length, [value]);
    const isNearLimit = useMemo(
      () => maxLength && charCount > maxLength * 0.8,
      [maxLength, charCount]
    );
    const isOverLimit = useMemo(
      () => maxLength && charCount > maxLength,
      [maxLength, charCount]
    );

    // TextArea styles
    const textAreaStyles = useMemo(
      () => ({
        ...componentStyles.input.base,
        minHeight: `${minHeight}px`,
        maxHeight: `${maxHeight}px`,
        resize: autoResize ? ('none' as const) : ('vertical' as const),
        fontFamily: designSystem.typography.fontFamily.primary,
        lineHeight: designSystem.typography.lineHeight.relaxed,
        ...(error && {
          borderColor: designSystem.colors.error,
          '&:focus': {
            borderColor: designSystem.colors.error,
            boxShadow: `0 0 0 3px ${designSystem.colors.error}20`,
          },
        }),
      }),
      [minHeight, maxHeight, autoResize, error]
    );

    // Character count styles
    const charCountStyles = useMemo(
      () => ({
        fontSize: designSystem.typography.fontSize.sm,
        fontWeight: designSystem.typography.fontWeight.medium,
        color: isOverLimit
          ? designSystem.colors.error
          : isNearLimit
          ? designSystem.colors.warning
          : designSystem.colors.neutral[500],
        transition: `color ${designSystem.transitions.duration.normal} ${designSystem.transitions.easing.out}`,
      }),
      [isOverLimit, isNearLimit]
    );

    // Progress bar styles
    const progressBarStyles = useMemo(
      () => ({
        width: '100%',
        height: '4px',
        backgroundColor: designSystem.colors.neutral[200],
        borderRadius: designSystem.borderRadius.full,
        overflow: 'hidden',
        marginTop: designSystem.spacing[2],
      }),
      []
    );

    const progressFillStyles = useMemo(
      () => ({
        height: '100%',
        backgroundColor: isOverLimit
          ? designSystem.colors.error
          : isNearLimit
          ? designSystem.colors.warning
          : designSystem.colors.primary[500],
        borderRadius: designSystem.borderRadius.full,
        transition: `all ${designSystem.transitions.duration.normal} ${designSystem.transitions.easing.out}`,
        width: maxLength
          ? `${Math.min((charCount / maxLength) * 100, 100)}%`
          : '0%',
      }),
      [charCount, maxLength, isOverLimit, isNearLimit]
    );

    // Label styles
    const labelStyles = useMemo(
      () => ({
        display: 'block',
        fontSize: designSystem.typography.fontSize.sm,
        fontWeight: designSystem.typography.fontWeight.medium,
        color: designSystem.colors.neutral[700],
        marginBottom: designSystem.spacing[2],
        ...(required && {
          '&::after': {
            content: '" *"',
            color: designSystem.colors.error,
          },
        }),
      }),
      [required]
    );

    // Error message styles
    const errorStyles = useMemo(
      () => ({
        fontSize: designSystem.typography.fontSize.sm,
        color: designSystem.colors.error,
        marginTop: designSystem.spacing[2],
        display: 'flex',
        alignItems: 'center',
        gap: designSystem.spacing[1],
      }),
      []
    );

    return (
      <div className={className} style={{ width: '100%' }}>
        {/* Label */}
        {label && <label style={labelStyles}>{label}</label>}

        {/* TextArea */}
        <div style={{ position: 'relative' }}>
          <textarea
            ref={ref}
            value={value}
            onChange={handleChange}
            onKeyDown={handleKeyDown}
            placeholder={placeholder}
            maxLength={maxLength}
            disabled={disabled}
            rows={rows}
            style={textAreaStyles}
            {...props}
          />

          {/* Error indicator */}
          {error && (
            <div
              style={{
                position: 'absolute',
                top: designSystem.spacing[3],
                right: designSystem.spacing[3],
                width: '8px',
                height: '8px',
                backgroundColor: designSystem.colors.error,
                borderRadius: '50%',
              }}
            />
          )}
        </div>

        {/* Character count and progress bar */}
        {showCharCount && (maxLength || value.length > 0) && (
          <div
            style={{
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center',
              marginTop: designSystem.spacing[3],
            }}
          >
            {/* Character count */}
            <span style={charCountStyles}>
              {charCount}
              {maxLength && ` / ${maxLength}`}
            </span>

            {/* Progress bar */}
            {maxLength && (
              <div style={progressBarStyles}>
                <div style={progressFillStyles} />
              </div>
            )}
          </div>
        )}

        {/* Error message */}
        {error && (
          <div style={errorStyles}>
            <span style={{ fontSize: '14px' }}>⚠️</span>
            {error}
          </div>
        )}
      </div>
    );
  }
);

TextArea.displayName = 'TextArea';

export default TextArea;
