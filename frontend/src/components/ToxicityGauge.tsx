interface ToxicityGaugeProps {
  percentage: number;
  size?: number;
  strokeWidth?: number;
}

export function ToxicityGauge({
  percentage,
  size = 200,
  strokeWidth = 12,
}: ToxicityGaugeProps) {
  const radius = (size - strokeWidth) / 2;
  const circumference = radius * 2 * Math.PI;
  const strokeDasharray = circumference;
  const strokeDashoffset = circumference - (percentage / 100) * circumference;

  // Determinar color basado en el porcentaje
  const getColor = (percent: number) => {
    if (percent < 30) return '#10B981'; // Verde - No tóxico
    if (percent < 70) return '#F59E0B'; // Amarillo - Borderline
    return '#EF4444'; // Rojo - Tóxico
  };

  // Determinar texto de estado
  const getStatusText = (percent: number) => {
    if (percent < 30) return 'Seguro';
    if (percent < 70) return 'Cuidado';
    return 'Tóxico';
  };

  const color = getColor(percentage);
  const statusText = getStatusText(percentage);

  return (
    <div className='flex flex-col items-center'>
      <div className='relative' style={{ width: size, height: size }}>
        {/* Gauge de fondo */}
        <svg width={size} height={size} className='transform -rotate-90'>
          <circle
            cx={size / 2}
            cy={size / 2}
            r={radius}
            stroke='#E5E7EB'
            strokeWidth={strokeWidth}
            fill='transparent'
          />
          {/* Gauge principal */}
          <circle
            cx={size / 2}
            cy={size / 2}
            r={radius}
            stroke={color}
            strokeWidth={strokeWidth}
            fill='transparent'
            strokeDasharray={strokeDasharray}
            strokeDashoffset={strokeDashoffset}
            strokeLinecap='round'
            className='transition-all duration-1000 ease-out'
            style={{
              filter: 'drop-shadow(0 0 8px rgba(0,0,0,0.1))',
            }}
          />
        </svg>

        {/* Contenido central */}
        <div className='absolute inset-0 flex flex-col items-center justify-center'>
          <div className='text-3xl font-bold' style={{ color }}>
            {Math.round(percentage)}%
          </div>
          <div className='text-sm font-medium text-gray-600 mt-1'>
            {statusText}
          </div>
        </div>
      </div>

      {/* Indicador de color */}
      <div className='flex items-center space-x-2 mt-4'>
        <div
          className='w-3 h-3 rounded-full'
          style={{ backgroundColor: color }}
        />
        <span className='text-sm text-gray-700 font-medium'>
          Nivel de toxicidad
        </span>
      </div>
    </div>
  );
}
