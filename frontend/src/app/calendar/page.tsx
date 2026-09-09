"use client";

import { useEffect, useState } from "react";
import DashboardLayout from "@/components/layout/DashboardLayout";
import { getAppointments, type Appointment } from "@/services/aiService";

export default function CalendarPage() {
  const [appointments, setAppointments] = useState<Appointment[]>([]);
  const [offline, setOffline] = useState(false);

  useEffect(() => {
    getAppointments().then(setAppointments).catch(() => setOffline(true));
  }, []);

  return (
    <DashboardLayout>
      <div className="space-y-8"><div><p className="text-sm font-semibold uppercase tracking-[0.2em] text-indigo-400">Human-reviewed scheduling</p><h1 className="mt-3 text-4xl font-bold text-white">Calendar</h1><p className="mt-2 text-zinc-400">Appointments are tracked here; CreatorOS never contacts a lead without the configured approval.</p></div>{offline && <p className="rounded-xl border border-amber-500/30 bg-amber-500/10 p-4 text-sm text-amber-200">Start FastAPI to load appointments.</p>}<div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">{appointments.length === 0 ? <div className="col-span-full rounded-3xl border border-dashed border-zinc-700 p-12 text-center text-zinc-500">No appointments recorded yet.</div> : appointments.map((appointment) => <div key={appointment.id} className="rounded-3xl border border-zinc-800 bg-zinc-900 p-6"><p className="text-xs uppercase text-indigo-300">Lead #{appointment.lead_id}</p><h2 className="mt-3 text-lg font-semibold text-white">{new Date(appointment.scheduled_for).toLocaleString()}</h2><p className="mt-2 text-sm text-zinc-400">{appointment.status}</p>{appointment.notes && <p className="mt-4 text-sm text-zinc-500">{appointment.notes}</p>}</div>)}</div></div>
    </DashboardLayout>
  );
}
