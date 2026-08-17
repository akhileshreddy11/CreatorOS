"use client";

import { useEffect, useState } from "react";
import type { FormEvent } from "react";
import DashboardLayout from "@/components/layout/DashboardLayout";
import { createOutreach, createProspect, getProspects, type Prospect } from "@/services/aiService";

export default function ProspectsPage() {
  const [prospects, setProspects] = useState<Prospect[]>([]);
  const [businessName, setBusinessName] = useState("");
  const [handle, setHandle] = useState("");
  const [audit, setAudit] = useState("");
  const [messageFor, setMessageFor] = useState<number | null>(null);
  const [message, setMessage] = useState("");
  const [notice, setNotice] = useState<string | null>(null);

  function loadProspects() {
    getProspects().then(setProspects).catch(() => setNotice("Start FastAPI to load prospects."));
  }

  useEffect(() => {
    getProspects().then(setProspects).catch(() => setNotice("Start FastAPI to load prospects."));
  }, []);

  async function handleCreate(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!businessName.trim()) return;
    try {
      await createProspect({ business_name: businessName, contact_handle: handle || undefined, audit_summary: audit || undefined });
      setBusinessName(""); setHandle(""); setAudit(""); setNotice("Prospect saved. Draft outreach only after reviewing the audit."); loadProspects();
    } catch (error) { setNotice(error instanceof Error ? error.message : "Could not save prospect."); }
  }

  async function handleOutreach(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (messageFor === null || !message.trim()) return;
    try { await createOutreach(messageFor, message); setMessage(""); setMessageFor(null); setNotice("Outreach draft created and placed in approval review."); } catch (error) { setNotice(error instanceof Error ? error.message : "Could not create outreach draft."); }
  }

  return <DashboardLayout><div className="space-y-8"><div><p className="text-sm font-semibold uppercase tracking-[0.2em] text-indigo-400">Prospect pipeline</p><h1 className="mt-3 text-4xl font-bold text-white">Local prospects</h1><p className="mt-2 text-zinc-400">Capture the 30-business research sprint without sending anything automatically.</p></div>{notice && <p className="rounded-xl border border-indigo-500/30 bg-indigo-500/10 p-4 text-sm text-indigo-200">{notice}</p>}<form onSubmit={handleCreate} className="grid gap-4 rounded-3xl border border-zinc-800 bg-zinc-900 p-6 md:grid-cols-3"><input value={businessName} onChange={(event) => setBusinessName(event.target.value)} placeholder="Gym business name" className="h-12 rounded-xl border border-zinc-700 bg-zinc-950 px-3 text-white outline-none focus:border-indigo-500" /><input value={handle} onChange={(event) => setHandle(event.target.value)} placeholder="Instagram / contact handle" className="h-12 rounded-xl border border-zinc-700 bg-zinc-950 px-3 text-white outline-none focus:border-indigo-500" /><input value={audit} onChange={(event) => setAudit(event.target.value)} placeholder="Short audit note" className="h-12 rounded-xl border border-zinc-700 bg-zinc-950 px-3 text-white outline-none focus:border-indigo-500" /><button type="submit" className="rounded-xl bg-indigo-600 px-4 py-3 font-semibold text-white hover:bg-indigo-500 md:col-span-3">Add prospect</button></form><div className="grid gap-5 lg:grid-cols-2">{prospects.length === 0 ? <div className="col-span-full rounded-3xl border border-dashed border-zinc-700 p-12 text-center text-zinc-500">No prospects recorded yet.</div> : prospects.map((prospect) => <article key={prospect.id} className="rounded-3xl border border-zinc-800 bg-zinc-900 p-6"><div className="flex items-start justify-between gap-4"><div><h2 className="text-xl font-semibold text-white">{prospect.business_name}</h2><p className="mt-1 text-sm text-zinc-500">{prospect.city} · {prospect.contact_handle || "No handle"}</p></div><span className="rounded-full bg-zinc-800 px-3 py-1 text-xs uppercase text-zinc-400">{prospect.status}</span></div>{prospect.audit_summary && <p className="mt-4 text-sm leading-6 text-zinc-400">{prospect.audit_summary}</p>}<button type="button" onClick={() => setMessageFor(prospect.id)} className="mt-5 rounded-xl border border-indigo-500/40 px-4 py-2 text-sm font-semibold text-indigo-300 hover:bg-indigo-500/10">Prepare outreach draft</button></article>)}</div>{messageFor !== null && <form onSubmit={handleOutreach} className="rounded-3xl border border-amber-500/30 bg-amber-500/5 p-6"><p className="text-sm font-semibold text-amber-200">Draft for prospect #{messageFor}</p><textarea value={message} onChange={(event) => setMessage(event.target.value)} rows={4} placeholder="Write a personalized, truthful message…" className="mt-4 w-full rounded-xl border border-zinc-700 bg-zinc-950 p-3 text-white outline-none focus:border-amber-400" /><div className="mt-4 flex gap-3"><button type="submit" className="rounded-xl bg-amber-500 px-4 py-2 font-semibold text-black">Save for approval</button><button type="button" onClick={() => setMessageFor(null)} className="rounded-xl border border-zinc-700 px-4 py-2 text-sm text-zinc-300">Cancel</button></div></form>}</div></DashboardLayout>;
}
