"use client";

import { useEffect, useState } from "react";
import DashboardLayout from "@/components/layout/DashboardLayout";
import { getLeads, type Lead } from "@/services/aiService";

const columns = ["new", "qualified", "trial_enquiry", "converted"];

export default function LeadsPage() {
  const [leads, setLeads] = useState<Lead[]>([]);

  useEffect(() => { getLeads().then(setLeads).catch(() => setLeads([])); }, []);

  return <DashboardLayout><div className="space-y-8"><div><p className="text-sm font-semibold uppercase tracking-[0.2em] text-indigo-400">Outcome pipeline</p><h1 className="mt-3 text-4xl font-bold text-white">Leads</h1><p className="mt-2 text-zinc-400">Track a person’s next step without inventing results or promising conversion.</p></div><div className="grid gap-4 lg:grid-cols-4">{columns.map((status) => <section key={status} className="min-h-64 rounded-3xl border border-zinc-800 bg-zinc-900 p-4"><h2 className="text-sm font-semibold uppercase tracking-wide text-zinc-400">{status.replaceAll("_", " ")}</h2><div className="mt-4 space-y-3">{leads.filter((lead) => lead.status === status).map((lead) => <div key={lead.id} className="rounded-2xl bg-zinc-950 p-4"><p className="font-medium text-zinc-200">{lead.name}</p><p className="mt-1 text-xs text-zinc-500">{lead.source}</p></div>)}{leads.filter((lead) => lead.status === status).length === 0 && <p className="text-sm text-zinc-600">Empty</p>}</div></section>)}</div></div></DashboardLayout>;
}
