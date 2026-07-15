import { useState, useEffect, type ChangeEvent, type MouseEvent } from "react";
import "./App.css";
import api from "./services/api";
import type { Message } from "./types/message";
import type { ConversationSummary } from "./types/chat";

interface DocumentInfo {
  document: string;
  chunk_count: number;
}

function App() {
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [conversationId, setConversationId] = useState<string>();
  const [conversations, setConversations] = useState<ConversationSummary[]>([]);
  const [documents, setDocuments] = useState<DocumentInfo[]>([]);

  // --- NEW: Summarizer State ---
  const [summarizingDoc, setSummarizingDoc] = useState<string | null>(null);
  const [activeSummary, setActiveSummary] = useState<{
    document: string;
    summary: string;
    key_points: string[];
  } | null>(null);

  const fetchData = async () => {
    try {
      const [convRes, docRes] = await Promise.all([
        api.get("/conversations"),
        api.get("/documents")
      ]);
      setConversations(convRes.data.conversations);
      setDocuments(docRes.data.documents);
    } catch (error) {
      console.error("Failed to load initial data", error);
    }
  };

  useEffect(() => {
    const load = async () => {
      await fetchData();
    };

    void load();
  }, []);

  const handleFileUpload = async (e: ChangeEvent<HTMLInputElement>) => {
    if (!e.target.files || e.target.files.length === 0) return;
    setUploading(true);
    const formData = new FormData();
    for (let i = 0; i < e.target.files.length; i++) {
      formData.append("files", e.target.files[i]);
    }

    try {
      await api.post("/documents/upload_multiple", formData, {
        headers: { "Content-Type": "multipart/form-data" }
      });
      void fetchData(); // Refresh document list
    } catch (_err) {
      const error = _err instanceof Error ? _err : new Error("Upload failed");
      console.error(error);
      alert("Error uploading files.");
    } finally {
      setUploading(false);
      if (e.target) e.target.value = '';
    }
  };

  // --- NEW: Summarize Function ---
  const handleSummarize = async (documentName: string) => {
    // If it's already open, close it!
    if (activeSummary?.document === documentName) {
      setActiveSummary(null);
      return;
    }

    setSummarizingDoc(documentName);
    try {
      // Calls the new /features/summarize endpoint
      const response = await api.post(`/features/summarize?document=${encodeURIComponent(documentName)}`);
      setActiveSummary({
        document: documentName,
        summary: response.data.summary,
        key_points: response.data.key_points,
      });
    } catch (err: unknown) {
      const error = err as { response?: { status?: number } };
      const status = error.response?.status;
      if (status === 502) {
        alert("Summarization failed (502): The AI returned malformed data.");
      } else {
        alert("Failed to summarize the document.");
      }
    } finally {
      setSummarizingDoc(null);
    }
  };

  // --- NEW: Delete Document Handler ---
  const handleDeleteDocument = async (documentName: string) => {
    if (!window.confirm(`Are you sure you want to delete "${documentName}"? The AI will forget its contents.`)) return;

    try {
      await api.delete(`/documents/${documentName}`);
      fetchData(); // Refresh the sidebar list!
    } catch (error) {
      alert("Failed to delete document.");
      console.error(error);
    }
  };

  const handleSelectConversation = async (id: string) => {
    setLoading(true);
    try {
      const response = await api.get(`/chat/${id}/history`);
      const loadedMessages = response.data.messages.map((msg: { role: string; content: string }, idx: number) => ({
        id: idx,
        text: msg.content,
        sender: msg.role === "assistant" ? "assistant" : "user",
      }));
      setConversationId(id);
      setMessages(loadedMessages);
    } catch (_err) {
      const error = _err instanceof Error ? _err : new Error("Failed to load history");
      console.error(error);
      alert("Unable to load conversation history.");
    } finally {
      setLoading(false);
    }
  };

  const handleNewConversation = () => {
    setConversationId(undefined);
    setMessages([]);
    setMessage("");
  };

  const handleSend = async () => {
    const trimmed = message.trim();
    if (!trimmed) return;

    setLoading(true);
    try {
      const response = await api.post("/chat", {
        conversation_id: conversationId,
        message: trimmed,
      });

      const reply = response.data.reply as string;
      const createdId = response.data.conversation_id as string;

      setMessages((prev) => [
        ...prev,
        { id: Date.now(), text: trimmed, sender: "user" },
        { id: Date.now() + 1, text: reply, sender: "assistant" },
      ]);
      setMessage("");
      setConversationId(createdId);
      void fetchData();
    } catch (err) {
      const axiosError = err as { response?: { status?: number }; message?: string };
      const status = axiosError.response?.status;
      const statusSuffix = status ? ` (HTTP ${status})` : "";

      let errorText: string;
      if (status === 503) {
        errorText = `AI Service is unavailable. Check API Key.${statusSuffix}`;
      } else if (status === 500) {
        errorText = `Backend database error occurred. Please try again.${statusSuffix}`;
      } else if (axiosError.message) {
        errorText = `Unable to reach the backend server. ${axiosError.message}${statusSuffix}`;
      } else {
        errorText = `Unable to reach the backend server. Please make sure Uvicorn is running!${statusSuffix}`;
      }

      const errorMessage: Message = {
        id: Date.now() + 1,
        text: errorText,
        sender: "assistant",
      };

      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteConversation = async (e: MouseEvent<HTMLButtonElement>, id: string) => {
    e.stopPropagation();

    if (!window.confirm("Delete this conversation?")) {
      return;
    }

    try {
      await api.delete(`/chat/${id}`);
      setConversations((current) => current.filter((conv) => conv.conversation_id !== id));

      if (conversationId === id) {
        setConversationId(undefined);
        setMessages([]);
      }
    } catch (_err) {
      const error = _err instanceof Error ? _err : new Error("Delete failed");
      console.error(error);
      alert("Unable to delete conversation.");
    }
  };

  return (
    <div className="app">
      <div className="sidebar">
        <div className="sidebar-header">
          <span>Conversations</span>
          <button className="new-chat-btn" onClick={handleNewConversation}>+ New</button>
        </div>

        <div className="upload-section">
          <label className="upload-btn">
            {uploading ? "Uploading..." : "📄 Upload Documents"}
            <input type="file" multiple accept=".pdf,.txt" onChange={handleFileUpload} disabled={uploading} style={{ display: 'none' }} />
          </label>
        </div>

        {/* --- NEW: Document List with Summarize --- */}
        <div className="documents-list">
          {documents.map((doc) => (
            <div key={doc.document} className="document-item-wrapper">
              
              {/* The Document Row */}
              <div className="document-row">
                <span className="document-title">{doc.document}</span>
                <div style={{ display: 'flex', gap: '6px' }}>
                  <button 
                    className="summarize-btn"
                    onClick={() => handleSummarize(doc.document)}
                    disabled={summarizingDoc === doc.document}
                  >
                    {summarizingDoc === doc.document ? "..." : "Summarize"}
                  </button>
                  <button 
                    onClick={() => handleDeleteDocument(doc.document)}
                    className="doc-delete-btn"
                    title="Delete Document"
                  >
                    Delete
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>

        <div className="conversation-list">
          {conversations.length === 0 ? <p className="no-conversations">No past conversations</p> : 
            conversations.map((conv) => (
              <div
                key={conv.conversation_id}
                className={`conversation-item ${conv.conversation_id === conversationId ? "active" : ""}`}
                onClick={() => handleSelectConversation(conv.conversation_id)}
              >
                <span className="conversation-preview">{conv.preview}</span>
                <button
                  className="delete-btn"
                  onClick={(e) => handleDeleteConversation(e, conv.conversation_id)}
                  aria-label="Delete conversation"
                >
                  ×
                </button>
              </div>
            ))
          }
        </div>
      </div>

      <div className="chat-container" style={{ position: 'relative' }}>
        <div className="header">
          <h1>SMART-SUPPORT-ASSISTANT</h1>
        </div>

        <div style={{ display: 'flex', flex: 1, overflow: 'hidden' }}>
          <div className="messages" style={{ flex: 1, minWidth: 0 }}>
            {loading && messages.length === 0 ? (
              <p>Loading conversation…</p>
            ) : messages.length === 0 ? (
              <p>No messages yet.</p>
            ) : (
              messages.map((msg) => (
                <div key={msg.id} className={`message ${msg.sender}`}>
                  {msg.text}
                </div>
              ))
            )}
          </div>

          {/* --- NEW: Scrollable Side Panel for Summary --- */}
          {activeSummary && (
            <div className="summary-panel">
              <div className="summary-panel-header">
                <h2>Summary — {activeSummary.document}</h2>
                <button className="close-summary-btn" onClick={() => setActiveSummary(null)}>×</button>
              </div>
              <div className="summary-panel-body">
                <p>{activeSummary.summary}</p>
                <ul>
                  {activeSummary.key_points.map((point, index) => (
                    <li key={index}>{point}</li>
                  ))}
                </ul>
              </div>
            </div>
          )}
        </div>
        

        <div className="input-area">
          <input
            type="text"
            placeholder="Ask your assistant something..."
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter") {
                e.preventDefault();
                handleSend();
              }
            }}
            disabled={loading}
          />
          <button onClick={handleSend} disabled={loading || message.trim() === ""}>
            {loading ? "Sending…" : "Send"}
          </button>
        </div>
      </div>
    </div>
  );
}

export default App;