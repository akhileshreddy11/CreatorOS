"use client";

import { useEffect, useState } from "react";
import { FileText } from "lucide-react";
import { getDrafts, type Draft } from "@/services/aiService";

export default function HistoryPanel() {
  const [drafts, setDrafts] = useState<Draft[]>([]);

  useEffect(() => {
    getDrafts().then(setDrafts).catch(() => setDrafts([]));
  }, []);

  return (
    <section className="rounded-3xl border border-zinc-800 bg-zinc-900 p-6">
      <div className="flex items-center gap-3"><FileText className="text-indigo-400" size={19} /><h2 className="text-xl font-bold text-white">Draft history</h2></div>
      <div className="mt-5 space-y-3">
        {drafts.length === 0 ? <p className="text-sm text-zinc-500">Generated drafts will be saved here.</p> : drafts.slice(0, 6).map((draft) => <div key={draft.id} className="flex items-center justify-between gap-3 rounded-xl bg-zinc-950 p-3"><span className="truncate text-sm text-zinc-300">{draft.title}</span><span className="text-xs uppercase text-zinc-500">{draft.status}</span></div>)}
      </div>
    </section>
  );
}
