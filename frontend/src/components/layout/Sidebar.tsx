"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { BarChart3, Calendar, ChevronRight, FileText, LayoutDashboard, Settings, Sparkles, TrendingUp, Users } from "lucide-react";

const menuItems = [
  { title: "Command center", href: "/", icon: LayoutDashboard },
  { title: "AI Studio", href: "/ai-studio", icon: Sparkles },
  { title: "Draft approvals", href: "/drafts", icon: FileText },
  { title: "Prospects", href: "/prospects", icon: Users },
  { title: "Leads", href: "/leads", icon: Users },
  { title: "Appointments", href: "/calendar", icon: Calendar },
  { title: "Analytics", href: "/analytics", icon: BarChart3 },
  { title: "Trends & ideas", href: "/trends", icon: TrendingUp },
  { title: "Settings", href: "/settings", icon: Settings },
];

export default function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="flex min-h-screen w-72 flex-col border-r border-zinc-800 bg-zinc-950 p-6 text-white">
      <div className="mb-10"><h1 className="text-4xl font-bold">CreatorOS<span className="text-indigo-400"> AI</span></h1><p className="mt-2 text-sm text-zinc-400">Local growth operations</p></div>
      <nav className="space-y-2">{menuItems.map((item) => { const Icon = item.icon; const active = pathname === item.href; return <Link key={item.title} href={item.href} className={`group flex items-center justify-between rounded-2xl px-4 py-3 transition-all duration-300 ${active ? "bg-gradient-to-r from-indigo-600 to-violet-600 text-white shadow-lg shadow-indigo-900/40" : "text-zinc-400 hover:bg-zinc-900 hover:text-white"}`}><div className="flex items-center gap-3"><Icon size={20} /><span>{item.title}</span></div>{active && <ChevronRight size={18} />}</Link>; })}</nav>
      <div className="mt-auto space-y-6">
        <div className="rounded-3xl border border-zinc-800 bg-zinc-900 p-5"><div className="flex items-center gap-3"><div className="rounded-xl bg-indigo-500/20 p-3"><Users className="text-indigo-300" size={22} /></div><div><h3 className="font-semibold">Pilot workspace</h3><p className="text-sm text-zinc-400">Gyms · Hyderabad</p></div></div><p className="mt-4 text-xs leading-5 text-zinc-500">AI drafts. Owner approvals. Measured enquiries.</p></div>
        <div className="flex items-center gap-3 rounded-2xl border border-zinc-800 bg-zinc-900 p-4"><div className="flex h-11 w-11 items-center justify-center rounded-full bg-indigo-600 font-bold">A</div><div><h3 className="font-semibold">Akhilesh</h3><p className="text-sm text-zinc-400">Owner oversight</p></div></div>
      </div>
    </aside>
  );
}
