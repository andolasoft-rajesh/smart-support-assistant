"use client";

import { useRef, useState } from "react";

interface MessageInputProps {
  onSend: (message: string) => void;
  onUpload: (file: File) => void;
  onSummary: () => void;
  disabled: boolean;
}

  export default function MessageInput({
    onSend,
    onUpload,
    onSummary,
    disabled,
}: MessageInputProps){
  const [input, setInput] = useState("");
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleSend = () => {
    if (input.trim()) {
      onSend(input);
      setInput("");
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      onUpload(file);
    }
    // Reset so selecting the same file again re-fires onChange.
    e.target.value = "";
  };

  return (
    <div className="p-4 border-t border-slate-700 bg-slate-900">
      <div className="flex gap-2">
        <input
          ref={fileInputRef}
          type="file"
          accept=".pdf,.txt,.md"
          onChange={handleFileChange}
          disabled={disabled}
          className="hidden"
        />
        <button
           onClick={() => fileInputRef.current?.click()}
          disabled={disabled}
          title="Upload a document"
          aria-label="Upload a document"
          className="px-3 py-2 border border-gray-300 rounded-lg text-gray-600 hover:bg-gray-100 disabled:bg-gray-100 disabled:cursor-not-allowed transition-colors"
        >
          📎
        </button>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Type your message..."
          disabled={disabled}
          className="flex-1 px-5 py-3 bg-slate-800 border border-slate-700 rounded-full text-white placeholder:text-gray-400 focus:outline-none focus:ring-2 focus:ring-cyan-500 focus:border-cyan-500 transition-all duration-300 disabled:opacity-50"
        />
        <button
          onClick={handleSend}
          disabled={disabled || !input.trim()}
          className="px-6 py-3 rounded-full bg-gradient-to-r from-cyan-500 to-blue-600 text-white font-medium hover:scale-105 hover:shadow-lg transition-all duration-300 disabled:opacity-50 disabled:hover:scale-100"
        >
          Send
        </button>

        <button
          onClick={onSummary}
          disabled={disabled}
          className="px-6 py-3 rounded-full bg-green-600 text-white hover:bg-green-700"
        >
          Summarize
        </button>
      </div>
    </div>
  );
}
