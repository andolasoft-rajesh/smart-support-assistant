"use client";

import { useCallback, useEffect, useState } from "react";
import {
  Message,
  ChatResponse,
  UploadResponse,
  DocumentInfo,
  SummaryResponse,
} from "@/types";
import MessageList from "./MessageList";
import MessageInput from "./MessageInput";
import DocumentPanel from "./DocumentPanel";

const API_BASE_URL = "http://localhost:8000";

export default function ChatWindow() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState(false);
  const [conversationId, setConversationId] = useState<string | undefined>();
  const [error, setError] = useState<string | null>(null);

  // Day 16 feature state: the uploaded documents and the latest summary.
  const [documents, setDocuments] = useState<DocumentInfo[]>([]);
  const [summarizing, setSummarizing] = useState<string | null>(null);
  const [summary, setSummary] = useState<SummaryResponse | null>(null);
  const [summaryDoc, setSummaryDoc] = useState<string | null>(null);

  const refreshDocuments = useCallback(async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/documents`);
      if (!response.ok) return;
      setDocuments((await response.json()) as DocumentInfo[]);
    } catch (err) {
      // Non-fatal: the panel just stays empty if the list can't load.
      console.error("Failed to load documents:", err);
    }
  }, []);

  // Populate the document list on first render so previously-ingested docs
  // (e.g. the trainer's demo doc) show up without needing a fresh upload.
  // The fetch runs in an async IIFE so setState happens after the await
  // (never synchronously in the effect body), with a guard against setting
  // state after unmount.
  useEffect(() => {
    let cancelled = false;
    (async () => {
      try {
        const response = await fetch(`${API_BASE_URL}/documents`);
        if (cancelled || !response.ok) return;
        const data = (await response.json()) as DocumentInfo[];
        if (!cancelled) setDocuments(data);
      } catch (err) {
        console.error("Failed to load documents:", err);
      }
    })();
    return () => {
      cancelled = true;
    };
  }, []);

  const summarize = async (filename: string) => {
    try {
      setError(null);
      setSummarizing(filename);

      const response = await fetch(
        `${API_BASE_URL}/features/summarize?document=${encodeURIComponent(filename)}`,
        { method: "POST" }
      );

      if (!response.ok) {
        throw new Error(`Summarize failed (status ${response.status})`);
      }

      setSummary((await response.json()) as SummaryResponse);
      setSummaryDoc(filename);
    } catch (err) {
      const errorMessage =
        err instanceof Error ? err.message : "Failed to summarize document";
      setError(errorMessage);
      console.error("Summarize error:", err);
    } finally {
      setSummarizing(null);
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

      // Show the ingest result inline so the user knows the doc is now
      // searchable and how many chunks it produced.
      setMessages((m) => [
        ...m,
        {
          role: "assistant",
          content: `📎 Uploaded "${data.filename}" — indexed ${data.chunks} chunk${
            data.chunks === 1 ? "" : "s"
          }. You can now ask questions about it.`,
        },
      ]);

      // Reflect the new document in the panel so it can be summarized.
      await refreshDocuments();
    } catch (err) {
      const errorMessage =
        err instanceof Error ? err.message : "Failed to upload file";
      setError(errorMessage);
      console.error("Upload error:", err);
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

      {/* Documents + Summarize feature (Day 16) */}
      <DocumentPanel
        documents={documents}
        onSummarize={summarize}
        summarizing={summarizing}
        summary={summary}
        summaryDoc={summaryDoc}
        onCloseSummary={() => setSummary(null)}
      />

      {/* Message list */}
      <MessageList messages={messages} loading={loading} />

      {/* Input */}
      <MessageInput onSend={send} onUpload={upload} disabled={loading} />
    </div>
  );
}
