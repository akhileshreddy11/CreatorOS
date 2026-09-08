"use client";

import { useEffect, useState } from "react";
import DashboardLayout from "@/components/layout/DashboardLayout";
import {
  approveDraft,
  getDrafts,
  rejectDraft,
  type Draft,
} from "@/services/aiService";

export default function DraftsPage() {
  const [drafts, setDrafts] = useState<Draft[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [updatingId, setUpdatingId] = useState<number | null>(null);

  async function loadDrafts() {
    try {
      setError(null);
      setLoading(true);

      const data = await getDrafts();

      setDrafts(data);
    } catch (requestError) {
      setError(
        requestError instanceof Error
          ? requestError.message
          : "Could not load drafts."
      );
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadDrafts();
  }, []);

  async function updateDraft(
    id: number,
    action: "approve" | "reject"
  ) {
    try {
      setError(null);
      setUpdatingId(id);

      if (action === "approve") {
        await approveDraft(id);
      } else {
        await rejectDraft(id);
      }

      await loadDrafts();
    } catch (requestError) {
      setError(
        requestError instanceof Error
          ? requestError.message
          : "Could not update draft."
      );
    } finally {
      setUpdatingId(null);
    }
  }

  return (
    <DashboardLayout>
      <div className="space-y-8">

        {/* HEADER */}
        <div>
          <p className="text-sm font-semibold uppercase tracking-[0.2em] text-indigo-400">
            Content operations
          </p>

          <h1 className="mt-3 text-4xl font-bold text-white">
            Draft review
          </h1>

          <p className="mt-2 text-zinc-400">
            Review AI-generated content before anything is published or sent.
          </p>
        </div>

        {/* ERROR */}
        {error && (
          <div className="rounded-2xl border border-red-500/30 bg-red-500/10 p-5">
            <p className="text-sm font-semibold text-red-300">
              Unable to load drafts
            </p>

            <p className="mt-2 text-sm text-red-400">
              {error}
            </p>

            <button
              type="button"
              onClick={loadDrafts}
              className="mt-4 rounded-xl border border-red-500/30 px-4 py-2 text-sm font-semibold text-red-300 hover:bg-red-500/10"
            >
              Try again
            </button>
          </div>
        )}

        {/* LOADING */}
        {loading && (
          <div className="rounded-3xl border border-zinc-800 bg-zinc-900 p-12 text-center">
            <div className="mx-auto h-8 w-8 animate-spin rounded-full border-2 border-zinc-700 border-t-indigo-400" />

            <p className="mt-5 text-sm font-medium text-zinc-300">
              Loading your drafts...
            </p>

            <p className="mt-2 text-xs text-zinc-500">
              Connecting to CreatorOS backend
            </p>
          </div>
        )}

        {/* EMPTY */}
        {!loading && !error && drafts.length === 0 && (
          <div className="rounded-3xl border border-dashed border-zinc-700 p-12 text-center">
            <p className="text-lg font-semibold text-zinc-300">
              No drafts yet
            </p>

            <p className="mt-2 text-sm text-zinc-500">
              Create a mission or generate content in AI Studio.
            </p>
          </div>
        )}

        {/* DRAFTS */}
        {!loading && drafts.length > 0 && (
          <div className="space-y-5">

            {drafts.map((draft) => (
              <article
                key={draft.id}
                className="rounded-3xl border border-zinc-800 bg-zinc-900 p-6 transition hover:border-zinc-700"
              >

                {/* TOP */}
                <div className="flex flex-wrap items-start justify-between gap-4">

                  <div>
                    <div className="flex flex-wrap items-center gap-2">
                      <span className="text-xs font-semibold uppercase tracking-wide text-indigo-300">
                        {draft.platform}
                      </span>

                      <span className="text-zinc-600">
                        •
                      </span>

                      <span className="text-xs uppercase tracking-wide text-zinc-500">
                        {draft.language}
                      </span>
                    </div>

                    <h2 className="mt-2 text-xl font-semibold text-white">
                      {draft.title}
                    </h2>

                    <p className="mt-1 text-xs text-zinc-600">
                      Draft #{draft.id}
                    </p>
                  </div>

                  <span
                    className={`rounded-full px-3 py-1 text-xs font-semibold uppercase ${
                      draft.status === "approved"
                        ? "bg-emerald-500/10 text-emerald-400"
                        : draft.status === "rejected"
                        ? "bg-red-500/10 text-red-400"
                        : "bg-amber-500/10 text-amber-400"
                    }`}
                  >
                    {draft.status.replace("_", " ")}
                  </span>
                </div>

                {/* CONTENT */}
                <div className="mt-6 space-y-4">

                  {/* HOOK */}
                  {draft.content.hook && (
                    <div>
                      <p className="mb-2 text-xs font-semibold uppercase tracking-[0.15em] text-indigo-400">
                        Hook
                      </p>

                      <div className="rounded-2xl bg-zinc-950 p-4 text-sm leading-6 text-zinc-200">
                        {draft.content.hook}
                      </div>
                    </div>
                  )}

                  {/* SCRIPT */}
                  {draft.content.script && (
                    <div>
                      <p className="mb-2 text-xs font-semibold uppercase tracking-[0.15em] text-indigo-400">
                        Script
                      </p>

                      <div className="whitespace-pre-wrap rounded-2xl bg-zinc-950 p-4 text-sm leading-7 text-zinc-300">
                        {draft.content.script}
                      </div>
                    </div>
                  )}

                  {/* CAPTION */}
                  {draft.content.caption && (
                    <div>
                      <p className="mb-2 text-xs font-semibold uppercase tracking-[0.15em] text-indigo-400">
                        Caption
                      </p>

                      <div className="rounded-2xl bg-zinc-950 p-4 text-sm leading-6 text-zinc-300">
                        {draft.content.caption}
                      </div>
                    </div>
                  )}

                  {/* CTA */}
                  {draft.content.cta && (
                    <div>
                      <p className="mb-2 text-xs font-semibold uppercase tracking-[0.15em] text-indigo-400">
                        Call to action
                      </p>

                      <div className="rounded-2xl bg-zinc-950 p-4 text-sm font-medium text-zinc-200">
                        {draft.content.cta}
                      </div>
                    </div>
                  )}

                  {/* HASHTAGS */}
                  {draft.content.hashtags && draft.content.hashtags.length > 0 && (
                    <div className="flex flex-wrap gap-2">
                      {draft.content.hashtags.map((hashtag) => (
                        <span
                          key={hashtag}
                          className="rounded-lg bg-indigo-500/10 px-3 py-1 text-xs text-indigo-300"
                        >
                          {hashtag}
                        </span>
                      ))}
                    </div>
                  )}

                  {/* PRODUCT PLAYBOOK FIELDS IF PRESENT */}
                  {draft.content.product_name && (
                    <div className="space-y-3 rounded-2xl border border-zinc-800 bg-zinc-950 p-4">
                      <p className="text-xs font-bold uppercase tracking-wider text-violet-400">Campaign Product Playbook</p>
                      <h3 className="text-base font-bold text-white">{draft.content.product_name}</h3>
                      {draft.content.tagline && <p className="text-xs text-zinc-400 italic">"{draft.content.tagline}"</p>}
                      {draft.content.description && <p className="text-xs text-zinc-300">{draft.content.description}</p>}
                      {draft.content.marketing_angle && (
                        <p className="text-xs text-indigo-300">
                          <span className="font-semibold text-zinc-400">Angle: </span>
                          {draft.content.marketing_angle}
                        </p>
                      )}
                    </div>
                  )}
                </div>

                {/* VALIDATION */}
                <div className="mt-6 rounded-2xl border border-zinc-800 bg-zinc-950 p-4">

                  <div className="flex flex-wrap items-center justify-between gap-3">

                    <div>
                      <p className="text-xs font-semibold uppercase tracking-[0.15em] text-zinc-500">
                        AI validation
                      </p>

                      <p className="mt-1 text-sm font-medium text-emerald-400">
                        ✓ Validation passed
                      </p>
                    </div>

                    <div className="text-right">
                      <p className="text-xs text-zinc-500">
                        Quality score
                      </p>

                      <p className="text-xl font-bold text-white">
                        {draft.validation.quality_score ?? "—"}
                        <span className="text-sm text-zinc-600">
                          /100
                        </span>
                      </p>
                    </div>

                  </div>

                  <p className="mt-3 text-xs text-zinc-600">
                    This content has passed automated validation but still
                    requires owner approval before publishing.
                  </p>
                </div>

                {/* ACTIONS */}
                <div className="mt-6 flex flex-wrap items-center justify-between gap-4">

                  <div className="text-xs text-zinc-600">
                    Approval required before external use
                  </div>

                  <div className="flex gap-3">

                    <button
                      type="button"
                      onClick={() =>
                        updateDraft(draft.id, "reject")
                      }
                      disabled={
                        updatingId === draft.id ||
                        draft.status === "rejected"
                      }
                      className="rounded-xl border border-red-500/30 px-5 py-2.5 text-sm font-semibold text-red-300 transition hover:bg-red-500/10 disabled:cursor-not-allowed disabled:opacity-40"
                    >
                      {updatingId === draft.id
                        ? "Updating..."
                        : "Reject"}
                    </button>

                    <button
                      type="button"
                      onClick={() =>
                        updateDraft(draft.id, "approve")
                      }
                      disabled={
                        updatingId === draft.id ||
                        draft.status === "approved"
                      }
                      className="rounded-xl bg-emerald-600 px-5 py-2.5 text-sm font-semibold text-white transition hover:bg-emerald-500 disabled:cursor-not-allowed disabled:opacity-40"
                    >
                      {updatingId === draft.id
                        ? "Updating..."
                        : "Approve"}
                    </button>

                  </div>
                </div>

              </article>
            ))}

          </div>
        )}

      </div>
    </DashboardLayout>
  );
}