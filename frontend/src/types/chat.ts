

export interface ResponseMessage {
  role: string;
  content: string;
}

export interface ChatResponse {
  user: ResponseMessage;
  reply: string;
  conversation_id: string;
}