"use client";

type OutputPanelProps = {
  content?: string;
  status?: string;
  message?: string;
};

export default function OutputPanel({ content, status, message }: OutputPanelProps) {
  return (
    <div className="rounded-3xl border border-zinc-800 bg-zinc-900 p-6">
      <div className="flex items-center justify-between gap-3">
        <h2 className="text-xl font-bold text-white">Generated output</h2>
        {status && <span className="rounded-full bg-amber-500/15 px-3 py-1 text-xs uppercase tracking-wide text-amber-300">{status}</span>}
      </div>
      <div className="mt-5 min-h-48 whitespace-pre-wrap rounded-2xl border border-zinc-800 bg-zinc-950 p-5 text-sm leading-7 text-zinc-300">
        {content || message || "Your reviewable draft will appear here."}
      </div>
    </div>
  );
}
