"use client";

import { useEffect, useRef, useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { AlertTriangle, ArrowRight, CheckCircle2, ChevronRight, Flame, Layers, RefreshCw, Shield, ShieldAlert, ShieldCheck, Sparkles, Target, TrendingUp, XCircle } from "lucide-react";
import DashboardLayout from "@/components/layout/DashboardLayout";
import { approveMission, getMorningBrief, refreshMorningBrief, rejectMission, type BriefData, type MissionStartResponse, type MorningBriefResponse, type Opportunity, type RankedNiche } from "@/services/aiService";

function scoreColor(score?: number) { if (score === undefined || score === null) return "text-zinc-500"; if (score >= 80) return "text-emerald-400"; if (score >= 60) return "text-amber-400"; return "text-red-400"; }
function scoreBg(score?: number) { if (score === undefined || score === null) return "bg-zinc-800/40 border-zinc-700/40"; if (score >= 80) return "bg-emerald-500/10 border-emerald-500/30 text-emerald-300"; if (score >= 60) return "bg-amber-500/10 border-amber-500/30 text-amber-300"; return "bg-red-500/10 border-red-500/30 text-red-300"; }
function formatScore(score?: number) { return score === undefined || score === null ? "—" : score; }

export default function OpportunitiesPage() {
  const router = useRouter();
  const [briefResponse, setBriefResponse] = useState<MorningBriefResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [approving, setApproving] = useState(false);
  const [rejecting, setRejecting] = useState(false);
  const [missionResult, setMissionResult] = useState<MissionStartResponse | null>(null);
  const [actionNotice, setActionNotice] = useState<string | null>(null);
  const [isReviewOpen, setIsReviewOpen] = useState(false);
  const pollingRef = useRef<NodeJS.Timeout | null>(null);

  async function checkBriefStatus(triggerRefresh = false) { try { if (triggerRefresh) { setLoading(true); setError(null); const refreshRes = await refreshMorningBrief(); setBriefResponse(refreshRes); } else { const res = await getMorningBrief(); setBriefResponse(res); if (res.status === "READY") setLoading(false); else if (res.status === "FAILED") { setLoading(false); setError(res.error || "COO morning brief failed to generate."); } } } catch (err) { setError(err instanceof Error ? err.message : "Could not connect to CreatorOS backend."); setLoading(false); } }
  useEffect(() => { void checkBriefStatus(); return () => { if (pollingRef.current) clearInterval(pollingRef.current); }; }, []);
  useEffect(() => { if (briefResponse?.status === "STARTED" || briefResponse?.status === "RUNNING") { setLoading(true); if (!pollingRef.current) pollingRef.current = setInterval(() => void checkBriefStatus(), 3000); } else { if (pollingRef.current) { clearInterval(pollingRef.current); pollingRef.current = null; } setLoading(false); } return () => { if (pollingRef.current && briefResponse?.status !== "STARTED" && briefResponse?.status !== "RUNNING") { clearInterval(pollingRef.current); pollingRef.current = null; } }; }, [briefResponse?.status]);

  const brief: BriefData | undefined = briefResponse?.brief;
  const rankedNiches: RankedNiche[] = brief?.niche_ranking?.ranked_niches ?? brief?.niche_research?.ranked_niches ?? [];
  const selectedNiche: RankedNiche | null = brief?.selected_niche ?? brief?.niche_ranking?.best_niche ?? brief?.niche_research?.best_niche ?? (rankedNiches.length > 0 ? rankedNiches[0] : null);
  const opportunities: Opportunity[] = brief?.opportunity_generation?.opportunities ?? [];
  const selectedOpportunity: Opportunity | null = brief?.selected_opportunity ?? brief?.opportunity_generation?.best_opportunity ?? (opportunities.length > 0 ? opportunities[0] : null);
  const evaluation = brief?.coo_evaluation;
  const safety = brief?.safety_review;
  const trend = brief?.trend_opportunity;

  async function handleCEOApprove() {
    if (!selectedOpportunity) return;
    try {
      setApproving(true); setError(null); setActionNotice(null);
      const result = await approveMission({ topic: selectedOpportunity.topic || "Hyderabad Gym Campaign", problem: selectedOpportunity.problem || "", audience: selectedOpportunity.audience || ["Gym owners", "Local adults"], strategy: selectedOpportunity.strategy || "", recommended_content: selectedOpportunity.recommended_content || [], product_idea: selectedOpportunity.product_idea || "" });
      setMissionResult(result);
      window.localStorage.setItem("creatoros:lastMissionJob", result.job_id);
      setActionNotice("Opportunity approved. Mission execution has started; validated Reel and campaign artifacts will appear in Mission Control as they are generated.");
    } catch (err) { setError(err instanceof Error ? err.message : "Failed to start mission."); }
    finally { setApproving(false); }
  }

  async function handleCEOReject() { if (!selectedOpportunity) return; try { setRejecting(true); setError(null); setActionNotice(null); const result = await rejectMission({ topic: selectedOpportunity.topic || "Hyderabad Gym Campaign", problem: selectedOpportunity.problem || "", audience: selectedOpportunity.audience || [], strategy: selectedOpportunity.strategy || "", recommended_content: selectedOpportunity.recommended_content || [], product_idea: selectedOpportunity.product_idea || "" }); setActionNotice(result.message || "Opportunity rejected by CEO."); } catch (err) { setError(err instanceof Error ? err.message : "Failed to reject opportunity."); } finally { setRejecting(false); } }

  return (
    <DashboardLayout>
      <div className="space-y-8">
        <div className="flex flex-wrap items-end justify-between gap-5"><div><div className="flex items-center gap-2 text-sm font-semibold uppercase tracking-[0.2em] text-indigo-400"><Sparkles size={16} /><span>COO Intelligence Employee</span></div><h1 className="mt-3 text-4xl font-extrabold text-white">Morning Brief & Opportunity Engine</h1><p className="mt-2 max-w-2xl text-zinc-400">CreatorOS COO runs sequential market intelligence: Trend Hunter → Niche Researcher → Deterministic Ranking → Opportunity Generator → COO Evaluation → Safety Gate.</p></div><div className="flex items-center gap-3"><button type="button" onClick={() => void checkBriefStatus(true)} disabled={loading} className="inline-flex items-center gap-2 rounded-xl border border-zinc-700 bg-zinc-900 px-5 py-2.5 text-sm font-semibold text-zinc-200 transition hover:bg-zinc-800 disabled:cursor-not-allowed disabled:opacity-50"><RefreshCw size={16} className={loading ? "animate-spin text-indigo-400" : ""} />{loading ? "Generating Brief..." : "Refresh Intelligence"}</button></div></div>
        {actionNotice && <div className="rounded-2xl border border-emerald-500/30 bg-emerald-500/10 p-5"><div className="flex flex-wrap items-center justify-between gap-4"><div className="flex items-center gap-3 text-emerald-300"><CheckCircle2 size={20} /><p className="font-semibold">{actionNotice}</p></div>{missionResult && <button type="button" onClick={() => router.push(`/missions?job_id=${encodeURIComponent(missionResult.job_id)}`)} className="inline-flex items-center gap-1 text-sm font-semibold text-emerald-400 hover:text-emerald-300 underline">Open Mission Control <ArrowRight size={16} /></button>}</div></div>}
        {error && <div className="rounded-2xl border border-red-500/30 bg-red-500/10 p-5"><div className="flex items-center gap-3 text-red-300"><XCircle size={20}/><p className="font-semibold">{error}</p></div></div>}
        {/* Existing intelligence sections remain below. */}
        <section className="rounded-3xl border border-zinc-800 bg-zinc-900 p-7"><div className="flex items-center justify-between gap-4"><div><p className="text-xs font-semibold uppercase tracking-wider text-indigo-400">Pipeline</p><h2 className="mt-2 text-xl font-bold text-white">{briefResponse?.status === "READY" ? "Intelligence ready for CEO review" : briefResponse?.message || "Preparing intelligence"}</h2></div><span className="rounded-full bg-zinc-800 px-3 py-1 text-xs font-semibold text-zinc-300">{briefResponse?.progress ?? 0}%</span></div><div className="mt-5 h-2 overflow-hidden rounded-full bg-zinc-800"><div className="h-full rounded-full bg-indigo-500 transition-all" style={{width:`${Math.max(0,Math.min(100,briefResponse?.progress ?? 0))}%`}}/></div></section>
        {selectedOpportunity && <section className="rounded-3xl border border-zinc-800 bg-zinc-900 p-7"><div className="flex flex-wrap items-start justify-between gap-5"><div><p className="text-xs font-semibold uppercase tracking-wider text-indigo-400">Recommended opportunity</p><h2 className="mt-2 text-2xl font-bold text-white">{selectedOpportunity.topic || "Untitled opportunity"}</h2><p className="mt-3 max-w-3xl text-sm leading-6 text-zinc-400">{selectedOpportunity.reason || selectedOpportunity.problem}</p></div><div className={`rounded-2xl border px-5 py-4 text-center ${scoreBg(selectedOpportunity.overall_score)}`}><p className="text-xs uppercase tracking-wider opacity-70">Overall score</p><p className={`mt-1 text-3xl font-black ${scoreColor(selectedOpportunity.overall_score)}`}>{formatScore(selectedOpportunity.overall_score)}</p></div></div><div className="mt-6 grid gap-4 md:grid-cols-2"><div className="rounded-2xl bg-zinc-950 p-4"><p className="text-xs uppercase tracking-wider text-zinc-500">Audience</p><p className="mt-2 text-sm text-zinc-200">{(selectedOpportunity.audience ?? []).join(", ") || "Not specified"}</p></div><div className="rounded-2xl bg-zinc-950 p-4"><p className="text-xs uppercase tracking-wider text-zinc-500">Strategy</p><p className="mt-2 text-sm text-zinc-200">{selectedOpportunity.strategy || "Not specified"}</p></div></div><div className="mt-6 flex flex-wrap gap-3"><button onClick={() => void handleCEOApprove()} disabled={approving || rejecting} className="rounded-xl bg-emerald-600 px-6 py-3 text-sm font-bold text-white hover:bg-emerald-500 disabled:opacity-50">{approving ? "Starting Mission..." : "Approve & Start Mission"}</button><button onClick={() => void handleCEOReject()} disabled={approving || rejecting} className="rounded-xl border border-red-500/30 px-6 py-3 text-sm font-bold text-red-300 hover:bg-red-500/10 disabled:opacity-50">{rejecting ? "Rejecting..." : "Reject Opportunity"}</button><button onClick={() => setIsReviewOpen(v => !v)} className="rounded-xl border border-zinc-700 px-6 py-3 text-sm font-semibold text-zinc-300 hover:bg-zinc-800">{isReviewOpen ? "Hide Details" : "Review Details"}</button></div>{isReviewOpen && <div className="mt-6 rounded-2xl border border-zinc-800 bg-zinc-950 p-5"><p className="text-xs uppercase tracking-wider text-zinc-500">Recommended content</p><ul className="mt-3 list-disc space-y-2 pl-5 text-sm text-zinc-300">{(selectedOpportunity.recommended_content ?? []).map(item => <li key={item}>{item}</li>)}</ul>{selectedOpportunity.product_idea && <p className="mt-4 text-sm text-violet-300">Product idea: {selectedOpportunity.product_idea}</p>}</div>}</section>}
        {!briefResponse?.brief && !loading && <div className="rounded-3xl border border-dashed border-zinc-700 p-12 text-center text-sm text-zinc-500">No intelligence is available yet. Run Refresh Intelligence to generate a new morning brief.</div>}
      </div>
    </DashboardLayout>
  );
}
