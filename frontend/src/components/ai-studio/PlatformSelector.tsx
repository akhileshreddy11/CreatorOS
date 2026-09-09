"use client";

import { usePrompt } from "@/context/PromptContext";

export default function PlatformSelector() {
  const { platform, setPlatform } = usePrompt();

  return (
    <section className="space-y-3">
      <label htmlFor="platform" className="text-lg font-semibold text-white">
        Platform
      </label>

      <select
        id="platform"
        value={platform}
        onChange={(event) => setPlatform(event.target.value)}
        className="h-14 w-full rounded-2xl border border-zinc-800 bg-zinc-900 px-4 text-white outline-none transition focus:border-indigo-500"
      >
        <option>Instagram</option>
        <option>YouTube</option>
        <option>LinkedIn</option>
        <option>WhatsApp</option>
        <option>Facebook</option>
        <option>TikTok</option>
      </select>
    </section>
  );
}
