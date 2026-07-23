"use client";

import { useEffect, useState } from "react";
import { Message, ChatResponse, UploadResponse } from "@/types";
import MessageList from "./MessageList";
import MessageInput from "./MessageInput";
import Sidebar from "./Sidebar";
import ChatHistory from "./ChatHistory";


const API_BASE_URL = "http://localhost:8000";

export default function ChatWindow() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState(false);
  const [conversationId, setConversationId] = useState<string | undefined>();
  const [error, setError] = useState<string | null>(null);
  const [uploadedDocument, setUploadedDocument] = useState("");
  const [documents, setDocuments] = useState<string[]>([]); 
  const [chats, setChats] = useState<{ id: string; title: string }[]>([]);
  const [showSidebar, setShowSidebar] = useState(true);
  

  const loadChats = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/conversations`);

    console.log(response.status);

    if (!response.ok) {
      throw new Error("Failed to load conversations");
    }

    const data = await response.json();

    console.log(data);

    setChats(data);
  } catch (err) {
    console.error(err);
  }
};

  const loadConversation = async (id: string) => {
    try {
      const response = await fetch(`${API_BASE_URL}/chat/${id}`);

      if (!response.ok) return;

      const data = await response.json();

      setConversationId(id);
      setMessages(data);
      } catch (err) {
      console.error(err);
    }
  };

  const loadDocuments = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/documents`);

    console.log(response.status);

    if (!response.ok)
      throw new Error("Failed to load documents");

    const docs = await response.json();

    console.log(docs);

    setDocuments(docs.map((d:any)=>d.filename));

    if(docs.length>0){
      setUploadedDocument(docs[0].filename);
    }

  } catch(err){
    console.error(err);
  }
};
  
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

      await loadChats();

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

  const upload = async (file: File) => {
  try {
    setError(null);
    setLoading(true);

    const formData = new FormData();
    formData.append("file", file);

    const response = await fetch(`${API_BASE_URL}/documents/upload`, {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      throw new Error(`Upload failed (status ${response.status})`);
    }

    const data: UploadResponse = await response.json();

    setUploadedDocument(data.filename);

    // Reload all documents from the backend
    await loadDocuments();

    setMessages((m) => [
    ...m,
  {
    role: "user",
    content: `📎 Uploaded: ${data.filename}`,
  },
  {
    role: "assistant",
    content: `Document uploaded successfully and indexed into ${data.chunks} chunks. You can now ask questions or click "Summarize".`,
  },
]);
  } catch (err) {
    const errorMessage =
      err instanceof Error ? err.message : "Failed to upload file";
    setError(errorMessage);
    console.error("Upload error:", err);
  } finally {
    setLoading(false);
  }
};
  
  const summarizeDocument = async () => {
    try {
      setError(null);
      setLoading(true);

      const response = await fetch(`${API_BASE_URL}/features/summary`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ document: uploadedDocument }),
      });

      if (!response.ok) {
        throw new Error("Failed to summarize document");
      }

      const data = await response.json();

      setMessages((m) => [
        ...m,
        {
          role: "assistant",
          content:
          `📄 Summary

            ${data.summary}

          🔹KEY POINTS
            • ${data.key_points.join("\n• ")}`,
        },
      ]);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Summary failed");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadDocuments();
    loadChats();
  }, []);

  return (
  <div className="flex h-screen bg-slate-950">

  {showSidebar && (
  <>
    <Sidebar
      documents={documents}
      selected={uploadedDocument}
      onSelect={setUploadedDocument}
    />

    <ChatHistory
      chats={chats}
      selectedId={conversationId}
      onSelect={loadConversation}
    />
  </>
)}

    {/* Chat Area */}
    <div className="flex flex-col flex-1">
      <div className="flex flex-col h-screen bg-slate-950 text-white">

      <div className="bg-gradient-to-r from-indigo-600 via-blue-600 to-cyan-500 shadow-xl px-6 py-3 flex items-center justify-between">

    {/* Left */}
    <button
  onClick={() => setShowSidebar(!showSidebar)}
  className="p-2 rounded-lg hover:bg-white/10 transition"
  >
  <span className="text-2xl">☰</span>
  </button>

    {/* Center */}
    <div className="text-center">
    <h1 className="text-xl font-semibold">
      Smart Support Assistant
    </h1>

    {uploadedDocument && (
      <p className="text-sm text-cyan-100">
        📄 {uploadedDocument}
      </p>
    )}
    </div>

    {/* Right */}
    <div className="flex items-center gap-3">

  </div>

  </div>


      {/* Error */}
      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3">
          <p className="text-sm">{error}</p>
        </div>
      )}

      {/* Messages */}
      <MessageList
        messages={messages}
        loading={loading}
      />

      {/* Input */}
      <MessageInput
        onSend={send}
        onUpload={upload}
        onSummary={summarizeDocument}
        disabled={loading}
      />

    </div>

  </div>

  </div>
);

}