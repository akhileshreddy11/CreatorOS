"use client";

import { Card, CardContent } from "@/components/ui/card";
import { FileText, Sparkles, Calendar, TrendingUp } from "lucide-react";

const stats = [
  {
    title: "Drafts",
    value: "24",
    icon: FileText,
  },
  {
    title: "Generated Today",
    value: "12",
    icon: Sparkles,
  },
  {
    title: "Scheduled",
    value: "8",
    icon: Calendar,
  },
  {
    title: "Growth",
    value: "+38%",
    icon: TrendingUp,
  },
];

export default function DashboardStats() {
  return (
    <div className="grid gap-6 md:grid-cols-2 xl:grid-cols-4">
      {stats.map((stat) => {
        const Icon = stat.icon;

        return (
          <Card
            key={stat.title}
            className="bg-zinc-900 border-zinc-800 text-white"
          >
            <CardContent className="flex items-center justify-between p-6">
              <div>
                <p className="text-sm text-zinc-400">
                  {stat.title}
                </p>

                <h2 className="mt-2 text-3xl font-bold">
                  {stat.value}
                </h2>
              </div>

              <div className="rounded-xl bg-blue-600 p-3">
                <Icon size={24} />
              </div>
            </CardContent>
          </Card>
        );
      })}
    </div>
  );
}