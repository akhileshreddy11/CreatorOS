"""
CreatorOS Opportunity Safety Gate

Validates selected business opportunities, recommended content, and
proposed deliverables before CEO approval.

Specifically guards against:
- Medical and physiotherapy claims (e.g. assuming qualified physiotherapists)
- Professional credential assumptions
- Health and outcome guarantees
- Revenue and client guarantees
- Fabricated statistics or testimonials
- Deceptive or high-risk claims
"""

import re
from typing import Any


class OpportunitySafetyGate:
    """
    Evaluates business opportunities for compliance, credential assumptions,
    and unsupported claims.
    """

    def __init__(self):
        self.rules = [
            {
                "category": "Medical & Physiotherapy Claims",
                "pattern": (
                    r"\b(physiotherap(?:y|ist)s?|physical therap(?:y|ist)s?|"
                    r"chiropractic|chiropractors?|medical assessment|doctor|"
                    r"diagnos(?:e|is|ed)|clinical|rehabilitation|rehab protocol|"
                    r"cure disease|treat pain|orthopedic|prescribed)\b"
                ),
                "severity": "high",
                "message": (
                    "Medical or physiotherapy claims detected. Do not assume "
                    "the business has licensed physiotherapists or medical staff "
                    "without explicit confirmation."
                ),
            },
            {
                "category": "Professional Credentials",
                "pattern": (
                    r"\b(licensed therapist|board-certified|certified physician|"
                    r"medical doctor|registered dietitian|licensed medical)\b"
                ),
                "severity": "high",
                "message": (
                    "Professional credential references detected. Ensure all referenced "
                    "certifications actually exist."
                ),
            },
            {
                "category": "Health & Outcome Guarantees",
                "pattern": (
                    r"\b(guaranteed (?:weight loss|results|transformation|fitness|fat loss)|"
                    r"lose \d+\s*(?:kg|lbs|pounds) guaranteed|100% (?:guaranteed|cure|effective)|"
                    r"permanent fix|guaranteed cure)\b"
                ),
                "severity": "high",
                "message": (
                    "Guaranteed health or fitness outcome detected. CreatorOS does not "
                    "permit unconditional outcome guarantees."
                ),
            },
            {
                "category": "Revenue & Business Guarantees",
                "pattern": (
                    r"\b(guaranteed (?:income|revenue|profit|clients|customers|enquiries)|"
                    r"make \$\d+ guaranteed|earn \$\d+ guaranteed|guaranteed \$\d+)\b"
                ),
                "severity": "high",
                "message": (
                    "Guaranteed revenue or client count detected. Financial outcomes "
                    "cannot be guaranteed."
                ),
            },
            {
                "category": "Fabricated Statistics & Claims",
                "pattern": (
                    r"\b(\d+%\s*(?:success rate|guaranteed|results)|"
                    r"proven by \d+ customers|100% success rate)\b"
                ),
                "severity": "medium",
                "message": (
                    "Specific numeric success rate detected. Verify statistical basis "
                    "before launching."
                ),
            },
            {
                "category": "Deceptive Marketing",
                "pattern": (
                    r"\b(miracle (?:cure|solution|transformation)|"
                    r"secret loophole|magic pill|instant cure)\b"
                ),
                "severity": "high",
                "message": (
                    "Potentially deceptive marketing phrasing detected."
                ),
            },
        ]

    def _flatten_to_text(self, data: Any) -> str:
        if isinstance(data, dict):
            return " ".join(self._flatten_to_text(v) for v in data.values())
        if isinstance(data, list):
            return " ".join(self._flatten_to_text(item) for item in data)
        return str(data or "")

    def inspect(self, opportunity: dict[str, Any] | None, deliverables: list[str] | None = None) -> dict[str, Any]:
        """
        Inspect an opportunity dictionary and optional deliverables list.
        Returns safety assessment dictionary.
        """
        if not opportunity or not isinstance(opportunity, dict):
            return {
                "status": "NEEDS_REVIEW",
                "passed": False,
                "safety_score": 0,
                "warnings": ["No opportunity data provided for safety inspection."],
                "flags": [
                    {
                        "category": "Missing Data",
                        "issue": "Opportunity data is empty or invalid.",
                        "severity": "high",
                        "matched_text": "",
                    }
                ],
                "recommendation": "NEEDS_REVIEW",
                "summary": "Safety check could not be completed due to missing data.",
            }

        search_corpus = [
            self._flatten_to_text(opportunity),
            self._flatten_to_text(deliverables or []),
        ]
        combined_text = " ".join(search_corpus)

        flags = []
        warnings = []
        score = 100

        for rule in self.rules:
            matches = re.findall(rule["pattern"], combined_text, re.IGNORECASE)
            if matches:
                matched_sample = ", ".join(sorted(set(matches))[:3])
                flags.append(
                    {
                        "category": rule["category"],
                        "issue": rule["message"],
                        "severity": rule["severity"],
                        "matched_text": matched_sample,
                    }
                )
                warnings.append(f"{rule['category']}: {rule['message']} (Found: '{matched_sample}')")
                if rule["severity"] == "high":
                    score -= 30
                else:
                    score -= 15

        score = max(0, min(100, score))
        has_high_severity = any(f["severity"] == "high" for f in flags)
        passed = (len(flags) == 0) or (score >= 80 and not has_high_severity)

        status = "SAFE" if passed and len(flags) == 0 else "NEEDS_REVIEW"

        if status == "SAFE":
            summary = "Opportunity passed safety gate with no high-risk claims detected."
            recommendation = "SAFE_TO_EXECUTE"
        else:
            summary = (
                f"Safety gate detected {len(flags)} potential risk item(s). "
                "Owner review and modification recommended before execution."
            )
            recommendation = "REQUIRES_OWNER_REVIEW"

        return {
            "status": status,
            "passed": passed,
            "safety_score": score,
            "warnings": warnings,
            "flags": flags,
            "recommendation": recommendation,
            "summary": summary,
        }
