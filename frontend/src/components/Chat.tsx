import { useState } from "react";
import { sendMessage } from "../services/api";
import type { ChatMessage } from "../types/chat";

export default function Chat() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [conversationId, setConversationId] = useState<string | null>(null);

  const handleSend = async () => {
    if (!input.trim() || loading) return;

    const userMessage = input;

    // Show user message immediately
    setMessages((prev) => [
      ...prev,
      { role: "user", content: userMessage },
    ]);

    setInput("");
    setLoading(true);
    setError("");

    try {
      const response = await sendMessage({
        message: userMessage,
        conversation_id: conversationId,
      });

      // Save conversation ID returned by backend
      setConversationId(response.conversation_id);

      // Add assistant reply
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: response.reply,
        },
      ]);
    } catch (err) {
      setError("Unable to connect to the backend.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="chat-container">
      <h1>Smart Support Assistant</h1>

      <div className="messages">
        {messages.map((msg, index) => (
          <div
            key={index}
            className={
              msg.role === "user"
                ? "message user-message"
                : "message assistant-message"
            }
          >
            {msg.content}
          </div>
        ))}
      </div>

      {error && <div className="error">{error}</div>}

      <div className="input-area">
        <input
          type="text"
          placeholder="Type your message..."
          value={input}
          disabled={loading}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter") {
              handleSend();
            }
          }}
        />

        <button onClick={handleSend} disabled={loading}>
          {loading ? "Sending..." : "Send"}
        </button>
      </div>
    </div>
  );
}