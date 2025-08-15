# 🛡️ ToxiGuard - Professional Content Moderation

A professional-grade content moderation system powered by advanced machine learning algorithms for detecting toxic and inappropriate content in text.

## ✨ Features

- **Advanced ML Detection**: Sophisticated machine learning models for accurate toxicity detection
- **Real-time Analysis**: Instant text analysis with detailed toxicity scoring
- **Interactive Dashboard**: Modern, responsive web interface with real-time feedback
- **Performance Optimized**: Fast and efficient backend with optimized ML pipeline
- **Professional UI**: Clean, intuitive interface designed for content moderators

## 🏗️ Architecture

### Backend (FastAPI + Python)
- **FastAPI**: High-performance async web framework
- **ML Pipeline**: Optimized machine learning models for toxicity detection
- **Database**: SQLite for analysis history and statistics
- **CORS**: Configured for frontend integration

### Frontend (React + TypeScript)
- **React 19**: Latest React with modern hooks and patterns
- **TypeScript**: Full type safety and better development experience
- **Tailwind CSS**: Utility-first CSS framework for responsive design
- **Vite**: Fast build tool and development server

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 18+
- npm or yarn

### Backend Setup
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m spacy download en_core_web_sm
python -m uvicorn app.main:app --reload
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

### Access the Application
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## 📊 API Endpoints

- `POST /analyze` - Analyze single text for toxicity
- `POST /batch-analyze` - Analyze multiple texts in batch
- `GET /history` - Get analysis history
- `GET /stats` - Get system statistics
- `GET /health` - Health check

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the backend directory:
```env
FRONTEND_URL=http://localhost:5173
MODEL_PATH=models/
DEBUG=true
```

### ML Model Configuration
The system automatically loads the best available ML models from the `models/` directory.

## 📁 Project Structure

```
toxiguard/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI application
│   │   ├── models.py            # Data models
│   │   ├── improved_classifier.py # ML classifier
│   │   └── database.py          # Database operations
│   ├── ml/
│   │   └── config.py            # ML configuration
│   ├── models/                  # Trained ML models
│   └── requirements.txt         # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── components/          # React components
│   │   ├── hooks/               # Custom React hooks
│   │   ├── styles/              # CSS and styling
│   │   └── App.tsx             # Main application
│   └── package.json            # Node.js dependencies
└── data/                       # Training and test data
```

## 🧪 Testing

### Backend Testing
```bash
cd backend
python -m pytest
```

### Frontend Testing
```bash
cd frontend
npm run test
```

## 📈 Performance

- **Response Time**: < 100ms for typical text analysis
- **Throughput**: 100+ requests/second
- **Memory Usage**: Optimized for production deployment
- **Scalability**: Horizontal scaling ready

## 🔒 Security

- Input validation and sanitization
- CORS configuration
- Rate limiting (configurable)
- Secure ML model loading

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Check the API documentation at `/docs`
- Review the code comments
- Open an issue on GitHub

---

**ToxiGuard** - Professional content moderation powered by AI 🚀
