"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { FileText } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { getDrafts, type Draft } from "@/services/aiService";

export default function RecentDrafts() {
  const [drafts, setDrafts] = useState<Draft[]>([]);

  useEffect(() => {
    getDrafts().then((items) => setDrafts(items.slice(0, 5))).catch(() => setDrafts([]));
  }, []);

  return (
    <Card className="border-zinc-800 bg-zinc-900 text-white">
      <CardHeader><CardTitle className="flex items-center gap-2"><FileText size={18} className="text-indigo-400" />Recent drafts</CardTitle></CardHeader>
      <CardContent>
        <div className="space-y-3">
          {drafts.length === 0 ? <p className="rounded-lg border border-dashed border-zinc-700 p-3 text-sm text-zinc-500">No drafts yet. Create one in AI Studio.</p> : drafts.map((draft) => <div key={draft.id} className="flex items-center justify-between gap-3 rounded-lg bg-zinc-950 p-3"><span className="truncate text-sm text-zinc-300">{draft.title}</span><span className="text-xs uppercase text-zinc-500">{draft.status}</span></div>)}
        </div>
        <Link href="/drafts" className="mt-4 inline-block text-sm font-semibold text-indigo-300 hover:text-indigo-200">View all drafts →</Link>
      </CardContent>
    </Card>
  );
}
