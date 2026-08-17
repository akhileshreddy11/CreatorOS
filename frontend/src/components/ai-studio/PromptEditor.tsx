"use client";

import { usePrompt } from "@/context/PromptContext";

export default function PromptEditor() {
  const { prompt, setPrompt } = usePrompt();

  return (
    <section className="space-y-5">
      <div>
        <h2 className="text-2xl font-bold text-white">
          Prompt Editor
        </h2>

        <p className="mt-2 text-zinc-400">
          Describe exactly what you want the AI to create.
        </p>
      </div>

      <textarea
        rows={12}
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
        placeholder="Describe what you want to create..."
        className="w-full rounded-3xl border border-zinc-800 bg-zinc-900 p-6 text-white placeholder:text-zinc-500 outline-none transition focus:border-indigo-500"
      />

      <div className="flex items-center justify-between text-sm text-zinc-500">
        <span>💡 The more detailed your prompt, the better the AI output.</span>
        <span>{prompt.length} characters</span>
      </div>
    </section>
  );
}