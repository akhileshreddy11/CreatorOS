"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import HeroActions from "./HeroActions";
import HeroStats from "./HeroStats";
import AICore from "./AICore";
import {
  approveMission,
  type MissionResponse,
} from "@/services/aiService";

export default function Hero() {
  const [launching, setLaunching] = useState(false);
  const [mission, setMission] = useState<MissionResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  async function handleLaunchMission() {
    try {
      setLaunching(true);
      setError(null);

      const result = await approveMission({
        topic: "Hyderabad gym trial-class enquiry campaign",

        problem:
          "Local gym prospects need a clear reason to enquire and an easy next step.",

        audience: [
          "Hyderabad gym owners",
          "Beginners looking for a nearby class",
        ],

        strategy:
          "Create useful local-language short videos and route every CTA through an owner-approved follow-up.",

        recommended_content: [
          "What to expect in your first gym trial class",
          "Three questions to ask before joining a Hyderabad gym",
          "A transparent introductory offer with a trial enquiry CTA",
        ],

        product_idea: "",
      });

      setMission(result);
    } catch (requestError) {
      setError(
        requestError instanceof Error
          ? requestError.message
          : "Mission could not be launched.",
      );
    } finally {
      setLaunching(false);
    }
  }

  return (
    <motion.section
      initial={{ opacity: 0, y: 25 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.7 }}
      className="relative overflow-hidden rounded-3xl border border-zinc-800 bg-gradient-to-br from-zinc-950 via-[#10111a] to-black p-10"
    >
      {/* Background glow */}
      <div className="absolute -top-24 left-20 h-72 w-72 rounded-full bg-indigo-600/10 blur-3xl" />

      <div className="absolute bottom-0 right-0 h-80 w-80 rounded-full bg-violet-600/10 blur-3xl" />

      <div className="relative z-10 grid items-center gap-12 lg:grid-cols-2">

        {/* LEFT SIDE */}
        <div>

          <div className="inline-flex items-center rounded-full border border-indigo-500/20 bg-indigo-500/10 px-4 py-2 text-sm text-indigo-300">
            ✨ AI-operated, owner-approved
          </div>

          <h1 className="mt-6 text-5xl font-extrabold leading-tight text-white">
            Turn local content into
            <span className="block bg-gradient-to-r from-indigo-400 via-violet-400 to-cyan-400 bg-clip-text text-transparent">
              trial-class enquiries
            </span>
          </h1>

          <p className="mt-6 max-w-xl text-lg leading-8 text-zinc-400">
            CreatorOS helps Hyderabad gyms plan useful short videos,
            prepare personalized outreach, and track replies and
            appointments without letting automation make high-risk
            decisions.
          </p>

          {/* EXISTING ACTIONS */}
          <HeroActions />

          {/* MISSION CONTROL */}
          <div className="mt-8 rounded-2xl border border-indigo-500/20 bg-indigo-500/5 p-5">

            <div className="flex flex-wrap items-start justify-between gap-4">

              <div>
                <p className="text-xs font-semibold uppercase tracking-[0.2em] text-indigo-400">
                  Mission Control
                </p>

                <h2 className="mt-2 text-lg font-semibold text-white">
                  Hyderabad Gym Pilot
                </h2>

                <p className="mt-1 max-w-lg text-sm leading-6 text-zinc-500">
                  Let CreatorOS research the opportunity, generate campaign
                  assets, validate them, and place the results in your
                  approval queue.
                </p>
              </div>

              <div className="rounded-xl border border-zinc-800 bg-zinc-950 px-3 py-2">
                <span className="text-xs text-zinc-500">
                  Owner approval required
                </span>
              </div>

            </div>

            <button
              type="button"
              onClick={handleLaunchMission}
              disabled={launching}
              className="mt-5 w-full rounded-xl bg-indigo-600 px-5 py-3 text-sm font-semibold text-white transition hover:bg-indigo-500 disabled:cursor-not-allowed disabled:opacity-50"
            >
              {launching
                ? "Launching CreatorOS mission..."
                : "Review & Launch Mission"}
            </button>

            {/* ERROR */}
            {error && (
              <div className="mt-4 rounded-xl border border-red-500/20 bg-red-500/10 p-4">
                <p className="text-sm font-semibold text-red-300">
                  Mission failed
                </p>

                <p className="mt-1 text-xs leading-5 text-red-400">
                  {error}
                </p>
              </div>
            )}

            {/* MISSION RESULT */}
            {mission && (
              <div className="mt-5 space-y-4">

                <div className="rounded-xl border border-emerald-500/20 bg-emerald-500/5 p-4">

                  <div className="flex items-center justify-between gap-3">
                    <p className="text-sm font-semibold text-emerald-300">
                      Mission executed
                    </p>

                    <span className="rounded-full bg-emerald-500/10 px-3 py-1 text-xs font-semibold uppercase text-emerald-400">
                      {mission.mission.execution_status ?? "COMPLETED"}
                    </span>
                  </div>

                  <p className="mt-2 text-xs leading-5 text-zinc-500">
                    {mission.message}
                  </p>

                </div>

                {/* TASKS */}
                <div className="space-y-2">

                  <p className="text-xs font-semibold uppercase tracking-[0.15em] text-zinc-500">
                    Mission tasks
                  </p>

                  {mission.mission.tasks.map((task) => (
                    <div
                      key={task.id}
                      className="flex items-center justify-between gap-3 rounded-xl bg-zinc-950 p-3"
                    >

                      <div className="min-w-0">
                        <p className="truncate text-sm font-medium text-zinc-200">
                          {task.title}
                        </p>

                        <p className="mt-1 text-xs text-zinc-600">
                          {task.assigned_to}
                        </p>
                      </div>

                      <span
                        className={`shrink-0 rounded-full px-2.5 py-1 text-[10px] font-semibold uppercase ${
                          task.status === "Completed"
                            ? "bg-emerald-500/10 text-emerald-400"
                            : "bg-amber-500/10 text-amber-400"
                        }`}
                      >
                        {task.status}
                      </span>

                    </div>
                  ))}

                </div>

                {/* RESULTS */}
                <div className="rounded-xl border border-zinc-800 bg-zinc-950 p-4">

                  <div className="flex items-center justify-between">
                    <p className="text-sm font-semibold text-zinc-200">
                      Generated artifacts
                    </p>

                    <span className="text-xs text-zinc-600">
                      {mission.execution_results.length} result
                      {mission.execution_results.length === 1 ? "" : "s"}
                    </span>
                  </div>

                  <div className="mt-3 space-y-2">

                    {mission.execution_results.map((result) => (
                      <div
                        key={result.task_id}
                        className="flex items-center justify-between gap-3 rounded-lg border border-zinc-800 px-3 py-2"
                      >

                        <div>
                          <p className="text-xs font-medium text-zinc-300">
                            {result.employee}
                          </p>

                          <p className="mt-1 text-[11px] text-zinc-600">
                            {result.artifact_status ??
                              "Execution completed"}
                          </p>
                        </div>

                        <span className="text-xs font-semibold text-emerald-400">
                          {result.status}
                        </span>

                      </div>
                    ))}

                  </div>

                </div>

                {/* DRAFT LINK */}
                <a
                  href="/drafts"
                  className="block w-full rounded-xl border border-indigo-500/30 bg-indigo-500/10 px-5 py-3 text-center text-sm font-semibold text-indigo-300 transition hover:bg-indigo-500/20"
                >
                  Review Generated Drafts →
                </a>

              </div>
            )}

          </div>

          {/* EXISTING STATS */}
          <HeroStats />

        </div>

        {/* RIGHT SIDE */}
        <AICore />

      </div>
    </motion.section>
  );
}