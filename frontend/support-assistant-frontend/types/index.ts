export interface Message {
  role: "user" | "assistant";
  content: string;
}

export interface ChatRequest {
  message: string;
  conversation_id?: string;
}

export interface ChatResponse {
  user: {
    role: "user";
    content: string;
  };
  reply: string;
  conversation_id: string;
}

export interface UploadResponse {
  filename: string;
  chunks: number;
}

export interface DocumentInfo {
  filename: string;
  chunks: number;
}

export interface SummaryResponse {
  summary: string;
  key_points: string[];
}
