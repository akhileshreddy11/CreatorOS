"use client";

import { useEffect, useRef, useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import {
  AlertTriangle,
  ArrowRight,
  CheckCircle2,
  ChevronRight,
  Flame,
  Layers,
  RefreshCw,
  Shield,
  ShieldAlert,
  ShieldCheck,
  Sparkles,
  Target,
  TrendingUp,
  XCircle,
} from "lucide-react";

import DashboardLayout from "@/components/layout/DashboardLayout";
import {
  approveMission,
  getMorningBrief,
  refreshMorningBrief,
  rejectMission,
  type BriefData,
  type MissionResponse,
  type MorningBriefResponse,
  type Opportunity,
  type RankedNiche,
} from "@/services/aiService";

function scoreColor(score?: number) {
  if (score === undefined || score === null) return "text-zinc-500";
  if (score >= 80) return "text-emerald-400";
  if (score >= 60) return "text-amber-400";
  return "text-red-400";
}

function scoreBg(score?: number) {
  if (score === undefined || score === null) return "bg-zinc-800/40 border-zinc-700/40";
  if (score >= 80) return "bg-emerald-500/10 border-emerald-500/30 text-emerald-300";
  if (score >= 60) return "bg-amber-500/10 border-amber-500/30 text-amber-300";
  return "bg-red-500/10 border-red-500/30 text-red-300";
}

function formatScore(score?: number) {
  return score === undefined || score === null ? "—" : score;
}

export default function OpportunitiesPage() {
  const router = useRouter();
  const [briefResponse, setBriefResponse] = useState<MorningBriefResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // CEO Actions state
  const [approving, setApproving] = useState(false);
  const [rejecting, setRejecting] = useState(false);
  const [missionResult, setMissionResult] = useState<MissionResponse | null>(null);
  const [actionNotice, setActionNotice] = useState<string | null>(null);
  const [isReviewOpen, setIsReviewOpen] = useState(false);

  const pollingRef = useRef<NodeJS.Timeout | null>(null);

  async function checkBriefStatus(triggerRefresh: boolean = false) {
    try {
      if (triggerRefresh) {
        setLoading(true);
        setError(null);
        const refreshRes = await refreshMorningBrief();
        setBriefResponse(refreshRes);
      } else {
        const res = await getMorningBrief();
        setBriefResponse(res);
        if (res.status === "READY") {
          setLoading(false);
        } else if (res.status === "FAILED") {
          setLoading(false);
          setError(res.error || "COO morning brief failed to generate.");
        }
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "Could not connect to CreatorOS backend.");
      setLoading(false);
    }
  }

  // Poll when STARTED or RUNNING
  useEffect(() => {
    checkBriefStatus();

    return () => {
      if (pollingRef.current) clearInterval(pollingRef.current);
    };
  }, []);

  useEffect(() => {
    if (briefResponse?.status === "STARTED" || briefResponse?.status === "RUNNING") {
      setLoading(true);
      if (!pollingRef.current) {
        pollingRef.current = setInterval(async () => {
          try {
            const res = await getMorningBrief();
            setBriefResponse(res);
            if (res.status === "READY" || res.status === "FAILED") {
              setLoading(false);
              if (pollingRef.current) {
                clearInterval(pollingRef.current);
                pollingRef.current = null;
              }
              if (res.status === "FAILED") {
                setError(res.error || "COO morning brief failed to generate.");
              }
            }
          } catch (e) {
            // Silently retry polling
          }
        }, 3000);
      }
    } else {
      if (pollingRef.current) {
        clearInterval(pollingRef.current);
        pollingRef.current = null;
      }
      setLoading(false);
    }
  }, [briefResponse?.status]);

  const brief: BriefData | undefined = briefResponse?.brief;

  const rankedNiches: RankedNiche[] =
    brief?.niche_ranking?.ranked_niches ??
    brief?.niche_research?.ranked_niches ??
    [];

  const selectedNiche: RankedNiche | null =
    brief?.selected_niche ??
    brief?.niche_ranking?.best_niche ??
    brief?.niche_research?.best_niche ??
    (rankedNiches.length > 0 ? rankedNiches[0] : null);

  const opportunities: Opportunity[] =
    brief?.opportunity_generation?.opportunities ?? [];

  const selectedOpportunity: Opportunity | null =
    brief?.selected_opportunity ??
    brief?.opportunity_generation?.best_opportunity ??
    (opportunities.length > 0 ? opportunities[0] : null);

  const evaluation = brief?.coo_evaluation;
  const safety = brief?.safety_review;
  const trend = brief?.trend_opportunity;

  async function handleCEOApprove() {
    if (!selectedOpportunity) return;
    try {
      setApproving(true);
      setError(null);
      setActionNotice(null);

      const result = await approveMission({
        topic: selectedOpportunity.topic || "Hyderabad Gym Campaign",
        problem: selectedOpportunity.problem || "",
        audience: selectedOpportunity.audience || ["Gym owners", "Local adults"],
        strategy: selectedOpportunity.strategy || "",
        recommended_content: selectedOpportunity.recommended_content || [],
        product_idea: selectedOpportunity.product_idea || "",
      });

      setMissionResult(result);
      setActionNotice(
        "Opportunity Approved! Mission executed and draft artifacts created in Draft Review.",
      );
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to execute mission.");
    } finally {
      setApproving(false);
    }
  }

  async function handleCEOReject() {
    if (!selectedOpportunity) return;
    try {
      setRejecting(true);
      setError(null);
      setActionNotice(null);

      const result = await rejectMission({
        topic: selectedOpportunity.topic || "Hyderabad Gym Campaign",
        problem: selectedOpportunity.problem || "",
        audience: selectedOpportunity.audience || [],
        strategy: selectedOpportunity.strategy || "",
        recommended_content: selectedOpportunity.recommended_content || [],
        product_idea: selectedOpportunity.product_idea || "",
      });

      setActionNotice(result.message || "Opportunity rejected by CEO.");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to reject opportunity.");
    } finally {
      setRejecting(false);
    }
  }

  return (
    <DashboardLayout>
      <div className="space-y-8">
        {/* HEADER */}
        <div className="flex flex-wrap items-end justify-between gap-5">
          <div>
            <div className="flex items-center gap-2 text-sm font-semibold uppercase tracking-[0.2em] text-indigo-400">
              <Sparkles size={16} />
              <span>COO Intelligence Employee</span>
            </div>

            <h1 className="mt-3 text-4xl font-extrabold text-white">
              Morning Brief & Opportunity Engine
            </h1>

            <p className="mt-2 max-w-2xl text-zinc-400">
              CreatorOS COO runs sequential market intelligence: Trend Hunter → Niche Researcher
              → Deterministic Ranking → Opportunity Generator → COO Evaluation → Safety Gate.
            </p>
          </div>

          <div className="flex items-center gap-3">
            <button
              type="button"
              onClick={() => checkBriefStatus(true)}
              disabled={loading}
              className="inline-flex items-center gap-2 rounded-xl border border-zinc-700 bg-zinc-900 px-5 py-2.5 text-sm font-semibold text-zinc-200 transition hover:bg-zinc-800 disabled:cursor-not-allowed disabled:opacity-50"
            >
              <RefreshCw size={16} className={loading ? "animate-spin text-indigo-400" : ""} />
              {loading ? "Generating Brief..." : "Refresh Intelligence"}
            </button>
          </div>
        </div>

        {/* NOTICES */}
        {actionNotice && (
          <div className="rounded-2xl border border-emerald-500/30 bg-emerald-500/10 p-5">
            <div className="flex items-center justify-between gap-4">
              <div className="flex items-center gap-3 text-emerald-300">
                <CheckCircle2 size={20} />
                <p className="font-semibold">{actionNotice}</p>
              </div>
              <Link
                href="/drafts"
                className="inline-flex items-center gap-1 text-sm font-semibold text-emerald-400 hover:text-emerald-300 underline"
              >
                Go to Draft Review <ArrowRight size={16} />
              </Link>
            </div>
          </div>
        )}

        {/* ERROR STATE */}
        {error && (
          <section className="rounded-2xl border border-red-500/30 bg-red-500/10 p-5">
            <div className="flex items-center gap-3 text-red-300">
              <AlertTriangle size={20} />
              <p className="font-semibold">Intelligence Error</p>
            </div>
            <p className="mt-2 text-sm text-red-400">{error}</p>
            <button
              type="button"
              onClick={() => checkBriefStatus(true)}
              className="mt-4 rounded-xl border border-red-500/40 px-4 py-2 text-sm font-semibold text-red-300 hover:bg-red-500/20"
            >
              Retry Brief Generation
            </button>
          </section>
        )}

        {/* LOADING / RUNNING STATE */}
        {(loading || briefResponse?.status === "STARTED" || briefResponse?.status === "RUNNING") && !brief && (
          <section className="rounded-3xl border border-zinc-800 bg-zinc-900/80 p-16 text-center backdrop-blur-xl">
            <div className="mx-auto h-12 w-12 animate-spin rounded-full border-2 border-zinc-700 border-t-indigo-500" />
            <h2 className="mt-6 text-2xl font-bold text-white">
              COO is preparing your morning brief...
            </h2>
            <p className="mx-auto mt-2 max-w-lg text-sm leading-6 text-zinc-400">
              Running deep multi-step analysis: Trend Hunter → Niche Researcher → Niche Ranking →
              Opportunity Generator → COO Evaluation → Safety Gate.
            </p>
            <div className="mt-8 flex justify-center gap-2">
              {["Trend", "Niches", "Rank", "Opportunities", "Evaluation", "Safety Gate"].map((step, idx) => (
                <span
                  key={step}
                  className="rounded-full bg-zinc-950 px-3 py-1 text-xs text-zinc-500 border border-zinc-800 animate-pulse"
                >
                  {idx + 1}. {step}
                </span>
              ))}
            </div>
          </section>
        )}

        {brief && (
          <>
            {/* GREETING & SNAPSHOT */}
            <section className="rounded-3xl border border-indigo-500/30 bg-gradient-to-br from-indigo-950/40 via-zinc-900 to-zinc-950 p-8 shadow-xl">
              <div className="flex flex-wrap items-start justify-between gap-6">
                <div>
                  <span className="rounded-full bg-indigo-500/20 px-3.5 py-1 text-xs font-semibold uppercase tracking-wider text-indigo-300">
                    Executive Briefing
                  </span>
                  <h2 className="mt-3 text-3xl font-extrabold text-white">
                    {brief.greeting || "Good Morning Boss 👋"}
                  </h2>
                  <p className="mt-2 text-sm text-zinc-300">
                    Pilot: <span className="font-semibold text-white">{brief.business || "CreatorOS"}</span> in{" "}
                    <span className="text-white font-semibold">Hyderabad</span> · KPI:{" "}
                    <span className="text-indigo-300 font-semibold">{brief.monthly_goal || "Trial enquiries"}</span> · Mode:{" "}
                    <span className="text-emerald-400 font-semibold">{brief.automation || "Approval-gated"}</span>
                  </p>
                </div>

                <div className="flex items-center gap-3">
                  <div className="rounded-2xl border border-zinc-800 bg-zinc-950/80 px-5 py-3 text-center">
                    <p className="text-[10px] uppercase font-semibold tracking-wider text-zinc-500">Pipeline Execution</p>
                    <p className="text-lg font-bold text-white">{brief.pipeline_time_seconds ? `${brief.pipeline_time_seconds}s` : "Complete"}</p>
                  </div>
                  <div className="rounded-2xl border border-zinc-800 bg-zinc-950/80 px-5 py-3 text-center">
                    <p className="text-[10px] uppercase font-semibold tracking-wider text-zinc-500">Status</p>
                    <span className={`text-sm font-bold uppercase ${brief.status === "NEEDS_REVIEW" ? "text-amber-400" : "text-emerald-400"}`}>
                      {brief.status || "Awaiting CEO Approval"}
                    </span>
                  </div>
                </div>
              </div>

              {/* TODAY'S TREND */}
              {trend && (
                <div className="mt-6 rounded-2xl border border-zinc-800 bg-zinc-950/90 p-5">
                  <div className="flex items-center gap-2 text-xs font-semibold uppercase tracking-wider text-amber-400">
                    <Flame size={16} />
                    <span>Today's Local Growth Trend</span>
                  </div>
                  <h3 className="mt-2 text-lg font-bold text-white">{trend.topic}</h3>
                  {trend.reason && <p className="mt-1 text-sm text-zinc-400">{trend.reason}</p>}
                  {trend.best_posting_time && (
                    <p className="mt-2 text-xs text-zinc-500">
                      Best posting window: <span className="text-zinc-300">{trend.best_posting_time}</span>
                    </p>
                  )}
                </div>
              )}
            </section>

            {/* CEO ACTION & OPPORTUNITY SPOTLIGHT */}
            {selectedOpportunity && (
              <section className="overflow-hidden rounded-3xl border-2 border-indigo-500/40 bg-zinc-900 p-8 shadow-2xl relative">
                <div className="flex flex-wrap items-start justify-between gap-6">
                  <div>
                    <div className="flex items-center gap-2">
                      <span className="rounded-full bg-indigo-500/20 px-3 py-1 text-xs font-bold uppercase tracking-wider text-indigo-300">
                        ⭐ COO Recommended Winning Opportunity
                      </span>
                      <span className="rounded-full bg-amber-500/10 px-3 py-1 text-xs font-bold uppercase tracking-wider text-amber-300">
                        CEO Decision Required
                      </span>
                    </div>

                    <h2 className="mt-4 text-3xl font-extrabold text-white">
                      {selectedOpportunity.topic || "Campaign Opportunity"}
                    </h2>

                    {selectedOpportunity.problem && (
                      <div className="mt-4 rounded-2xl bg-zinc-950 p-4 border border-zinc-800/80">
                        <p className="text-xs font-bold uppercase tracking-wider text-zinc-500">Audience Problem</p>
                        <p className="mt-1 text-sm text-zinc-300 leading-relaxed">{selectedOpportunity.problem}</p>
                      </div>
                    )}
                  </div>

                  <div className="rounded-3xl border border-indigo-500/30 bg-indigo-950/40 px-8 py-5 text-center">
                    <p className="text-xs uppercase font-bold tracking-widest text-zinc-400">Opportunity Score</p>
                    <p className={`mt-2 text-5xl font-black ${scoreColor(selectedOpportunity.overall_score)}`}>
                      {formatScore(selectedOpportunity.overall_score)}
                    </p>
                    <p className="text-xs text-zinc-500 font-semibold mt-1">/ 100 Points</p>
                  </div>
                </div>

                {/* STRATEGY & PRODUCT PLAYBOOK */}
                <div className="mt-6 grid gap-4 md:grid-cols-2">
                  {selectedOpportunity.strategy && (
                    <div className="rounded-2xl border border-zinc-800 bg-zinc-950 p-5">
                      <p className="text-xs font-bold uppercase tracking-wider text-indigo-400">Execution Strategy</p>
                      <p className="mt-2 text-sm text-zinc-300 leading-relaxed">{selectedOpportunity.strategy}</p>
                    </div>
                  )}

                  {selectedOpportunity.product_idea && (
                    <div className="rounded-2xl border border-zinc-800 bg-zinc-950 p-5">
                      <p className="text-xs font-bold uppercase tracking-wider text-violet-400">Product / Campaign Playbook</p>
                      <p className="mt-2 text-sm text-zinc-300 leading-relaxed">{selectedOpportunity.product_idea}</p>
                    </div>
                  )}
                </div>

                {/* RECOMMENDED CONTENT */}
                {selectedOpportunity.recommended_content && selectedOpportunity.recommended_content.length > 0 && (
                  <div className="mt-6 rounded-2xl border border-zinc-800 bg-zinc-950 p-5">
                    <p className="text-xs font-bold uppercase tracking-wider text-zinc-400">Proposed Content Angles for Hyderabad Pilot</p>
                    <div className="mt-3 grid gap-2.5 sm:grid-cols-3">
                      {selectedOpportunity.recommended_content.map((content, idx) => (
                        <div key={idx} className="rounded-xl border border-zinc-800/80 bg-zinc-900/60 p-3.5 text-xs text-zinc-300">
                          <span className="font-bold text-indigo-400 mr-1.5">Reel #{idx + 1}:</span>
                          {content}
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* OPPORTUNITY SAFETY GATE CARD */}
                {safety && (
                  <div className={`mt-6 rounded-2xl border p-5 ${safety.status === "SAFE" ? "border-emerald-500/30 bg-emerald-950/20" : "border-amber-500/40 bg-amber-950/20"}`}>
                    <div className="flex flex-wrap items-center justify-between gap-4">
                      <div className="flex items-center gap-3">
                        {safety.status === "SAFE" ? (
                          <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-emerald-500/20 text-emerald-400">
                            <ShieldCheck size={24} />
                          </div>
                        ) : (
                          <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-amber-500/20 text-amber-400">
                            <ShieldAlert size={24} />
                          </div>
                        )}
                        <div>
                          <div className="flex items-center gap-2">
                            <h4 className="text-sm font-bold text-white">Opportunity Safety Gate Review</h4>
                            <span className={`rounded-full px-2.5 py-0.5 text-[10px] font-bold uppercase ${safety.status === "SAFE" ? "bg-emerald-500/20 text-emerald-300" : "bg-amber-500/20 text-amber-300"}`}>
                              {safety.status}
                            </span>
                          </div>
                          <p className="text-xs text-zinc-400 mt-0.5">{safety.summary}</p>
                        </div>
                      </div>

                      <div className="text-right">
                        <span className="text-[10px] font-semibold uppercase text-zinc-400">Safety Score</span>
                        <p className={`text-xl font-bold ${scoreColor(safety.safety_score)}`}>{safety.safety_score}/100</p>
                      </div>
                    </div>

                    {safety.warnings && safety.warnings.length > 0 && (
                      <div className="mt-4 space-y-2 border-t border-zinc-800/80 pt-3">
                        {safety.warnings.map((warn, i) => (
                          <div key={i} className="flex items-start gap-2 text-xs text-amber-300/90">
                            <AlertTriangle size={14} className="mt-0.5 shrink-0 text-amber-400" />
                            <span>{warn}</span>
                          </div>
                        ))}
                      </div>
                    )}
                  </div>
                )}

                {/* CEO DECISION BUTTONS */}
                <div className="mt-8 border-t border-zinc-800 pt-6 flex flex-wrap items-center justify-between gap-4">
                  <div className="text-xs text-zinc-400 flex items-center gap-2">
                    <Shield size={16} className="text-indigo-400" />
                    <span>Approving creates tasks for Content & Product employees and routes drafts for review.</span>
                  </div>

                  <div className="flex items-center gap-3">
                    <button
                      type="button"
                      onClick={handleCEOReject}
                      disabled={rejecting || approving}
                      className="rounded-xl border border-red-500/30 px-5 py-3 text-sm font-semibold text-red-400 transition hover:bg-red-500/10 disabled:opacity-40"
                    >
                      {rejecting ? "Rejecting..." : "Reject Opportunity"}
                    </button>

                    <button
                      type="button"
                      onClick={() => setIsReviewOpen(!isReviewOpen)}
                      className="rounded-xl border border-zinc-700 bg-zinc-800 px-5 py-3 text-sm font-semibold text-zinc-200 transition hover:bg-zinc-700"
                    >
                      {isReviewOpen ? "Hide Details" : "Review Details"}
                    </button>

                    <button
                      type="button"
                      onClick={handleCEOApprove}
                      disabled={approving || rejecting}
                      className="rounded-xl bg-gradient-to-r from-emerald-600 to-teal-600 px-7 py-3 text-sm font-bold text-white shadow-lg shadow-emerald-900/40 transition hover:scale-[1.02] hover:from-emerald-500 hover:to-teal-500 disabled:opacity-40"
                    >
                      {approving ? "Executing Mission..." : "Approve & Launch Mission →"}
                    </button>
                  </div>
                </div>

                {/* MISSION EXECUTION RESULT EXPANSION */}
                {missionResult && (
                  <div className="mt-6 rounded-2xl border border-emerald-500/40 bg-zinc-950 p-6 space-y-4">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-2">
                        <CheckCircle2 className="text-emerald-400" size={20} />
                        <h4 className="font-bold text-white">Mission Executed Successfully</h4>
                      </div>
                      <span className="rounded-full bg-emerald-500/20 px-3 py-1 text-xs font-bold uppercase text-emerald-400">
                        {missionResult.mission?.execution_status || "COMPLETED"}
                      </span>
                    </div>

                    <div className="grid gap-2 sm:grid-cols-2">
                      {missionResult.mission?.tasks?.map((t) => (
                        <div key={t.id} className="rounded-xl bg-zinc-900 p-3 text-xs border border-zinc-800">
                          <div className="flex justify-between font-semibold text-zinc-200">
                            <span>{t.title}</span>
                            <span className="text-emerald-400 uppercase">{t.status}</span>
                          </div>
                          <p className="text-zinc-500 mt-1">{t.assigned_to}</p>
                        </div>
                      ))}
                    </div>

                    <Link
                      href="/drafts"
                      className="block w-full text-center rounded-xl bg-indigo-600 py-3 text-sm font-bold text-white hover:bg-indigo-500 transition"
                    >
                      Review Generated Drafts ({missionResult.execution_results?.length || 0} Artifacts) →
                    </Link>
                  </div>
                )}
              </section>
            )}

            {/* COO EVALUATION BREAKDOWN */}
            {evaluation && (
              <section className="rounded-3xl border border-zinc-800 bg-zinc-900 p-7 space-y-6">
                <div className="flex flex-wrap items-center justify-between gap-4">
                  <div>
                    <p className="text-xs font-bold uppercase tracking-widest text-violet-400">Executive Evaluation</p>
                    <h2 className="text-2xl font-bold text-white mt-1">COO Scorecard</h2>
                  </div>
                  <span
                    className={`rounded-full px-4 py-1.5 text-xs font-bold uppercase ${
                      evaluation.recommendation === "APPROVE"
                        ? "bg-emerald-500/20 text-emerald-400"
                        : evaluation.recommendation === "REJECT"
                          ? "bg-red-500/20 text-red-400"
                          : "bg-amber-500/20 text-amber-400"
                    }`}
                  >
                    Recommendation: {evaluation.recommendation || "REVIEW"}
                  </span>
                </div>

                <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-5">
                  {[
                    ["Audience Fit", evaluation.audience_fit],
                    ["Content Potential", evaluation.content_potential],
                    ["Monetization", evaluation.monetization_potential],
                    ["Revenue Alignment", evaluation.revenue_alignment],
                    ["Overall Score", evaluation.overall_score],
                  ].map(([label, score]) => (
                    <div key={String(label)} className="rounded-2xl bg-zinc-950 p-4 border border-zinc-800 text-center">
                      <p className="text-[10px] font-bold uppercase tracking-wider text-zinc-500">{label}</p>
                      <p className={`mt-2 text-2xl font-bold ${scoreColor(score as number)}`}>
                        {formatScore(score as number)}
                      </p>
                    </div>
                  ))}
                </div>

                {evaluation.reason && (
                  <div className="rounded-2xl bg-zinc-950 p-4 border border-zinc-800">
                    <p className="text-xs font-bold uppercase tracking-wider text-zinc-400">COO Rationale</p>
                    <p className="mt-1 text-sm text-zinc-300 leading-relaxed">{evaluation.reason}</p>
                  </div>
                )}

                {evaluation.proposed_deliverables && evaluation.proposed_deliverables.length > 0 && (
                  <div>
                    <p className="text-xs font-bold uppercase tracking-wider text-zinc-400 mb-3">Planned Deliverables</p>
                    <div className="grid gap-2.5 sm:grid-cols-3">
                      {evaluation.proposed_deliverables.map((item, idx) => (
                        <div key={idx} className="rounded-xl border border-zinc-800 bg-zinc-950 p-3 text-xs text-zinc-300">
                          <span className="font-bold text-indigo-400 mr-2">0{idx + 1}</span>
                          {item}
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </section>
            )}

            {/* 5 RANKED NICHES DISPLAY */}
            <section className="space-y-4">
              <div>
                <p className="text-xs font-bold uppercase tracking-widest text-zinc-500">Niche Discovery</p>
                <h2 className="text-2xl font-bold text-white mt-1">Five Ranked Pilot Niches</h2>
                <p className="text-sm text-zinc-400">Deterministic scoring applied across demand, reach, trend, competition, and monetization.</p>
              </div>

              <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
                {rankedNiches.map((item, idx) => {
                  const isWinning = selectedNiche?.niche === item.niche || selectedNiche?.topic === item.topic;
                  return (
                    <article
                      key={`${item.niche ?? item.topic ?? "niche"}-${idx}`}
                      className={`rounded-3xl border p-6 transition ${
                        isWinning ? "border-indigo-500/50 bg-indigo-950/20 ring-1 ring-indigo-500/30" : "border-zinc-800 bg-zinc-900/90"
                      }`}
                    >
                      <div className="flex items-start justify-between gap-3">
                        <div>
                          <div className="flex items-center gap-2">
                            <span className="text-xs font-bold text-indigo-400">#{item.rank ?? idx + 1}</span>
                            {isWinning && (
                              <span className="rounded-full bg-emerald-500/20 px-2.5 py-0.5 text-[10px] font-bold uppercase text-emerald-300">
                                Winner
                              </span>
                            )}
                          </div>
                          <h3 className="mt-2 text-lg font-bold text-white">{item.niche || item.topic || "Local Niche"}</h3>
                        </div>

                        <div className="text-right">
                          <p className={`text-2xl font-black ${scoreColor(item.overall_score)}`}>
                            {formatScore(item.overall_score)}
                          </p>
                        </div>
                      </div>

                      {item.reason && <p className="mt-3 text-xs text-zinc-400 leading-relaxed">{item.reason}</p>}

                      {item.scores && (
                        <div className="mt-4 grid grid-cols-3 gap-2 border-t border-zinc-800/80 pt-3">
                          <div className="text-center">
                            <span className="text-[9px] uppercase text-zinc-500">Demand</span>
                            <p className="text-xs font-semibold text-zinc-200">{item.scores.demand ?? "—"}</p>
                          </div>
                          <div className="text-center">
                            <span className="text-[9px] uppercase text-zinc-500">Reach</span>
                            <p className="text-xs font-semibold text-zinc-200">{item.scores.reach ?? "—"}</p>
                          </div>
                          <div className="text-center">
                            <span className="text-[9px] uppercase text-zinc-500">Monetize</span>
                            <p className="text-xs font-semibold text-zinc-200">{item.scores.monetization ?? "—"}</p>
                          </div>
                        </div>
                      )}
                    </article>
                  );
                })}
              </div>
            </section>

            {/* GENERATED CAMPAIGN OPPORTUNITIES */}
            {opportunities.length > 0 && (
              <section className="space-y-4">
                <div>
                  <p className="text-xs font-bold uppercase tracking-widest text-zinc-500">Campaign Alternatives</p>
                  <h2 className="text-2xl font-bold text-white mt-1">Generated Opportunities</h2>
                </div>

                <div className="grid gap-4 lg:grid-cols-2">
                  {opportunities.map((opp, index) => (
                    <article
                      key={`${opp.topic ?? "opp"}-${index}`}
                      className="rounded-3xl border border-zinc-800 bg-zinc-900 p-6 transition hover:border-zinc-700"
                    >
                      <div className="flex items-start justify-between gap-3">
                        <div>
                          <span className="text-xs font-bold text-indigo-400">Opportunity #{opp.rank ?? index + 1}</span>
                          <h3 className="mt-1 text-lg font-bold text-white">{opp.topic}</h3>
                        </div>
                        <span className={`text-xl font-bold ${scoreColor(opp.overall_score)}`}>
                          {formatScore(opp.overall_score)}
                        </span>
                      </div>

                      {opp.problem && <p className="mt-3 text-xs text-zinc-400">{opp.problem}</p>}

                      {opp.recommended_content && opp.recommended_content.length > 0 && (
                        <div className="mt-4 border-t border-zinc-800/80 pt-3">
                          <p className="text-[10px] font-bold uppercase text-zinc-500">Recommended angles:</p>
                          <ul className="mt-1.5 space-y-1 text-xs text-zinc-300">
                            {opp.recommended_content.slice(0, 2).map((c, i) => (
                              <li key={i} className="flex gap-2">
                                <span className="text-indigo-400">•</span>
                                <span>{c}</span>
                              </li>
                            ))}
                          </ul>
                        </div>
                      )}
                    </article>
                  ))}
                </div>
              </section>
            )}
          </>
        )}
      </div>
    </DashboardLayout>
  );
}