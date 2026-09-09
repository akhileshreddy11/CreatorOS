"use client";

import { motion } from "framer-motion";
import { Sparkles } from "lucide-react";

export default function AICore() {
  return (
    <div className="relative flex items-center justify-center h-[420px]">

      {/* Outer Glow */}
      <motion.div
        animate={{
          scale: [1, 1.08, 1],
          opacity: [0.35, 0.6, 0.35],
        }}
        transition={{
          duration: 4,
          repeat: Infinity,
        }}
        className="absolute h-72 w-72 rounded-full bg-indigo-500 blur-3xl"
      />

      {/* Middle Ring */}
      <motion.div
        animate={{
          rotate: 360,
        }}
        transition={{
          duration: 25,
          repeat: Infinity,
          ease: "linear",
        }}
        className="absolute h-56 w-56 rounded-full border border-indigo-400/30"
      />

      {/* Inner Ring */}
      <motion.div
        animate={{
          rotate: -360,
        }}
        transition={{
          duration: 18,
          repeat: Infinity,
          ease: "linear",
        }}
        className="absolute h-44 w-44 rounded-full border border-violet-400/30"
      />

      {/* Core */}
      <motion.div
        animate={{
          scale: [1, 1.05, 1],
        }}
        transition={{
          duration: 2,
          repeat: Infinity,
        }}
        className="relative flex h-32 w-32 items-center justify-center rounded-full bg-gradient-to-br from-indigo-500 via-violet-500 to-cyan-500 shadow-[0_0_70px_rgba(99,102,241,0.5)]"
      >
        <Sparkles size={42} className="text-white" />
      </motion.div>

    </div>
  );
}