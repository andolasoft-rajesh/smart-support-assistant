"use client";

import { useState } from "react";
import { Message, ChatResponse } from "@/types";
import MessageList from "./MessageList";
import MessageInput from "./MessageInput";

const API_BASE_URL = "http://localhost:8000";

export default function ChatWindow() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState(false);
  const [conversationId, setConversationId] = useState<string | undefined>();
  const [error, setError] = useState<string | null>(null);

  const send = async (text: string) => {
    try {
      setError(null);
      // Add user message to the UI immediately
      setMessages((m) => [...m, { role: "user", content: text }]);
      setLoading(true);

      const response = await fetch(`${API_BASE_URL}/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          message: text,
          conversation_id: conversationId,
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data: ChatResponse = await response.json();

      // Update conversation ID if it's a new one
      if (!conversationId) {
        setConversationId(data.conversation_id);
      }

      // Add assistant message
      setMessages((m) => [
        ...m,
        { role: "assistant", content: data.reply },
      ]);
    } catch (err) {
      const errorMessage =
        err instanceof Error ? err.message : "Failed to send message";
      setError(errorMessage);
      console.error("Chat error:", err);

      // Remove the user message if there was an error
      setMessages((m) => m.slice(0, -1));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-screen bg-white">
      {/* Header */}
      <div className="bg-blue-600 text-white p-4 shadow-md">
        <h1 className="text-xl font-semibold">Smart Support Assistant</h1>
        {conversationId && (
          <p className="text-sm text-blue-100">ID: {conversationId}</p>
        )}
      </div>

      {/* Error message */}
      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3">
          <p className="text-sm">{error}</p>
        </div>
      )}

      {/* Message list */}
      <MessageList messages={messages} loading={loading} />

      {/* Input */}
      <MessageInput onSend={send} disabled={loading} />
    </div>
  );
}
