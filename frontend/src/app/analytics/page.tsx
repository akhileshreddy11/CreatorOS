"use client";

import { useEffect, useState } from "react";
import DashboardLayout from "@/components/layout/DashboardLayout";
import { getDashboardSummary, type DashboardSummary } from "@/services/aiService";

const metricLabels: Array<[keyof DashboardSummary["metrics"], string]> = [
  ["prospects", "Prospects researched"],
  ["contacted", "Approved sends recorded"],
  ["replies", "Replies"],
  ["qualified_leads", "Qualified leads"],
  ["appointments", "Appointments"],
  ["trial_class_enquiries", "Trial-class enquiries"],
];

export default function AnalyticsPage() {
  const [summary, setSummary] = useState<DashboardSummary | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    getDashboardSummary().then(setSummary).catch((requestError) => setError(requestError instanceof Error ? requestError.message : "Analytics unavailable."));
  }, []);

  return (
    <DashboardLayout>
      <div className="space-y-8"><div><p className="text-sm font-semibold uppercase tracking-[0.2em] text-indigo-400">Outcome reporting</p><h1 className="mt-3 text-4xl font-bold text-white">Analytics</h1><p className="mt-2 text-zinc-400">Measure the path from local outreach to a real trial-class enquiry.</p></div>{error && <p className="rounded-xl border border-amber-500/30 bg-amber-500/10 p-4 text-sm text-amber-200">{error}</p>}<div className="grid gap-5 md:grid-cols-2 xl:grid-cols-3">{metricLabels.map(([key, label]) => <div key={key} className="rounded-3xl border border-zinc-800 bg-zinc-900 p-6"><p className="text-sm text-zinc-500">{label}</p><p className="mt-3 text-4xl font-bold text-white">{summary?.metrics[key] ?? 0}</p></div>)}</div><div className="rounded-3xl border border-zinc-800 bg-zinc-900 p-6"><h2 className="text-xl font-bold text-white">Conversion checkpoint</h2><p className="mt-2 text-sm text-zinc-400">Qualified leads divided by recorded approved sends. This is an operating signal, not a guaranteed forecast.</p><p className="mt-5 text-5xl font-bold text-emerald-300">{summary?.conversion_rate ?? 0}%</p></div></div>
    </DashboardLayout>
  );
}
