export interface Document {
  id: string;
  filename: string;
  uploaded_at: string;
  chunk_count?: number;
}