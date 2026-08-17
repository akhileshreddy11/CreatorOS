"use client";

import { useEffect, useState } from "react";
import DashboardLayout from "@/components/layout/DashboardLayout";
import { API_URL } from "@/services/aiService";

type Profile = { name: string; niche: string; city: string; primary_language: string; supported_languages: string[]; offer: string; primary_kpi: string; monthly_targets: Record<string, string | number>; approval_policy: Record<string, string> };

export default function SettingsPage() {
  const [profile, setProfile] = useState<Profile | null>(null);
  const [error, setError] = useState(false);

  useEffect(() => {
    fetch(`${API_URL}/business-profile`).then((response) => { if (!response.ok) throw new Error(); return response.json() as Promise<Profile>; }).then(setProfile).catch(() => setError(true));
  }, []);

  return <DashboardLayout><div className="space-y-8"><div><p className="text-sm font-semibold uppercase tracking-[0.2em] text-indigo-400">Operating configuration</p><h1 className="mt-3 text-4xl font-bold text-white">Settings</h1><p className="mt-2 text-zinc-400">Keep the niche, offer, KPI, and approval boundaries explicit.</p></div>{error && <p className="rounded-xl border border-amber-500/30 bg-amber-500/10 p-4 text-sm text-amber-200">Start FastAPI to load settings.</p>}{profile && <div className="grid gap-6 lg:grid-cols-2"><section className="rounded-3xl border border-zinc-800 bg-zinc-900 p-6"><h2 className="text-xl font-bold text-white">Business profile</h2><dl className="mt-5 space-y-4 text-sm"><div><dt className="text-zinc-500">Niche & city</dt><dd className="mt-1 text-zinc-200">{profile.niche} · {profile.city}</dd></div><div><dt className="text-zinc-500">Primary language</dt><dd className="mt-1 text-zinc-200">{profile.primary_language} ({profile.supported_languages.join(", ")})</dd></div><div><dt className="text-zinc-500">Offer</dt><dd className="mt-1 leading-6 text-zinc-200">{profile.offer}</dd></div><div><dt className="text-zinc-500">Primary KPI</dt><dd className="mt-1 text-emerald-300">{profile.primary_kpi}</dd></div></dl></section><section className="rounded-3xl border border-zinc-800 bg-zinc-900 p-6"><h2 className="text-xl font-bold text-white">Approval policy</h2><div className="mt-5 space-y-3">{Object.entries(profile.approval_policy).map(([action, policy]) => <div key={action} className="flex items-center justify-between gap-4 rounded-2xl bg-zinc-950 p-4"><span className="text-sm capitalize text-zinc-300">{action.replaceAll("_", " ")}</span><span className="text-xs font-semibold uppercase text-amber-300">{policy}</span></div>)}</div></section></div>}</div></DashboardLayout>;
}
