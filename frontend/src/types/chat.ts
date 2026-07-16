export interface ChatRequest {
  message: string;
  conversation_id?: string | null;
  document_id?: string | null;
  strict_document?: boolean;
}

export interface ChatResponse {
  reply: string;
  conversation_id: string;
}

export interface ChatMessage {
  role: "user" | "assistant";
  content: string;
}