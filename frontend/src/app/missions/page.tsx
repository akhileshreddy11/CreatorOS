"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { ArrowLeft, CheckCircle2, Clock3, Loader2, ShieldCheck, XCircle } from "lucide-react";
import DashboardLayout from "@/components/layout/DashboardLayout";

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://127.0.0.1:8000";

type Job = {
  job_id: string;
  type: string;
  status: "PENDING" | "RUNNING" | "COMPLETED" | "FAILED";
  stage: string;
  progress: number;
  result?: {
    message?: string;
    mission?: {
      mission?: string;
      execution_status?: string;
      tasks?: Array<{ id: string; title: string; status: string; assigned_to: string; depends_on?: string[] }>;
    };
    execution_results?: Array<{
      task_id: string;
      employee: string;
      status: string;
      artifact_status?: string;
      approval_status?: string;
      artifact_id?: number;
      error?: string;
    }>;
  };
  error?: string;
};

function statusIcon(status: Job["status"]) {
  if (status === "COMPLETED") return <CheckCircle2 className="h-5 w-5 text-emerald-400" />;
  if (status === "FAILED") return <XCircle className="h-5 w-5 text-red-400" />;
  return status === "RUNNING" ? <Loader2 className="h-5 w-5 animate-spin text-indigo-400" /> : <Clock3 className="h-5 w-5 text-amber-400" />;
}

export default function MissionsPage() {
  const [jobId, setJobId] = useState("");
  const [job, setJob] = useState<Job | null>(null);
  const [error, setError] = useState<string | null>(null);

  async function load(id: string) {
    if (!id) return;
    try {
      const response = await fetch(`${API_URL}/missions/${id}`, { cache: "no-store" });
      if (!response.ok) throw new Error("Mission job could not be loaded.");
      setJob(await response.json());
      setError(null);
    } catch (requestError) {
      setError(requestError instanceof Error ? requestError.message : "Could not load mission status.");
    }
  }

  useEffect(() => {
    const stored = window.localStorage.getItem("creatoros:lastMissionJob");
    if (stored) setJobId(stored);
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
          <div>
            <p className="text-sm font-semibold uppercase tracking-[0.2em] text-indigo-400">CEO command center</p>
            <h1 className="mt-3 text-4xl font-extrabold text-white">Mission Control</h1>
            <p className="mt-2 max-w-2xl text-zinc-400">Track approved mission execution, task dependencies, and generated artifacts without triggering external sends or publishing.</p>
          </div>
          <Link href="/opportunities" className="inline-flex items-center gap-2 rounded-xl border border-zinc-700 bg-zinc-900 px-4 py-2.5 text-sm font-semibold text-zinc-200 hover:bg-zinc-800">
            <ArrowLeft className="h-4 w-4" /> Opportunity Engine
          </Link>
        </div>

        <section className="rounded-3xl border border-zinc-800 bg-zinc-900 p-6">
          <div className="flex flex-wrap items-end gap-3">
            <div className="min-w-[280px] flex-1">
              <label htmlFor="mission-job" className="text-xs font-semibold uppercase tracking-wider text-zinc-500">Mission job ID</label>
              <input id="mission-job" value={jobId} onChange={(event) => setJobId(event.target.value.trim())} placeholder="Paste a job ID returned after approval" className="mt-2 w-full rounded-xl border border-zinc-700 bg-zinc-950 px-4 py-3 text-sm text-white outline-none focus:border-indigo-500" />
            </div>
            <button type="button" onClick={() => void load(jobId)} className="rounded-xl bg-indigo-600 px-5 py-3 text-sm font-semibold text-white hover:bg-indigo-500">Refresh</button>
          </div>
          <p className="mt-3 text-xs text-zinc-500">The latest mission job is remembered locally in this browser.</p>
        </section>

        {error && <div className="rounded-2xl border border-red-500/30 bg-red-500/10 p-5 text-sm text-red-300">{error}</div>}

        {job && (
          <>
            <section className="rounded-3xl border border-zinc-800 bg-zinc-900 p-7">
              <div className="flex flex-wrap items-center justify-between gap-4">
                <div className="flex items-center gap-3">{statusIcon(job.status)}<div><p className="text-xs uppercase tracking-wider text-zinc-500">Execution status</p><p className="text-lg font-bold text-white">{job.status}</p></div></div>
                <div className="text-right"><p className="text-xs uppercase tracking-wider text-zinc-500">Progress</p><p className="text-2xl font-bold text-white">{Math.round(job.progress)}%</p></div>
              </div>
              <div className="mt-5 h-2 overflow-hidden rounded-full bg-zinc-800"><div className="h-full rounded-full bg-indigo-500 transition-all" style={{ width: `${Math.max(0, Math.min(100, job.progress))}%` }} /></div>
              <p className="mt-3 text-sm text-zinc-400">{job.stage}</p>
              {job.error && <p className="mt-4 rounded-xl bg-red-500/10 p-4 text-sm text-red-300">{job.error}</p>}
            </section>

            {mission && (
              <section className="rounded-3xl border border-zinc-800 bg-zinc-900 p-7">
                <div className="flex items-start justify-between gap-4">
                  <div><p className="text-xs font-semibold uppercase tracking-wider text-indigo-400">Approved mission</p><h2 className="mt-2 text-2xl font-bold text-white">{mission.mission || "CreatorOS Mission"}</h2></div>
                  <div className="flex items-center gap-2 rounded-full border border-emerald-500/20 bg-emerald-500/10 px-3 py-1.5 text-xs font-semibold text-emerald-300"><ShieldCheck className="h-4 w-4" /> External actions remain gated</div>
                </div>

                <div className="mt-6 space-y-3">
                  {(mission.tasks ?? []).map((task) => {
                    const result = results.find((item) => item.task_id === task.id);
                    return <div key={task.id} className="rounded-2xl border border-zinc-800 bg-zinc-950 p-4">
                      <div className="flex flex-wrap items-center justify-between gap-3"><div><p className="font-semibold text-zinc-100">{task.title}</p><p className="mt-1 text-xs text-zinc-500">{task.assigned_to}{task.depends_on?.length ? ` · depends on ${task.depends_on.join(", ")}` : ""}</p></div><span className="rounded-full bg-zinc-800 px-3 py-1 text-xs font-semibold text-zinc-300">{result?.status ?? task.status}</span></div>
                      {result?.artifact_id && <p className="mt-3 text-xs text-emerald-400">Artifact #{result.artifact_id} · {result.approval_status ?? "approval_required"}</p>}
                      {result?.error && <p className="mt-3 text-xs text-red-400">{result.error}</p>}
                    </div>;
                  })}
                </div>
              </section>
            )}
          </>
        )}

        {!job && !error && <div className="rounded-3xl border border-dashed border-zinc-700 p-12 text-center text-sm text-zinc-500">Approve an opportunity in the Opportunity Engine, then open Mission Control with the returned job ID.</div>}
      </div>
    </DashboardLayout>
  );
}
