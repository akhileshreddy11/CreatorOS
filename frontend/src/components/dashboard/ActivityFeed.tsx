"use client";

import { useEffect, useState } from "react";
import { AlertTriangle, CheckCircle2, Clock3 } from "lucide-react";
import { getDrafts, getErrors, type Draft } from "@/services/aiService";

type Activity = { id: string; label: string; detail: string; tone: "good" | "warning" | "neutral" };

export default function ActivityFeed() {
  const [activities, setActivities] = useState<Activity[]>([]);

  useEffect(() => {
    Promise.all([getDrafts(), getErrors()])
      .then(([drafts, errors]) => {
        const draftActivities = drafts.slice(0, 3).map((draft: Draft) => ({
          id: `draft-${draft.id}`,
          label: `Draft ${draft.status}`,
          detail: draft.title,
          tone: draft.status === "approved" ? "good" as const : "neutral" as const,
        }));
        const errorActivities = errors.slice(0, 2).map((item) => ({
          id: `error-${item.id}`,
          label: `${item.severity} · ${item.component}`,
          detail: item.message,
          tone: "warning" as const,
        }));
        setActivities([...draftActivities, ...errorActivities]);
      })
      .catch(() => setActivities([]));
  }, []);

  return (
    <section className="rounded-3xl border border-zinc-800 bg-zinc-900 p-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-xl font-bold text-white">Activity & warnings</h2>
          <p className="mt-1 text-sm text-zinc-500">The owner sees exceptions before they become surprises.</p>
        </div>
        <Clock3 className="text-indigo-400" size={20} />
      </div>
      <div className="mt-6 space-y-3">
        {activities.length === 0 ? (
          <p className="rounded-2xl border border-dashed border-zinc-700 p-4 text-sm text-zinc-500">No activity recorded yet.</p>
        ) : activities.map((activity) => {
          const Icon = activity.tone === "warning" ? AlertTriangle : activity.tone === "good" ? CheckCircle2 : Clock3;
          const iconColor = activity.tone === "warning" ? "text-amber-300" : activity.tone === "good" ? "text-emerald-300" : "text-zinc-400";
          return (
            <div key={activity.id} className="flex gap-3 rounded-2xl bg-zinc-950 p-3">
              <Icon className={iconColor} size={18} />
              <div className="min-w-0"><p className="text-sm font-medium text-zinc-200">{activity.label}</p><p className="truncate text-xs text-zinc-500">{activity.detail}</p></div>
            </div>
          );
        })}
      </div>
    </section>
  );
}
