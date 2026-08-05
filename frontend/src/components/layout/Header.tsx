"use client";

import { Bell, Search, UserCircle2 } from "lucide-react";

export default function Header() {
  return (
    <header className="h-20 border-b border-zinc-800 bg-zinc-950 flex items-center justify-between px-8">
      <div>
        <h1 className="text-2xl font-bold text-white">
          Welcome Back 👋
        </h1>

        <p className="text-zinc-400 text-sm">
          Let's create something amazing today.
        </p>
      </div>

      <div className="flex items-center gap-4">
        <div className="flex items-center gap-2 rounded-xl bg-zinc-900 px-4 py-2">
          <Search size={18} className="text-zinc-400" />
          <input
            placeholder="Search..."
            className="bg-transparent outline-none text-white placeholder:text-zinc-500"
          />
        </div>

        <button className="rounded-xl bg-zinc-900 p-3 hover:bg-zinc-800 transition">
          <Bell className="text-white" size={20} />
        </button>

        <button className="rounded-full bg-blue-600 p-2">
          <UserCircle2 className="text-white" size={28} />
        </button>
      </div>
    </header>
  );
}