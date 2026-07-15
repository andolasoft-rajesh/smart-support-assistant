export interface ChatRequest {
  message: string;
  conversation_id?: string | null;
  document_id?: string | null;
}

export interface ChatResponse {
  reply: string;
  conversation_id: string;
}

export interface ChatMessage {
  role: "user" | "assistant";
  content: string;
}