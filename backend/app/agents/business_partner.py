import json
import time
from pathlib import Path

from app.agents.trend_hunter import TrendHunter
from app.agents.niche_researcher import NicheResearcher
from app.agents.niche_ranking import NicheRanking
from app.agents.opportunity_generator import OpportunityGenerator
from app.services.ai_brain import AIBrain
from app.services.validation.opportunity_safety_gate import OpportunitySafetyGate


class BusinessPartner:
    """
    CreatorOS COO / Business Partner.

    Pipeline:

        Trend Hunter
             ↓
        Niche Researcher
             ↓
        Niche Ranking
             ↓
        Opportunity Generator
             ↓
        COO Evaluation
             ↓
        CEO Approval

    This class deliberately keeps the intelligence pipeline sequential
    because each stage depends on the result of the previous stage.

    Every stage is logged with timing information so a slow or failed
    intelligence employee can be identified immediately.
    """

    def __init__(self):
        self.memory_path = (
            Path(__file__).parent.parent
            / "memory"
            / "business_profile.json"
        )

        self.business = self.load_business_profile()

        print("[COO] Initializing intelligence employees...")

        self.trend_hunter = TrendHunter()
        self.niche_researcher = NicheResearcher()
        self.niche_ranking = NicheRanking()
        self.opportunity_generator = OpportunityGenerator()

        self.brain = AIBrain()
        self.safety_gate = OpportunitySafetyGate()

        print("[COO] Business Partner ready.")

    # ============================================================
    # BUSINESS PROFILE
    # ============================================================

    def load_business_profile(self):
        if not self.memory_path.exists():
            raise FileNotFoundError(
                f"Business profile not found: {self.memory_path}"
            )

        with open(
            self.memory_path,
            "r",
            encoding="utf-8",
        ) as file:
            return json.load(file)

    # ============================================================
    # STAGE LOGGER
    # ============================================================

    @staticmethod
    def _stage_start(name):
        print()
        print("=" * 60)
        print(f"[COO] STARTING: {name}")
        print("=" * 60)

        return time.perf_counter()

    @staticmethod
    def _stage_complete(name, started_at):
        elapsed = time.perf_counter() - started_at

        print()
        print(
            f"[COO] COMPLETED: {name} "
            f"in {elapsed:.2f}s"
        )

        return elapsed

    @staticmethod
    def _stage_failed(name, started_at, error):
        elapsed = time.perf_counter() - started_at

        print()
        print(
            f"[COO] FAILED: {name} "
            f"after {elapsed:.2f}s"
        )

        print(
            f"[COO] ERROR: {str(error)[:1000]}"
        )

    # ============================================================
    # JSON PARSER
    # ============================================================

    @staticmethod
    def _parse_json(response):
        if isinstance(response, dict):
            return response

        if response is None:
            return {
                "status": "FAILED",
                "error": "AI returned no response.",
            }

        cleaned = str(response).strip()

        if cleaned.startswith("```json"):
            cleaned = cleaned[7:]

        elif cleaned.startswith("```"):
            cleaned = cleaned[3:]

        if cleaned.endswith("```"):
            cleaned = cleaned[:-3]

        cleaned = cleaned.strip()

        try:
            return json.loads(cleaned)

        except json.JSONDecodeError:
            return {
                "status": "FAILED",
                "error": "AI returned invalid JSON.",
                "raw_response": response,
            }

    # ============================================================
    # SAFE FAILURE RESPONSE
    # ============================================================

    def _failure_response(
        self,
        business,
        goals,
        stage,
        error,
    ):
        return {
            "greeting": "Good Morning Boss 👋",
            "business": business.get(
                "name",
                "CreatorOS",
            ),
            "monthly_goal": goals.get(
                "monthly_income",
                self.business.get(
                    "operating_configuration",
                    {},
                ).get(
                    "primary_kpi",
                    "trial_class_enquiries",
                ),
            ),
            "platform": goals.get(
                "primary_platform",
                self.business.get(
                    "operating_configuration",
                    {},
                ).get(
                    "content_platforms",
                    ["Instagram"],
                )[0],
            ),
            "automation": goals.get(
                "automation_level",
                "Approval-gated",
            ),
            "status": "FAILED",
            "failed_stage": stage,
            "reason": str(error)[:1500],
        }

    # ============================================================
    # COO EVALUATION
    # ============================================================

    def evaluate_opportunity(self, opportunity):
        """
        Evaluate the selected opportunity using the COO AI brain.
        """

        stage = "COO Evaluation"
        started_at = self._stage_start(stage)

        system_prompt = """
You are the Chief Operating Officer of CreatorOS.

You are evaluating a business opportunity selected by the
CreatorOS intelligence pipeline.

Think like a practical business executive.

Evaluate:

1. Audience fit
2. Content potential
3. Monetization potential
4. Revenue alignment
5. Overall business potential

IMPORTANT:

- Do not claim access to live Instagram analytics.
- Do not invent real revenue numbers.
- Do not guarantee income.
- Use only the information provided.
- Be realistic and conservative.
- Return ONLY valid JSON.
- Do not use markdown.
- Do not use code fences.
"""

        user_prompt = f"""
Business Profile:

{json.dumps(self.business, indent=2)}

Selected Business Opportunity:

{json.dumps(opportunity, indent=2)}

Return JSON in exactly this format:

{{
    "audience_fit": 0,
    "content_potential": 0,
    "monetization_potential": 0,
    "revenue_alignment": 0,
    "overall_score": 0,
    "recommendation": "APPROVE",
    "reason": "...",
    "proposed_deliverables": [
        "...",
        "...",
        "..."
    ]
}}

All scores must be between 0 and 100.

Recommendation must be one of:

APPROVE
REVIEW
REJECT
"""

        try:
            response = self.brain.think(
                system_prompt,
                user_prompt,
            )

            result = self._parse_json(response)

            self._stage_complete(
                stage,
                started_at,
            )

            return result

        except Exception as error:
            self._stage_failed(
                stage,
                started_at,
                error,
            )

            return {
                "status": "FAILED",
                "recommendation": "REVIEW",
                "error": str(error)[:1500],
            }

    # ============================================================
    # MORNING BRIEF
    # ============================================================

    def morning_brief(self):
        """
        Run the complete CreatorOS intelligence pipeline.
        """

        total_started_at = time.perf_counter()

        business = self.business.get(
            "business",
            {},
        )

        goals = self.business.get(
            "goals",
            {},
        )

        print()
        print()
        print("#" * 70)
        print("# CREATOROS COO MORNING BRIEF")
        print("#" * 70)

        # ========================================================
        # STEP 1 — TREND HUNTER
        # ========================================================

        stage = "Trend Hunter"
        started_at = self._stage_start(stage)

        try:
            trend_opportunity = self.trend_hunter.analyze()

            self._stage_complete(
                stage,
                started_at,
            )

        except Exception as error:
            self._stage_failed(
                stage,
                started_at,
                error,
            )

            return self._failure_response(
                business,
                goals,
                stage,
                error,
            )

        # ========================================================
        # STEP 2 — NICHE RESEARCH
        # ========================================================

        stage = "Niche Researcher"
        started_at = self._stage_start(stage)

        try:
            niche_research = self.niche_researcher.research()

            self._stage_complete(
                stage,
                started_at,
            )

        except Exception as error:
            self._stage_failed(
                stage,
                started_at,
                error,
            )

            return self._failure_response(
                business,
                goals,
                stage,
                error,
            )

        # ========================================================
        # STEP 3 — NICHE RANKING
        # ========================================================

        stage = "Niche Ranking"
        started_at = self._stage_start(stage)

        try:
            niche_ranking = self.niche_ranking.rank(
                niche_research
            )

            self._stage_complete(
                stage,
                started_at,
            )

        except Exception as error:
            self._stage_failed(
                stage,
                started_at,
                error,
            )

            return self._failure_response(
                business,
                goals,
                stage,
                error,
            )

        # ========================================================
        # STEP 4 — SELECT NICHE
        # ========================================================

        best_niche = niche_ranking.get(
            "best_niche"
        )

        if not best_niche:
            best_niche = niche_research

        if not best_niche:
            return self._failure_response(
                business,
                goals,
                "Niche Selection",
                "No winning niche was returned.",
            )

        print()
        print(
            "[COO] SELECTED NICHE:"
        )

        print(
            json.dumps(
                best_niche,
                indent=2,
                ensure_ascii=False,
            )[:3000]
        )

        # ========================================================
        # STEP 5 — OPPORTUNITY GENERATION
        # ========================================================

        stage = "Opportunity Generator"
        started_at = self._stage_start(stage)

        try:
            opportunity_data = (
                self.opportunity_generator.generate(
                    best_niche
                )
            )

            self._stage_complete(
                stage,
                started_at,
            )

        except Exception as error:
            self._stage_failed(
                stage,
                started_at,
                error,
            )

            return self._failure_response(
                business,
                goals,
                stage,
                error,
            )

        # ========================================================
        # STEP 6 — SELECT OPPORTUNITY
        # ========================================================

        best_opportunity = opportunity_data.get(
            "best_opportunity"
        )

        if not best_opportunity:

            return self._failure_response(
                business,
                goals,
                "Opportunity Selection",
                (
                    "Opportunity Generator did not return "
                    "a best opportunity."
                ),
            )

        print()
        print(
            "[COO] SELECTED OPPORTUNITY:"
        )

        print(
            json.dumps(
                best_opportunity,
                indent=2,
                ensure_ascii=False,
            )
        )

        # STEP 7 — COO EVALUATION
        # ========================================================

        evaluation = self.evaluate_opportunity(
            best_opportunity
        )

        # ========================================================
        # STEP 8 — OPPORTUNITY SAFETY GATE
        # ========================================================

        safety_review = self.safety_gate.inspect(
            opportunity=best_opportunity,
            deliverables=evaluation.get("proposed_deliverables", []),
        )

        print()
        print(f"[COO] SAFETY GATE STATUS: {safety_review['status']} (Score: {safety_review['safety_score']}/100)")
        if safety_review.get("warnings"):
            for w in safety_review["warnings"]:
                print(f"[COO] SAFETY WARNING: {w}")

        # ========================================================
        # FINAL REPORT
        # ========================================================

        total_elapsed = (
            time.perf_counter()
            - total_started_at
        )

        print()
        print("#" * 70)
        print(
            f"# COO PIPELINE COMPLETE "
            f"IN {total_elapsed:.2f}s"
        )
        print("#" * 70)

        status = "NEEDS_REVIEW" if safety_review.get("status") == "NEEDS_REVIEW" else "Awaiting CEO Approval"

        return {
            "greeting": "Good Morning Boss 👋",

            "business": business.get(
                "name",
                "CreatorOS",
            ),

            "monthly_goal": goals.get(
                "monthly_income",
                self.business.get(
                    "operating_configuration",
                    {},
                ).get(
                    "primary_kpi",
                    "trial_class_enquiries",
                ),
            ),

            "platform": goals.get(
                "primary_platform",
                self.business.get(
                    "operating_configuration",
                    {},
                ).get(
                    "content_platforms",
                    ["Instagram"],
                )[0],
            ),

            "automation": goals.get(
                "automation_level",
                "Approval-gated",
            ),

            "trend_opportunity": trend_opportunity,

            "niche_research": niche_research,

            "niche_ranking": niche_ranking,

            "selected_niche": best_niche,

            "opportunity_generation": opportunity_data,

            "selected_opportunity": best_opportunity,

            "coo_evaluation": evaluation,

            "safety_review": safety_review,

            "status": status,

            "pipeline_time_seconds": round(
                total_elapsed,
                2,
            ),
        }