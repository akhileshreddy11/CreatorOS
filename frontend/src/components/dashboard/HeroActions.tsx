import Link from "next/link";
import { ArrowRight, Sparkles } from "lucide-react";

export default function HeroActions() {
  return (
    <div className="mt-8 flex flex-wrap gap-4">
      <Link href="/ai-studio" className="inline-flex h-14 items-center rounded-2xl bg-gradient-to-r from-indigo-600 via-violet-600 to-purple-600 px-8 font-semibold text-white shadow-lg shadow-indigo-500/30 transition hover:scale-[1.02]">
        <Sparkles className="mr-2 h-5 w-5" />
        Generate with AI
      </Link>
      <Link href="/drafts" className="inline-flex h-14 items-center rounded-2xl border border-zinc-700 bg-zinc-900 px-8 font-semibold text-white transition hover:bg-zinc-800">
        Review drafts
        <ArrowRight className="ml-2 h-5 w-5" />
      </Link>
    </div>
  );
}
