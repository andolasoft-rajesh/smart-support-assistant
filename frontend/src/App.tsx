import { useState, useEffect } from "react";
import "./App.css";
import api from "./services/api";
import type { Message } from "./types/message";
import type { ConversationSummary } from "./types/chat";

function App() {
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState(false);
  const [conversationId, setConversationId] = useState<string>();
  const [conversations, setConversations] = useState<ConversationSummary[]>([]);

  const loadConversations = async () => {
    try {
      const response = await api.get("/conversations");
      setConversations(response.data.conversations);
    } catch {
      // Silently ignore — sidebar just stays empty/stale if this fails
    }
  };

  useEffect(() => {
  const fetchConversations = async () => {
    try {
      const response = await api.get("/conversations");
      setConversations(response.data.conversations);
    } catch {
      // Silently ignore — sidebar just stays empty/stale if this fails
    }
  };

  fetchConversations();
}, []);

  const handleSelectConversation = async (id: string) => {
    setConversationId(id);
    setLoading(true);
    try {
      const response = await api.get(`/chat/${id}/history`);
      const loadedMessages: Message[] = response.data.messages.map(
        (m: { role: string; content: string }, index: number) => ({
          id: Date.now() + index,
          text: m.content,
          sender: m.role === "user" ? "user" : "assistant",
        })
      );
      setMessages(loadedMessages);
    } catch {
      setMessages([]);
    } finally {
      setLoading(false);
    }
  };

  const handleNewConversation = () => {
    setConversationId(undefined);
    setMessages([]);
  };

  const handleSend = async () => {
    if (!message.trim()) return;

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

      const assistantMessage: Message = {
        id: Date.now() + 1,
        text: response.data.reply,
        sender: "assistant",
      };

      setMessages((prev) => [...prev, assistantMessage]);
      setConversationId(response.data.conversation_id);

      // Refresh sidebar so a brand-new conversation shows up immediately
      loadConversations();
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
      <div className="sidebar">
        <div className="sidebar-header">
          <span>Conversations</span>
          <button className="new-chat-btn" onClick={handleNewConversation}>
            + New
          </button>
        </div>
        <div className="conversation-list">
          {conversations.length === 0 ? (
            <p className="no-conversations">No past conversations</p>
          ) : (
            conversations.map((conv) => (
              <div
                key={conv.conversation_id}
                className={
                  conv.conversation_id === conversationId
                    ? "conversation-item active"
                    : "conversation-item"
                }
                onClick={() => handleSelectConversation(conv.conversation_id)}
              >
                {conv.preview}
              </div>
            ))
          )}
        </div>
      </div>

      <div className="chat-container">
        <div className="header">
          <h1>SMART-SUPPORT-ASSISTANT</h1>
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