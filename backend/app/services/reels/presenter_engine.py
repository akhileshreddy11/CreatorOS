from pathlib import Path
import os
import requests


class PresenterEngine:
    """
    CreatorOS Realistic AI Presenter Engine

    Responsible for generating realistic talking-human
    presenter videos through an external avatar provider.

    The provider is intentionally abstracted so CreatorOS
    can switch providers later without changing the Reel
    generation architecture.
    """

    def __init__(self):
        self.output_dir = Path("generated_presenters")

        self.output_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        # -----------------------------------------------------
        # Provider configuration
        # -----------------------------------------------------

        self.provider = os.getenv(
            "CREATOROS_AVATAR_PROVIDER",
            "heygen"
        )

        self.api_key = os.getenv(
            "CREATOROS_AVATAR_API_KEY"
        )

    # =========================================================
    # PROVIDER STATUS
    # =========================================================

    def is_configured(self):
        """
        Check whether an avatar provider has been configured.
        """

        return bool(self.api_key)

    # =========================================================
    # GET PROVIDER
    # =========================================================

    def get_provider(self):
        """
        Return the currently configured provider.
        """

        return self.provider

    # =========================================================
    # VALIDATE INPUT
    # =========================================================

    def _validate_input(
        self,
        script,
        avatar_id=None,
        image_url=None
    ):
        """
        Validate presenter generation input.
        """

        if not script or not script.strip():

            raise ValueError(
                "Presenter Engine received empty script."
            )

        if not avatar_id and not image_url:

            raise ValueError(
                "Presenter Engine requires either "
                "avatar_id or image_url."
            )

    # =========================================================
    # HEYGEN REQUEST
    # =========================================================

    def _create_heygen_video(
        self,
        script,
        avatar_id=None,
        image_url=None,
        voice_id=None
    ):
        """
        Submit a talking-presenter generation request.

        This method is intentionally isolated from the rest
        of CreatorOS so the provider can be replaced later.
        """

        if not self.api_key:

            raise RuntimeError(
                "CreatorOS avatar API key is not configured.\n"
                "Set CREATOROS_AVATAR_API_KEY before "
                "generating a presenter video."
            )

        url = (
            "https://api.heygen.com/v2/video/generate"
        )

        headers = {
            "X-Api-Key": self.api_key,
            "Content-Type": "application/json"
        }

        avatar_config = {}

        # -----------------------------------------------------
        # Avatar
        # -----------------------------------------------------

        if avatar_id:

            avatar_config[
                "avatar_id"
            ] = avatar_id

        elif image_url:

            avatar_config[
                "photo_avatar_id"
            ] = image_url

        # -----------------------------------------------------
        # Voice
        # -----------------------------------------------------

        voice_config = {}

        if voice_id:

            voice_config[
                "voice_id"
            ] = voice_id

        # -----------------------------------------------------
        # Payload
        # -----------------------------------------------------

        payload = {
            "video_inputs": [
                {
                    "character": {
                        "type": "avatar",
                        **avatar_config
                    },
                    "voice": {
                        "type": "text",
                        "input_text": script,
                        **voice_config
                    }
                }
            ],

            "dimension": {
                "width": 1080,
                "height": 1920
            }
        }

        print(
            "\n[Presenter Engine] "
            "Submitting realistic presenter job..."
        )

        response = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=60
        )

        # -----------------------------------------------------
        # Error handling
        # -----------------------------------------------------

        if response.status_code >= 400:

            raise RuntimeError(
                "Avatar provider rejected request.\n"
                f"Status: {response.status_code}\n"
                f"Response: {response.text}"
            )

        data = response.json()

        # -----------------------------------------------------
        # Extract job ID
        # -----------------------------------------------------

        data_section = data.get(
            "data",
            {}
        )

        video_id = data_section.get(
            "video_id"
        )

        if not video_id:

            raise RuntimeError(
                "Avatar provider did not return "
                "a video job ID.\n"
                f"Response: {data}"
            )

        print(
            "[Presenter Engine] "
            f"Job created: {video_id}"
        )

        return video_id

    # =========================================================
    # CREATE PRESENTER
    # =========================================================

    def create_presenter(
        self,
        script,
        avatar_id=None,
        image_url=None,
        voice_id=None,
        output_name="creatoros_presenter.mp4"
    ):
        """
        Generate a realistic talking-human presenter.

        Parameters
        ----------
        script:
            Text the presenter should speak.

        avatar_id:
            Provider-specific avatar identifier.

        image_url:
            Optional portrait source.

        voice_id:
            Provider-specific voice.

        output_name:
            Local output filename.
        """

        self._validate_input(
            script=script,
            avatar_id=avatar_id,
            image_url=image_url
        )

        # -----------------------------------------------------
        # Provider
        # -----------------------------------------------------

        if self.provider.lower() == "heygen":

            video_id = self._create_heygen_video(
                script=script.strip(),
                avatar_id=avatar_id,
                image_url=image_url,
                voice_id=voice_id
            )

        else:

            raise ValueError(
                f"Unsupported avatar provider: "
                f"{self.provider}"
            )

        # -----------------------------------------------------
        # We intentionally stop here for Step 1.
        # -----------------------------------------------------
        #
        # The provider returns an asynchronous job.
        # A separate polling/download layer will retrieve
        # the finished MP4.
        #
        # This prevents ReelGenerator from being tightly
        # coupled to provider-specific job handling.
        # -----------------------------------------------------

        return {
            "provider": self.provider,
            "video_id": video_id,
            "status": "submitted",
            "output_path": str(
                self.output_dir / output_name
            )
        }