# 📁 ToxiGuard Project Structure

This document provides a comprehensive overview of the ToxiGuard project structure and organization.

## 🏗️ Overall Architecture

```
toxiguard/
├── 📁 frontend/          # React + TypeScript frontend application
├── 📁 backend/           # FastAPI + Python backend application
├── 📁 data/              # Training data and datasets
├── 📁 models/            # Trained ML models and artifacts
├── 📄 README.md          # Main project documentation
├── 📄 package.json       # Root package.json with project scripts
├── 📄 .gitignore         # Comprehensive gitignore file
├── 📄 start.sh           # Unix/Linux startup script
├── 📄 start.bat          # Windows startup script
└── 📄 PROJECT_STRUCTURE.md # This file
```

## 🎨 Frontend Structure (`frontend/`)

```
frontend/
├── 📁 src/
│   ├── 📁 components/    # Reusable UI components
│   │   ├── Button.tsx           # Button component with variants
│   │   ├── TextArea.tsx         # Text input with validation
│   │   ├── LoadingSpinner.tsx   # Loading indicators
│   │   ├── ErrorBoundary.tsx    # Error handling component
│   │   ├── Card.tsx             # Card layout component
│   │   ├── Badge.tsx            # Badge/tag component
│   │   ├── ToxicityGauge.tsx    # Toxicity visualization
│   │   ├── ColoredText.tsx      # Text highlighting
│   │   ├── SeverityBreakdown.tsx # Detailed analysis view
│   │   ├── AnalysisDetails.tsx  # Analysis results display
│   │   ├── Footer.tsx           # Page footer
│   │   └── About.tsx            # About page
│   ├── 📁 hooks/         # Custom React hooks
│   │   └── useToxicityAnalysis.ts # Main analysis hook
│   ├── 📁 lib/            # Utility functions and API
│   │   └── api.ts         # API client functions
│   ├── 📁 styles/         # Design system and styling
│   │   ├── common.ts      # Design system tokens
│   │   ├── responsive.ts  # Responsive utilities
│   │   └── index.ts       # Style exports
│   ├── 📁 assets/         # Static assets
│   ├── App.tsx            # Main application component
│   ├── main.tsx           # Application entry point
│   └── index.css          # Global styles
├── 📄 package.json        # Frontend dependencies
├── 📄 vite.config.ts      # Vite build configuration
├── 📄 tailwind.config.js  # Tailwind CSS configuration
└── 📄 tsconfig.json       # TypeScript configuration
```

## 🐍 Backend Structure (`backend/`)

```
backend/
├── 📁 app/
│   ├── 📁 ml/            # Machine learning modules
│   │   ├── __init__.py
│   │   ├── config.py      # ML configuration
│   │   └── model_evaluator.py # Model evaluation utilities
│   ├── main.py            # FastAPI application entry point
│   ├── models.py          # Data models and schemas
│   ├── services.py        # Business logic and ML services
│   ├── database.py        # Database operations
│   ├── improved_classifier.py    # Enhanced ML classifier
│   ├── ml_classifier.py          # Traditional ML classifier
│   ├── hybrid_classifier.py      # Hybrid approach classifier
│   ├── contextual_classifier.py  # Context-aware classifier
│   ├── advanced_preprocessor.py  # Text preprocessing
│   ├── advanced_toxicity_classifier.py # Advanced toxicity detection
│   ├── weight_optimizer.py       # Model weight optimization
│   └── model_trainer.py          # Model training utilities
├── 📁 models/             # Trained ML models
│   ├── *.pkl              # Pickled model files
│   ├── *.joblib           # Joblib model files
│   └── evaluation_results.json   # Model evaluation results
├── 📄 requirements.txt    # Python dependencies
└── 📄 README.md           # Backend-specific documentation
```

## 📊 Data Structure (`data/`)

```
data/
├── 📄 toxic_comments_processed.csv  # Processed training data
└── 📁 raw/                # Raw data files (if any)
```

## 🤖 ML Models Structure (`models/`)

```
models/
├── 📄 all_models.pkl      # Combined model file
├── 📄 evaluation_results.json # Model performance metrics
├── 📄 toxic_model.pkl     # Toxicity detection model
├── 📄 vectorizer.pkl      # Text vectorizer
├── 📄 gradient_boosting_trained.pkl    # Gradient boosting model
├── 📄 gradient_boosting_vectorizer.pkl # GB vectorizer
├── 📄 linear_svm_trained.pkl          # Linear SVM model
├── 📄 linear_svm_vectorizer.pkl       # SVM vectorizer
├── 📄 logistic_regression_trained.pkl  # Logistic regression model
├── 📄 logistic_regression_vectorizer.pkl # LR vectorizer
├── 📄 naive_bayes_trained.pkl         # Naive Bayes model
├── 📄 naive_bayes_vectorizer.pkl      # NB vectorizer
├── 📄 random_forest_trained.pkl       # Random Forest model
└── 📄 random_forest_vectorizer.pkl    # RF vectorizer
```

## 🚀 Quick Start Commands

### One-Command Setup

```bash
# Unix/Linux/macOS
./start.sh

# Windows
start.bat

# Or using npm
npm run setup
```

### Development

```bash
# Start both frontend and backend
npm run dev

# Start only frontend
npm run dev:frontend

# Start only backend
npm run dev:backend
```

### Building

```bash
# Build frontend for production
npm run build

# Preview production build
npm run preview
```

### Maintenance

```bash
# Clean all build artifacts
npm run clean

# Reset entire project
npm run reset

# Run all tests
npm run test

# Lint all code
npm run lint

# Format all code
npm run format
```

## 🔧 Key Technologies

### Frontend

- **React 18** - Modern React with hooks
- **TypeScript** - Type-safe development
- **Vite** - Fast build tool
- **Tailwind CSS** - Utility-first CSS
- **Custom Design System** - Consistent UI components

### Backend

- **FastAPI** - Modern Python web framework
- **Python 3.8+** - Core language
- **SQLite** - Lightweight database
- **Scikit-learn** - Machine learning library

### ML Components

- **Multiple Classifiers** - Ensemble approach
- **Hybrid Classification** - Rule-based + ML
- **Contextual Analysis** - Understanding context
- **Advanced Preprocessing** - Text preparation

## 📱 Responsive Design

The project implements a comprehensive responsive design system:

- **Mobile-first approach** - Designed for mobile first
- **6 breakpoints** - From 320px to 1536px
- **Consistent spacing** - 24 standardized spacing values
- **Typography scale** - Responsive font sizing
- **Component variants** - Adaptive component behavior

## 🎨 Design System

- **Typography Scale** - Consistent font hierarchy
- **Color Palette** - Semantic color system
- **Spacing System** - Standardized spacing values
- **Component Library** - Reusable UI components
- **Responsive Patterns** - Mobile-first layouts

## 🔒 Security & Performance

- **Input Validation** - Comprehensive input sanitization
- **Error Handling** - Graceful error management
- **Performance Optimization** - Efficient ML processing
- **Caching** - Smart result caching
- **Rate Limiting** - API protection

## 📈 Monitoring & Analytics

- **Health Checks** - System status monitoring
- **Performance Metrics** - Response time tracking
- **Error Logging** - Comprehensive error tracking
- **Usage Statistics** - API usage analytics

---

**Note**: This structure is designed for long-term maintainability and scalability. All components follow consistent patterns and are well-documented for easy development and contribution.
