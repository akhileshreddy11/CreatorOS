"use client";

import { useEffect, useState } from "react";
import DashboardLayout from "@/components/layout/DashboardLayout";
import { getTrends } from "@/services/aiService";

export default function TrendsPage() {
  const [trends, setTrends] = useState<Array<{ title: string; angle: string; status: string }>>([]);

  useEffect(() => {
    getTrends().then(setTrends).catch(() => setTrends([]));
  }, []);

  return <DashboardLayout><div className="space-y-8"><div><p className="text-sm font-semibold uppercase tracking-[0.2em] text-indigo-400">Research queue</p><h1 className="mt-3 text-4xl font-bold text-white">Trends & ideas</h1><p className="mt-2 text-zinc-400">Use these local angles as hypotheses and validate them with the business owner before publishing.</p></div><div className="grid gap-5 md:grid-cols-2">{trends.map((trend) => <article key={trend.title} className="rounded-3xl border border-zinc-800 bg-zinc-900 p-6"><span className="text-xs uppercase text-indigo-300">{trend.status}</span><h2 className="mt-3 text-xl font-semibold text-white">{trend.title}</h2><p className="mt-3 text-sm leading-6 text-zinc-400">{trend.angle}</p></article>)}{trends.length === 0 && <div className="col-span-full rounded-3xl border border-dashed border-zinc-700 p-12 text-center text-zinc-500">Start FastAPI to load the research queue.</div>}</div></div></DashboardLayout>;
}
