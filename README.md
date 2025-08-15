# ToxiGuard - Advanced Toxicity Detection System

A comprehensive, production-ready system for detecting toxic content in text using advanced machine learning algorithms and contextual analysis.

## 🚀 Features

- **Advanced ML Classification**: Multiple algorithms including SVM, Random Forest, Naive Bayes, and Logistic Regression
- **Contextual Analysis**: Embedding-based analysis with sentence transformers for better context understanding
- **Hybrid Classification**: Combines rule-based, ML, and contextual approaches for optimal accuracy
- **Ultra-Sensitive Detection**: Advanced toxicity detection with severity weighting and repetition analysis
- **Real-time API**: FastAPI backend with comprehensive endpoints
- **Modern Frontend**: React-based dashboard with real-time analysis and visualization
- **Production Ready**: Clean, modular codebase with comprehensive error handling

## 🏗️ Architecture

```
toxiguard/
├── backend/                 # FastAPI backend server
│   ├── app/                # Core application modules
│   │   ├── main.py         # FastAPI application with endpoints
│   │   ├── models.py       # Pydantic data models
│   │   ├── database.py     # SQLite database for analysis history
│   │   ├── hybrid_classifier.py      # Main hybrid classifier
│   │   ├── advanced_toxicity_classifier.py  # Ultra-sensitive classifier
│   │   ├── contextual_classifier.py  # Contextual analysis with embeddings
│   │   ├── improved_classifier.py    # Rule-based classifier
│   │   ├── ml_classifier.py          # ML-based classifier
│   │   ├── ml_models.py              # ML model management
│   │   ├── model_trainer.py          # Model training utilities
│   │   ├── weight_optimizer.py       # Weight optimization system
│   │   ├── advanced_preprocessor.py  # Text preprocessing
│   │   └── services.py               # Legacy services (maintained for compatibility)
│   ├── ml/                 # ML utilities and configuration
│   │   ├── config.py       # ML configuration
│   │   └── model_evaluator.py  # Model evaluation utilities
│   ├── models/             # Trained ML models
│   ├── requirements.txt    # Python dependencies
│   └── README.md           # Backend documentation
├── frontend/               # React frontend application
│   ├── src/                # Source code
│   │   ├── components/     # React components
│   │   ├── hooks/          # Custom React hooks
│   │   ├── lib/            # Utility libraries
│   │   └── styles/         # Styling and design system
│   ├── package.json        # Node.js dependencies
│   └── README.md           # Frontend documentation
├── data/                   # Training and test datasets
└── README.md               # This file
```

## 🔧 Backend Features

### Core Classifiers

- **Hybrid Classifier**: Combines all approaches with intelligent fallback
- **Advanced Toxicity Classifier**: Ultra-sensitive detection with severity weighting
- **Contextual Classifier**: Embedding-based analysis using sentence-transformers
- **ML Classifier**: Support for multiple ML algorithms
- **Improved Classifier**: Rule-based approach with context awareness

### API Endpoints

- `POST /analyze` - Analyze text for toxicity
- `POST /batch-analyze` - Analyze multiple texts
- `GET /classifier-info` - Get classifier information
- `POST /switch-classifier` - Switch between classifiers
- `GET /history` - Get analysis history
- `GET /stats` - Get system statistics

### Advanced Features

- **Contextual Analysis**: Detects negations and context (e.g., "not stupid" vs "stupid")
- **Severity Weighting**: Different weights for different types of toxicity
- **Repetition Analysis**: Detects repeated toxic content
- **Multi-language Support**: English and Spanish text analysis
- **Real-time Processing**: Optimized for low-latency responses

## 🎨 Frontend Features

### User Interface

- **Modern Design**: Clean, responsive interface with Tailwind CSS
- **Real-time Analysis**: Instant toxicity detection with visual feedback
- **Interactive Dashboard**: Comprehensive analysis results with explanations
- **Toxicity Visualization**: Color-coded text highlighting and gauge displays
- **Responsive Layout**: Works on desktop and mobile devices

### Analysis Features

- **Text Highlighting**: Toxic words are highlighted with color coding
- **Severity Breakdown**: Detailed breakdown of toxicity by category
- **Explanation System**: Clear explanations for why content was flagged
- **Category Detection**: Identifies specific types of toxicity
- **Confidence Scoring**: Shows confidence level for each analysis

## 🚀 Quick Start

### Backend Setup

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

### Access Points

- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Frontend**: http://localhost:5173

## 📊 Model Performance

The system includes multiple pre-trained models:

- **Linear SVM**: High accuracy for general toxicity detection
- **Random Forest**: Robust performance with complex patterns
- **Naive Bayes**: Fast classification with good baseline performance
- **Logistic Regression**: Balanced accuracy and interpretability

## 🔍 Analysis Examples

### Contextual Understanding

- **"You are stupid"** → High toxicity (85%)
- **"You are not stupid"** → Low toxicity (15%) - Context detected
- **"I hate you"** → High toxicity (90%)
- **"I don't hate you"** → Low toxicity (10%) - Negation detected

### Multi-category Detection

- **Insults**: Mild, moderate, and severe levels
- **Harassment**: Direct threats and intimidation
- **Discrimination**: Racism, sexism, homophobia
- **Spam**: Toxic promotional content

## 🛠️ Development

### Code Quality

- **Clean Architecture**: Modular, maintainable code structure
- **Type Hints**: Full Python type annotation support
- **Error Handling**: Comprehensive error handling and logging
- **Testing**: Built-in testing utilities and examples
- **Documentation**: Detailed docstrings and comments

### Performance Optimizations

- **Caching**: Intelligent caching of model predictions
- **Async Processing**: Non-blocking API responses
- **Memory Management**: Efficient memory usage for large texts
- **Batch Processing**: Optimized for multiple text analysis

## 📈 Production Deployment

### Requirements

- Python 3.8+
- Node.js 18+
- 4GB+ RAM (for ML models)
- Fast storage for model files

### Environment Variables

```bash
FRONTEND_URL=http://localhost:5173
HOST=0.0.0.0
PORT=8000
DATABASE_URL=sqlite:///analysis_history.db
```

### Scaling Considerations

- **Load Balancing**: Multiple backend instances
- **Model Caching**: Shared model storage
- **Database**: Consider PostgreSQL for high-volume production
- **Monitoring**: Health checks and performance metrics

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes with proper testing
4. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For issues and questions:

1. Check the documentation
2. Review existing issues
3. Create a new issue with detailed information

---

**ToxiGuard** - Advanced toxicity detection powered by machine learning and contextual analysis.
