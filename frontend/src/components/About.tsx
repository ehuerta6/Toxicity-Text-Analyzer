import React from 'react';

const About: React.FC = () => {
  return (
    <div
      style={{
        minHeight: '100vh',
        backgroundColor: 'var(--background)',
        fontFamily:
          'DM Sans, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
      }}
    >
      {/* Header */}
      <header
        style={{
          backgroundColor: 'var(--card)',
          borderBottom: '1px solid var(--border)',
          padding: '20px 0',
          boxShadow: '0 2px 4px rgba(0, 0, 0, 0.05)',
        }}
      >
        <div
          style={{
            maxWidth: '1400px',
            margin: '0 auto',
            padding: '0 20px',
          }}
        >
          <div style={{ textAlign: 'center' }}>
            <div
              style={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                gap: '12px',
                marginBottom: '8px',
              }}
            >
              <div style={{ fontSize: '24px' }}>ℹ️</div>
              <h1
                style={{
                  fontSize: '28px',
                  fontWeight: '700',
                  color: 'var(--foreground)',
                  margin: 0,
                }}
              >
                About ToxiGuard
              </h1>
            </div>
            <p
              style={{
                fontSize: '16px',
                color: 'var(--muted-foreground)',
                maxWidth: '600px',
                margin: '0 auto',
                lineHeight: '1.5',
              }}
            >
              Professional content moderation powered by advanced machine
              learning
            </p>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <div
        style={{
          maxWidth: '800px',
          margin: '0 auto',
          padding: '60px 20px',
          textAlign: 'center',
        }}
      >
        <div
          style={{
            backgroundColor: 'var(--card)',
            borderRadius: '12px',
            padding: '40px',
            boxShadow: '0 4px 12px rgba(0, 0, 0, 0.1)',
            border: '1px solid var(--border)',
          }}
        >
          <div
            style={{
              fontSize: '64px',
              marginBottom: '24px',
              animation: 'fadeInUp 0.8s ease-out',
            }}
          >
            🚧
          </div>

          <h2
            style={{
              fontSize: '24px',
              fontWeight: '600',
              color: 'var(--foreground)',
              margin: '0 0 16px 0',
              animation: 'fadeInUp 0.8s ease-out 0.1s both',
            }}
          >
            Under Construction
          </h2>

          <p
            style={{
              fontSize: '16px',
              color: 'var(--muted-foreground)',
              lineHeight: '1.6',
              margin: '0 0 32px 0',
              animation: 'fadeInUp 0.8s ease-out 0.2s both',
            }}
          >
            This page is currently being developed. Soon you'll find detailed
            information about ToxiGuard, our mission, the technology behind our
            content moderation system, and more.
          </p>

          <div
            style={{
              display: 'flex',
              justifyContent: 'center',
              gap: '16px',
              flexWrap: 'wrap',
              animation: 'fadeInUp 0.8s ease-out 0.3s both',
            }}
          >
            <button
              onClick={() => window.history.back()}
              style={{
                backgroundColor: 'var(--primary)',
                color: 'var(--primary-foreground)',
                border: 'none',
                borderRadius: '8px',
                padding: '12px 24px',
                fontSize: '16px',
                fontWeight: '600',
                cursor: 'pointer',
                transition: 'all 0.2s ease',
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.backgroundColor =
                  'oklch(0.548 0.15 197.137 / 0.9)';
                e.currentTarget.style.transform = 'translateY(-1px)';
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.backgroundColor = 'var(--primary)';
                e.currentTarget.style.transform = 'translateY(0)';
              }}
            >
              ← Go Back
            </button>

            <button
              onClick={() => (window.location.href = '/')}
              style={{
                backgroundColor: 'var(--muted)',
                color: 'var(--muted-foreground)',
                border: '1px solid var(--border)',
                borderRadius: '8px',
                padding: '12px 24px',
                fontSize: '16px',
                fontWeight: '600',
                cursor: 'pointer',
                transition: 'all 0.2s ease',
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.backgroundColor = 'var(--border)';
                e.currentTarget.style.transform = 'translateY(-1px)';
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.backgroundColor = 'var(--muted)';
                e.currentTarget.style.transform = 'translateY(0)';
              }}
            >
              🏠 Home
            </button>
          </div>
        </div>
      </div>

      {/* CSS styles for animations */}
      <style>
        {`
          @keyframes fadeInUp {
            from {
              opacity: 0;
              transform: translateY(20px);
            }
            to {
              opacity: 1;
              transform: translateY(0);
            }
          }
        `}
      </style>
    </div>
  );
};

export default About;
