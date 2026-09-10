"""Local photorealistic talking-presenter generation using SadTalker.

SadTalker takes one portrait image plus speech audio and generates a talking-head
video with audio-driven lip motion, facial expression and head pose. It runs
locally; no avatar SaaS account or API key is required.
"""

from __future__ import annotations

import os
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass
class LocalAvatarResult:
    video_path: Path
    provider: str = "sadtalker"


class SadTalkerGenerationError(RuntimeError):
    """Raised when the local SadTalker pipeline cannot generate a video."""


class SadTalkerGenerator:
    """Run a local SadTalker installation from CreatorOS."""

    def __init__(self, project_root: Optional[str | Path] = None):
        backend_root = Path(__file__).resolve().parents[3]
        self.project_root = Path(project_root or os.getenv("CREATOROS_PROJECT_ROOT") or backend_root.parent)
        self.sadtalker_dir = Path(
            os.getenv("CREATOROS_SADTALKER_DIR")
            or self.project_root / "tools" / "SadTalker"
        )
        self.source_image = Path(
            os.getenv("CREATOROS_AVATAR_IMAGE")
            or self.project_root / "assets" / "creatoros_presenter.png"
        )
        configured_python = os.getenv("CREATOROS_SADTALKER_PYTHON")
        self.python_executable = Path(configured_python) if configured_python else self._default_python()
        self.result_root = Path(
            os.getenv("CREATOROS_SADTALKER_RESULTS")
            or self.project_root / "backend" / "generated_reels" / "sadtalker_results"
        )

    def _default_python(self) -> Path:
        if os.name == "nt":
            return self.sadtalker_dir / ".venv" / "Scripts" / "python.exe"
        return self.sadtalker_dir / ".venv" / "bin" / "python"

    def generate(self, audio_path: str | Path, output_path: str | Path) -> LocalAvatarResult:
        audio_path = Path(audio_path).resolve()
        output_path = Path(output_path).resolve()
        self._validate_installation(audio_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        self.result_root.mkdir(parents=True, exist_ok=True)

        run_dir = self.result_root / output_path.stem
        run_dir.mkdir(parents=True, exist_ok=True)
        before = {p.resolve() for p in run_dir.rglob("*.mp4")}

        command = [
            str(self.python_executable),
            str(self.sadtalker_dir / "inference.py"),
            "--driven_audio",
            str(audio_path),
            "--source_image",
            str(self.source_image.resolve()),
            "--result_dir",
            str(run_dir.resolve()),
            "--still",
            "--preprocess",
            "full",
            "--expression_scale",
            os.getenv("CREATOROS_SADTALKER_EXPRESSION_SCALE", "1.0"),
        ]

        print("[Avatar Generator] Starting local photorealistic presenter...", flush=True)
        print(f"[Avatar Generator] Presenter: {self.source_image}", flush=True)
        print(f"[Avatar Generator] Engine: SadTalker ({self.python_executable})", flush=True)

        try:
            completed = subprocess.run(
                command,
                cwd=str(self.sadtalker_dir),
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                check=False,
            )
        except OSError as exc:
            raise SadTalkerGenerationError(f"Unable to start SadTalker: {exc}") from exc

        if completed.stdout:
            print(completed.stdout, end="", flush=True)
        if completed.returncode != 0:
            raise SadTalkerGenerationError(
                f"SadTalker exited with code {completed.returncode}. See the backend log above."
            )

        candidates = sorted(
            [p for p in run_dir.rglob("*.mp4") if p.resolve() not in before],
            key=lambda p: p.stat().st_mtime,
            reverse=True,
        )
        if not candidates:
            raise SadTalkerGenerationError(
                f"SadTalker completed but no MP4 was produced in {run_dir}."
            )

        generated = candidates[0]
        generated.replace(output_path)
        print(
            f"[Avatar Generator] Photorealistic presenter saved: {output_path} "
            f"({output_path.stat().st_size} bytes)",
            flush=True,
        )
        return LocalAvatarResult(video_path=output_path)

    def _validate_installation(self, audio_path: Path) -> None:
        if not audio_path.exists() or audio_path.stat().st_size == 0:
            raise SadTalkerGenerationError(f"Narration audio does not exist: {audio_path}")
        if not self.sadtalker_dir.exists():
            raise SadTalkerGenerationError(
                f"SadTalker is not installed at {self.sadtalker_dir}. Run backend/scripts/setup_sadtalker.ps1."
            )
        if not (self.sadtalker_dir / "inference.py").exists():
            raise SadTalkerGenerationError(f"SadTalker inference.py is missing: {self.sadtalker_dir}")
        if not self.python_executable.exists():
            raise SadTalkerGenerationError(
                f"SadTalker Python environment is missing: {self.python_executable}. "
                "Run backend/scripts/setup_sadtalker.ps1."
            )
        if not self.source_image.exists() or self.source_image.stat().st_size == 0:
            raise SadTalkerGenerationError(
                f"Presenter image is missing: {self.source_image}. "
                "Place the CreatorOS generated presenter image there."
            )
