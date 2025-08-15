import React from 'react';

interface FooterProps {
  showAboutLink?: boolean;
}

const Footer: React.FC<FooterProps> = ({ showAboutLink = true }) => {
  const currentYear = new Date().getFullYear();

  return (
    <footer
      style={{
        backgroundColor: 'var(--card)',
        borderTop: '1px solid var(--border)',
        marginTop: 'auto',
        padding: '24px 0',
        boxShadow: '0 -2px 4px rgba(0, 0, 0, 0.05)',
      }}
    >
      <div
        style={{
          maxWidth: '1400px',
          margin: '0 auto',
          padding: '0 20px',
        }}
      >
        {/* Main Footer Content */}
        <div
          style={{
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            flexWrap: 'wrap',
            gap: '20px',
            marginBottom: '20px',
          }}
        >
          {/* Left Section - Brand & Copyright */}
          <div
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '12px',
            }}
          >
            <div
              style={{
                fontSize: '20px',
                animation: 'pulse 2s infinite',
              }}
            >
              🛡️
            </div>
            <div>
              <div
                style={{
                  fontSize: '16px',
                  fontWeight: '600',
                  color: 'var(--foreground)',
                  marginBottom: '2px',
                }}
              >
                ToxiGuard
              </div>
              <div
                style={{
                  fontSize: '12px',
                  color: 'var(--muted-foreground)',
                }}
              >
                Made by Emi
              </div>
            </div>
          </div>

          {/* Center Section - Quick Links */}
          <div
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '24px',
              flexWrap: 'wrap',
            }}
          >
            {showAboutLink && (
              <a
                href='/about'
                style={{
                  fontSize: '14px',
                  color: 'var(--muted-foreground)',
                  textDecoration: 'none',
                  fontWeight: '500',
                  transition: 'all 0.2s ease',
                  padding: '8px 12px',
                  borderRadius: '6px',
                }}
                onMouseEnter={(e) => {
                  e.currentTarget.style.color = 'var(--foreground)';
                  e.currentTarget.style.backgroundColor = 'var(--muted)';
                }}
                onMouseLeave={(e) => {
                  e.currentTarget.style.color = 'var(--muted-foreground)';
                  e.currentTarget.style.backgroundColor = 'transparent';
                }}
              >
                About
              </a>
            )}

            <a
              href='#'
              style={{
                fontSize: '14px',
                color: 'var(--muted-foreground)',
                textDecoration: 'none',
                fontWeight: '500',
                transition: 'all 0.2s ease',
                padding: '8px 12px',
                borderRadius: '6px',
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.color = 'var(--foreground)';
                e.currentTarget.style.backgroundColor = 'var(--muted)';
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.color = 'var(--muted-foreground)';
                e.currentTarget.style.backgroundColor = 'transparent';
              }}
            >
              Privacy Policy
            </a>

            <a
              href='#'
              style={{
                fontSize: '14px',
                color: 'var(--muted-foreground)',
                textDecoration: 'none',
                fontWeight: '500',
                transition: 'all 0.2s ease',
                padding: '8px 12px',
                borderRadius: '6px',
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.color = 'var(--foreground)';
                e.currentTarget.style.backgroundColor = 'var(--muted)';
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.color = 'var(--muted-foreground)';
                e.currentTarget.style.backgroundColor = 'transparent';
              }}
            >
              Terms of Service
            </a>
          </div>

          {/* Right Section - Year */}
          <div
            style={{
              fontSize: '14px',
              color: 'var(--muted-foreground)',
              fontWeight: '500',
            }}
          >
            © {currentYear}
          </div>
        </div>

        {/* Bottom Section - Additional Info */}
        <div
          style={{
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            flexWrap: 'wrap',
            gap: '16px',
            paddingTop: '16px',
            borderTop: '1px solid var(--border)',
            fontSize: '12px',
            color: 'var(--muted-foreground)',
          }}
        >
          <div>All rights reserved • Professional content moderation tools</div>

          <div
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '8px',
            }}
          >
            <span>Powered by</span>
            <span
              style={{
                color: 'var(--primary)',
                fontWeight: '600',
              }}
            >
              Advanced ML
            </span>
          </div>
        </div>
      </div>

      {/* CSS styles for animations */}
      <style>
        {`
          @keyframes pulse {
            0%, 100% {
              opacity: 1;
            }
            50% {
              opacity: 0.7;
            }
          }
          
          @media (max-width: 768px) {
            .footer-content {
              flex-direction: column;
              text-align: center;
              gap: 16px;
            }
            
            .footer-links {
              justify-content: center;
            }
            
            .footer-bottom {
              flex-direction: column;
              text-align: center;
              gap: 12px;
            }
          }
        `}
      </style>
    </footer>
  );
};

export default Footer;
