import { Message } from "@/types";
import { useEffect, useRef } from "react";

interface MessageListProps {
  messages: Message[];
  loading: boolean;
}

export default function MessageList({ messages, loading }: MessageListProps) {

  const bottomRef = useRef<HTMLDivElement>(null);

useEffect(() => {
  bottomRef.current?.scrollIntoView({ behavior: "smooth" });
}, [messages, loading]);
  return (
    <div className="flex-1 overflow-y-auto bg-slate-950 px-6 py-6 space-y-6">
      {messages.length === 0 && !loading && (
        <div className="flex items-center justify-center h-full text-slate-400">
  <div className="text-center">
    <div className="text-5xl mb-3">🤖</div>
    <p className="text-lg font-medium">
      Start chatting with Smart Support Assistant
    </p>
    <p className="text-sm mt-2 text-slate-500">
      Upload a PDF or TXT file, or simply ask a question.
    </p>
  </div>
</div>
      )}
      {messages.map((msg, idx) => (
        <div
          key={idx}
          className={`flex items-end gap-3 ${
          msg.role === "user" ? "justify-end" : "justify-start"
          }`}
        >
          <div ref={bottomRef} />
          <>
  {msg.role === "assistant" && (
    <div className="w-10 h-10 rounded-full bg-cyan-500 flex items-center justify-center text-white text-lg shadow-lg">
      🤖
    </div>
  )}

  <div
  className={`max-w-md lg:max-w-2xl px-5 py-3 rounded-3xl shadow-lg transition-all duration-300 hover:scale-[1.02] ${
    msg.role === "user"
      ? "bg-gradient-to-r from-blue-600 to-cyan-500 text-white rounded-br-md"
      : "bg-slate-800 text-gray-100 rounded-bl-md border border-slate-700"
  }`}
>
    <p className="text-[15px] leading-7 whitespace-pre-wrap">
      {msg.content}
    </p>
  </div>

  {msg.role === "user" && (
    <div className="w-10 h-10 rounded-full bg-indigo-600 flex items-center justify-center text-white text-lg shadow-lg">
      👤
    </div>
  )}
</>
        </div>
      ))}
      {loading && (
        <div className="flex items-end gap-3">
  <div className="w-10 h-10 rounded-full bg-cyan-500 flex items-center justify-center text-white">
    🤖
  </div>

  <div className="bg-slate-800 border border-slate-700 px-5 py-3 rounded-3xl">
    <div className="flex gap-2">
      <span className="w-2 h-2 bg-cyan-400 rounded-full animate-bounce"></span>
      <span className="w-2 h-2 bg-cyan-400 rounded-full animate-bounce delay-150"></span>
      <span className="w-2 h-2 bg-cyan-400 rounded-full animate-bounce delay-300"></span>
    </div>
  </div>
</div>
      )}
    </div>
  );
}
