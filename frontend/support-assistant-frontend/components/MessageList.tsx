import { Message } from "@/types";

interface MessageListProps {
  messages: Message[];
  loading: boolean;
}

export default function MessageList({ messages, loading }: MessageListProps) {
  return (
    <div className="flex-1 overflow-y-auto p-4 space-y-4">
      {messages.length === 0 && !loading && (
        <div className="flex items-center justify-center h-full text-gray-500">
          <p>Start a conversation by sending a message...</p>
        </div>
      )}
      {messages.map((msg, idx) => (
        <div
          key={idx}
          className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}
        >
          <div
            className={`max-w-xs lg:max-w-md px-4 py-2 rounded-lg ${
              msg.role === "user"
                ? "bg-blue-500 text-white rounded-br-none"
                : "bg-gray-200 text-gray-900 rounded-bl-none"
            }`}
          >
            <p className="text-sm">{msg.content}</p>
          </div>
        </div>
      ))}
      {loading && (
        <div className="flex justify-start">
          <div className="bg-gray-200 text-gray-900 px-4 py-2 rounded-lg rounded-bl-none">
            <p className="text-sm">Assistant is typing...</p>
          </div>
        </div>
      )}
    </div>
  );
}
