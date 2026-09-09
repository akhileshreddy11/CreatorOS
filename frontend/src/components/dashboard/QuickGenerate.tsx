"use client";

import Link from "next/link";
import { ArrowRight, Sparkles } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

export default function QuickGenerate() {
  return (
    <Card className="border-zinc-800 bg-zinc-900 text-white">
      <CardHeader>
        <CardTitle className="flex items-center gap-2"><Sparkles className="text-indigo-400" size={19} />Quick draft</CardTitle>
      </CardHeader>
      <CardContent>
        <p className="text-sm leading-6 text-zinc-400">Create a reviewable Hyderabad gym asset with a trial-class enquiry CTA.</p>
        <Link href="/ai-studio" className="mt-4 inline-flex items-center rounded-xl bg-indigo-600 px-4 py-3 text-sm font-semibold text-white hover:bg-indigo-500">Open AI Studio <ArrowRight className="ml-2" size={16} /></Link>
      </CardContent>
    </Card>
  );
}
