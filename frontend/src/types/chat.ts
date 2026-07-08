export interface ConversationSummary {
  conversation_id: string;
  preview: string;
  created_at: string;
}

export interface ConversationListResponse {
  conversations: ConversationSummary[];
}

export interface HistoryMessage {
  role: string;
  content: string;
}

export interface HistoryResponse {
  messages: HistoryMessage[];
}