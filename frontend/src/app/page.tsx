import Link from "next/link";
import DashboardLayout from "@/components/layout/DashboardLayout";
import ActivityFeed from "@/components/dashboard/ActivityFeed";
import CreatorInsights from "@/components/dashboard/CreatorInsights";
import Hero from "@/components/dashboard/Hero";
import RecentDrafts from "@/components/dashboard/RecentDrafts";
import TrendingIdeas from "@/components/dashboard/TrendingIdeas";

export default function HomePage() {
  return (
    <DashboardLayout>
      <div className="space-y-8">
        <Hero />
        <CreatorInsights />

        <div className="grid gap-8 xl:grid-cols-3">
          <div className="space-y-8 xl:col-span-2">
            <section className="rounded-3xl border border-zinc-800 bg-zinc-900 p-8">
              <div className="flex flex-wrap items-start justify-between gap-4">
                <div><p className="text-sm font-semibold uppercase tracking-[0.2em] text-indigo-400">30-day pilot loop</p><h2 className="mt-2 text-2xl font-bold text-white">From local insight to appointment</h2><p className="mt-2 max-w-2xl text-sm leading-6 text-zinc-400">Research 30 gyms, prepare personalized drafts, request approval, then track replies, qualified leads, trial enquiries, and appointments.</p></div>
                <Link href="/analytics" className="rounded-xl border border-zinc-700 px-4 py-2 text-sm font-semibold text-zinc-200 hover:bg-zinc-800">View analytics</Link>
              </div>
              <div className="mt-8 grid gap-3 md:grid-cols-4">
                {["Research & audit", "Draft & approve", "Follow up", "Measure outcome"].map((step, index) => <div key={step} className="rounded-2xl bg-zinc-950 p-4"><span className="text-xs font-semibold text-indigo-400">0{index + 1}</span><p className="mt-3 font-medium text-zinc-200">{step}</p><p className="mt-1 text-xs leading-5 text-zinc-500">{index === 0 ? "Find the right local businesses." : index === 1 ? "Keep claims and sends reviewable." : index === 2 ? "Use a clear, human-approved CTA." : "Report enquiries and appointments."}</p></div>)}
              </div>
            </section>

            <ActivityFeed />
          </div>

          <div className="space-y-8">
            <RecentDrafts />
            <TrendingIdeas />
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
}
