"use client";

import { motion } from "framer-motion";
import HeroActions from "./HeroActions";
import HeroStats from "./HeroStats";
import AICore from "./AICore";

export default function Hero() {
  return (
    <motion.section initial={{ opacity: 0, y: 25 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.7 }} className="relative overflow-hidden rounded-3xl border border-zinc-800 bg-gradient-to-br from-zinc-950 via-[#10111a] to-black p-10">
      <div className="absolute -top-24 left-20 h-72 w-72 rounded-full bg-indigo-600/10 blur-3xl" />
      <div className="absolute bottom-0 right-0 h-80 w-80 rounded-full bg-violet-600/10 blur-3xl" />
      <div className="relative z-10 grid items-center gap-12 lg:grid-cols-2">
        <div>
          <div className="inline-flex items-center rounded-full border border-indigo-500/20 bg-indigo-500/10 px-4 py-2 text-sm text-indigo-300">✨ AI-operated, owner-approved</div>
          <h1 className="mt-6 text-5xl font-extrabold leading-tight text-white">Turn local content into<span className="block bg-gradient-to-r from-indigo-400 via-violet-400 to-cyan-400 bg-clip-text text-transparent">trial-class enquiries</span></h1>
          <p className="mt-6 max-w-xl text-lg leading-8 text-zinc-400">CreatorOS helps Hyderabad gyms plan useful short videos, prepare personalized outreach, and track replies and appointments without letting automation make high-risk decisions.</p>
          <HeroActions />
          <HeroStats />
        </div>
        <AICore />
      </div>
    </motion.section>
  );
}
