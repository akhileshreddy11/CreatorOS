import Link from "next/link";
import { ArrowRight, Sparkles } from "lucide-react";

export default function AICommandCenter() {
  return (
    <section className="rounded-3xl border border-zinc-800 bg-zinc-900/70 p-8 backdrop-blur-xl">
      <p className="text-sm font-semibold uppercase tracking-[0.2em] text-indigo-400">AI command center</p>
      <h2 className="mt-3 text-2xl font-bold text-white">Create a reviewable local-growth asset</h2>
      <p className="mt-2 max-w-xl text-zinc-400">Use the AI Studio to generate content, inspect claim warnings, and keep every external action behind approval.</p>
      <Link href="/ai-studio" className="mt-6 inline-flex items-center rounded-xl bg-gradient-to-r from-indigo-600 to-violet-600 px-5 py-3 font-semibold text-white hover:opacity-90"><Sparkles className="mr-2" size={18} />Open AI Studio<ArrowRight className="ml-2" size={18} /></Link>
    </section>
  );
}
