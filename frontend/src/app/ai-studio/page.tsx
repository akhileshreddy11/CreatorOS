"use client";

import { useState } from "react";
import DashboardLayout from "@/components/layout/DashboardLayout";
import LengthSelector from "@/components/ai-studio/LengthSelector";
import PlatformSelector from "@/components/ai-studio/PlatformSelector";
import PromptEditor from "@/components/ai-studio/PromptEditor";
import TemplateCards from "@/components/ai-studio/TemplateCards";
import { usePrompt } from "@/context/PromptContext";
import {
  approveDraft,
  generateContent,
  rejectDraft,
  type GenerationResponse,
} from "@/services/aiService";

export default function AIStudioPage() {
  const {
    prompt,
    platform,
    length,
    language,
    setLanguage,
    niche,
    setNiche,
    city,
    setCity,
    objective,
    setObjective,
    offer,
    setOffer,
    tone,
    setTone,
  } = usePrompt();
  const [result, setResult] = useState<GenerationResponse | null>(null);
  const [isGenerating, setIsGenerating] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [copied, setCopied] = useState(false);

  async function handleGenerate() {
    if (!prompt.trim()) {
      setError("Choose a template or describe the content you want to create first.");
      return;
    }

    setIsGenerating(true);
    setError(null);
    setCopied(false);

    try {
      const generated = await generateContent({
        prompt,
        platform,
        length,
        niche,
        city,
        language,
        objective,
        offer,
        tone,
      });
      setResult(generated);
    } catch (requestError) {
      setError(requestError instanceof Error ? requestError.message : "Generation failed.");
    } finally {
      setIsGenerating(false);
    }
  }

  async function handleCopy() {
    if (!result) return;
    await navigator.clipboard.writeText(result.response);
    setCopied(true);
  }

  async function handleApproval(action: "approve" | "reject") {
    if (!result?.draft_id) return;
    try {
      const draft = action === "approve"
        ? await approveDraft(result.draft_id)
        : await rejectDraft(result.draft_id);
      setResult({ ...result, approval_status: draft.status });
      setError(null);
    } catch (requestError) {
      setError(requestError instanceof Error ? requestError.message : "Approval update failed.");
    }
  }

  return (
    <DashboardLayout>
      <div className="space-y-10">
        <div>
          <p className="text-sm font-semibold uppercase tracking-[0.25em] text-indigo-400">
            Approval-gated content operations
          </p>
          <h1 className="mt-3 text-4xl font-bold text-white">AI Studio</h1>
          <p className="mt-2 max-w-2xl text-zinc-400">
            Create useful local content for Hyderabad gyms, review claims, and approve every customer-facing action.
          </p>
        </div>

        <TemplateCards />

        <div className="grid gap-8 lg:grid-cols-2">
          <div className="space-y-6 rounded-3xl border border-zinc-800 bg-zinc-900 p-8">
            <PromptEditor />

            <div className="grid gap-4 sm:grid-cols-2">
              <label className="space-y-2 text-sm font-medium text-zinc-300">
                Niche
                <input value={niche} onChange={(event) => setNiche(event.target.value)} className="h-12 w-full rounded-xl border border-zinc-800 bg-zinc-950 px-3 text-white outline-none focus:border-indigo-500" />
              </label>
              <label className="space-y-2 text-sm font-medium text-zinc-300">
                City
                <input value={city} onChange={(event) => setCity(event.target.value)} className="h-12 w-full rounded-xl border border-zinc-800 bg-zinc-950 px-3 text-white outline-none focus:border-indigo-500" />
              </label>
              <label className="space-y-2 text-sm font-medium text-zinc-300">
                Language
                <select value={language} onChange={(event) => setLanguage(event.target.value)} className="h-12 w-full rounded-xl border border-zinc-800 bg-zinc-950 px-3 text-white outline-none focus:border-indigo-500">
                  <option value="en">English / Hinglish</option>
                  <option value="te">Telugu</option>
                  <option value="hi">Hindi</option>
                </select>
              </label>
              <label className="space-y-2 text-sm font-medium text-zinc-300">
                Tone
                <select value={tone} onChange={(event) => setTone(event.target.value)} className="h-12 w-full rounded-xl border border-zinc-800 bg-zinc-950 px-3 text-white outline-none focus:border-indigo-500">
                  <option>Helpful and local</option>
                  <option>Direct and energetic</option>
                  <option>Warm and encouraging</option>
                </select>
              </label>
            </div>

            <PlatformSelector />
            <LengthSelector />

            <label className="space-y-2 text-sm font-medium text-zinc-300">
              Business objective
              <input value={objective} onChange={(event) => setObjective(event.target.value)} className="h-12 w-full rounded-xl border border-zinc-800 bg-zinc-950 px-3 text-white outline-none focus:border-indigo-500" />
            </label>
            <label className="space-y-2 text-sm font-medium text-zinc-300">
              Offer and CTA context
              <textarea value={offer} onChange={(event) => setOffer(event.target.value)} rows={3} className="w-full rounded-xl border border-zinc-800 bg-zinc-950 px-3 py-3 text-white outline-none focus:border-indigo-500" />
            </label>

            {error && <p className="rounded-xl border border-red-500/30 bg-red-500/10 p-3 text-sm text-red-300">{error}</p>}

            <button
              type="button"
              onClick={handleGenerate}
              disabled={isGenerating}
              className="w-full rounded-2xl bg-gradient-to-r from-indigo-600 via-violet-600 to-purple-600 py-4 text-lg font-semibold text-white transition hover:scale-[1.02] disabled:cursor-wait disabled:opacity-60"
            >
              {isGenerating ? "Creating a safe draft…" : "✨ Generate with AI"}
            </button>
          </div>

          <div className="rounded-3xl border border-zinc-800 bg-zinc-900 p-8">
            <div className="flex items-start justify-between gap-4">
              <div>
                <h2 className="text-2xl font-bold text-white">AI Output</h2>
                <p className="mt-2 text-sm text-zinc-400">Every generated asset starts in review and cannot publish automatically.</p>
              </div>
              {result && <span className="rounded-full bg-amber-500/15 px-3 py-1 text-xs font-semibold uppercase tracking-wide text-amber-300">{result.approval_status}</span>}
            </div>

            {result ? (
              <div className="mt-6 space-y-5">
                <div className="min-h-[420px] whitespace-pre-wrap rounded-2xl border border-zinc-800 bg-zinc-950 p-5 text-sm leading-7 text-zinc-200">{result.response}</div>
                <div className="rounded-2xl border border-zinc-800 bg-zinc-950 p-4 text-sm">
                  <div className="flex items-center justify-between text-zinc-300">
                    <span>Claim-safety score</span>
                    <span className="font-semibold text-emerald-300">{result.validation.quality_score ?? "—"}/100</span>
                  </div>
                  {!!result.validation.warnings?.length && <p className="mt-2 text-amber-300">{result.validation.warnings.join(" ")}</p>}
                  {!!result.validation.errors?.length && <p className="mt-2 text-red-300">{result.validation.errors.join(" ")}</p>}
                </div>
                <div className="flex flex-wrap gap-3">
                  <button type="button" onClick={handleCopy} className="rounded-xl border border-zinc-700 px-4 py-2 text-sm font-semibold text-white hover:bg-zinc-800">{copied ? "Copied" : "Copy draft"}</button>
                  <button type="button" onClick={() => handleApproval("approve")} disabled={result.approval_status === "approved"} className="rounded-xl bg-emerald-600 px-4 py-2 text-sm font-semibold text-white hover:bg-emerald-500 disabled:opacity-50">Approve for publishing</button>
                  <button type="button" onClick={() => handleApproval("reject")} disabled={result.approval_status === "rejected"} className="rounded-xl border border-red-500/40 px-4 py-2 text-sm font-semibold text-red-300 hover:bg-red-500/10 disabled:opacity-50">Reject</button>
                </div>
              </div>
            ) : (
              <div className="mt-6 flex h-[650px] items-center justify-center rounded-2xl border border-dashed border-zinc-700 px-8 text-center text-zinc-500">
                Choose a template, add a local business angle, and generate a reviewable draft.
              </div>
            )}
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
}
