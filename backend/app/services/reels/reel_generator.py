from pathlib import Path

from moviepy import AudioFileClip, concatenate_videoclips

from app.services.reels.voice_generator import VoiceGenerator
from app.services.reels.visual_engine import VisualEngine


class ReelGenerator:
    """Render validated CreatorOS content into a narrated 9:16 Instagram Reel."""

    WIDTH = 1080
    HEIGHT = 1920
    FPS = 30

    def __init__(self, voice_generator=None, visual_engine=None, output_dir=None):
        self.output_dir = Path(output_dir or "generated_reels")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.voice_generator = voice_generator or VoiceGenerator()
        self.visual_engine = visual_engine or VisualEngine()

    @staticmethod
    def _clean_text(value):
        if value is None:
            return ""
        return str(value).strip()

    def _split_script(self, script):
        text = self._clean_text(script).replace("\r", "\n")
        if not text:
            return []

        raw_parts = []
        for line in text.split("\n"):
            line = line.strip()
            if not line:
                continue
            sentences = [part.strip() for part in line.replace("!", "!\n").replace("?", "?\n").replace(".", ".\n").split("\n") if part.strip()]
            raw_parts.extend(sentences or [line])

        scenes = []
        current = ""
        for part in raw_parts:
            candidate = f"{current} {part}".strip()
            if current and len(candidate) > 150:
                scenes.append(current)
                current = part
            else:
                current = candidate
        if current:
            scenes.append(current)
        return scenes

    @staticmethod
    def _calculate_scene_durations(scene_texts, total_duration):
        if not scene_texts:
            return []
        total_duration = max(float(total_duration or 0), 0.5)
        weights = [max(len(text.strip()), 1) for text in scene_texts]
        total_weight = sum(weights)
        return [total_duration * weight / total_weight for weight in weights]

    def _build_scene_texts(self, content):
        hook = self._clean_text(content.get("hook"))
        script = self._clean_text(content.get("script"))
        cta = self._clean_text(content.get("cta"))
        scenes = []
        if hook:
            scenes.append(hook)
        scenes.extend(self._split_script(script))
        if cta:
            scenes.append(cta)
        return scenes or ["CreatorOS"]

    def create_reel(self, content, output_name="creatoros_reel.mp4", language="en"):
        if not isinstance(content, dict):
            raise ValueError("Reel Generator requires a content object.")

        narration_parts = [
            self._clean_text(content.get("hook")),
            self._clean_text(content.get("script")),
            self._clean_text(content.get("cta")),
        ]
        narration_text = " ".join(part for part in narration_parts if part)
        if not narration_text:
            raise ValueError("Reel Generator received no content to narrate.")

        output_name = Path(output_name).name
        if not output_name.lower().endswith(".mp4"):
            output_name += ".mp4"
        output_path = self.output_dir / output_name

        audio_name = f"{output_path.stem}_{language}.mp3"
        audio_path = self.voice_generator.create_voice(
            text=narration_text,
            language=language,
            output_name=audio_name,
        )
        print(f"[Reel Generator] Voice ready: {audio_path}", flush=True)
        print("[Reel Generator] Loading narration audio...", flush=True)
        audio = AudioFileClip(str(audio_path))
        scenes = []
        final_video = None

        try:
            duration = float(audio.duration or 0)
            if duration <= 0:
                raise ValueError("Generated narration has no usable duration.")
            print(f"[Reel Generator] Narration duration: {duration:.2f}s", flush=True)

            scene_texts = self._build_scene_texts(content)
            durations = self._calculate_scene_durations(scene_texts, duration)
            print(f"[Reel Generator] Building {len(scene_texts)} visual scenes...", flush=True)

            for index, (text, scene_duration) in enumerate(zip(scene_texts, durations)):
                print(f"[Reel Generator] Scene {index + 1}/{len(scene_texts)}: {scene_duration:.2f}s", flush=True)
                scene = self.visual_engine.create_scene(
                    text=text,
                    duration=max(scene_duration, 0.05),
                    scene_number=index,
                )
                scenes.append(scene)

            if not scenes:
                raise RuntimeError("Reel generation produced no scenes.")

            print("[Reel Generator] Combining scenes...", flush=True)
            final_video = concatenate_videoclips(scenes, method="compose")
            final_video = final_video.with_duration(duration).with_audio(audio)
            print(f"[Reel Generator] Rendering {self.WIDTH}x{self.HEIGHT} @ {self.FPS}fps...", flush=True)
            final_video.write_videofile(
                str(output_path),
                fps=self.FPS,
                codec="libx264",
                audio_codec="aac",
                audio=True,
                preset="ultrafast",
                threads=4,
                logger="bar",
            )

            if not output_path.exists() or output_path.stat().st_size == 0:
                raise RuntimeError("Reel render completed without a valid MP4 file.")

            print(f"[Reel Generator] Reel saved: {output_path} ({output_path.stat().st_size} bytes)", flush=True)
            return str(output_path)
        finally:
            if final_video is not None:
                final_video.close()
            for scene in scenes:
                scene.close()
            audio.close()
