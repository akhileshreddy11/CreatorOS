"""Orchestrate the approval-aware morning operating brief."""

from app.agents.business_partner import BusinessPartner


class MorningWorkflow:
    """Run intelligence preparation without executing external actions."""

    def run(self) -> dict:
        return BusinessPartner().morning_brief()
