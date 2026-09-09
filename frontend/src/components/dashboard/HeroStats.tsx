"use client";

import CountUp from "react-countup";

const stats = [
  { value: 30, label: "Prospects in first sprint" },
  { value: 1, label: "Pilot customer target" },
  { value: 4, suffix: "–6", label: "Recurring customers" },
  { value: 1, label: "Primary KPI" },
];

export default function HeroStats() {
  return (
    <div className="mt-10 grid grid-cols-2 gap-5 lg:grid-cols-4">
      {stats.map((item) => (
        <div key={item.label} className="rounded-2xl border border-zinc-800 bg-zinc-900/60 p-5 backdrop-blur-xl">
          <h2 className="text-3xl font-bold text-white"><CountUp end={item.value} duration={1.5} />{item.suffix}</h2>
          <p className="mt-2 text-sm text-zinc-400">{item.label}</p>
        </div>
      ))}
    </div>
  );
}
