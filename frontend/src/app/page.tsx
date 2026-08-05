import DashboardLayout from "@/components/layout/DashboardLayout";
import DashboardStats from "@/components/dashboard/DashboardStats";
import QuickGenerate from "@/components/dashboard/QuickGenerate";
import RecentDrafts from "@/components/dashboard/RecentDrafts";

export default function Home() {
  return (
    <DashboardLayout>
      <div className="space-y-8">
        <DashboardStats />

        <div className="grid gap-8 lg:grid-cols-2">
          <QuickGenerate />
          <RecentDrafts />
        </div>
      </div>
    </DashboardLayout>
  );
}