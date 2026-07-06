import type { ChatRequest, ChatResponse } from "../types/chat";

const API_URL = "http://127.0.0.1:8000/chat";

export async function sendMessage(
  request: ChatRequest
): Promise<ChatResponse> {
  const response = await fetch(API_URL, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(request),
  });

  if (!response.ok) {
    throw new Error("Failed to connect to backend");
  }

  return response.json();
}