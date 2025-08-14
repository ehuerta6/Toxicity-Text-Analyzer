// Tipos para la API
export interface AnalyzeRequest {
  text: string;
}

export interface AnalyzeResponse {
  toxic: boolean;
  score: number;
  labels: string[];
  text_length: number;
  keywords_found: number;
}

// Función para analizar texto usando el backend
export async function analyze(text: string): Promise<AnalyzeResponse> {
  const apiUrl = import.meta.env.VITE_API_URL;

  if (!apiUrl) {
    throw new Error('VITE_API_URL no está configurada');
  }

  try {
    const response = await fetch(`${apiUrl}/analyze`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ text } as AnalyzeRequest),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(
        errorData.detail || `Error ${response.status}: ${response.statusText}`
      );
    }

    const data: AnalyzeResponse = await response.json();
    return data;
  } catch (error) {
    if (error instanceof Error) {
      throw error;
    }
    throw new Error('Error desconocido al analizar el texto');
  }
}

// Función para verificar la salud del backend
export async function checkBackendHealth(): Promise<boolean> {
  const apiUrl = import.meta.env.VITE_API_URL;

  if (!apiUrl) {
    return false;
  }

  try {
    const response = await fetch(`${apiUrl}/health`);
    return response.ok;
  } catch {
    return false;
  }
}
