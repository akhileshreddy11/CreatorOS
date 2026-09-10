"""Free local talking-avatar generation for CreatorOS Reels.

This module deliberately has no paid avatar-service dependency.  It creates a
clean presenter-style avatar locally and drives mouth motion from the generated
Edge-TTS narration.  The provider interface is kept small so a higher-fidelity
local lip-sync model such as MuseTalk can be plugged in later without changing
the Reel pipeline.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import numpy as np
from moviepy import AudioFileClip, VideoClip


@dataclass
class AvatarResult:
    video_path: Path
    provider: str
    video_id: str


class AvatarGenerationError(RuntimeError):
    """Raised when local talking-avatar generation fails."""


class AvatarGenerator:
    """Generate a free local presenter avatar driven by CreatorOS narration."""

    WIDTH = 540
    HEIGHT = 960
    FPS = 24
    AUDIO_ANALYSIS_FPS = 60

    def __init__(self, provider: Optional[str] = None):
        self.provider = (
            provider
            or __import__("os").getenv("CREATOROS_AVATAR_PROVIDER", "local")
        ).strip().lower()

    def generate(self, audio_path: str | Path, output_path: str | Path) -> AvatarResult:
        if self.provider in {"", "none", "disabled", "local", "free", "builtin"}:
            return self._generate_local(audio_path, output_path)
        if self.provider in {"musetalk", "local_musetalk"}:
            raise AvatarGenerationError(
                "MuseTalk is selected but is not installed yet. Use CREATOROS_AVATAR_PROVIDER=local "
                "for the zero-setup free avatar, or install the optional MuseTalk runtime."
            )
        if self.provider == "heygen":
            raise AvatarGenerationError(
                "HeyGen is a paid provider and is intentionally disabled in the free CreatorOS pipeline."
            )
        raise AvatarGenerationError(f"Unsupported avatar provider: {self.provider}")

    def _generate_local(self, audio_path: str | Path, output_path: str | Path) -> AvatarResult:
        audio_path = Path(audio_path)
        output_path = Path(output_path)
        if not audio_path.exists() or audio_path.stat().st_size == 0:
            raise AvatarGenerationError(f"Narration audio does not exist: {audio_path}")
        output_path.parent.mkdir(parents=True, exist_ok=True)

        print("[Avatar Generator] Using free local talking avatar...", flush=True)
        audio = AudioFileClip(str(audio_path))
        try:
            duration = float(audio.duration or 0)
            if duration <= 0:
                raise AvatarGenerationError("Narration has no usable duration.")

            # A small amplitude envelope is enough for natural open/close mouth
            # motion without decoding the full audio at video-frame frequency.
            analysis = audio.to_soundarray(
                fps=self.AUDIO_ANALYSIS_FPS,
                nbytes=2,
                buffersize=12000,
            )
            if analysis.ndim == 2:
                mono = np.mean(analysis.astype(np.float32), axis=1)
            else:
                mono = analysis.astype(np.float32)
            envelope = np.sqrt(np.maximum(np.convolve(mono * mono, np.ones(5) / 5, mode="same"), 0.0))
            peak = float(np.percentile(envelope, 95)) if envelope.size else 1.0
            peak = max(peak, 1e-4)
            envelope = np.clip(envelope / peak, 0.0, 1.0)

            def mouth_level(t: float) -> float:
                idx = min(int(max(t, 0.0) * self.AUDIO_ANALYSIS_FPS), len(envelope) - 1)
                level = float(envelope[idx]) if len(envelope) else 0.0
                # Add a small rhythmic component so low-volume phonemes do not
                # freeze the mouth completely.
                return max(0.04, min(1.0, level * 0.92 + 0.08 * (0.5 + 0.5 * math.sin(t * 17.0))))

            frame = self._frame_factory(mouth_level)
            clip = VideoClip(frame_function=frame, duration=duration)
            clip = clip.with_audio(audio)
            try:
                print(
                    f"[Avatar Generator] Rendering local avatar {self.WIDTH}x{self.HEIGHT} @ {self.FPS}fps...",
                    flush=True,
                )
                clip.write_videofile(
                    str(output_path),
                    fps=self.FPS,
                    codec="libx264",
                    audio_codec="aac",
                    audio=True,
                    preset="ultrafast",
                    threads=4,
                    logger="bar",
                )
            finally:
                clip.close()

            if not output_path.exists() or output_path.stat().st_size == 0:
                raise AvatarGenerationError("Local avatar render produced an empty video.")

            print(
                f"[Avatar Generator] Free talking avatar saved: {output_path} "
                f"({output_path.stat().st_size} bytes)",
                flush=True,
            )
            return AvatarResult(
                video_path=output_path,
                provider="local",
                video_id=f"local-{output_path.stem}",
            )
        finally:
            audio.close()

    def _frame_factory(self, mouth_level):
        width, height = self.WIDTH, self.HEIGHT
        yy, xx = np.mgrid[0:height, 0:width]
        x = xx.astype(np.float32)
        y = yy.astype(np.float32)

        # Premium-looking dark studio background with a soft center glow.
        radial = np.sqrt(((x - width * 0.5) / width) ** 2 + ((y - height * 0.40) / height) ** 2)
        glow = np.clip(1.0 - radial * 2.2, 0.0, 1.0)
        background = np.zeros((height, width, 3), dtype=np.uint8)
        background[..., 0] = (11 + 20 * glow).astype(np.uint8)
        background[..., 1] = (16 + 24 * glow).astype(np.uint8)
        background[..., 2] = (29 + 34 * glow).astype(np.uint8)

        # Presenter geometry.
        face = (((x - width * 0.5) / (width * 0.245)) ** 2 + ((y - height * 0.34) / (height * 0.255)) ** 2) <= 1
        ears = (
            (((x - width * 0.252) / (width * 0.035)) ** 2 + ((y - height * 0.35) / (height * 0.055)) ** 2) <= 1
        ) | (
            (((x - width * 0.748) / (width * 0.035)) ** 2 + ((y - height * 0.35) / (height * 0.055)) ** 2) <= 1
        )
        neck = (x > width * 0.43) & (x < width * 0.57) & (y > height * 0.50) & (y < height * 0.68)
        shoulders = (((x - width * 0.5) / (width * 0.47)) ** 2 + ((y - height * 0.82) / (height * 0.30)) ** 2) <= 1
        hair = face & (
            (((x - width * 0.5) / (width * 0.25)) ** 2 + ((y - height * 0.31) / (height * 0.22)) ** 2) <= 1
        ) & (y < height * 0.36)

        skin = np.array([205, 145, 112], dtype=np.uint8)
        shirt = np.array([31, 43, 68], dtype=np.uint8)
        hair_color = np.array([25, 20, 20], dtype=np.uint8)
        eye = np.array([18, 15, 13], dtype=np.uint8)
        white = np.array([245, 245, 242], dtype=np.uint8)

        def render(t: float):
            image = background.copy()
            image[shoulders] = shirt
            image[neck] = skin
            image[face | ears] = skin
            image[hair] = hair_color

            # Eyes and brows.
            left_eye = (((x - width * 0.42) / (width * 0.045)) ** 2 + ((y - height * 0.345) / (height * 0.018)) ** 2) <= 1
            right_eye = (((x - width * 0.58) / (width * 0.045)) ** 2 + ((y - height * 0.345) / (height * 0.018)) ** 2) <= 1
            image[left_eye | right_eye] = white
            left_pupil = (((x - width * 0.42) / (width * 0.013)) ** 2 + ((y - height * 0.345) / (height * 0.013)) ** 2) <= 1
            right_pupil = (((x - width * 0.58) / (width * 0.013)) ** 2 + ((y - height * 0.345) / (height * 0.013)) ** 2) <= 1
            image[left_pupil | right_pupil] = eye

            # Nose shadow/highlight.
            nose = (((x - width * 0.5) / (width * 0.022)) ** 2 + ((y - height * 0.405) / (height * 0.065)) ** 2) <= 1
            image[nose] = np.array([184, 124, 95], dtype=np.uint8)

            # Audio-driven mouth: opening height grows with narration energy.
            level = mouth_level(t)
            mouth_center_y = height * 0.455
            mouth_w = width * 0.085
            mouth_h = height * (0.010 + 0.040 * level)
            mouth = (((x - width * 0.5) / mouth_w) ** 2 + ((y - mouth_center_y) / mouth_h) ** 2) <= 1
            image[mouth] = np.array([58, 18, 24], dtype=np.uint8)

            # Teeth appear on stronger syllables for a more expressive result.
            teeth_h = max(1.0, mouth_h * 0.20)
            teeth = mouth & (y < mouth_center_y - mouth_h * 0.15) & (y > mouth_center_y - teeth_h)
            image[teeth] = np.array([238, 232, 220], dtype=np.uint8)

            # Subtle chest highlight.
            highlight = shoulders & (((x - width * 0.5) / (width * 0.28)) ** 2 + ((y - height * 0.70) / (height * 0.20)) ** 2 <= 1)
            image[highlight] = np.clip(image[highlight].astype(np.int16) + np.array([8, 9, 12]), 0, 255).astype(np.uint8)
            return image

        return render
