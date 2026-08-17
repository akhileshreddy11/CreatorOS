"use client";

import Link from "next/link";
import { Sparkles } from "lucide-react";

export default function GenerateButton() {
  return <Link href="/ai-studio" className="inline-flex h-14 w-full items-center justify-center rounded-xl bg-gradient-to-r from-indigo-600 via-violet-600 to-purple-600 text-base font-semibold text-white transition-all hover:opacity-90"><Sparkles className="mr-2 h-5 w-5" />Open AI Studio</Link>;
}
