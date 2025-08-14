import { AnalyzeResponse } from '../lib/api';

interface ResultExplanationProps {
  result: AnalyzeResponse;
}

export function ResultExplanation({ result }: ResultExplanationProps) {
  const getExplanation = () => {
    const { toxic, toxicity_percentage, category, labels } = result;
    
    if (!toxic) {
      return {
        title: "Texto Seguro ✅",
        description: "El análisis indica que este texto no contiene contenido tóxico significativo.",
        details: "Puede ser compartido de manera segura en la mayoría de contextos."
      };
    }

    if (toxicity_percentage >= 80) {
      return {
        title: "Alto Nivel de Toxicidad ⚠️",
        description: "Este texto contiene múltiples elementos tóxicos que requieren atención inmediata.",
        details: "Se recomienda revisar y posiblemente moderar antes de publicar."
      };
    }

    if (toxicity_percentage >= 50) {
      return {
        title: "Nivel Moderado de Toxicidad ⚠️",
        description: "El texto muestra algunos signos de toxicidad que podrían ser problemáticos.",
        details: "Considera revisar el contenido antes de compartirlo."
      };
    }

    return {
      title: "Bajo Nivel de Toxicidad ⚠️",
      description: "Se detectaron algunos elementos que podrían ser considerados tóxicos.",
      details: "El texto es mayormente seguro, pero ten cuidado con ciertas frases."
    };
  };

  const getCategoryInfo = () => {
    if (!result.category) return null;

    const categoryInfo = {
      insulto: {
        name: "Insulto",
        description: "Contiene palabras o frases ofensivas dirigidas a personas o grupos.",
        icon: "💬"
      },
      acoso: {
        name: "Acoso",
        description: "Incluye amenazas, intimidación o comportamiento hostil.",
        icon: "🚫"
      },
      discriminacion: {
        name: "Discriminación",
        description: "Contiene prejuicios o comentarios discriminatorios.",
        icon: "⚠️"
      },
      spam: {
        name: "Spam",
        description: "Contenido no deseado o comercial no solicitado.",
        icon: "📧"
      }
    };

    return categoryInfo[result.category as keyof typeof categoryInfo];
  };

  const explanation = getExplanation();
  const categoryInfo = getCategoryInfo();

  return (
    <div className="bg-gradient-to-r from-blue-50 to-indigo-50 border border-blue-200 rounded-xl p-6">
      <div className="space-y-4">
        {/* Título y descripción principal */}
        <div className="text-center">
          <h3 className="text-xl font-bold text-gray-900 mb-2">
            {explanation.title}
          </h3>
          <p className="text-gray-700 leading-relaxed">
            {explanation.description}
          </p>
          <p className="text-sm text-gray-600 mt-2">
            {explanation.details}
          </p>
        </div>

        {/* Información de categoría */}
        {categoryInfo && (
          <div className="bg-white rounded-lg p-4 border border-blue-100">
            <div className="flex items-center space-x-3">
              <span className="text-2xl">{categoryInfo.icon}</span>
              <div>
                <h4 className="font-semibold text-gray-900">
                  Categoría: {categoryInfo.name}
                </h4>
                <p className="text-sm text-gray-600">
                  {categoryInfo.description}
                </p>
              </div>
            </div>
          </div>
        )}

        {/* Etiquetas detectadas */}
        {result.labels.length > 0 && (
          <div className="text-center">
            <p className="text-sm text-gray-600 mb-2">
              Elementos detectados:
            </p>
            <div className="flex flex-wrap justify-center gap-2">
              {result.labels.map((label, index) => (
                <span
                  key={index}
                  className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-800"
                >
                  {label}
                </span>
              ))}
            </div>
          </div>
        )}

        {/* Información técnica */}
        <div className="grid grid-cols-2 gap-4 text-center text-sm">
          <div className="bg-white rounded-lg p-3 border border-blue-100">
            <div className="font-semibold text-gray-900">
              {result.response_time_ms}ms
            </div>
            <div className="text-gray-500">Tiempo de respuesta</div>
          </div>
          <div className="bg-white rounded-lg p-3 border border-blue-100">
            <div className="font-semibold text-gray-900">
              {result.model_used}
            </div>
            <div className="text-gray-500">Modelo utilizado</div>
          </div>
        </div>
      </div>
    </div>
  );
}
