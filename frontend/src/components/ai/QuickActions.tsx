import Link from "next/link";
import { Clapperboard, FileText, Image, Sparkles } from "lucide-react";

const actions = [
  { title: "Trial-class Reel", icon: Clapperboard },
  { title: "Local Offer", icon: Sparkles },
  { title: "Visual Prompt", icon: Image },
  { title: "Caption", icon: FileText },
];

export default function QuickActions() {
  return <div className="space-y-4"><h3 className="text-lg font-semibold text-white">Quick actions</h3><div className="grid grid-cols-2 gap-4">{actions.map((action) => { const Icon = action.icon; return <Link key={action.title} href="/ai-studio" className="group rounded-2xl border border-zinc-800 bg-zinc-900 p-5 text-left transition-all duration-300 hover:-translate-y-1 hover:border-indigo-500 hover:bg-zinc-800"><Icon size={28} className="mb-3 text-indigo-400 transition-transform duration-300 group-hover:scale-110" /><h4 className="font-semibold text-white">{action.title}</h4><p className="mt-1 text-sm text-zinc-400">Open review workspace</p></Link>; })}</div></div>;
}
