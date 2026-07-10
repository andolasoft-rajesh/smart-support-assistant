"use client";

import { DocumentInfo, SummaryResponse } from "@/types";

interface DocumentPanelProps {
  documents: DocumentInfo[];
  onSummarize: (filename: string) => void;
  summarizing: string | null;
  summary: SummaryResponse | null;
  summaryDoc: string | null;
  onCloseSummary: () => void;
}

// Day 16 feature UI: lists the uploaded documents and puts a "Summarize"
// button next to each. Clicking one calls POST /features/summarize and the
// returned key_points render as a bullet list — the whole feature loop.
export default function DocumentPanel({
  documents,
  onSummarize,
  summarizing,
  summary,
  summaryDoc,
  onCloseSummary,
}: DocumentPanelProps) {
  if (documents.length === 0) return null;

  return (
    <div className="border-b border-gray-300 bg-gray-50 p-3">
      <p className="mb-2 text-xs font-semibold uppercase tracking-wide text-gray-500">
        Documents
      </p>

      <ul className="space-y-1">
        {documents.map((doc) => (
          <li
            key={doc.filename}
            className="flex items-center justify-between gap-3 rounded bg-white px-3 py-1.5 text-sm text-gray-800 shadow-sm"
          >
            <span className="truncate" title={doc.filename}>
              {doc.filename}{" "}
              <span className="text-gray-400">
                ({doc.chunks} chunk{doc.chunks === 1 ? "" : "s"})
              </span>
            </span>
            <button
              onClick={() => onSummarize(doc.filename)}
              disabled={summarizing !== null}
              className="shrink-0 rounded border border-blue-500 px-2 py-1 text-xs text-blue-600 hover:bg-blue-50 disabled:cursor-not-allowed disabled:opacity-50"
            >
              {summarizing === doc.filename ? "Summarizing…" : "Summarize"}
            </button>
          </li>
        ))}
      </ul>

      {summary && (
        <div className="mt-3 rounded border border-blue-200 bg-white p-3">
          <div className="mb-1 flex items-start justify-between gap-2">
            <p className="text-xs font-semibold text-gray-500">
              Summary — {summaryDoc}
            </p>
            <button
              onClick={onCloseSummary}
              aria-label="Dismiss summary"
              className="text-gray-400 hover:text-gray-600"
            >
              ✕
            </button>
          </div>

          <p className="mb-2 text-sm text-gray-800">{summary.summary}</p>

          {summary.key_points.length > 0 && (
            <ul className="list-disc space-y-0.5 pl-5 text-sm text-gray-700">
              {summary.key_points.map((point, idx) => (
                <li key={idx}>{point}</li>
              ))}
            </ul>
          )}
        </div>
      )}
    </div>
  );
}
