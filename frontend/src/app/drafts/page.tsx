"use client";

import { useEffect, useState } from "react";
import DashboardLayout from "@/components/layout/DashboardLayout";
import { approveDraft, getDrafts, rejectDraft, API_URL, type Draft } from "@/services/aiService";

function mediaUrl(path?: string) {
  if (!path) return null;
  const normalized = path.replaceAll("\\", "/");
  const marker = "/generated_reels/";
  const index = normalized.lastIndexOf(marker);
  return index >= 0 ? `${API_URL}/media/reels/${encodeURIComponent(normalized.slice(index + marker.length))}` : null;
}

export default function DraftsPage() {
  const [drafts, setDrafts] = useState<Draft[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [updatingId, setUpdatingId] = useState<number | null>(null);

  async function loadDrafts() { try { setError(null); setLoading(true); setDrafts(await getDrafts()); } catch (e) { setError(e instanceof Error ? e.message : "Could not load drafts."); } finally { setLoading(false); } }
  useEffect(() => { void loadDrafts(); }, []);
  async function updateDraft(id: number, action: "approve" | "reject") { try { setError(null); setUpdatingId(id); if (action === "approve") await approveDraft(id); else await rejectDraft(id); await loadDrafts(); } catch (e) { setError(e instanceof Error ? e.message : "Could not update draft."); } finally { setUpdatingId(null); } }

  return <DashboardLayout><div className="space-y-8">
    <div><p className="text-sm font-semibold uppercase tracking-[0.2em] text-indigo-400">Content operations</p><h1 className="mt-3 text-4xl font-bold text-white">Draft review</h1><p className="mt-2 text-zinc-400">Review AI-generated content and preview rendered Reels before anything is published or sent.</p></div>
    {error && <div className="rounded-2xl border border-red-500/30 bg-red-500/10 p-5 text-sm text-red-300">{error}<button type="button" onClick={() => void loadDrafts()} className="ml-4 underline">Try again</button></div>}
    {loading && <div className="rounded-3xl border border-zinc-800 bg-zinc-900 p-12 text-center"><div className="mx-auto h-8 w-8 animate-spin rounded-full border-2 border-zinc-700 border-t-indigo-400"/><p className="mt-5 text-sm text-zinc-300">Loading your drafts...</p></div>}
    {!loading && !error && drafts.length === 0 && <div className="rounded-3xl border border-dashed border-zinc-700 p-12 text-center"><p className="text-lg font-semibold text-zinc-300">No drafts yet</p><p className="mt-2 text-sm text-zinc-500">Create a mission or generate content in AI Studio.</p></div>}
    {!loading && drafts.length > 0 && <div className="space-y-5">{drafts.map(draft => { const validationPassed = draft.validation.valid !== false; const video = draft.content.media?.media_type === "video/mp4" ? mediaUrl(draft.content.media.media_path) : null; return <article key={draft.id} className="rounded-3xl border border-zinc-800 bg-zinc-900 p-6 transition hover:border-zinc-700">
      <div className="flex flex-wrap items-start justify-between gap-4"><div><div className="flex items-center gap-2"><span className="text-xs font-semibold uppercase tracking-wide text-indigo-300">{draft.platform}</span><span className="text-zinc-600">•</span><span className="text-xs uppercase tracking-wide text-zinc-500">{draft.language}</span></div><h2 className="mt-2 text-xl font-semibold text-white">{draft.title}</h2><p className="mt-1 text-xs text-zinc-600">Draft #{draft.id}</p></div><span className={`rounded-full px-3 py-1 text-xs font-semibold uppercase ${draft.status === "approved" ? "bg-emerald-500/10 text-emerald-400" : draft.status === "rejected" ? "bg-red-500/10 text-red-400" : "bg-amber-500/10 text-amber-400"}`}>{draft.status.replace("_", " ")}</span></div>
      {video && <div className="mt-6 max-w-sm overflow-hidden rounded-2xl border border-zinc-800 bg-black"><div className="border-b border-zinc-800 px-4 py-3 text-xs font-semibold uppercase tracking-wider text-indigo-300">Generated Reel · 1080×1920 · 30 FPS</div><video className="aspect-[9/16] w-full object-cover" controls preload="metadata" src={video}/><div className="px-4 py-3 text-xs text-amber-300">Rendered by CreatorOS · owner approval required before external use.</div></div>}
      <div className="mt-6 space-y-4">{draft.content.hook && <div><p className="mb-2 text-xs font-semibold uppercase tracking-[0.15em] text-indigo-400">Hook</p><div className="rounded-2xl bg-zinc-950 p-4 text-sm leading-6 text-zinc-200">{draft.content.hook}</div></div>}{draft.content.script && <div><p className="mb-2 text-xs font-semibold uppercase tracking-[0.15em] text-indigo-400">Script</p><div className="whitespace-pre-wrap rounded-2xl bg-zinc-950 p-4 text-sm leading-7 text-zinc-300">{draft.content.script}</div></div>}{draft.content.caption && <div><p className="mb-2 text-xs font-semibold uppercase tracking-[0.15em] text-indigo-400">Caption</p><div className="rounded-2xl bg-zinc-950 p-4 text-sm leading-6 text-zinc-300">{draft.content.caption}</div></div>}{draft.content.cta && <div><p className="mb-2 text-xs font-semibold uppercase tracking-[0.15em] text-indigo-400">Call to action</p><div className="rounded-2xl bg-zinc-950 p-4 text-sm font-medium text-zinc-200">{draft.content.cta}</div></div>}{draft.content.hashtags?.length ? <div className="flex flex-wrap gap-2">{draft.content.hashtags.map(h => <span key={h} className="rounded-lg bg-indigo-500/10 px-3 py-1 text-xs text-indigo-300">{h}</span>)}</div> : null}</div>
      <div className="mt-6 rounded-2xl border border-zinc-800 bg-zinc-950 p-4"><div className="flex flex-wrap items-center justify-between gap-3"><div><p className="text-xs font-semibold uppercase tracking-[0.15em] text-zinc-500">AI validation</p><p className={`mt-1 text-sm font-medium ${validationPassed ? "text-emerald-400" : "text-red-400"}`}>{validationPassed ? "✓ Validation passed" : "✕ Validation failed"}</p></div><div className="text-right"><p className="text-xs text-zinc-500">Quality score</p><p className="text-xl font-bold text-white">{draft.validation.quality_score ?? "—"}<span className="text-sm text-zinc-600">/100</span></p></div></div>{draft.validation.errors?.length ? <ul className="mt-3 list-disc space-y-1 pl-5 text-xs text-red-300">{draft.validation.errors.map(item => <li key={item}>{item}</li>)}</ul> : null}{draft.validation.warnings?.length ? <ul className="mt-3 list-disc space-y-1 pl-5 text-xs text-amber-300">{draft.validation.warnings.map(item => <li key={item}>{item}</li>)}</ul> : null}<p className="mt-3 text-xs text-zinc-600">Validated content still requires owner approval before publishing or external use.</p></div>
      <div className="mt-6 flex flex-wrap items-center justify-between gap-4"><div className="text-xs text-zinc-600">External actions remain approval-gated</div><div className="flex gap-3"><button type="button" onClick={() => void updateDraft(draft.id, "reject")} disabled={updatingId === draft.id || draft.status === "rejected"} className="rounded-xl border border-red-500/30 px-5 py-2.5 text-sm font-semibold text-red-300 hover:bg-red-500/10 disabled:opacity-40">{updatingId === draft.id ? "Updating..." : "Reject"}</button><button type="button" onClick={() => void updateDraft(draft.id, "approve")} disabled={updatingId === draft.id || draft.status === "approved" || !validationPassed} className="rounded-xl bg-emerald-600 px-5 py-2.5 text-sm font-semibold text-white hover:bg-emerald-500 disabled:opacity-40">{updatingId === draft.id ? "Updating..." : "Approve"}</button></div></div>
    </article>; })}</div>}
  </div></DashboardLayout>;
}
