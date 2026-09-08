"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { ArrowLeft, CheckCircle2, Clock3, Loader2, ShieldCheck, Video, XCircle } from "lucide-react";
import DashboardLayout from "@/components/layout/DashboardLayout";
import { API_URL, getLatestMissionJob, getMissionJob, type MissionJob } from "@/services/aiService";

function statusIcon(status: MissionJob["status"]) {
  if (status === "COMPLETED") return <CheckCircle2 className="h-5 w-5 text-emerald-400" />;
  if (status === "FAILED") return <XCircle className="h-5 w-5 text-red-400" />;
  return status === "RUNNING" ? <Loader2 className="h-5 w-5 animate-spin text-indigo-400" /> : <Clock3 className="h-5 w-5 text-amber-400" />;
}

function mediaUrl(path?: string) {
  if (!path) return null;
  const marker = "/generated_reels/";
  const index = path.replaceAll("\\", "/").lastIndexOf(marker);
  return index >= 0 ? `${API_URL}/media/reels/${encodeURIComponent(path.replaceAll("\\", "/").slice(index + marker.length))}` : null;
}

export default function MissionsPage() {
  const [jobId, setJobId] = useState("");
  const [job, setJob] = useState<MissionJob | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [discovering, setDiscovering] = useState(true);

  async function load(id: string) {
    if (!id) return;
    try { setJob(await getMissionJob(id)); setError(null); }
    catch (e) { setError(e instanceof Error ? e.message : "Could not load mission status."); }
  }

  async function discoverLatest() {
    try {
      const latest = await getLatestMissionJob();
      setJobId(latest.job_id); setJob(latest); setError(null);
      window.localStorage.setItem("creatoros:lastMissionJob", latest.job_id);
    } catch { /* empty state */ }
    finally { setDiscovering(false); }
  }

  useEffect(() => {
    const stored = window.localStorage.getItem("creatoros:lastMissionJob");
    if (stored) { setJobId(stored); setDiscovering(false); } else void discoverLatest();
  }, []);

  useEffect(() => {
    if (!jobId) return;
    window.localStorage.setItem("creatoros:lastMissionJob", jobId);
    void load(jobId);
    const timer = window.setInterval(() => void load(jobId), 2500);
    return () => window.clearInterval(timer);
  }, [jobId]);

  const mission = job?.result?.mission;
  const results = job?.result?.execution_results ?? [];

  return (
    <DashboardLayout>
      <div className="space-y-8">
        <div className="flex flex-wrap items-end justify-between gap-5">
          <div><p className="text-sm font-semibold uppercase tracking-[0.2em] text-indigo-400">CEO command center</p><h1 className="mt-3 text-4xl font-extrabold text-white">Mission Control</h1><p className="mt-2 max-w-2xl text-zinc-400">Track approved execution, generated content, Reel rendering, and approval-gated artifacts.</p></div>
          <Link href="/opportunities" className="inline-flex items-center gap-2 rounded-xl border border-zinc-700 bg-zinc-900 px-4 py-2.5 text-sm font-semibold text-zinc-200 hover:bg-zinc-800"><ArrowLeft className="h-4 w-4" /> Opportunity Engine</Link>
        </div>

        <section className="rounded-3xl border border-zinc-800 bg-zinc-900 p-6">
          <div className="flex flex-wrap items-end gap-3"><div className="min-w-[280px] flex-1"><label htmlFor="mission-job" className="text-xs font-semibold uppercase tracking-wider text-zinc-500">Mission job ID</label><input id="mission-job" value={jobId} onChange={e => setJobId(e.target.value.trim())} placeholder="Mission job ID" className="mt-2 w-full rounded-xl border border-zinc-700 bg-zinc-950 px-4 py-3 text-sm text-white outline-none focus:border-indigo-500" /></div><button onClick={() => void load(jobId)} className="rounded-xl bg-indigo-600 px-5 py-3 text-sm font-semibold text-white hover:bg-indigo-500">Refresh</button><button onClick={() => void discoverLatest()} className="rounded-xl border border-zinc-700 bg-zinc-950 px-5 py-3 text-sm font-semibold text-zinc-200 hover:bg-zinc-800">Find Latest</button></div>
          <p className="mt-3 text-xs text-zinc-500">Polling every 2.5 seconds while the mission is running.</p>
        </section>

        {error && <div className="rounded-2xl border border-red-500/30 bg-red-500/10 p-5 text-sm text-red-300">{error}</div>}

        {job && <>
          <section className="rounded-3xl border border-zinc-800 bg-zinc-900 p-7"><div className="flex flex-wrap items-center justify-between gap-4"><div className="flex items-center gap-3">{statusIcon(job.status)}<div><p className="text-xs uppercase tracking-wider text-zinc-500">Execution status</p><p className="text-lg font-bold text-white">{job.status}</p></div></div><div className="text-right"><p className="text-xs uppercase tracking-wider text-zinc-500">Progress</p><p className="text-2xl font-bold text-white">{Math.round(job.progress)}%</p></div></div><div className="mt-5 h-2 overflow-hidden rounded-full bg-zinc-800"><div className="h-full rounded-full bg-indigo-500 transition-all" style={{ width: `${Math.max(0, Math.min(100, job.progress))}%` }} /></div><p className="mt-3 text-sm text-zinc-400">{job.stage}</p>{job.error && <p className="mt-4 rounded-xl bg-red-500/10 p-4 text-sm text-red-300">{job.error}</p>}</section>

          {mission && <section className="rounded-3xl border border-zinc-800 bg-zinc-900 p-7"><div className="flex items-start justify-between gap-4"><div><p className="text-xs font-semibold uppercase tracking-wider text-indigo-400">Approved mission</p><h2 className="mt-2 text-2xl font-bold text-white">{mission.mission || "CreatorOS Mission"}</h2></div><div className="flex items-center gap-2 rounded-full border border-emerald-500/20 bg-emerald-500/10 px-3 py-1.5 text-xs font-semibold text-emerald-300"><ShieldCheck className="h-4 w-4" /> External actions gated</div></div>
            <div className="mt-6 space-y-3">{(mission.tasks ?? []).map(task => { const result = results.find(item => item.task_id === task.id); const video = result?.media_type === "video/mp4" ? mediaUrl(result.media_path) : null; return <div key={task.id} className="rounded-2xl border border-zinc-800 bg-zinc-950 p-4"><div className="flex flex-wrap items-center justify-between gap-3"><div><p className="font-semibold text-zinc-100">{task.title}</p><p className="mt-1 text-xs text-zinc-500">{task.assigned_to}{task.depends_on?.length ? ` · depends on ${task.depends_on.join(", ")}` : ""}</p></div><span className="rounded-full bg-zinc-800 px-3 py-1 text-xs font-semibold text-zinc-300">{result?.status ?? task.status}</span></div>
              {video && <div className="mt-4 max-w-sm overflow-hidden rounded-2xl border border-zinc-800 bg-black"><div className="flex items-center gap-2 border-b border-zinc-800 px-4 py-3 text-xs font-semibold text-zinc-300"><Video className="h-4 w-4 text-indigo-400" /> Generated Reel · 9:16</div><video className="aspect-[9/16] w-full object-cover" controls preload="metadata" src={video} /></div>}
              {result?.artifact_id && <p className="mt-3 text-xs text-emerald-400">Artifact #{result.artifact_id} · {result.approval_status ?? "approval_required"}</p>}{result?.error && <p className="mt-3 text-xs text-red-400">{result.error}</p>}</div>; })}</div>
          </section>}
        </>}

        {!job && !error && <div className="rounded-3xl border border-dashed border-zinc-700 p-12 text-center text-sm text-zinc-500">{discovering ? "Finding the latest mission..." : "Approve an opportunity in the Opportunity Engine, then return here."}</div>}
      </div>
    </DashboardLayout>
  );
}
