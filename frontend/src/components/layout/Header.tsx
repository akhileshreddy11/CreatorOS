"use client";

import Link from "next/link";
import { Bell, Search, UserCircle2 } from "lucide-react";
import { Input } from "@/components/ui/input";

export default function Header() {
  return (
    <header className="sticky top-0 z-40 flex h-20 items-center justify-between border-b border-zinc-800 bg-[#09090b]/80 px-8 backdrop-blur-xl">
      <div><h1 className="text-2xl font-bold text-white">CreatorOS</h1><p className="mt-1 text-sm text-zinc-400">AI Operating System · Hyderabad pilot</p></div>
      <div className="flex items-center gap-4">
        <div className="relative hidden md:block"><Search size={18} className="absolute left-4 top-1/2 -translate-y-1/2 text-zinc-500" /><Input placeholder="Search operations…" aria-label="Search operations" className="h-12 w-80 rounded-2xl border-zinc-700 bg-zinc-900 pl-11" /></div>
        <Link href="/drafts" aria-label="Open pending draft approvals" className="relative flex h-12 w-12 items-center justify-center rounded-2xl border border-zinc-800 bg-zinc-900 transition hover:bg-zinc-800"><Bell size={20} /><span className="absolute right-3 top-3 h-2 w-2 rounded-full bg-indigo-500" /></Link>
        <Link href="/settings" aria-label="Open settings" className="flex h-12 w-12 items-center justify-center rounded-full bg-gradient-to-br from-indigo-500 to-violet-500"><UserCircle2 size={26} /></Link>
      </div>
    </header>
  );
}
