export const API_URL =
  process.env.NEXT_PUBLIC_API_URL ?? "http://127.0.0.1:8000";


// ============================================================
// CONTENT GENERATION
// ============================================================

export type GeneratedContent = {
  hook?: string;
  script?: string;
  caption?: string;
  cta?: string;
  hashtags?: string[];
  product_name?: string;
  tagline?: string;
  description?: string;
  target_audience?: string[];
  product_structure?: Array<{
    module: string;
    description: string;
    contents: string[];
  }>;
  prompt_pack?: Array<{
    name: string;
    purpose: string;
    prompt: string;
  }>;
  notion_workspace?: {
    pages: string[];
    databases: string[];
  };
  automation_blueprints?: Array<{
    name: string;
    purpose: string;
    workflow: string[];
  }>;
  pricing?: {
    recommended_price: string;
    premium_price: string;
    reason: string;
  };
  marketing_angle?: string;
  launch_strategy?: string[];
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


// ============================================================
// DASHBOARD
// ============================================================

export type DashboardSummary = {
  profile: {
    id: number;
    name: string;
    niche: string;
    city: string;
    primary_language: string;
    supported_languages: string[];
    offer: string;
    primary_kpi: string;
    monthly_targets: Record<string, string | number>;
    approval_policy: Record<string, string>;
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


// ============================================================
// DRAFTS
// ============================================================

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


// ============================================================
// MORNING BRIEF & OPPORTUNITY INTELLIGENCE
// ============================================================

export type SafetyFlag = {
  category: string;
  issue: string;
  severity: "high" | "medium" | "warning" | string;
  matched_text: string;
};

export type SafetyReview = {
  status: "SAFE" | "NEEDS_REVIEW" | string;
  passed: boolean;
  safety_score: number;
  warnings: string[];
  flags: SafetyFlag[];
  recommendation: string;
  summary: string;
};

export type RankedNiche = {
  rank?: number;
  niche?: string;
  topic?: string;
  overall_score?: number;
  scores?: {
    demand?: number;
    reach?: number;
    trend?: number;
    competition?: number;
    monetization?: number;
    content_potential?: number;
    product_potential?: number;
    sustainability?: number;
  };
  audience?: string[];
  audience_problems?: string[];
  content_opportunities?: string[];
  product_opportunity?: string;
  reason?: string;
  recommended_strategy?: string;
};

export type Opportunity = {
  rank?: number;
  niche?: string;
  topic?: string;
  problem?: string;
  audience?: string[];
  demand_score?: number;
  reach_score?: number;
  trend_score?: number;
  content_score?: number;
  monetization_score?: number;
  product_score?: number;
  sustainability_score?: number;
  automation_score?: number;
  overall_score?: number;
  reason?: string;
  recommended_content?: string[];
  product_idea?: string;
  strategy?: string;
};

export type TrendOpportunity = {
  topic?: string;
  reason?: string;
  confidence?: number;
  recommended_content?: string[];
  best_posting_time?: string;
  product_idea?: string;
};

export type COOEvaluation = {
  audience_fit?: number;
  content_potential?: number;
  monetization_potential?: number;
  revenue_alignment?: number;
  overall_score?: number;
  recommendation?: "APPROVE" | "REVIEW" | "REJECT" | string;
  reason?: string;
  proposed_deliverables?: string[];
};

export type BriefData = {
  greeting?: string;
  business?: string;
  monthly_goal?: string | number;
  platform?: string;
  automation?: string;
  status?: string;

  trend_opportunity?: TrendOpportunity;

  niche_research?: {
    ranked_niches?: RankedNiche[];
    best_niche?: RankedNiche | null;
    status?: string;
  };

  niche_ranking?: {
    ranked_niches?: RankedNiche[];
    best_niche?: RankedNiche | null;
    status?: string;
  };

  selected_niche?: RankedNiche | null;

  opportunity_generation?: {
    niche?: string;
    opportunities?: Opportunity[];
    best_opportunity?: Opportunity | null;
    status?: string;
  };

  selected_opportunity?: Opportunity | null;

  coo_evaluation?: COOEvaluation;

  safety_review?: SafetyReview;

  pipeline_time_seconds?: number;
};

export type MorningBriefResponse = {
  status: "NOT_STARTED" | "STARTED" | "RUNNING" | "READY" | "FAILED";
  message: string;
  brief?: BriefData;
  error?: string;
  started_at?: string;
  completed_at?: string;
};


// ============================================================
// MISSIONS
// ============================================================

export type MissionOpportunity = {
  topic: string;
  problem: string;
  audience: string[];
  strategy: string;
  recommended_content: string[];
  product_idea: string;
};

export type MissionTask = {
  id: string;
  title: string;
  description: string;
  assigned_to: string;
  priority: string;
  status: string;
};

export type MissionExecutionValidation = {
  status?: string;
  valid?: boolean;
  errors?: string[];
  warnings?: string[];
  quality_score?: number;
};

export type MissionExecutionResult = {
  task_id: string;
  employee: string;
  status: string;

  result: unknown;

  validation?: MissionExecutionValidation;

  attempts: number;

  artifact_status?: string;
  approval_status?: string;
  action_class?: string;

  artifact_type?: string;
  artifact_id?: number;

  error?: string;
};

export type Mission = {
  mission: string;
  status: string;

  tasks: MissionTask[];

  execution_status?: string;
};

export type MissionResponse = {
  status: string;
  message: string;

  mission: Mission;

  execution_results: MissionExecutionResult[];
  safety_review?: SafetyReview;
};


// ============================================================
// APPOINTMENTS
// ============================================================

export type Appointment = {
  id: number;
  lead_id: number;
  scheduled_for: string;
  status: string;
  notes?: string | null;
};


// ============================================================
// PROSPECTS
// ============================================================

export type Prospect = {
  id: number;
  business_name: string;
  category?: string;
  city: string;
  contact_name?: string | null;
  status: string;
  contact_channel: string;
  contact_handle?: string | null;
  audit_summary?: string | null;
  created_at?: string;
};

export type Outreach = {
  id: number;
  prospect_id: number;
  message: string;
  channel: string;
  status: string;
  approval_status: string;
  action_class: string;
  response_status: string;
  follow_up_at?: string | null;
  sent_at?: string | null;
  created_at: string;
};


// ============================================================
// LEADS
// ============================================================

export type Lead = {
  id: number;
  name: string;
  status: string;
  source: string;
  notes?: string | null;
  prospect_id?: number | null;
  created_at?: string;
  updated_at?: string;
};


// ============================================================
// GENERIC API REQUEST
// ============================================================

async function request<T>(
  path: string,
  init?: RequestInit,
): Promise<T> {
  const response = await fetch(
    `${API_URL}${path}`,
    {
      ...init,

      headers: {
        "Content-Type": "application/json",
        ...(init?.headers ?? {}),
      },
    },
  );

  if (!response.ok) {
    let detail =
      "CreatorOS could not complete the request.";

    try {
      const payload =
        (await response.json()) as {
          detail?: string;
        };

      detail =
        payload.detail ?? detail;
    } catch {
      // Keep fallback message when the server
      // does not return JSON.
    }

    throw new Error(detail);
  }

  return response.json() as Promise<T>;
}


// ============================================================
// AI CONTENT
// ============================================================

export function generateContent(
  payload: GenerationRequest,
) {
  return request<GenerationResponse>(
    "/ai/generate",
    {
      method: "POST",

      body: JSON.stringify(payload),
    },
  );
}


// ============================================================
// DASHBOARD API
// ============================================================

export function getDashboardSummary() {
  return request<DashboardSummary>(
    "/dashboard/summary",
    {
      cache: "no-store",
    },
  );
}

export function getBusinessProfile() {
  return request<DashboardSummary["profile"]>(
    "/business-profile",
    {
      cache: "no-store",
    },
  );
}


// ============================================================
// MORNING BRIEF / COO INTELLIGENCE
// ============================================================

export function getMorningBrief() {
  return request<MorningBriefResponse>(
    "/morning-brief",
    {
      cache: "no-store",
    },
  );
}

export function refreshMorningBrief() {
  return request<MorningBriefResponse>(
    "/morning-brief/refresh",
    {
      method: "POST",
    },
  );
}


// ============================================================
// MISSION CONTROL
// ============================================================

export function approveMission(
  opportunity?: MissionOpportunity | Opportunity,
) {
  return request<MissionResponse>(
    "/approve-mission",
    {
      method: "POST",

      body: JSON.stringify({
        approved: true,
        opportunity,
      }),
    },
  );
}

export function rejectMission(
  opportunity?: MissionOpportunity | Opportunity,
) {
  return request<{ status: string; message: string; next_step?: string }>(
    "/approve-mission",
    {
      method: "POST",

      body: JSON.stringify({
        approved: false,
        opportunity,
      }),
    },
  );
}


// ============================================================
// DRAFT API
// ============================================================

export function getDrafts() {
  return request<Draft[]>(
    "/drafts",
    {
      cache: "no-store",
    },
  );
}

export function approveDraft(
  id: number,
) {
  return request<Draft>(
    `/drafts/${id}/approve`,
    {
      method: "POST",
    },
  );
}

export function rejectDraft(
  id: number,
) {
  return request<Draft>(
    `/drafts/${id}/reject`,
    {
      method: "POST",
    },
  );
}


// ============================================================
// APPOINTMENTS API
// ============================================================

export function getAppointments() {
  return request<Appointment[]>(
    "/appointments",
    {
      cache: "no-store",
    },
  );
}

export function createAppointment(payload: {
  lead_id: number;
  scheduled_for: string;
  status?: string;
  notes?: string;
}) {
  return request<Appointment>(
    "/appointments",
    {
      method: "POST",
      body: JSON.stringify(payload),
    },
  );
}


// ============================================================
// PROSPECT API
// ============================================================

export function getProspects() {
  return request<Prospect[]>(
    "/prospects",
    {
      cache: "no-store",
    },
  );
}

export function createProspect(
  payload: {
    business_name: string;
    category?: string;
    city?: string;
    contact_name?: string;
    contact_handle?: string;
    audit_summary?: string;
  },
) {
  return request<Prospect>(
    "/prospects",
    {
      method: "POST",

      body: JSON.stringify(payload),
    },
  );
}


// ============================================================
// OUTREACH API
// ============================================================

export function getOutreachList() {
  return request<Outreach[]>(
    "/outreach",
    {
      cache: "no-store",
    },
  );
}

export function createOutreach(
  prospectId: number,
  message: string,
  channel: string = "instagram",
) {
  return request<Outreach>(
    `/prospects/${prospectId}/outreach`,
    {
      method: "POST",

      body: JSON.stringify({
        message,
        channel,
      }),
    },
  );
}

export function approveOutreach(outreachId: number) {
  return request<Outreach>(
    `/outreach/${outreachId}/approve`,
    {
      method: "POST",
    },
  );
}

export function recordOutreachSend(outreachId: number) {
  return request<{ message: string; outreach: Outreach }>(
    `/outreach/${outreachId}/record-send`,
    {
      method: "POST",
    },
  );
}

export function recordOutreachResponse(outreachId: number, responseStatus: string) {
  return request<Outreach>(
    `/outreach/${outreachId}/response`,
    {
      method: "POST",
      body: JSON.stringify({
        response_status: responseStatus,
      }),
    },
  );
}


// ============================================================
// LEADS API
// ============================================================

export function getLeads() {
  return request<Lead[]>(
    "/leads",
    {
      cache: "no-store",
    },
  );
}

export function createLead(payload: {
  name: string;
  prospect_id?: number | null;
  source?: string;
  status?: string;
  notes?: string | null;
}) {
  return request<Lead>(
    "/leads",
    {
      method: "POST",
      body: JSON.stringify(payload),
    },
  );
}

export function updateLeadStatus(
  leadId: number,
  status: string,
  notes?: string | null,
) {
  return request<Lead>(
    `/leads/${leadId}/status`,
    {
      method: "POST",
      body: JSON.stringify({
        status,
        notes,
      }),
    },
  );
}


// ============================================================
// TRENDS API
// ============================================================

export function getTrends() {
  return request<
    Array<{
      title: string;
      angle: string;
      status: string;
    }>
  >(
    "/trends",
    {
      cache: "no-store",
    },
  );
}


// ============================================================
// ERROR API
// ============================================================

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
  >(
    "/errors",
    {
      cache: "no-store",
    },
  );
}