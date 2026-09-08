"use client";

import { useEffect, useMemo, useState } from "react";

import DashboardLayout from "@/components/layout/DashboardLayout";

import {
  getLeads,
  type Lead,
} from "@/services/aiService";

const columns = [
  {
    key: "new",
    label: "New",
    description: "Newly captured enquiries",
  },
  {
    key: "qualified",
    label: "Qualified",
    description: "Leads worth following up",
  },
  {
    key: "trial_enquiry",
    label: "Trial enquiry",
    description: "Interested in a trial",
  },
  {
    key: "converted",
    label: "Converted",
    description: "Successful outcomes",
  },
];

export default function LeadsPage() {
  const [leads, setLeads] = useState<Lead[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  async function loadLeads() {
    try {
      setLoading(true);
      setError(null);

      const data = await getLeads();

      setLeads(data);
    } catch (requestError) {
      setError(
        requestError instanceof Error
          ? requestError.message
          : "Could not load leads.",
      );
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadLeads();
  }, []);

  const counts = useMemo(() => {
    return {
      total: leads.length,
      new: leads.filter(
        (lead) => lead.status === "new",
      ).length,
      qualified: leads.filter(
        (lead) => lead.status === "qualified",
      ).length,
      trial: leads.filter(
        (lead) => lead.status === "trial_enquiry",
      ).length,
      converted: leads.filter(
        (lead) => lead.status === "converted",
      ).length,
    };
  }, [leads]);

  return (
    <DashboardLayout>
      <div className="space-y-8">

        {/* HEADER */}
        <div className="flex flex-wrap items-end justify-between gap-5">

          <div>
            <p className="text-sm font-semibold uppercase tracking-[0.2em] text-indigo-400">
              Outcome pipeline
            </p>

            <h1 className="mt-3 text-4xl font-bold text-white">
              Leads
            </h1>

            <p className="mt-2 max-w-2xl text-zinc-400">
              Track a person's next step from initial enquiry through
              qualification, trial interest, and conversion.
            </p>
          </div>

          <button
            type="button"
            onClick={loadLeads}
            disabled={loading}
            className="rounded-xl border border-zinc-700 px-4 py-2.5 text-sm font-semibold text-zinc-300 transition hover:bg-zinc-900 disabled:cursor-not-allowed disabled:opacity-50"
          >
            {loading ? "Refreshing..." : "Refresh leads"}
          </button>

        </div>

        {/* ERROR */}
        {error && (
          <div className="rounded-2xl border border-red-500/20 bg-red-500/5 p-5">

            <p className="text-sm font-semibold text-red-300">
              Unable to load leads
            </p>

            <p className="mt-1 text-sm text-red-400">
              {error}
            </p>

            <button
              type="button"
              onClick={loadLeads}
              className="mt-3 rounded-lg border border-red-500/30 px-3 py-2 text-xs font-semibold text-red-300 transition hover:bg-red-500/10"
            >
              Try again
            </button>

          </div>
        )}

        {/* PIPELINE SUMMARY */}
        <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-5">

          <div className="rounded-2xl border border-zinc-800 bg-zinc-900 p-5">
            <p className="text-xs font-semibold uppercase tracking-[0.15em] text-zinc-500">
              Total leads
            </p>

            <p className="mt-3 text-3xl font-bold text-white">
              {counts.total}
            </p>

            <p className="mt-1 text-xs text-zinc-600">
              Entire outcome pipeline
            </p>
          </div>

          <div className="rounded-2xl border border-zinc-800 bg-zinc-900 p-5">
            <p className="text-xs font-semibold uppercase tracking-[0.15em] text-zinc-500">
              New
            </p>

            <p className="mt-3 text-3xl font-bold text-indigo-400">
              {counts.new}
            </p>

            <p className="mt-1 text-xs text-zinc-600">
              Awaiting qualification
            </p>
          </div>

          <div className="rounded-2xl border border-zinc-800 bg-zinc-900 p-5">
            <p className="text-xs font-semibold uppercase tracking-[0.15em] text-zinc-500">
              Qualified
            </p>

            <p className="mt-3 text-3xl font-bold text-violet-400">
              {counts.qualified}
            </p>

            <p className="mt-1 text-xs text-zinc-600">
              Worth following up
            </p>
          </div>

          <div className="rounded-2xl border border-zinc-800 bg-zinc-900 p-5">
            <p className="text-xs font-semibold uppercase tracking-[0.15em] text-zinc-500">
              Trial enquiries
            </p>

            <p className="mt-3 text-3xl font-bold text-amber-400">
              {counts.trial}
            </p>

            <p className="mt-1 text-xs text-zinc-600">
              Trial-class interest
            </p>
          </div>

          <div className="rounded-2xl border border-zinc-800 bg-zinc-900 p-5">
            <p className="text-xs font-semibold uppercase tracking-[0.15em] text-zinc-500">
              Converted
            </p>

            <p className="mt-3 text-3xl font-bold text-emerald-400">
              {counts.converted}
            </p>

            <p className="mt-1 text-xs text-zinc-600">
              Recorded outcomes
            </p>
          </div>

        </div>

        {/* PIPELINE */}
        <section>

          <div className="mb-5">
            <p className="text-xs font-semibold uppercase tracking-[0.2em] text-zinc-500">
              Lead management
            </p>

            <h2 className="mt-2 text-2xl font-bold text-white">
              Outcome pipeline
            </h2>
          </div>

          {loading ? (
            <div className="rounded-3xl border border-zinc-800 bg-zinc-900 p-16 text-center">

              <div className="mx-auto h-8 w-8 animate-spin rounded-full border-2 border-zinc-700 border-t-indigo-400" />

              <p className="mt-5 text-sm text-zinc-400">
                Loading lead pipeline...
              </p>

            </div>
          ) : (
            <div className="grid gap-4 xl:grid-cols-4">

              {columns.map((column) => {
                const columnLeads = leads.filter(
                  (lead) => lead.status === column.key,
                );

                return (
                  <section
                    key={column.key}
                    className="min-h-[360px] rounded-3xl border border-zinc-800 bg-zinc-900 p-4"
                  >

                    {/* COLUMN HEADER */}
                    <div className="flex items-start justify-between gap-3">

                      <div>
                        <h3 className="text-sm font-semibold uppercase tracking-[0.12em] text-zinc-300">
                          {column.label}
                        </h3>

                        <p className="mt-1 text-xs leading-5 text-zinc-600">
                          {column.description}
                        </p>
                      </div>

                      <span className="flex h-7 min-w-7 items-center justify-center rounded-full bg-zinc-800 px-2 text-xs font-semibold text-zinc-400">
                        {columnLeads.length}
                      </span>

                    </div>

                    {/* LEADS */}
                    <div className="mt-5 space-y-3">

                      {columnLeads.map((lead) => (
                        <article
                          key={lead.id}
                          className="rounded-2xl border border-zinc-800 bg-zinc-950 p-4 transition hover:border-zinc-700"
                        >

                          <div className="flex items-start justify-between gap-3">

                            <div className="min-w-0">

                              <p className="truncate font-medium text-zinc-200">
                                {lead.name}
                              </p>

                              <p className="mt-1 text-xs text-zinc-600">
                                Lead #{lead.id}
                              </p>

                            </div>

                            <span className="shrink-0 rounded-full bg-zinc-900 px-2 py-1 text-[10px] font-semibold uppercase text-zinc-500">
                              {lead.source}
                            </span>

                          </div>

                          {lead.notes && (
                            <div className="mt-4 rounded-xl bg-zinc-900 p-3">
                              <p className="text-xs leading-5 text-zinc-500">
                                {lead.notes}
                              </p>
                            </div>
                          )}

                        </article>
                      ))}

                      {columnLeads.length === 0 && (
                        <div className="rounded-2xl border border-dashed border-zinc-800 p-8 text-center">
                          <p className="text-sm text-zinc-700">
                            No leads here
                          </p>
                        </div>
                      )}

                    </div>

                  </section>
                );
              })}

            </div>
          )}

        </section>

        {/* OPERATING PRINCIPLE */}
        <section className="rounded-3xl border border-zinc-800 bg-zinc-950 p-6">

          <div className="flex items-start gap-4">

            <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-indigo-500/10 text-indigo-400">
              ✦
            </div>

            <div>

              <h3 className="font-semibold text-white">
                Outcome tracking
              </h3>

              <p className="mt-2 max-w-3xl text-sm leading-6 text-zinc-500">
                CreatorOS records actual business outcomes rather than
                estimating or inventing conversions. A lead only moves
                through the pipeline when the underlying outcome is recorded.
              </p>

            </div>

          </div>

        </section>

      </div>
    </DashboardLayout>
  );
}