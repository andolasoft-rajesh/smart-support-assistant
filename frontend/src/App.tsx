import { useState } from "react";
import "./App.css";
import api from "./services/api";
import type { Message } from "./types/message";


function App() {
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState(false);
  const [conversationId, setConversationId] = useState<string>();

  const handleSend = async () => {
    if (!message.trim()) return;

    // Save the user's message
    const userMessage: Message = {
      id: Date.now(),
      text: message,
      sender: "user",
    };

    setMessages((prev) => [...prev, userMessage]);

    const currentMessage = message;
    setMessage("");

    setLoading(true);

    try {
      const response = await api.post("/chat", {
        message: currentMessage,
        conversation_id: conversationId,
      });
      

      // Save assistant response
      const assistantMessage: Message = {
        id: Date.now() + 1,
        text: response.data.reply,
        sender: "assistant",
      };

      setMessages((prev) => [...prev, assistantMessage]);

      setConversationId(response.data.conversation_id);
    } catch {
      const errorMessage: Message = {
        id: Date.now() + 1,
        text: "Unable to reach the backend.",
        sender: "assistant",
      };

      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      <div className="chat-container">
        <div className="header">
          Smart Support Assistant
        </div>

        <div className="messages">
          {messages.length === 0 ? (
            <p>No messages yet.</p>
          ) : (
            messages.map((msg) => (
              <div
                key={msg.id}
                className={
                  msg.sender === "user"
                    ? "message user"
                    : "message assistant"
                }
              >
                {msg.text}
              </div>
            ))
          )}
        </div>

        <div className="input-area">
          <input
            type="text"
            placeholder="Type your message..."
            value={message}
            disabled={loading}
            onChange={(e) => setMessage(e.target.value)}
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
    </div>
  );
}

export default App;