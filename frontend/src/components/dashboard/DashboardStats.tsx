"use client";

import { useEffect, useState } from "react";
import { Calendar, FileCheck2, MessageCircle, Users, type LucideIcon } from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";
import { getDashboardSummary, type DashboardSummary } from "@/services/aiService";

const stats: Array<[keyof DashboardSummary["metrics"], string, LucideIcon]> = [
  ["prospects", "Prospects researched", Users],
  ["pending_approvals", "Pending approvals", FileCheck2],
  ["replies", "Replies", MessageCircle],
  ["appointments", "Appointments", Calendar],
];

export default function DashboardStats() {
  const [summary, setSummary] = useState<DashboardSummary | null>(null);

  useEffect(() => {
    getDashboardSummary().then(setSummary).catch(() => setSummary(null));
  }, []);

  return (
    <div className="grid gap-6 md:grid-cols-2 xl:grid-cols-4">
      {stats.map(([key, title, Icon]) => (
        <Card key={key} className="border-zinc-800 bg-zinc-900 text-white">
          <CardContent className="flex items-center justify-between p-6">
            <div>
              <p className="text-sm text-zinc-400">{title}</p>
              <h2 className="mt-2 text-3xl font-bold">{summary?.metrics[key] ?? "—"}</h2>
            </div>
            <div className="rounded-xl bg-indigo-600 p-3"><Icon size={24} /></div>
          </CardContent>
        </Card>
      ))}
    </div>
  );
}
