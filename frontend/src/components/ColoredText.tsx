import React from 'react';

interface ToxicityMap {
  [word: string]: number;
}

interface ColoredTextProps {
  text: string;
  toxicityMap: ToxicityMap;
}

const ColoredText: React.FC<ColoredTextProps> = ({ text, toxicityMap }) => {
  const getToxicityColor = (percentage: number): string => {
    if (percentage <= 30) return '#10b981'; // Green
    if (percentage <= 60) return '#f59e0b'; // Yellow
    return '#ef4444'; // Red
  };

  const getToxicityClass = (percentage: number): string => {
    if (percentage <= 30) return 'text-green-600';
    if (percentage <= 60) return 'text-yellow-600';
    return 'text-red-600';
  };

  const renderText = () => {
    if (!text || !toxicityMap || Object.keys(toxicityMap).length === 0) {
      return <span className='text-gray-700'>{text}</span>;
    }

    const words = text.split(/(\s+)/);

    return words.map((word, index) => {
      const cleanWord = word.toLowerCase().replace(/[^\w]/g, '');
      const toxicityPercentage = toxicityMap[cleanWord] || 0;

      if (toxicityPercentage > 0) {
        const color = getToxicityColor(toxicityPercentage);
        const textClass = getToxicityClass(toxicityPercentage);

        return (
          <span
            key={index}
            className={`${textClass} cursor-help transition-all duration-200 hover:scale-105`}
            style={{
              borderBottom: `3px solid ${color}`,
              borderBottomStyle: 'solid',
              borderBottomWidth: '3px',
              borderBottomColor: color,
            }}
            title={`Toxicity: ${toxicityPercentage}%`}
          >
            {word}
          </span>
        );
      }

      return <span key={index}>{word}</span>;
    });
  };

  return <div className='text-gray-800 leading-relaxed'>{renderText()}</div>;
};

export default ColoredText;
