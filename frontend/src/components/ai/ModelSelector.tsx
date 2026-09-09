"use client";

export default function ModelSelector() {
  return (
    <div className="space-y-3">
      <label htmlFor="ai-model" className="text-sm font-medium text-zinc-300">AI provider</label>
      <select id="ai-model" disabled className="h-14 w-full rounded-xl border border-zinc-700 bg-zinc-950 px-4 text-white outline-none disabled:cursor-not-allowed disabled:opacity-80">
        <option>Gemini (configured backend provider)</option>
      </select>
      <p className="text-xs text-zinc-500">Provider changes belong in backend configuration, never in customer-facing drafts.</p>
    </div>
  );
}
