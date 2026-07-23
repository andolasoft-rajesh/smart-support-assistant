interface ChatItem {
  id: string;
  title: string;
}

interface Props {
  chats: ChatItem[];
  selectedId?: string;
  onSelect: (id: string) => void;
}

export default function ChatHistory({
  chats,
  selectedId,
  onSelect,
}: Props) {
  return (
    <div className="w-64 bg-slate-900 border-r border-slate-800 flex flex-col">

      <div className="p-4 border-b border-slate-800">
        <h2 className="text-lg font-semibold text-white">
          💬 Chats
        </h2>
      </div>

      <div className="flex-1 overflow-y-auto p-2 space-y-2">
        {chats.map((chat) => (
          <button
            key={chat.id}
            onClick={() => onSelect(chat.id)}
            className={`w-full text-left p-3 rounded-xl transition ${
              selectedId === chat.id
                ? "bg-cyan-600 text-white"
                : "bg-slate-800 hover:bg-slate-700 text-gray-300"
            }`}
          >
            <div className="text-sm font-medium truncate">
              {chat.title}
            </div>
          </button>
        ))}
      </div>
    </div>
  );
}