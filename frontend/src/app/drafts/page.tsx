"use client";

import { useEffect, useState } from "react";
import DashboardLayout from "@/components/layout/DashboardLayout";
import { approveDraft, getDrafts, rejectDraft, type Draft } from "@/services/aiService";

export default function DraftsPage() {
  const [drafts, setDrafts] = useState<Draft[]>([]);
  const [error, setError] = useState<string | null>(null);

  function loadDrafts() {
    getDrafts().then(setDrafts).catch((requestError) => setError(requestError instanceof Error ? requestError.message : "Could not load drafts."));
  }

  useEffect(() => {
    getDrafts().then(setDrafts).catch((requestError) => setError(requestError instanceof Error ? requestError.message : "Could not load drafts."));
  }, []);

  async function updateDraft(id: number, action: "approve" | "reject") {
    try {
      if (action === "approve") await approveDraft(id);
      else await rejectDraft(id);
      loadDrafts();
    } catch (requestError) {
      setError(requestError instanceof Error ? requestError.message : "Could not update draft.");
    }
  }

  return (
    <DashboardLayout>
      <div className="space-y-8">
        <div><p className="text-sm font-semibold uppercase tracking-[0.2em] text-indigo-400">Content operations</p><h1 className="mt-3 text-4xl font-bold text-white">Draft review</h1><p className="mt-2 text-zinc-400">Approve claims and customer-facing content before publishing.</p></div>
        {error && <p className="rounded-xl border border-red-500/30 bg-red-500/10 p-4 text-sm text-red-300">{error}</p>}
        <div className="space-y-5">
          {drafts.length === 0 ? <div className="rounded-3xl border border-dashed border-zinc-700 p-12 text-center text-zinc-500">No drafts yet. Create one in AI Studio.</div> : drafts.map((draft) => <article key={draft.id} className="rounded-3xl border border-zinc-800 bg-zinc-900 p-6"><div className="flex flex-wrap items-start justify-between gap-4"><div><span className="text-xs uppercase tracking-wide text-indigo-300">{draft.platform} · {draft.language}</span><h2 className="mt-2 text-xl font-semibold text-white">{draft.title}</h2></div><span className="rounded-full bg-zinc-800 px-3 py-1 text-xs uppercase text-zinc-400">{draft.status}</span></div><div className="mt-5 whitespace-pre-wrap rounded-2xl bg-zinc-950 p-5 text-sm leading-7 text-zinc-300">{[draft.content.hook, draft.content.script, draft.content.caption, draft.content.cta].filter(Boolean).join("\n\n")}</div><div className="mt-5 flex flex-wrap items-center gap-3"><span className="text-sm text-zinc-500">Safety score: {draft.validation.quality_score ?? "—"}/100</span><button type="button" onClick={() => updateDraft(draft.id, "approve")} disabled={draft.status === "approved"} className="rounded-xl bg-emerald-600 px-4 py-2 text-sm font-semibold text-white disabled:opacity-50">Approve</button><button type="button" onClick={() => updateDraft(draft.id, "reject")} disabled={draft.status === "rejected"} className="rounded-xl border border-red-500/40 px-4 py-2 text-sm font-semibold text-red-300 disabled:opacity-50">Reject</button></div></article>)}
        </div>
      </div>
    </DashboardLayout>
  );
}
