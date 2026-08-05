"use client";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

const drafts = [
  "Top 10 AI Tools",
  "Morning Productivity",
  "React Tips",
  "Instagram Growth",
  "Best Coding Habits",
];

export default function RecentDrafts() {
  return (
    <Card className="bg-zinc-900 border-zinc-800 text-white">
      <CardHeader>
        <CardTitle>📄 Recent Drafts</CardTitle>
      </CardHeader>

      <CardContent>
        <div className="space-y-3">
          {drafts.map((draft) => (
            <div
              key={draft}
              className="rounded-lg bg-zinc-950 p-3 hover:bg-zinc-800 transition"
            >
              {draft}
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}