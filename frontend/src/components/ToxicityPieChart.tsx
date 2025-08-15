import React from 'react';

interface ToxicityPieChartProps {
  toxicityPercentage: number;
  size?: number;
  strokeWidth?: number;
}

const ToxicityPieChart: React.FC<ToxicityPieChartProps> = ({ 
  toxicityPercentage, 
  size = 120, 
  strokeWidth = 12 
}) => {
  const radius = (size - strokeWidth) / 2;
  const circumference = radius * 2 * Math.PI;
  const progress = (toxicityPercentage / 100) * circumference;
  const remaining = circumference - progress;

  const getToxicityColor = (percentage: number): string => {
    if (percentage <= 30) return '#10b981'; // Verde
    if (percentage <= 60) return '#f59e0b'; // Amarillo
    return '#ef4444'; // Rojo
  };

  const getToxicityLabel = (percentage: number): string => {
    if (percentage <= 30) return 'Baja';
    if (percentage <= 60) return 'Moderada';
    return 'Alta';
  };

  const centerX = size / 2;
  const centerY = size / 2;

  return (
    <div className="flex flex-col items-center space-y-3">
      <div className="relative">
        <svg width={size} height={size} className="transform -rotate-90">
          {/* Fondo del círculo */}
          <circle
            cx={centerX}
            cy={centerY}
            r={radius}
            stroke="#e5e7eb"
            strokeWidth={strokeWidth}
            fill="transparent"
          />
          
          {/* Progreso de toxicidad */}
          <circle
            cx={centerX}
            cy={centerY}
            r={radius}
            stroke={getToxicityColor(toxicityPercentage)}
            strokeWidth={strokeWidth}
            fill="transparent"
            strokeDasharray={circumference}
            strokeDashoffset={remaining}
            strokeLinecap="round"
            className="transition-all duration-1000 ease-out"
            style={{
              filter: 'drop-shadow(0 4px 8px rgba(0, 0, 0, 0.1))'
            }}
          />
        </svg>
        
        {/* Porcentaje central */}
        <div className="absolute inset-0 flex items-center justify-center">
          <div className="text-center">
            <div className={`text-2xl font-bold ${getToxicityColor(toxicityPercentage) === '#10b981' ? 'text-green-600' : getToxicityColor(toxicityPercentage) === '#f59e0b' ? 'text-yellow-600' : 'text-red-600'}`}>
              {toxicityPercentage}%
            </div>
            <div className="text-xs text-gray-500 font-medium">
              {getToxicityLabel(toxicityPercentage)}
            </div>
          </div>
        </div>
      </div>
      
      {/* Leyenda */}
      <div className="text-center">
        <div className="text-sm font-semibold text-gray-700 mb-1">
          Nivel de Toxicidad
        </div>
        <div className="flex items-center justify-center space-x-3 text-xs">
          <div className="flex items-center space-x-1">
            <div className="w-3 h-3 rounded-full bg-green-500"></div>
            <span className="text-gray-600">0-30%</span>
          </div>
          <div className="flex items-center space-x-1">
            <div className="w-3 h-3 rounded-full bg-yellow-500"></div>
            <span className="text-gray-600">30-60%</span>
          </div>
          <div className="flex items-center space-x-1">
            <div className="w-3 h-3 rounded-full bg-red-500"></div>
            <span className="text-gray-600">60-100%</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ToxicityPieChart;
