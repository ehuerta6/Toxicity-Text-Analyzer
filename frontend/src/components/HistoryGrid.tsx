import React from 'react';
import ToxicityPieChart from './ToxicityPieChart';

interface HistoryItem {
  id: string;
  text: string;
  toxicity_percentage: number;
  category: string;
  timestamp: string;
  is_toxic: boolean;
}

interface HistoryGridProps {
  history: HistoryItem[];
  onDeleteItem: (id: string) => void;
  isLoading: boolean;
}

const HistoryGrid: React.FC<HistoryGridProps> = ({ history, onDeleteItem, isLoading }) => {
  const formatTimestamp = (timestamp: string): string => {
    const date = new Date(timestamp);
    return date.toLocaleString('es-ES', {
      day: '2-digit',
      month: '2-digit',
      year: '2-digit',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const truncateText = (text: string, maxLength: number = 50): string => {
    if (text.length <= maxLength) return text;
    return text.substring(0, maxLength) + '...';
  };

  const getCategoryColor = (category: string): string => {
    const colors: { [key: string]: string } = {
      'insulto_leve': 'bg-blue-100 text-blue-800',
      'insulto_moderado': 'bg-orange-100 text-orange-800',
      'insulto_severo': 'bg-red-100 text-red-800',
      'acoso': 'bg-purple-100 text-purple-800',
      'discriminacion': 'bg-pink-100 text-pink-800',
      'spam': 'bg-gray-100 text-gray-800'
    };
    return colors[category] || 'bg-gray-100 text-gray-800';
  };

  if (isLoading) {
    return (
      <div className="col-span-full flex justify-center items-center py-8">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (history.length === 0) {
    return (
      <div className="col-span-full text-center py-8 text-gray-500">
        <div className="text-lg font-medium mb-2">No hay análisis previos</div>
        <div className="text-sm">Realiza tu primer análisis para ver el historial aquí</div>
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      {history.slice(0, 6).map((item) => (
        <div
          key={item.id}
          className="bg-white rounded-lg border border-gray-200 p-4 hover:shadow-md transition-all duration-200 hover:scale-105"
        >
          {/* Header con timestamp y botón eliminar */}
          <div className="flex justify-between items-start mb-3">
            <div className="text-xs text-gray-500 font-medium">
              {formatTimestamp(item.timestamp)}
            </div>
            <button
              onClick={() => onDeleteItem(item.id)}
              className="text-gray-400 hover:text-red-500 transition-colors duration-200 p-1"
              title="Eliminar análisis"
            >
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          {/* Mini gráfica y porcentaje */}
          <div className="flex items-center space-x-3 mb-3">
            <ToxicityPieChart 
              toxicityPercentage={item.toxicity_percentage} 
              size={60} 
              strokeWidth={6} 
            />
            <div className="flex-1">
              <div className="text-lg font-bold text-gray-800">
                {item.toxicity_percentage}%
              </div>
              <div className={`inline-block px-2 py-1 rounded-full text-xs font-medium ${getCategoryColor(item.category)}`}>
                {item.category.replace('_', ' ')}
              </div>
            </div>
          </div>

          {/* Texto analizado */}
          <div className="text-sm text-gray-700 leading-relaxed">
            {truncateText(item.text, 80)}
          </div>

          {/* Indicador de toxicidad */}
          <div className="mt-3 flex items-center justify-between">
            <div className={`flex items-center space-x-1 text-xs ${
              item.is_toxic ? 'text-red-600' : 'text-green-600'
            }`}>
              <div className={`w-2 h-2 rounded-full ${
                item.is_toxic ? 'bg-red-500' : 'bg-green-500'
              }`}></div>
              <span className="font-medium">
                {item.is_toxic ? 'Tóxico' : 'Seguro'}
              </span>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
};

export default HistoryGrid;
