from pathlib import Path

from moviepy import AudioFileClip

from app.services.reels.avatar_generator import AvatarGenerator
from app.services.reels.voice_generator import VoiceGenerator


class ReelGenerator:
    """Render CreatorOS content into a vertical Reel with a speaking avatar."""

    WIDTH = 1080
    HEIGHT = 1920
    FPS = 30

    def __init__(self, voice_generator=None, visual_engine=None, avatar_generator=None, output_dir=None):
        self.output_dir = Path(output_dir or "generated_reels")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.voice_generator = voice_generator or VoiceGenerator()
        self.avatar_generator = avatar_generator or AvatarGenerator()

    @staticmethod
    def _clean_text(value):
        return "" if value is None else str(value).strip()

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

        avatar_path = self.output_dir / f"{output_path.stem}_avatar.mp4"
        print("[Reel Generator] Generating free talking avatar...", flush=True)
        avatar_result = self.avatar_generator.generate(
            audio_path=audio_path,
            output_path=avatar_path,
        )
        print(f"[Reel Generator] Talking avatar ready: {avatar_result.video_path}", flush=True)

        from moviepy import VideoFileClip

        avatar_video = None
        audio = None
        final_video = None
        try:
            avatar_video = VideoFileClip(str(avatar_result.video_path))
            audio = AudioFileClip(str(audio_path))
            duration = min(float(avatar_video.duration or 0), float(audio.duration or 0))
            if duration <= 0:
                raise ValueError("Generated avatar video has no usable duration.")

            avatar_video = avatar_video.with_duration(duration).with_audio(audio)
            final_video = avatar_video
            print(
                f"[Reel Generator] Rendering final Reel {self.WIDTH}x{self.HEIGHT} @ {self.FPS}fps...",
                flush=True,
            )
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
                raise RuntimeError("Talking-avatar Reel render completed without a valid MP4 file.")
            print(
                f"[Reel Generator] Talking-avatar Reel saved: {output_path} "
                f"({output_path.stat().st_size} bytes)",
                flush=True,
            )
            return str(output_path)
        finally:
            if final_video is not None:
                final_video.close()
            if avatar_video is not None:
                avatar_video.close()
            if audio is not None:
                audio.close()
