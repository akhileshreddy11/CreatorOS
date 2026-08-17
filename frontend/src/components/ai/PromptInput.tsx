"use client";

import { Input } from "@/components/ui/input";

export default function PromptInput() {
  return (
    <div className="space-y-3">
      <label htmlFor="command-prompt" className="text-sm font-medium text-zinc-300">What do you want to create?</label>
      <Input id="command-prompt" placeholder="Example: Explain a beginner trial class at a Hyderabad gym…" className="h-14 rounded-xl border-zinc-700 bg-zinc-950 text-white" />
    </div>
  );
}
