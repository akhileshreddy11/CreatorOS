import json
from pathlib import Path

from app.agents.trend_hunter import TrendHunter
from app.agents.niche_researcher import NicheResearcher
from app.agents.niche_ranking import NicheRanking
from app.agents.opportunity_generator import OpportunityGenerator
from app.services.ai_brain import AIBrain


class BusinessPartner:
    """
    CreatorOS COO

    Responsibilities:
    - Understand the business
    - Discover trends
    - Research profitable niches
    - Rank niches
    - Generate business opportunities
    - Select the strongest opportunity
    - Evaluate business potential
    - Recommend the best strategy
    - Wait for CEO approval
    """

    def __init__(self):

        self.memory_path = (
            Path(__file__).parent.parent
            / "memory"
            / "business_profile.json"
        )

        self.business = self.load_business_profile()

        # Intelligence employees
        self.trend_hunter = TrendHunter()
        self.niche_researcher = NicheResearcher()
        self.niche_ranking = NicheRanking()
        self.opportunity_generator = OpportunityGenerator()

        # AI brain
        self.brain = AIBrain()

    def load_business_profile(self):

        with open(
            self.memory_path,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    def evaluate_opportunity(self, opportunity):

        system_prompt = """
You are the Chief Operating Officer of CreatorOS.

You are evaluating a business opportunity selected by the
CreatorOS intelligence pipeline.

Your job is to think like a practical business executive.

Evaluate the opportunity based on:

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
- Do not include ```json.
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

        response = self.brain.think(
            system_prompt,
            user_prompt
        )

        return self._parse_json(response)

    def morning_brief(self):

        business = self.business["business"]
        goals = self.business["goals"]

        # --------------------------------------------------
        # STEP 1: Discover current opportunity signals
        # --------------------------------------------------

        trend_opportunity = self.trend_hunter.analyze()

        # --------------------------------------------------
        # STEP 2: Research profitable niches
        # --------------------------------------------------

        niche_research = self.niche_researcher.research()

        # --------------------------------------------------
        # STEP 3: Rank possible niches
        # --------------------------------------------------

        niche_ranking = self.niche_ranking.rank(
            niche_research
        )

        # --------------------------------------------------
        # STEP 4: Select the winning niche
        # --------------------------------------------------

        best_niche = niche_ranking.get(
            "best_niche"
        )

        if not best_niche:

            best_niche = niche_research

        # --------------------------------------------------
        # STEP 5: Generate business opportunities
        # --------------------------------------------------

        opportunity_data = self.opportunity_generator.generate(
            best_niche
        )

        # --------------------------------------------------
        # STEP 6: Select strongest opportunity
        # --------------------------------------------------

        best_opportunity = opportunity_data.get(
            "best_opportunity"
        )

        if not best_opportunity:

            return {
                "greeting": "Good Morning Boss 👋",
                "business": business["name"],
                "monthly_goal": goals.get(
                    "monthly_income",
                    self.business.get("operating_configuration", {}).get(
                        "primary_kpi",
                        "trial_class_enquiries"
                    )
                ),
                "platform": goals.get(
                    "primary_platform",
                    self.business.get("operating_configuration", {}).get(
                        "content_platforms",
                        ["Instagram"]
                    )[0]
                ),
                "automation": goals.get(
                    "automation_level",
                    "Approval-gated"
                ),
                "status": "FAILED",
                "reason": (
                    "Opportunity Generator did not return "
                    "a best opportunity."
                )
            }

        # --------------------------------------------------
        # STEP 7: COO evaluates winning opportunity
        # --------------------------------------------------

        evaluation = self.evaluate_opportunity(
            best_opportunity
        )

        # --------------------------------------------------
        # FINAL COO REPORT
        # --------------------------------------------------

        return {

            "greeting": "Good Morning Boss 👋",

            "business": business["name"],

            "monthly_goal": goals.get(
                "monthly_income",
                self.business.get("operating_configuration", {}).get(
                    "primary_kpi",
                    "trial_class_enquiries"
                )
            ),

            "platform": goals.get(
                "primary_platform",
                self.business.get("operating_configuration", {}).get(
                    "content_platforms",
                    ["Instagram"]
                )[0]
            ),

            "automation": goals.get(
                "automation_level",
                "Approval-gated"
            ),

            "trend_opportunity": trend_opportunity,

            "niche_research": niche_research,

            "niche_ranking": niche_ranking,

            "selected_niche": best_niche,

            "opportunity_generation": opportunity_data,

            "selected_opportunity": best_opportunity,

            "coo_evaluation": evaluation,

            "status": "Awaiting CEO Approval"
        }

    def _parse_json(self, response):

        if isinstance(response, dict):
            return response

        cleaned = response.strip()

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
                "error": "COO returned invalid JSON",
                "raw_response": response
            }