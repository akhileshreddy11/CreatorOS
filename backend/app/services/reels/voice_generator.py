import asyncio
from pathlib import Path

import edge_tts


class VoiceGenerator:
    """
    CreatorOS Multilingual AI Voice Generation Engine

    Converts generated Reel scripts into AI voice narration.

    Supported languages currently configured:
        English
        Hindi
        Telugu
        German
        Spanish
    """

    LANGUAGE_VOICES = {
        "en": "en-US-AndrewMultilingualNeural",
        "hi": "hi-IN-MadhurNeural",
        "te": "te-IN-MohanNeural",
        "de": "de-DE-ConradNeural",
        "es": "es-ES-AlvaroNeural",
    }

    LANGUAGE_NAMES = {
        "en": "English",
        "hi": "Hindi",
        "te": "Telugu",
        "de": "German",
        "es": "Spanish",
    }

    DEFAULT_LANGUAGE = "en"

    def __init__(self):
        self.output_dir = Path("generated_audio")

        self.output_dir.mkdir(
            parents=True,
            exist_ok=True
        )

    # =========================================================
    # GET AVAILABLE LANGUAGES
    # =========================================================

    def get_supported_languages(self):
        """
        Return all languages currently supported.
        """

        return self.LANGUAGE_NAMES.copy()

    # =========================================================
    # GET VOICE
    # =========================================================

    def get_voice(self, language="en"):
        """
        Get the configured voice for a language.
        """

        language = language.lower().strip()

        if language not in self.LANGUAGE_VOICES:
            supported = ", ".join(
                self.LANGUAGE_VOICES.keys()
            )

            raise ValueError(
                f"Unsupported language: {language}. "
                f"Supported languages: {supported}"
            )

        return self.LANGUAGE_VOICES[language]

    # =========================================================
    # ASYNC VOICE GENERATION
    # =========================================================

    async def _generate_voice(
        self,
        text,
        output_path,
        voice
    ):
        """
        Generate the actual speech audio.
        """

        communicate = edge_tts.Communicate(
            text=text,
            voice=voice
        )

        await communicate.save(
            str(output_path)
        )

    # =========================================================
    # CREATE VOICE
    # =========================================================

    def create_voice(
        self,
        text,
        language="en",
        output_name=None
    ):
        """
        Convert text into an MP3 voice narration.

        Example:

            generator.create_voice(
                text="Welcome to CreatorOS",
                language="en"
            )

        """

        # -----------------------------------------------------
        # VALIDATE TEXT
        # -----------------------------------------------------

        if not text or not text.strip():

            raise ValueError(
                "Voice Generator received empty text."
            )

        # -----------------------------------------------------
        # NORMALIZE LANGUAGE
        # -----------------------------------------------------

        language = language.lower().strip()

        # -----------------------------------------------------
        # GET VOICE
        # -----------------------------------------------------

        voice = self.get_voice(
            language
        )

        # -----------------------------------------------------
        # DEFAULT OUTPUT NAME
        # -----------------------------------------------------

        if output_name is None:

            output_name = (
                f"creatoros_voice_{language}.mp3"
            )

        # -----------------------------------------------------
        # OUTPUT PATH
        # -----------------------------------------------------

        output_path = (
            self.output_dir / output_name
        )

        # -----------------------------------------------------
        # INFORMATION
        # -----------------------------------------------------

        print(
            "\n[Voice Generator] "
            "Generating AI voice..."
        )

        print(
            f"[Voice Generator] "
            f"Language: "
            f"{self.LANGUAGE_NAMES[language]}"
        )

        print(
            f"[Voice Generator] "
            f"Voice: {voice}"
        )

        # -----------------------------------------------------
        # GENERATE
        # -----------------------------------------------------

        asyncio.run(
            self._generate_voice(
                text=text.strip(),
                output_path=output_path,
                voice=voice
            )
        )

        # -----------------------------------------------------
        # VERIFY OUTPUT
        # -----------------------------------------------------

        if not output_path.exists():

            raise RuntimeError(
                "Voice generation failed: "
                "audio file was not created."
            )

        # -----------------------------------------------------
        # COMPLETE
        # -----------------------------------------------------

        print(
            "[Voice Generator] "
            f"Voice saved: {output_path}"
        )

        return str(output_path)