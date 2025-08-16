import React, { Component } from 'react';
import type { ErrorInfo, ReactNode } from 'react';
import { designSystem } from '../styles/common';
import Button from './Button';

interface Props {
  children: ReactNode;
  fallback?: ReactNode;
  onError?: (error: Error, errorInfo: ErrorInfo) => void;
  showDetails?: boolean;
  resetOnPropsChange?: boolean;
}

interface State {
  hasError: boolean;
  error?: Error;
  errorInfo?: ErrorInfo;
}

class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error('ErrorBoundary caught an error:', error, errorInfo);

    this.setState({ error, errorInfo });

    if (this.props.onError) {
      this.props.onError(error, errorInfo);
    }
  }

  componentDidUpdate(prevProps: Props) {
    if (
      this.props.resetOnPropsChange &&
      prevProps.children !== this.props.children
    ) {
      this.setState({
        hasError: false,
        error: undefined,
        errorInfo: undefined,
      });
    }
  }

  handleReset = () => {
    this.setState({ hasError: false, error: undefined, errorInfo: undefined });
  };

  handleReload = () => {
    window.location.reload();
  };

  render() {
    if (this.state.hasError) {
      if (this.props.fallback) {
        return this.props.fallback;
      }

      return (
        <div
          style={{
            minHeight: '100vh',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            padding: designSystem.spacing[6],
            backgroundColor: designSystem.colors.neutral[50],
          }}
        >
          <div
            style={{
              maxWidth: '500px',
              width: '100%',
              textAlign: 'center',
              backgroundColor: 'white',
              borderRadius: designSystem.borderRadius.xl,
              padding: designSystem.spacing[8],
              boxShadow: designSystem.shadows.lg,
              border: `1px solid ${designSystem.colors.neutral[200]}`,
            }}
          >
            {/* Error Icon */}
            <div
              style={{
                fontSize: '64px',
                marginBottom: designSystem.spacing[6],
                animation: 'shake 0.5s ease-in-out',
              }}
            >
              ⚠️
            </div>

            {/* Error Title */}
            <h1
              style={{
                ...designSystem.typography.styles.h2,
                color: designSystem.colors.error,
                marginBottom: designSystem.spacing[4],
              }}
            >
              Something went wrong
            </h1>

            {/* Error Description */}
            <p
              style={{
                ...designSystem.typography.styles.body,
                color: designSystem.colors.neutral[600],
                marginBottom: designSystem.spacing[6],
                lineHeight: designSystem.typography.lineHeight.relaxed,
              }}
            >
              We encountered an unexpected error. This helps us improve the
              application.
            </p>

            {/* Action Buttons */}
            <div
              style={{
                display: 'flex',
                gap: designSystem.spacing[3],
                justifyContent: 'center',
                flexWrap: 'wrap' as const,
              }}
            >
              <Button
                onClick={this.handleReset}
                variant='primary'
                size='md'
                ariaLabel='Try again'
              >
                🔄 Try Again
              </Button>

              <Button
                onClick={this.handleReload}
                variant='outline'
                size='md'
                ariaLabel='Reload page'
              >
                🔃 Reload Page
              </Button>
            </div>

            {/* Error Details (Development Only) */}
            {this.props.showDetails && this.state.error && (
              <details
                style={{
                  marginTop: designSystem.spacing[6],
                  textAlign: 'left' as const,
                }}
              >
                <summary
                  style={{
                    cursor: 'pointer',
                    fontSize: designSystem.typography.fontSize.sm,
                    fontWeight: designSystem.typography.fontWeight.medium,
                    color: designSystem.colors.neutral[600],
                    padding: designSystem.spacing[2],
                    backgroundColor: designSystem.colors.neutral[100],
                    borderRadius: designSystem.borderRadius.md,
                    border: `1px solid ${designSystem.colors.neutral[200]}`,
                    userSelect: 'none' as const,
                  }}
                >
                  🔍 Error Details (Development)
                </summary>

                <div
                  style={{
                    marginTop: designSystem.spacing[3],
                    padding: designSystem.spacing[3],
                    backgroundColor: designSystem.colors.neutral[50],
                    borderRadius: designSystem.borderRadius.md,
                    border: `1px solid ${designSystem.colors.neutral[200]}`,
                    fontSize: designSystem.typography.fontSize.sm,
                    fontFamily: designSystem.typography.fontFamily.mono,
                    overflow: 'auto',
                    maxHeight: '300px',
                  }}
                >
                  {/* Error Message */}
                  <div
                    style={{
                      marginBottom: designSystem.spacing[3],
                      padding: designSystem.spacing[2],
                      backgroundColor: designSystem.colors.error + '10',
                      borderRadius: designSystem.borderRadius.sm,
                      border: `1px solid ${designSystem.colors.error + '20'}`,
                    }}
                  >
                    <strong style={{ color: designSystem.colors.error }}>
                      Error:
                    </strong>
                    <div style={{ marginTop: designSystem.spacing[1] }}>
                      {this.state.error.message}
                    </div>
                  </div>

                  {/* Error Stack */}
                  {this.state.error.stack && (
                    <div
                      style={{
                        marginBottom: designSystem.spacing[3],
                      }}
                    >
                      <strong
                        style={{ color: designSystem.colors.neutral[700] }}
                      >
                        Stack Trace:
                      </strong>
                      <pre
                        style={{
                          marginTop: designSystem.spacing[1],
                          whiteSpace: 'pre-wrap' as const,
                          wordBreak: 'break-word' as const,
                          color: designSystem.colors.neutral[600],
                          fontSize: designSystem.typography.fontSize.xs,
                        }}
                      >
                        {this.state.error.stack}
                      </pre>
                    </div>
                  )}

                  {/* Component Stack */}
                  {this.state.errorInfo?.componentStack && (
                    <div>
                      <strong
                        style={{ color: designSystem.colors.neutral[700] }}
                      >
                        Component Stack:
                      </strong>
                      <pre
                        style={{
                          marginTop: designSystem.spacing[1],
                          whiteSpace: 'pre-wrap' as const,
                          wordBreak: 'break-word' as const,
                          color: designSystem.colors.neutral[600],
                          fontSize: designSystem.typography.fontSize.xs,
                        }}
                      >
                        {this.state.errorInfo.componentStack}
                      </pre>
                    </div>
                  )}
                </div>
              </details>
            )}

            {/* Help Text */}
            <div
              style={{
                marginTop: designSystem.spacing[6],
                padding: designSystem.spacing[3],
                backgroundColor: designSystem.colors.primary[50],
                borderRadius: designSystem.borderRadius.md,
                border: `1px solid ${designSystem.colors.primary[100]}`,
              }}
            >
              <p
                style={{
                  fontSize: designSystem.typography.fontSize.sm,
                  color: designSystem.colors.primary[700],
                  margin: 0,
                }}
              >
                💡 <strong>Need help?</strong> If this problem persists, please
                contact support.
              </p>
            </div>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}

export default ErrorBoundary;
