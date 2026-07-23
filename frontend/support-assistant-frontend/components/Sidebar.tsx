interface SidebarProps {
  documents: string[];
  selected: string;
  onSelect: (doc: string) => void;
}

export default function Sidebar({
  documents,
  selected,
  onSelect,
}: SidebarProps) {
  return (
    <div className="w-72 bg-slate-900 border-r border-slate-800 flex flex-col">

      <div className="p-5 border-b border-slate-800">
        <h2 className="text-xl font-bold text-white">
          📂 Documents
        </h2>
      </div>

      <div className="flex-1 overflow-y-auto p-3">

        {documents.length === 0 ? (
          <p className="text-slate-500 text-sm">
            No document uploaded
          </p>
        ) : (
          documents.map((doc) => (
            <button
              key={doc}
              onClick={() => onSelect(doc)}
              className={`w-full text-left p-3 rounded-xl mb-2 transition
              ${
                selected === doc
                  ? "bg-cyan-600 text-white"
                  : "bg-slate-800 hover:bg-slate-700 text-gray-300"
              }`}
            >
              📄 {doc}
            </button>
          ))
        )}

      </div>
    </div>
  );
}