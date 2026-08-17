export const API_URL =
  process.env.NEXT_PUBLIC_API_URL ?? "http://127.0.0.1:8000";

export type GeneratedContent = {
  hook?: string;
  script?: string;
  caption?: string;
  cta?: string;
  hashtags?: string[];
  [key: string]: unknown;
};

export type GenerationRequest = {
  prompt: string;
  platform: string;
  length: string;
  niche: string;
  city: string;
  language: string;
  objective: string;
  offer: string;
  tone: string;
};

export type GenerationResponse = {
  response: string;
  content: GeneratedContent;
  validation: {
    status?: string;
    valid?: boolean;
    errors?: string[];
    warnings?: string[];
    quality_score?: number;
  };
  approval_status: string;
  action_class: string;
  draft_id: number | null;
};

export type DashboardSummary = {
  profile: {
    name: string;
    niche: string;
    city: string;
    primary_language: string;
    supported_languages: string[];
    offer: string;
    primary_kpi: string;
    monthly_targets: Record<string, string | number>;
  } | null;
  metrics: {
    prospects: number;
    contacted: number;
    replies: number;
    qualified_leads: number;
    appointments: number;
    trial_class_enquiries: number;
    pending_approvals: number;
    open_errors: number;
  };
  conversion_rate: number;
  safety: {
    external_sends_require_approval: boolean;
    payments_contracts_and_deletion_require_human: boolean;
  };
};

export type Draft = {
  id: number;
  title: string;
  prompt: string;
  platform: string;
  language: string;
  content: GeneratedContent;
  validation: GenerationResponse["validation"];
  status: string;
  action_class: string;
  created_at: string;
  updated_at: string;
};

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_URL}${path}`, {
    ...init,
    headers: {
      "Content-Type": "application/json",
      ...(init?.headers ?? {}),
    },
  });

  if (!response.ok) {
    let detail = "CreatorOS could not complete the request.";
    try {
      const payload = (await response.json()) as { detail?: string };
      detail = payload.detail ?? detail;
    } catch {
      // Keep the actionable fallback when the server did not return JSON.
    }
    throw new Error(detail);
  }

  return response.json() as Promise<T>;
}

export function generateContent(payload: GenerationRequest) {
  return request<GenerationResponse>("/ai/generate", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export function getDashboardSummary() {
  return request<DashboardSummary>("/dashboard/summary", {
    cache: "no-store",
  });
}

export function getDrafts() {
  return request<Draft[]>("/drafts", { cache: "no-store" });
}

export function approveDraft(id: number) {
  return request<Draft>(`/drafts/${id}/approve`, { method: "POST" });
}

export function rejectDraft(id: number) {
  return request<Draft>(`/drafts/${id}/reject`, { method: "POST" });
}

export type Appointment = {
  id: number;
  lead_id: number;
  scheduled_for: string;
  status: string;
  notes?: string | null;
};

export type Prospect = {
  id: number;
  business_name: string;
  city: string;
  status: string;
  contact_channel: string;
  contact_handle?: string | null;
  audit_summary?: string | null;
};

export type Lead = {
  id: number;
  name: string;
  status: string;
  source: string;
  notes?: string | null;
};

export function getAppointments() {
  return request<Appointment[]>("/appointments", { cache: "no-store" });
}

export function getProspects() {
  return request<Prospect[]>("/prospects", { cache: "no-store" });
}

export function createProspect(payload: {
  business_name: string;
  contact_handle?: string;
  audit_summary?: string;
}) {
  return request<Prospect>("/prospects", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export function createOutreach(prospectId: number, message: string) {
  return request(`/prospects/${prospectId}/outreach`, {
    method: "POST",
    body: JSON.stringify({ message }),
  });
}

export function getLeads() {
  return request<Lead[]>("/leads", { cache: "no-store" });
}

export function getTrends() {
  return request<Array<{ title: string; angle: string; status: string }>>(
    "/trends",
    { cache: "no-store" },
  );
}

export function getErrors() {
  return request<
    Array<{
      id: number;
      severity: string;
      component: string;
      message: string;
      resolved: boolean;
      created_at: string;
    }>
  >("/errors", { cache: "no-store" });
}
