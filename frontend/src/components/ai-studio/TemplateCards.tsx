"use client";

import { Briefcase, Clapperboard, FileText, Image, Lightbulb, Sparkles } from "lucide-react";
import { usePrompt } from "@/context/PromptContext";

const templates = [
  { title: "Trial-class Reel", description: "Explain what a first gym visit feels like.", icon: Clapperboard, prompt: "Create a short Reel that explains what a beginner can expect in a Hyderabad gym trial class." },
  { title: "Local Offer", description: "Present a transparent offer without guarantees.", icon: Sparkles, prompt: "Write a local offer post for a Hyderabad gym that invites people to ask about an introductory trial class." },
  { title: "WhatsApp Follow-up", description: "Prepare a helpful reply for an interested lead.", icon: Briefcase, prompt: "Draft a warm WhatsApp follow-up for a person who asked about gym timings and a trial class." },
  { title: "Caption", description: "Generate a caption with a clear enquiry CTA.", icon: FileText, prompt: "Generate an Instagram caption for a Hyderabad gym focused on a simple trial-class enquiry." },
  { title: "Visual Prompt", description: "Describe a safe, inclusive gym visual.", icon: Image, prompt: "Create a detailed visual prompt for an inclusive Hyderabad gym trial-class Reel cover." },
  { title: "Content Ideas", description: "Brainstorm useful local education topics.", icon: Lightbulb, prompt: "Brainstorm 10 useful content ideas for Hyderabad gym beginners that can lead to genuine enquiries." },
];

export default function TemplateCards() {
  const { setPrompt } = usePrompt();

  return (
    <section className="space-y-6">
      <div><h2 className="text-2xl font-bold text-white">Quick templates</h2><p className="mt-2 text-zinc-400">Start with a local-business brief designed around trial-class enquiries.</p></div>
      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
        {templates.map((template) => { const Icon = template.icon; return <button type="button" key={template.title} onClick={() => setPrompt(template.prompt)} className="group rounded-3xl border border-zinc-800 bg-zinc-900 p-6 text-left transition-all duration-300 hover:-translate-y-1 hover:border-indigo-500 hover:bg-zinc-800"><Icon size={30} className="mb-5 text-indigo-400 transition-transform duration-300 group-hover:scale-110" /><h3 className="text-lg font-semibold text-white">{template.title}</h3><p className="mt-2 text-sm leading-6 text-zinc-400">{template.description}</p></button>; })}
      </div>
    </section>
  );
}
