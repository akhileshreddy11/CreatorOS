"use client";

import { useEffect, useState } from "react";
import type { FormEvent } from "react";

import DashboardLayout from "@/components/layout/DashboardLayout";

import {
  createOutreach,
  createProspect,
  getProspects,
  type Prospect,
} from "@/services/aiService";

export default function ProspectsPage() {
  const [prospects, setProspects] = useState<Prospect[]>([]);

  const [businessName, setBusinessName] = useState("");
  const [handle, setHandle] = useState("");
  const [audit, setAudit] = useState("");

  const [messageFor, setMessageFor] = useState<number | null>(null);
  const [message, setMessage] = useState("");

  const [notice, setNotice] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const [loading, setLoading] = useState(true);
  const [savingProspect, setSavingProspect] = useState(false);
  const [savingOutreach, setSavingOutreach] = useState(false);

  async function loadProspects() {
    try {
      setError(null);
      setLoading(true);

      const data = await getProspects();

      setProspects(data);
    } catch (requestError) {
      setError(
        requestError instanceof Error
          ? requestError.message
          : "Could not load prospects.",
      );
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadProspects();
  }, []);

  async function handleCreate(
    event: FormEvent<HTMLFormElement>,
  ) {
    event.preventDefault();

    if (!businessName.trim()) {
      setError("Business name is required.");
      return;
    }

    try {
      setSavingProspect(true);
      setError(null);
      setNotice(null);

      await createProspect({
        business_name: businessName.trim(),
        contact_handle: handle.trim() || undefined,
        audit_summary: audit.trim() || undefined,
      });

      setBusinessName("");
      setHandle("");
      setAudit("");

      setNotice(
        "Prospect saved. Review the business before preparing outreach.",
      );

      await loadProspects();
    } catch (requestError) {
      setError(
        requestError instanceof Error
          ? requestError.message
          : "Could not save prospect.",
      );
    } finally {
      setSavingProspect(false);
    }
  }

  async function handleOutreach(
    event: FormEvent<HTMLFormElement>,
  ) {
    event.preventDefault();

    if (messageFor === null || !message.trim()) {
      setError("Write an outreach message before saving it.");
      return;
    }

    try {
      setSavingOutreach(true);
      setError(null);
      setNotice(null);

      await createOutreach(
        messageFor,
        message.trim(),
      );

      setMessage("");
      setMessageFor(null);

      setNotice(
        "Outreach draft created and placed in approval review.",
      );
    } catch (requestError) {
      setError(
        requestError instanceof Error
          ? requestError.message
          : "Could not create outreach draft.",
      );
    } finally {
      setSavingOutreach(false);
    }
  }

  const newProspects = prospects.filter(
    (prospect) => prospect.status === "new",
  ).length;

  const contactedProspects = prospects.filter(
    (prospect) =>
      prospect.status === "contacted",
  ).length;

  return (
    <DashboardLayout>
      <div className="space-y-8">

        {/* HEADER */}
        <div>
          <p className="text-sm font-semibold uppercase tracking-[0.2em] text-indigo-400">
            Prospect pipeline
          </p>

          <h1 className="mt-3 text-4xl font-bold text-white">
            Local prospects
          </h1>

          <p className="mt-2 max-w-2xl text-zinc-400">
            Build the local-business pipeline, review your research,
            and prepare personalized outreach without sending anything
            automatically.
          </p>
        </div>

        {/* NOTICES */}
        {notice && (
          <div className="rounded-2xl border border-emerald-500/20 bg-emerald-500/5 p-4">
            <p className="text-sm font-medium text-emerald-300">
              ✓ {notice}
            </p>
          </div>
        )}

        {error && (
          <div className="rounded-2xl border border-red-500/20 bg-red-500/5 p-4">
            <p className="text-sm font-semibold text-red-300">
              Something went wrong
            </p>

            <p className="mt-1 text-sm text-red-400">
              {error}
            </p>

            <button
              type="button"
              onClick={loadProspects}
              className="mt-3 rounded-lg border border-red-500/30 px-3 py-2 text-xs font-semibold text-red-300 hover:bg-red-500/10"
            >
              Retry
            </button>
          </div>
        )}

        {/* PIPELINE STATS */}
        <div className="grid gap-4 sm:grid-cols-3">

          <div className="rounded-2xl border border-zinc-800 bg-zinc-900 p-5">
            <p className="text-xs font-semibold uppercase tracking-[0.15em] text-zinc-500">
              Total prospects
            </p>

            <p className="mt-3 text-3xl font-bold text-white">
              {prospects.length}
            </p>

            <p className="mt-1 text-xs text-zinc-600">
              Businesses in pipeline
            </p>
          </div>

          <div className="rounded-2xl border border-zinc-800 bg-zinc-900 p-5">
            <p className="text-xs font-semibold uppercase tracking-[0.15em] text-zinc-500">
              New
            </p>

            <p className="mt-3 text-3xl font-bold text-indigo-400">
              {newProspects}
            </p>

            <p className="mt-1 text-xs text-zinc-600">
              Awaiting next action
            </p>
          </div>

          <div className="rounded-2xl border border-zinc-800 bg-zinc-900 p-5">
            <p className="text-xs font-semibold uppercase tracking-[0.15em] text-zinc-500">
              Contacted
            </p>

            <p className="mt-3 text-3xl font-bold text-emerald-400">
              {contactedProspects}
            </p>

            <p className="mt-1 text-xs text-zinc-600">
              Outreach already initiated
            </p>
          </div>

        </div>

        {/* ADD PROSPECT */}
        <section className="rounded-3xl border border-zinc-800 bg-zinc-900 p-6">

          <div className="mb-5">
            <p className="text-xs font-semibold uppercase tracking-[0.2em] text-indigo-400">
              Research pipeline
            </p>

            <h2 className="mt-2 text-xl font-semibold text-white">
              Add a local business
            </h2>

            <p className="mt-1 text-sm text-zinc-500">
              Record the business and any research you already have.
            </p>
          </div>

          <form
            onSubmit={handleCreate}
            className="grid gap-4 md:grid-cols-2"
          >

            <div>
              <label className="mb-2 block text-xs font-medium text-zinc-500">
                Business name
              </label>

              <input
                value={businessName}
                onChange={(event) =>
                  setBusinessName(event.target.value)
                }
                placeholder="Example: Hyderabad Fitness Club"
                className="h-12 w-full rounded-xl border border-zinc-700 bg-zinc-950 px-4 text-sm text-white outline-none transition placeholder:text-zinc-700 focus:border-indigo-500"
              />
            </div>

            <div>
              <label className="mb-2 block text-xs font-medium text-zinc-500">
                Contact / Instagram
              </label>

              <input
                value={handle}
                onChange={(event) =>
                  setHandle(event.target.value)
                }
                placeholder="@businesshandle"
                className="h-12 w-full rounded-xl border border-zinc-700 bg-zinc-950 px-4 text-sm text-white outline-none transition placeholder:text-zinc-700 focus:border-indigo-500"
              />
            </div>

            <div className="md:col-span-2">
              <label className="mb-2 block text-xs font-medium text-zinc-500">
                Research / audit note
              </label>

              <textarea
                value={audit}
                onChange={(event) =>
                  setAudit(event.target.value)
                }
                rows={3}
                placeholder="What did you notice about this business?"
                className="w-full rounded-xl border border-zinc-700 bg-zinc-950 p-4 text-sm text-white outline-none transition placeholder:text-zinc-700 focus:border-indigo-500"
              />
            </div>

            <button
              type="submit"
              disabled={savingProspect}
              className="rounded-xl bg-indigo-600 px-5 py-3 text-sm font-semibold text-white transition hover:bg-indigo-500 disabled:cursor-not-allowed disabled:opacity-50 md:col-span-2"
            >
              {savingProspect
                ? "Saving prospect..."
                : "Add Prospect"}
            </button>

          </form>
        </section>

        {/* PROSPECT LIST */}
        <section>

          <div className="mb-5 flex flex-wrap items-end justify-between gap-3">

            <div>
              <p className="text-xs font-semibold uppercase tracking-[0.2em] text-zinc-500">
                Business database
              </p>

              <h2 className="mt-2 text-2xl font-bold text-white">
                Prospects
              </h2>
            </div>

            <button
              type="button"
              onClick={loadProspects}
              disabled={loading}
              className="rounded-xl border border-zinc-700 px-4 py-2 text-sm font-medium text-zinc-300 hover:bg-zinc-900 disabled:opacity-50"
            >
              {loading ? "Refreshing..." : "Refresh"}
            </button>

          </div>

          {loading ? (
            <div className="rounded-3xl border border-zinc-800 bg-zinc-900 p-12 text-center">
              <div className="mx-auto h-8 w-8 animate-spin rounded-full border-2 border-zinc-700 border-t-indigo-400" />

              <p className="mt-4 text-sm text-zinc-400">
                Loading prospects...
              </p>
            </div>
          ) : prospects.length === 0 ? (
            <div className="rounded-3xl border border-dashed border-zinc-700 p-12 text-center">
              <p className="text-lg font-semibold text-zinc-300">
                No prospects yet
              </p>

              <p className="mt-2 text-sm text-zinc-500">
                Add your first local business above to start the pipeline.
              </p>
            </div>
          ) : (
            <div className="grid gap-5 lg:grid-cols-2">

              {prospects.map((prospect) => (
                <article
                  key={prospect.id}
                  className="rounded-3xl border border-zinc-800 bg-zinc-900 p-6 transition hover:border-zinc-700"
                >

                  {/* CARD HEADER */}
                  <div className="flex items-start justify-between gap-4">

                    <div className="min-w-0">

                      <p className="text-xs font-semibold uppercase tracking-[0.15em] text-indigo-400">
                        Prospect #{prospect.id}
                      </p>

                      <h3 className="mt-2 truncate text-xl font-semibold text-white">
                        {prospect.business_name}
                      </h3>

                      <p className="mt-1 text-sm text-zinc-500">
                        {prospect.city}
                        {" · "}
                        {prospect.contact_handle || "No contact handle"}
                      </p>

                    </div>

                    <span
                      className={`shrink-0 rounded-full px-3 py-1 text-xs font-semibold uppercase ${
                        prospect.status === "contacted"
                          ? "bg-emerald-500/10 text-emerald-400"
                          : prospect.status === "qualified"
                            ? "bg-indigo-500/10 text-indigo-400"
                            : "bg-zinc-800 text-zinc-400"
                      }`}
                    >
                      {prospect.status}
                    </span>

                  </div>

                  {/* AUDIT */}
                  <div className="mt-5 rounded-2xl bg-zinc-950 p-4">

                    <p className="text-xs font-semibold uppercase tracking-[0.15em] text-zinc-600">
                      Research / audit
                    </p>

                    {prospect.audit_summary ? (
                      <p className="mt-2 text-sm leading-6 text-zinc-400">
                        {prospect.audit_summary}
                      </p>
                    ) : (
                      <p className="mt-2 text-sm text-zinc-600">
                        No audit has been recorded yet.
                      </p>
                    )}

                  </div>

                  {/* ACTION */}
                  <div className="mt-5 flex flex-wrap items-center justify-between gap-3">

                    <p className="text-xs text-zinc-600">
                      Outreach remains approval-gated.
                    </p>

                    <button
                      type="button"
                      onClick={() => {
                        setMessageFor(prospect.id);
                        setMessage("");
                        setError(null);
                      }}
                      className="rounded-xl border border-indigo-500/40 px-4 py-2 text-sm font-semibold text-indigo-300 transition hover:bg-indigo-500/10"
                    >
                      Prepare outreach
                    </button>

                  </div>

                </article>
              ))}

            </div>
          )}

        </section>

        {/* OUTREACH COMPOSER */}
        {messageFor !== null && (
          <section className="rounded-3xl border border-amber-500/30 bg-amber-500/5 p-6">

            <div className="flex flex-wrap items-start justify-between gap-4">

              <div>
                <p className="text-xs font-semibold uppercase tracking-[0.2em] text-amber-400">
                  Approval-gated outreach
                </p>

                <h2 className="mt-2 text-xl font-semibold text-white">
                  Prepare message
                </h2>

                <p className="mt-1 text-sm text-zinc-500">
                  Prospect #{messageFor}
                </p>
              </div>

              <span className="rounded-full border border-amber-500/20 bg-amber-500/10 px-3 py-1 text-xs font-semibold text-amber-300">
                Owner approval required
              </span>

            </div>

            <form
              onSubmit={handleOutreach}
              className="mt-5"
            >

              <textarea
                value={message}
                onChange={(event) =>
                  setMessage(event.target.value)
                }
                rows={6}
                placeholder="Write a personalized, truthful message..."
                className="w-full rounded-2xl border border-zinc-700 bg-zinc-950 p-4 text-sm leading-6 text-white outline-none placeholder:text-zinc-700 focus:border-amber-400"
              />

              <div className="mt-4 flex flex-wrap gap-3">

                <button
                  type="submit"
                  disabled={savingOutreach}
                  className="rounded-xl bg-amber-500 px-5 py-2.5 text-sm font-semibold text-black transition hover:bg-amber-400 disabled:cursor-not-allowed disabled:opacity-50"
                >
                  {savingOutreach
                    ? "Saving..."
                    : "Save for approval"}
                </button>

                <button
                  type="button"
                  onClick={() => {
                    setMessageFor(null);
                    setMessage("");
                  }}
                  disabled={savingOutreach}
                  className="rounded-xl border border-zinc-700 px-5 py-2.5 text-sm font-medium text-zinc-300 hover:bg-zinc-900"
                >
                  Cancel
                </button>

              </div>

            </form>

          </section>
        )}

        {/* OPERATING PRINCIPLE */}
        <section className="rounded-3xl border border-zinc-800 bg-zinc-950 p-6">

          <div className="flex items-start gap-4">

            <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-indigo-500/10 text-indigo-400">
              ✦
            </div>

            <div>
              <h3 className="font-semibold text-white">
                CreatorOS operating principle
              </h3>

              <p className="mt-2 max-w-3xl text-sm leading-6 text-zinc-500">
                AI can research, draft, validate, and recommend. External
                communication remains under owner control. Nothing on this
                page automatically sends a message to a prospect.
              </p>
            </div>

          </div>

        </section>

      </div>
    </DashboardLayout>
  );
}