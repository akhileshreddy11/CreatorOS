"use client";

import {
  LayoutDashboard,
  Sparkles,
  FileText,
  Calendar,
  BarChart3,
  Settings,
} from "lucide-react";

const menuItems = [
  {
    title: "Dashboard",
    icon: LayoutDashboard,
  },
  {
    title: "AI Studio",
    icon: Sparkles,
  },
  {
    title: "Drafts",
    icon: FileText,
  },
  {
    title: "Calendar",
    icon: Calendar,
  },
  {
    title: "Analytics",
    icon: BarChart3,
  },
  {
    title: "Settings",
    icon: Settings,
  },
];

export default function Sidebar() {
  return (
    <aside className="w-72 min-h-screen bg-zinc-950 border-r border-zinc-800 text-white p-6">
      <div className="mb-10">
        <h1 className="text-3xl font-bold">
          CreatorOS
          <span className="text-blue-500"> AI</span>
        </h1>

        <p className="text-zinc-400 text-sm mt-2">
          Personal AI Content Studio
        </p>
      </div>

      <nav className="space-y-2">
        {menuItems.map((item) => {
          const Icon = item.icon;

          return (
            <button
              key={item.title}
              className="flex items-center gap-3 w-full rounded-xl px-4 py-3 hover:bg-zinc-900 transition"
            >
              <Icon size={20} />
              <span>{item.title}</span>
            </button>
          );
        })}
      </nav>

      <div className="absolute bottom-6 left-6 right-6">
        <div className="rounded-xl bg-blue-600 p-4">
          <h2 className="font-semibold">CreatorOS AI</h2>
          <p className="text-sm text-blue-100 mt-1">
            Build viral content faster with AI.
          </p>
        </div>
      </div>
    </aside>
  );
}