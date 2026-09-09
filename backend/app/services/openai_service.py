"""Provider compatibility note.

CreatorOS currently uses ``AIBrain`` with Gemini. This module stays as a clear
extension point for callers that imported the old placeholder, but it does not
silently route requests to a different provider.
"""


class OpenAIService:
    """Explicitly reject the retired provider integration."""

    def __init__(self, *args, **kwargs):
        raise RuntimeError(
            "OpenAI is not configured for CreatorOS. Use app.services.ai_brain.AIBrain "
            "with the Gemini provider instead."
        )
