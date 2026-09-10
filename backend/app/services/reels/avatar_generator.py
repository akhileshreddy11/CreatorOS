"""Avatar provider facade for CreatorOS Reels.

The default provider is the local SadTalker photorealistic presenter. Paid hosted
avatar providers are intentionally not required. A simple built-in renderer is
kept only as a diagnostic fallback when explicitly selected.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from app.services.reels.sadtalker_generator import SadTalkerGenerator


@dataclass
class AvatarResult:
    video_path: Path
    provider: str
    video_id: str


class AvatarGenerationError(RuntimeError):
    """Raised when local avatar generation fails."""


class AvatarGenerator:
    """Generate the CreatorOS photorealistic presenter locally."""

    def __init__(self, provider: Optional[str] = None):
        self.provider = (
            provider
            or os.getenv("CREATOROS_AVATAR_PROVIDER", "sadtalker")
        ).strip().lower()
        self.sadtalker = SadTalkerGenerator()

    def generate(self, audio_path: str | Path, output_path: str | Path) -> AvatarResult:
        if self.provider in {"sadtalker", "local_sadtalker", "realistic", "local"}:
            result = self.sadtalker.generate(audio_path=audio_path, output_path=output_path)
            return AvatarResult(
                video_path=result.video_path,
                provider="sadtalker",
                video_id=f"sadtalker-{Path(output_path).stem}",
            )
        if self.provider in {"none", "disabled"}:
            raise AvatarGenerationError("Talking avatar is disabled.")
        if self.provider == "heygen":
            raise AvatarGenerationError(
                "HeyGen is intentionally disabled because CreatorOS is using the free local presenter."
            )
        raise AvatarGenerationError(f"Unsupported avatar provider: {self.provider}")
