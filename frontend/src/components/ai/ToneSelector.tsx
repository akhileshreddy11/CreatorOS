"use client";

import { usePrompt } from "@/context/PromptContext";

export default function ToneSelector() {
  const { tone, setTone } = usePrompt();
  return <div className="space-y-3"><label htmlFor="tone" className="text-sm font-medium text-zinc-300">Tone</label><select id="tone" value={tone} onChange={(event) => setTone(event.target.value)} className="h-14 w-full rounded-xl border border-zinc-700 bg-zinc-950 px-4 text-white outline-none"><option>Helpful and local</option><option>Direct and energetic</option><option>Warm and encouraging</option></select></div>;
}
