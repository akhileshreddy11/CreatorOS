"use client";

import { useEffect, useState } from "react";
import { CalendarCheck2, MessageCircle, ShieldCheck, Target, Users, Video } from "lucide-react";
import { getDashboardSummary, type DashboardSummary } from "@/services/aiService";

const cards = [
  { key: "trial_class_enquiries", label: "Trial enquiries", icon: Target, color: "from-emerald-500 to-teal-500" },
  { key: "qualified_leads", label: "Qualified leads", icon: Users, color: "from-indigo-500 to-violet-500" },
  { key: "appointments", label: "Appointments", icon: CalendarCheck2, color: "from-orange-500 to-amber-500" },
  { key: "pending_approvals", label: "Pending approvals", icon: ShieldCheck, color: "from-cyan-500 to-blue-500" },
] as const;

export default function CreatorInsights() {
  const [summary, setSummary] = useState<DashboardSummary | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    getDashboardSummary().then(setSummary).catch((requestError) => {
      setError(requestError instanceof Error ? requestError.message : "Dashboard data unavailable.");
    });
  }, []);

  return (
    <section className="space-y-4">
      <div className="flex items-end justify-between gap-4">
        <div>
          <p className="text-sm font-semibold uppercase tracking-[0.2em] text-indigo-400">Operating pulse</p>
          <h2 className="mt-2 text-2xl font-bold text-white">Growth signals that matter</h2>
        </div>
        {summary && <p className="text-sm text-zinc-400">{summary.profile?.niche} · {summary.profile?.city}</p>}
      </div>

      {error && <p className="rounded-xl border border-amber-500/30 bg-amber-500/10 p-3 text-sm text-amber-200">Backend is offline. Start FastAPI to load live metrics.</p>}
      <div className="grid gap-6 md:grid-cols-2 xl:grid-cols-4">
        {cards.map((item) => {
          const Icon = item.icon;
          const value = summary?.metrics[item.key] ?? 0;
          return (
            <div key={item.key} className="group rounded-3xl border border-zinc-800 bg-zinc-900/70 p-6 backdrop-blur-xl transition-all duration-300 hover:-translate-y-1 hover:border-indigo-500">
              <div className="flex items-center justify-between">
                <div className={`rounded-2xl bg-gradient-to-br ${item.color} p-3`}><Icon className="text-white" size={22} /></div>
                <span className="text-xs text-zinc-500">live</span>
              </div>
              <h3 className="mt-6 text-sm text-zinc-400">{item.label}</h3>
              <p className="mt-2 text-4xl font-bold text-white">{value}</p>
            </div>
          );
        })}
      </div>

      {summary && (
        <div className="grid gap-4 rounded-3xl border border-zinc-800 bg-zinc-900/60 p-5 text-sm text-zinc-300 sm:grid-cols-3">
          <span><MessageCircle className="mr-2 inline text-indigo-400" size={16} />{summary.metrics.replies} replies</span>
          <span><Video className="mr-2 inline text-violet-400" size={16} />{summary.metrics.contacted} businesses contacted</span>
          <span><span className="mr-2 text-emerald-400">{summary.conversion_rate}%</span>qualified conversion rate</span>
        </div>
      )}
    </section>
  );
}
