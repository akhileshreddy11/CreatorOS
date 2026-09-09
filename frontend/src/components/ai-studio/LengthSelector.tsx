"use client";

import { usePrompt } from "@/context/PromptContext";

export default function LengthSelector() {
  const { length, setLength } = usePrompt();

  return (
    <section className="space-y-3">
      <label htmlFor="content-length" className="text-lg font-semibold text-white">
        Content Length
      </label>

      <select
        id="content-length"
        value={length}
        onChange={(event) => setLength(event.target.value)}
        className="h-14 w-full rounded-2xl border border-zinc-800 bg-zinc-900 px-4 text-white outline-none transition focus:border-indigo-500"
      >
        <option value="Short">Short (100–200 words)</option>
        <option value="Medium">Medium (300–600 words)</option>
        <option value="Long">Long (700–1200 words)</option>
        <option value="Detailed">Detailed (1500+ words)</option>
      </select>
    </section>
  );
}
