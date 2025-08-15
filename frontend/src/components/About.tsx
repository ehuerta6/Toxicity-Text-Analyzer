import React from 'react';

const About: React.FC = () => {
  const mlTechniques = [
    {
      title: 'Naive Bayes',
      description:
        'Probabilistic algorithm that analyzes the frequency of toxic words in text. Efficient and fast for basic content classification.',
      icon: '📊',
      color: 'var(--secondary)',
    },
    {
      title: 'Random Forest',
      description:
        'Ensemble of decision trees that improves accuracy by combining multiple classifiers. Robust against overfitting.',
      icon: '🌳',
      color: 'var(--primary)',
    },
    {
      title: 'Support Vector Machine',
      description:
        'Algorithm that finds the optimal hyperplane to separate toxic content from safe content. Excellent for binary classification.',
      icon: '⚡',
      color: 'oklch(0.769 0.188 70.08)',
    },
    {
      title: 'Gradient Boosting',
      description:
        'Technique that sequentially combines multiple weak models, gradually improving classification accuracy.',
      icon: '🚀',
      color: 'var(--destructive)',
    },
    {
      title: 'Contextual Analysis',
      description:
        'Advanced system that uses semantic embeddings to understand complete context, detecting negations and nuances.',
      icon: '🧠',
      color: 'oklch(0.6 0.2 30)',
    },
    {
      title: 'Hybrid Classifier',
      description:
        'Intelligent combination of multiple techniques that optimizes overall detection system accuracy.',
      icon: '🔗',
      color: 'oklch(0.8 0.15 120)',
    },
  ];

  const technologies = [
    {
      name: 'React 19',
      category: 'Frontend',
      description: 'Modern framework for user interfaces',
    },
    {
      name: 'TypeScript',
      category: 'Frontend',
      description: 'Typed language for robust development',
    },
    {
      name: 'Tailwind CSS',
      category: 'Frontend',
      description: 'Utility-first CSS framework',
    },
    {
      name: 'Vite',
      category: 'Frontend',
      description: 'Fast and modern build tool',
    },
    {
      name: 'FastAPI',
      category: 'Backend',
      description: 'Modern and fast web framework',
    },
    {
      name: 'Python 3.8+',
      category: 'Backend',
      description: 'Primary backend language',
    },
    {
      name: 'scikit-learn',
      category: 'ML',
      description: 'Machine learning library',
    },
    {
      name: 'sentence-transformers',
      category: 'ML',
      description: 'Semantic embedding models',
    },
    {
      name: 'spaCy',
      category: 'NLP',
      description: 'Natural language processing',
    },
    { name: 'PyTorch', category: 'ML', description: 'Deep learning framework' },
  ];

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
          padding: '24px 0',
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
              <div style={{ fontSize: '28px' }}>ℹ️</div>
              <h1
                style={{
                  fontSize: '32px',
                  fontWeight: '700',
                  color: 'var(--foreground)',
                  margin: 0,
                }}
              >
                About This Project
              </h1>
            </div>
            <p
              style={{
                fontSize: '18px',
                color: 'var(--muted-foreground)',
                maxWidth: '700px',
                margin: '0 auto',
                lineHeight: '1.6',
              }}
            >
              Professional content moderation powered by advanced machine
              learning algorithms
            </p>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <div
        style={{
          maxWidth: '1400px',
          margin: '0 auto',
          padding: '40px 20px',
        }}
      >
        {/* Main Project Card */}
        <div
          style={{
            backgroundColor: 'var(--card)',
            borderRadius: '16px',
            padding: '40px',
            boxShadow: '0 4px 20px rgba(0, 0, 0, 0.08)',
            border: '1px solid var(--border)',
            marginBottom: '40px',
            animation: 'fadeInUp 0.8s ease-out',
          }}
        >
          <h2
            style={{
              fontSize: '28px',
              fontWeight: '700',
              color: 'var(--foreground)',
              margin: '0 0 24px 0',
              textAlign: 'center',
            }}
          >
            🛡️ ToxiGuard: Content Moderation System
          </h2>

          <p
            style={{
              fontSize: '16px',
              color: 'var(--muted-foreground)',
              lineHeight: '1.7',
              textAlign: 'center',
              maxWidth: '800px',
              margin: '0 auto 32px auto',
            }}
          >
            ToxiGuard is an advanced content moderation system that uses
            multiple machine learning techniques to detect and classify toxic,
            offensive, or inappropriate text. The system analyzes the complete
            context of the text, including negations and semantic nuances, to
            provide accurate and contextual toxicity assessment.
          </p>

          {/* How It Works */}
          <div
            style={{
              backgroundColor: 'var(--muted)',
              borderRadius: '12px',
              padding: '24px',
              marginBottom: '32px',
              border: '1px solid var(--border)',
            }}
          >
            <h3
              style={{
                fontSize: '20px',
                fontWeight: '600',
                color: 'var(--foreground)',
                margin: '0 0 16px 0',
                textAlign: 'center',
              }}
            >
              🔄 How It Works
            </h3>
            <div
              style={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                gap: '16px',
                flexWrap: 'wrap',
                fontSize: '14px',
                color: 'var(--muted-foreground)',
              }}
            >
              <span>📝 User Input</span>
              <span>→</span>
              <span>🧠 ML Analysis</span>
              <span>→</span>
              <span>📊 Results Dashboard</span>
            </div>
          </div>

          {/* Technologies Grid */}
          <div
            style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))',
              gap: '16px',
              marginBottom: '24px',
            }}
          >
            {technologies.map((tech, index) => (
              <div
                key={index}
                style={{
                  backgroundColor: 'var(--background)',
                  borderRadius: '8px',
                  padding: '16px',
                  border: '1px solid var(--border)',
                  transition: 'all 0.2s ease',
                }}
                onMouseEnter={(e) => {
                  e.currentTarget.style.transform = 'translateY(-2px)';
                  e.currentTarget.style.boxShadow =
                    '0 4px 12px rgba(0, 0, 0, 0.1)';
                }}
                onMouseLeave={(e) => {
                  e.currentTarget.style.transform = 'translateY(0)';
                  e.currentTarget.style.boxShadow = 'none';
                }}
              >
                <div
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: '8px',
                    marginBottom: '8px',
                  }}
                >
                  <span
                    style={{
                      fontSize: '12px',
                      padding: '4px 8px',
                      borderRadius: '12px',
                      backgroundColor: 'var(--primary)',
                      color: 'var(--primary-foreground)',
                      fontWeight: '600',
                      textTransform: 'uppercase',
                      letterSpacing: '0.5px',
                    }}
                  >
                    {tech.category}
                  </span>
                </div>
                <div
                  style={{
                    fontSize: '16px',
                    fontWeight: '600',
                    color: 'var(--foreground)',
                    marginBottom: '4px',
                  }}
                >
                  {tech.name}
                </div>
                <div
                  style={{
                    fontSize: '14px',
                    color: 'var(--muted-foreground)',
                    lineHeight: '1.4',
                  }}
                >
                  {tech.description}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* ML Techniques Section */}
        <div style={{ marginBottom: '40px' }}>
          <h2
            style={{
              fontSize: '24px',
              fontWeight: '600',
              color: 'var(--foreground)',
              margin: '0 0 24px 0',
              textAlign: 'center',
            }}
          >
            🧠 Machine Learning Techniques
          </h2>

          <div
            style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fit, minmax(400px, 1fr))',
              gap: '20px',
            }}
          >
            {mlTechniques.map((technique, index) => (
              <div
                key={index}
                style={{
                  backgroundColor: 'var(--card)',
                  borderRadius: '12px',
                  padding: '24px',
                  border: '1px solid var(--border)',
                  boxShadow: '0 2px 8px rgba(0, 0, 0, 0.05)',
                  transition: 'all 0.3s ease',
                  animation: `fadeInUp 0.8s ease-out ${index * 0.1}s both`,
                  display: 'flex',
                  flexDirection: 'column',
                  alignItems: 'center',
                  textAlign: 'center',
                }}
                onMouseEnter={(e) => {
                  e.currentTarget.style.transform = 'translateY(-4px)';
                  e.currentTarget.style.boxShadow =
                    '0 8px 25px rgba(0, 0, 0, 0.12)';
                }}
                onMouseLeave={(e) => {
                  e.currentTarget.style.transform = 'translateY(0)';
                  e.currentTarget.style.boxShadow =
                    '0 2px 8px rgba(0, 0, 0, 0.05)';
                }}
              >
                <div
                  style={{
                    fontSize: '48px',
                    width: '80px',
                    height: '80px',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    borderRadius: '16px',
                    backgroundColor: `${technique.color}15`,
                    border: `3px solid ${technique.color}`,
                    marginBottom: '20px',
                  }}
                >
                  {technique.icon}
                </div>

                <h3
                  style={{
                    fontSize: '22px',
                    fontWeight: '600',
                    color: 'var(--foreground)',
                    margin: '0 0 16px 0',
                  }}
                >
                  {technique.title}
                </h3>

                <p
                  style={{
                    fontSize: '15px',
                    color: 'var(--muted-foreground)',
                    lineHeight: '1.6',
                    margin: 0,
                    maxWidth: '320px',
                  }}
                >
                  {technique.description}
                </p>
              </div>
            ))}
          </div>
        </div>

        {/* Project Features */}
        <div
          style={{
            backgroundColor: 'var(--card)',
            borderRadius: '16px',
            padding: '32px',
            boxShadow: '0 4px 20px rgba(0, 0, 0, 0.08)',
            border: '1px solid var(--border)',
            marginBottom: '40px',
          }}
        >
          <h2
            style={{
              fontSize: '24px',
              fontWeight: '600',
              color: 'var(--foreground)',
              margin: '0 0 24px 0',
              textAlign: 'center',
            }}
          >
            ✨ Key Features
          </h2>

          <div
            style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
              gap: '20px',
            }}
          >
            {[
              {
                title: 'Contextual Analysis',
                description:
                  'Understands negations and complete semantic context',
                icon: '🎯',
              },
              {
                title: 'Multi-Model Ensemble',
                description:
                  'Combines multiple algorithms for greater accuracy',
                icon: '🔗',
              },
              {
                title: 'Real-time Processing',
                description: 'Instant analysis with millisecond response times',
                icon: '⚡',
              },
              {
                title: 'Detailed Explanations',
                description: 'Provides clear reasons for each classification',
                icon: '💡',
              },
              {
                title: 'Responsive Dashboard',
                description: 'Modern and adaptive interface for all devices',
                icon: '📱',
              },
              {
                title: 'API RESTful',
                description:
                  'Robust backend with FastAPI and auto-documentation',
                icon: '🌐',
              },
            ].map((feature, index) => (
              <div
                key={index}
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '16px',
                  padding: '20px',
                  backgroundColor: 'var(--background)',
                  borderRadius: '12px',
                  border: '1px solid var(--border)',
                  transition: 'all 0.2s ease',
                }}
                onMouseEnter={(e) => {
                  e.currentTarget.style.transform = 'translateY(-2px)';
                  e.currentTarget.style.boxShadow =
                    '0 4px 12px rgba(0, 0, 0, 0.1)';
                }}
                onMouseLeave={(e) => {
                  e.currentTarget.style.transform = 'translateY(0)';
                  e.currentTarget.style.boxShadow = 'none';
                }}
              >
                <div
                  style={{
                    fontSize: '28px',
                    flexShrink: 0,
                    width: '48px',
                    height: '48px',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    backgroundColor: 'var(--muted)',
                    borderRadius: '8px',
                  }}
                >
                  {feature.icon}
                </div>
                <div>
                  <h4
                    style={{
                      fontSize: '16px',
                      fontWeight: '600',
                      color: 'var(--foreground)',
                      margin: '0 0 4px 0',
                    }}
                  >
                    {feature.title}
                  </h4>
                  <p
                    style={{
                      fontSize: '14px',
                      color: 'var(--muted-foreground)',
                      margin: 0,
                      lineHeight: '1.4',
                    }}
                  >
                    {feature.description}
                  </p>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Navigation Buttons */}
        <div
          style={{
            display: 'flex',
            justifyContent: 'center',
            gap: '16px',
            flexWrap: 'wrap',
          }}
        >
          <button
            onClick={() => window.history.back()}
            style={{
              backgroundColor: 'var(--primary)',
              color: 'var(--primary-foreground)',
              border: 'none',
              borderRadius: '8px',
              padding: '14px 28px',
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
              padding: '14px 28px',
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
          
          @media (max-width: 768px) {
            .ml-techniques-grid {
              grid-template-columns: 1fr;
            }
            
            .technologies-grid {
              grid-template-columns: 1fr;
            }
            
            .features-grid {
              grid-template-columns: 1fr;
            }
          }
        `}
      </style>
    </div>
  );
};

export default About;
