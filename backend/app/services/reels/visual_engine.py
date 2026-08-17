from pathlib import Path
import math

from moviepy import (
    ColorClip,
    TextClip,
    CompositeVideoClip
)


class VisualEngine:
    """
    CreatorOS Professional Visual Engine

    Creates animated vertical Reel scenes.

    This engine is intentionally independent from:
        - Content Employee
        - Voice Generator
        - Mission Executor
        - Reel Generator

    It will later become one of the rendering layers
    used by ReelGenerator.
    """

    WIDTH = 1080
    HEIGHT = 1920
    FPS = 30

    # =========================================================
    # INITIALIZATION
    # =========================================================

    def __init__(self):
        self.output_dir = Path("generated_visuals")

        self.output_dir.mkdir(
            parents=True,
            exist_ok=True
        )

    # =========================================================
    # COLOR PALETTE
    # =========================================================

    BACKGROUND_COLORS = [
        (10, 10, 18),
        (15, 12, 30),
        (8, 18, 28),
        (20, 10, 25),
    ]

    ACCENT_COLORS = [
        (80, 180, 255),
        (160, 100, 255),
        (0, 220, 180),
        (255, 180, 70),
    ]

    # =========================================================
    # CREATE BACKGROUND
    # =========================================================

    def _create_background(
        self,
        duration,
        scene_number
    ):
        """
        Create the base animated-looking background.

        MoviePy's basic ColorClip is used as the foundation.
        Additional moving layers are added above it.
        """

        background_color = (
            self.BACKGROUND_COLORS[
                scene_number %
                len(self.BACKGROUND_COLORS)
            ]
        )

        background = ColorClip(
            size=(
                self.WIDTH,
                self.HEIGHT
            ),
            color=background_color,
            duration=duration
        )

        return background

    # =========================================================
    # CREATE MOVING GLOW
    # =========================================================

    def _create_glow(
        self,
        duration,
        scene_number
    ):
        """
        Create a large moving accent layer.

        This gives the background some visual movement
        instead of leaving it completely static.
        """

        accent_color = (
            self.ACCENT_COLORS[
                scene_number %
                len(self.ACCENT_COLORS)
            ]
        )

        glow_size = 750

        glow = ColorClip(
            size=(
                glow_size,
                glow_size
            ),
            color=accent_color,
            duration=duration
        )

        def animated_position(t):

            progress = (
                t / max(duration, 0.01)
            )

            x = (
                -200
                +
                progress * 500
            )

            y = (
                300
                +
                math.sin(
                    progress * math.pi * 2
                ) * 180
            )

            return (
                int(x),
                int(y)
            )

        glow = glow.with_position(
            animated_position
        )

        # Keep the glow subtle.
        glow = glow.with_opacity(0.12)

        return glow

    # =========================================================
    # CREATE SECONDARY MOVING ELEMENT
    # =========================================================

    def _create_secondary_motion(
        self,
        duration,
        scene_number
    ):
        """
        Create a second moving visual element.
        """

        accent_color = (
            self.ACCENT_COLORS[
                (
                    scene_number + 1
                )
                %
                len(self.ACCENT_COLORS)
            ]
        )

        element = ColorClip(
            size=(
                420,
                420
            ),
            color=accent_color,
            duration=duration
        )

        def animated_position(t):

            progress = (
                t / max(duration, 0.01)
            )

            x = (
                700
                +
                math.sin(
                    progress * math.pi * 2
                ) * 160
            )

            y = (
                1100
                +
                math.cos(
                    progress * math.pi * 2
                ) * 220
            )

            return (
                int(x),
                int(y)
            )

        element = element.with_position(
            animated_position
        )

        element = element.with_opacity(
            0.10
        )

        return element

    # =========================================================
    # CREATE TEXT
    # =========================================================

    def _create_text(
        self,
        text,
        duration,
        scene_number,
        font_size=72
    ):
        """
        Create large readable Reel typography.
        """

        text_clip = TextClip(
            text=text,
            font_size=font_size,
            color="white",
            size=(
                900,
                900
            ),
            method="caption"
        )

        # -----------------------------------------------------
        # Animated vertical entrance
        # -----------------------------------------------------

        def animated_position(t):

            animation_time = min(
                t,
                0.5
            )

            progress = (
                animation_time / 0.5
            )

            # Ease-out animation
            eased = (
                1
                -
                (1 - progress) ** 3
            )

            start_y = 1100
            end_y = 820

            y = (
                start_y
                +
                (end_y - start_y)
                * eased
            )

            # Small horizontal movement
            x = (
                90
                +
                math.sin(
                    t * 2
                ) * 4
            )

            return (
                int(x),
                int(y)
            )

        text_clip = (
            text_clip
            .with_position(
                animated_position
            )
            .with_duration(duration)
        )

        return text_clip

    # =========================================================
    # CREATE TOP LABEL
    # =========================================================

    def _create_label(
        self,
        duration
    ):
        """
        Small CreatorOS branding label.
        """

        label = TextClip(
            text="CREATOROS",
            font_size=34,
            color="white",
            size=(
                500,
                80
            ),
            method="caption"
        )

        label = (
            label
            .with_position(
                ("center", 150)
            )
            .with_duration(duration)
            .with_opacity(0.75)
        )

        return label

    # =========================================================
    # CREATE SCENE
    # =========================================================

    def create_scene(
        self,
        text,
        duration=4,
        scene_number=0,
        font_size=72
    ):
        """
        Create one professional animated Reel scene.
        """

        background = (
            self._create_background(
                duration,
                scene_number
            )
        )

        glow = (
            self._create_glow(
                duration,
                scene_number
            )
        )

        secondary = (
            self._create_secondary_motion(
                duration,
                scene_number
            )
        )

        text_clip = (
            self._create_text(
                text,
                duration,
                scene_number,
                font_size
            )
        )

        label = (
            self._create_label(
                duration
            )
        )

        scene = CompositeVideoClip(
            [
                background,
                glow,
                secondary,
                label,
                text_clip
            ],
            size=(
                self.WIDTH,
                self.HEIGHT
            )
        )

        scene = scene.with_duration(
            duration
        )

        return scene

    # =========================================================
    # CREATE VISUAL TEST
    # =========================================================

    def create_test_video(
        self,
        output_name="visual_engine_test.mp4"
    ):
        """
        Create a standalone test Reel.

        This is ONLY for testing the Visual Engine.
        """

        scenes_data = [
            (
                "STOP WASTING TIME",
                3.0
            ),
            (
                "Automate the repetitive work.",
                4.0
            ),
            (
                "Build systems.\nCreate more.",
                4.0
            ),
            (
                "FOLLOW CREATOROS",
                3.0
            )
        ]

        scenes = []

        print(
            "\n[Visual Engine] "
            f"Creating {len(scenes_data)} scenes..."
        )

        current_time = 0

        for index, (
            text,
            duration
        ) in enumerate(scenes_data):

            scene = self.create_scene(
                text=text,
                duration=duration,
                scene_number=index
            )

            scene = scene.with_start(
                current_time
            )

            scenes.append(scene)

            current_time += duration

        # =====================================================
        # COMPOSITE
        # =====================================================

        final_video = CompositeVideoClip(
            scenes,
            size=(
                self.WIDTH,
                self.HEIGHT
            )
        )

        final_video = (
            final_video
            .with_duration(current_time)
        )

        # =====================================================
        # OUTPUT
        # =====================================================

        output_path = (
            self.output_dir /
            output_name
        )

        print(
            "[Visual Engine] "
            f"Duration: {current_time:.1f} seconds"
        )

        print(
            "[Visual Engine] "
            "Rendering visual test..."
        )

        final_video.write_videofile(
            str(output_path),
            fps=self.FPS,
            codec="libx264",
            audio=False
        )

        # =====================================================
        # CLEANUP
        # =====================================================

        final_video.close()

        for scene in scenes:
            scene.close()

        print(
            "[Visual Engine] "
            f"Saved: {output_path}"
        )

        return str(output_path)