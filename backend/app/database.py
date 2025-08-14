import sqlite3
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional

class AnalysisHistoryDB:
    """Base de datos SQLite para el historial de análisis"""
    
    def __init__(self, db_path: str = "analysis_history.db"):
        self.db_path = Path(db_path)
        self.init_database()
    
    def init_database(self):
        """Inicializa la base de datos y crea las tablas necesarias"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS analysis_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    text TEXT NOT NULL,
                    toxic BOOLEAN NOT NULL,
                    score REAL NOT NULL,
                    toxicity_percentage REAL,
                    category TEXT,
                    labels TEXT,  -- JSON string
                    text_length INTEGER NOT NULL,
                    keywords_found INTEGER NOT NULL,
                    response_time_ms REAL,
                    model_used TEXT,
                    timestamp DATETIME NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()
            print("✅ Base de datos de historial inicializada")
    
    def save_analysis(self, text: str, result: Dict[str, Any]) -> int:
        """Guarda un análisis en el historial"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                INSERT INTO analysis_history (
                    text, toxic, score, toxicity_percentage, category,
                    labels, text_length, keywords_found, response_time_ms,
                    model_used, timestamp
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                text,
                result.get('toxic', False),
                result.get('score', 0.0),
                result.get('toxicity_percentage'),
                result.get('category'),
                json.dumps(result.get('labels', [])),
                result.get('text_length', 0),
                result.get('keywords_found', 0),
                result.get('response_time_ms'),
                result.get('model_used'),
                result.get('timestamp', datetime.now().isoformat())
            ))
            conn.commit()
            return cursor.lastrowid
    
    def get_history(self, limit: int = 50, offset: int = 0) -> List[Dict[str, Any]]:
        """Obtiene el historial de análisis"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("""
                SELECT * FROM analysis_history 
                ORDER BY created_at DESC 
                LIMIT ? OFFSET ?
            """, (limit, offset))
            
            results = []
            for row in cursor.fetchall():
                result = dict(row)
                # Convertir JSON string de vuelta a lista
                if result['labels']:
                    result['labels'] = json.loads(result['labels'])
                else:
                    result['labels'] = []
                results.append(result)
            
            return results
    
    def get_statistics(self) -> Dict[str, Any]:
        """Obtiene estadísticas del historial"""
        with sqlite3.connect(self.db_path) as conn:
            # Total de análisis
            total_cursor = conn.execute("SELECT COUNT(*) as total FROM analysis_history")
            total = total_cursor.fetchone()[0]
            
            # Análisis tóxicos
            toxic_cursor = conn.execute("SELECT COUNT(*) as toxic FROM analysis_history WHERE toxic = 1")
            toxic = toxic_cursor.fetchone()[0]
            
            # Promedio de toxicidad
            avg_cursor = conn.execute("SELECT AVG(toxicity_percentage) as avg_toxicity FROM analysis_history")
            avg_toxicity = avg_cursor.fetchone()[0] or 0
            
            # Análisis por categoría
            categories_cursor = conn.execute("""
                SELECT category, COUNT(*) as count 
                FROM analysis_history 
                WHERE category IS NOT NULL 
                GROUP BY category 
                ORDER BY count DESC
            """)
            categories = {row[0]: row[1] for row in categories_cursor.fetchall()}
            
            # Análisis recientes (últimas 24 horas)
            recent_cursor = conn.execute("""
                SELECT COUNT(*) as recent 
                FROM analysis_history 
                WHERE created_at >= datetime('now', '-1 day')
            """)
            recent = recent_cursor.fetchone()[0]
            
            return {
                'total_analyses': total,
                'toxic_analyses': toxic,
                'safe_analyses': total - toxic,
                'toxicity_rate': (toxic / total * 100) if total > 0 else 0,
                'average_toxicity': round(avg_toxicity, 1),
                'categories': categories,
                'recent_analyses': recent
            }
    
    def delete_analysis(self, analysis_id: int) -> bool:
        """Elimina un análisis del historial"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("DELETE FROM analysis_history WHERE id = ?", (analysis_id,))
            conn.commit()
            return cursor.rowcount > 0
    
    def clear_history(self) -> int:
        """Limpia todo el historial"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("DELETE FROM analysis_history")
            conn.commit()
            return cursor.rowcount
    
    def search_history(self, query: str, limit: int = 20) -> List[Dict[str, Any]]:
        """Busca en el historial por texto"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("""
                SELECT * FROM analysis_history 
                WHERE text LIKE ? 
                ORDER BY created_at DESC 
                LIMIT ?
            """, (f"%{query}%", limit))
            
            results = []
            for row in cursor.fetchall():
                result = dict(row)
                if result['labels']:
                    result['labels'] = json.loads(result['labels'])
                else:
                    result['labels'] = []
                results.append(result)
            
            return results

# Instancia global de la base de datos
history_db = AnalysisHistoryDB()

