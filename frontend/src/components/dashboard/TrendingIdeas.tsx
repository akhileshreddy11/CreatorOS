"use client";

import { useEffect, useState } from "react";
import { ArrowUpRight, Lightbulb } from "lucide-react";
import { getTrends } from "@/services/aiService";

export default function TrendingIdeas() {
  const [ideas, setIdeas] = useState<Array<{ title: string; angle: string; status: string }>>([]);

  useEffect(() => {
    getTrends().then(setIdeas).catch(() => setIdeas([]));
  }, []);

  return (
    <section className="rounded-3xl border border-zinc-800 bg-zinc-900 p-6">
      <div className="flex items-center justify-between">
        <div><h2 className="text-xl font-bold text-white">Local content angles</h2><p className="mt-1 text-sm text-zinc-500">Ideas are starting points, not live trend guarantees.</p></div>
        <Lightbulb className="text-amber-300" size={20} />
      </div>
      <div className="mt-6 space-y-3">
        {ideas.map((idea) => (
          <div key={idea.title} className="group rounded-2xl border border-zinc-800 bg-zinc-950 p-4 transition hover:border-indigo-500">
            <div className="flex items-start justify-between gap-3"><h3 className="font-semibold text-zinc-100">{idea.title}</h3><ArrowUpRight className="text-zinc-600 transition group-hover:text-indigo-300" size={17} /></div>
            <p className="mt-2 text-sm leading-6 text-zinc-400">{idea.angle}</p>
          </div>
        ))}
        {ideas.length === 0 && <p className="rounded-2xl border border-dashed border-zinc-700 p-4 text-sm text-zinc-500">Start the backend to load local content ideas.</p>}
      </div>
    </section>
  );
}
