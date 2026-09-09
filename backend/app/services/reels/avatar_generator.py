"""Talking-avatar generation boundary for CreatorOS Reels.

The local pipeline already owns script generation and TTS. This module provides a
provider boundary so a real avatar/lip-sync service can be plugged in without
rewriting mission execution. Until a provider is configured, it fails clearly
instead of silently producing a non-speaking Reel.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass
class AvatarResult:
    video_path: Path
    provider: str


class AvatarGenerationError(RuntimeError):
    """Raised when a configured talking-avatar provider cannot generate video."""


class AvatarGenerator:
    """Generate a lip-synced presenter video from an image and narration audio.

    Provider integration is selected through AVATAR_PROVIDER. Supported values
    are currently ``none`` and ``heygen``. The HeyGen adapter is intentionally
    kept behind this boundary so API credentials never enter mission logic.
    """

    def __init__(self, provider: Optional[str] = None):
        self.provider = (provider or os.getenv("AVATAR_PROVIDER", "none")).strip().lower()

    def generate(self, image_path: str | Path, audio_path: str | Path, output_path: str | Path) -> AvatarResult:
        if self.provider in {"", "none", "disabled"}:
            raise AvatarGenerationError(
                "Talking avatar is not configured. Set AVATAR_PROVIDER and the provider credentials."
            )

        if self.provider == "heygen":
            return self._generate_heygen(image_path, audio_path, output_path)

        raise AvatarGenerationError(f"Unsupported avatar provider: {self.provider}")

    def _generate_heygen(self, image_path: str | Path, audio_path: str | Path, output_path: str | Path) -> AvatarResult:
        # Kept as a clear integration boundary rather than faking lip-sync locally.
        # A production adapter must submit the image + audio to the provider and
        # download the completed MP4 to output_path.
        raise AvatarGenerationError(
            "HeyGen adapter is not wired to the provider API yet. Configure a provider integration before enabling it."
        )
