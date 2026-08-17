from pathlib import Path

from moviepy import (
    TextClip,
    ColorClip,
    CompositeVideoClip,
    AudioFileClip
)

from app.services.reels.voice_generator import VoiceGenerator


class ReelGenerator:
    """
    CreatorOS Professional Reel Generation Engine

    Step 5:
    - Generates AI narration
    - Uses narration duration for the Reel
    - Creates multiple visual scenes
    - Adds animated text
    - Adds narration to the final video
    - Supports multilingual voice generation
    """

    WIDTH = 1080
    HEIGHT = 1920
    FPS = 30

    MIN_SCENE_DURATION = 3
    MAX_SCENE_DURATION = 6

    def __init__(self):
        self.output_dir = Path("generated_reels")
        self.output_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        self.voice_generator = VoiceGenerator()

    # =========================================================
    # CREATE TEXT CLIP
    # =========================================================

    def _create_text_clip(
        self,
        text,
        duration,
        scene_number
    ):
        """
        Create a readable vertical text scene.
        """

        text_clip = TextClip(
            text=text,
            font_size=68,
            color="white",
            size=(880, 1100),
            method="caption"
        )

        # -----------------------------------------------------
        # Scene-based positioning
        # -----------------------------------------------------

        if scene_number == 0:

            position = ("center", 700)

        elif scene_number % 2 == 0:

            position = ("center", 760)

        else:

            position = ("center", 820)

        text_clip = (
            text_clip
            .with_position(position)
            .with_duration(duration)
        )

        return text_clip

    # =========================================================
    # CREATE SCENE
    # =========================================================

    def _create_scene(
        self,
        text,
        duration,
        scene_number
    ):
        """
        Create one vertical Reel scene.
        """

        background = ColorClip(
            size=(self.WIDTH, self.HEIGHT),
            color=(15, 15, 20),
            duration=duration
        )

        text_clip = self._create_text_clip(
            text,
            duration,
            scene_number
        )

        scene = CompositeVideoClip(
            [
                background,
                text_clip
            ],
            size=(self.WIDTH, self.HEIGHT)
        )

        scene = scene.with_duration(duration)

        return scene

    # =========================================================
    # SPLIT SCRIPT
    # =========================================================

    def _split_script(
        self,
        script
    ):
        """
        Convert the script into readable Reel scenes.
        """

        if not script:
            return []

        script = (
            script
            .replace("\n", " ")
            .strip()
        )

        # -----------------------------------------------------
        # Split by sentence
        # -----------------------------------------------------

        sentences = [
            sentence.strip()
            for sentence in script.split(".")
            if sentence.strip()
        ]

        scenes = []

        current = ""

        for sentence in sentences:

            sentence = sentence.strip()

            if not current:

                current = sentence

                continue

            # Keep individual scenes readable
            if len(current) + len(sentence) <= 150:

                current += ". " + sentence

            else:

                scenes.append(
                    current + "."
                )

                current = sentence

        if current:

            scenes.append(
                current + "."
            )

        return scenes

    # =========================================================
    # CALCULATE SCENE DURATIONS
    # =========================================================

    def _calculate_scene_durations(
        self,
        scene_texts,
        total_duration
    ):
        """
        Distribute the narration duration across scenes.

        Longer scenes receive slightly more time.
        """

        if not scene_texts:

            return []

        total_characters = sum(
            len(text)
            for text in scene_texts
        )

        if total_characters <= 0:

            duration = (
                total_duration /
                len(scene_texts)
            )

            return [
                max(
                    self.MIN_SCENE_DURATION,
                    duration
                )
                for _ in scene_texts
            ]

        durations = []

        for text in scene_texts:

            proportion = (
                len(text) /
                total_characters
            )

            duration = (
                total_duration *
                proportion
            )

            duration = max(
                self.MIN_SCENE_DURATION,
                duration
            )

            duration = min(
                self.MAX_SCENE_DURATION,
                duration
            )

            durations.append(duration)

        # -----------------------------------------------------
        # Normalize durations
        # -----------------------------------------------------

        calculated_total = sum(durations)

        if calculated_total > 0:

            scale = (
                total_duration /
                calculated_total
            )

            durations = [
                duration * scale
                for duration in durations
            ]

        return durations

    # =========================================================
    # CREATE REEL
    # =========================================================

    def create_reel(
        self,
        content,
        output_name="creatoros_reel.mp4",
        language="en"
    ):
        """
        Create a narrated vertical Instagram Reel.

        Expected content:

        {
            "hook": "...",
            "script": "...",
            "caption": "...",
            "cta": "...",
            "hashtags": [...]
        }
        """

        # =====================================================
        # OUTPUT
        # =====================================================

        output_path = (
            self.output_dir /
            output_name
        )

        # =====================================================
        # CONTENT
        # =====================================================

        hook = content.get(
            "hook",
            "Welcome to CreatorOS."
        )

        script = content.get(
            "script",
            ""
        )

        cta = content.get(
            "cta",
            "Follow CreatorOS for more."
        )

        # =====================================================
        # BUILD NARRATION SCRIPT
        # =====================================================

        narration_parts = []

        if hook:
            narration_parts.append(
                hook.strip()
            )

        if script:
            narration_parts.append(
                script.strip()
            )

        if cta:
            narration_parts.append(
                cta.strip()
            )

        narration_text = " ".join(
            narration_parts
        )

        if not narration_text:

            raise ValueError(
                "Reel Generator received no "
                "content to narrate."
            )

        # =====================================================
        # GENERATE VOICE
        # =====================================================

        print(
            "\n[Reel Generator] "
            "Generating narration..."
        )

        audio_name = (
            Path(output_name).stem +
            f"_{language}.mp3"
        )

        audio_path = (
            self.voice_generator.create_voice(
                text=narration_text,
                language=language,
                output_name=audio_name
            )
        )

        # =====================================================
        # LOAD AUDIO
        # =====================================================

        print(
            "[Reel Generator] "
            "Loading narration..."
        )

        audio = AudioFileClip(
            audio_path
        )

        audio_duration = audio.duration

        print(
            "[Reel Generator] "
            f"Voice duration: "
            f"{audio_duration:.2f} seconds"
        )

        # =====================================================
        # BUILD SCENE TEXT
        # =====================================================

        scene_texts = []

        # Hook
        if hook:

            scene_texts.append(
                hook.strip()
            )

        # Script
        script_scenes = self._split_script(
            script
        )

        scene_texts.extend(
            script_scenes
        )

        # CTA
        if cta:

            scene_texts.append(
                cta.strip()
            )

        # =====================================================
        # FALLBACK
        # =====================================================

        if not scene_texts:

            scene_texts = [
                "Welcome to CreatorOS."
            ]

        # =====================================================
        # CALCULATE TIMING
        # =====================================================

        scene_durations = (
            self._calculate_scene_durations(
                scene_texts,
                audio_duration
            )
        )

        # =====================================================
        # CREATE SCENES
        # =====================================================

        scenes = []

        print(
            "\n[Reel Generator] "
            f"Creating {len(scene_texts)} scenes..."
        )

        for index, text in enumerate(
            scene_texts
        ):

            duration = scene_durations[index]

            scene = self._create_scene(
                text=text,
                duration=duration,
                scene_number=index
            )

            scenes.append(scene)

        # =====================================================
        # SEQUENTIAL TIMING
        # =====================================================

        timed_scenes = []

        current_time = 0

        for scene in scenes:

            timed_scene = scene.with_start(
                current_time
            )

            timed_scenes.append(
                timed_scene
            )

            current_time += scene.duration

        # =====================================================
        # FINAL VIDEO
        # =====================================================

        final_video = CompositeVideoClip(
            timed_scenes,
            size=(
                self.WIDTH,
                self.HEIGHT
            )
        )

        # Ensure video matches narration
        final_video = (
            final_video
            .with_duration(audio_duration)
            .with_audio(audio)
        )

        # =====================================================
        # INFORMATION
        # =====================================================

        print(
            "[Reel Generator] "
            f"Final duration: "
            f"{audio_duration:.2f} seconds"
        )

        print(
            "[Reel Generator] "
            f"Rendering narrated Reel..."
        )

        # =====================================================
        # EXPORT
        # =====================================================

        final_video.write_videofile(
            str(output_path),
            fps=self.FPS,
            codec="libx264",
            audio_codec="aac",
            audio=True
        )

        # =====================================================
        # CLEANUP
        # =====================================================

        final_video.close()

        audio.close()

        for scene in scenes:

            scene.close()

        # =====================================================
        # RESULT
        # =====================================================

        print(
            "[Reel Generator] "
            f"Reel saved: {output_path}"
        )

        return str(output_path)